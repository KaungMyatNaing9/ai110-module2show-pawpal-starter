"""
main.py
Testing script for the PawPal+ pet care planning system.

Run with:
    python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def print_section(title: str) -> None:
    width = 52
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


# ---------------------------------------------------------------------------
# 1. Build owner
# ---------------------------------------------------------------------------

owner = Owner(
    name="Alex",
    daily_available_time=90,
    preferences=["high-priority tasks first", "keep sessions under 30 min"],
)

# ---------------------------------------------------------------------------
# 2. Build pets and assign tasks
# ---------------------------------------------------------------------------

# --- Pet 1: Bella the dog ---
bella = Pet(id=1, name="Bella", species="dog", age=3,
            care_needs=["daily exercise", "evening feeding"])

bella.add_task(Task(id=1, title="Morning Walk",
                    duration_minutes=30, priority="high",
                    category="exercise", frequency="daily"))

bella.add_task(Task(id=2, title="Breakfast",
                    duration_minutes=10, priority="high",
                    category="feeding", frequency="daily"))

bella.add_task(Task(id=3, title="Dental Chew",
                    duration_minutes=5, priority="medium",
                    category="grooming", frequency="daily"))

bella.add_task(Task(id=4, title="Obedience Training",
                    duration_minutes=20, priority="medium",
                    category="exercise", frequency="daily"))

# --- Pet 2: Oliver the cat ---
oliver = Pet(id=2, name="Oliver", species="cat", age=5,
             care_needs=["weekly brushing", "indoor enrichment"])

oliver.add_task(Task(id=5, title="Brush Fur",
                     duration_minutes=10, priority="medium",
                     category="grooming", frequency="weekly"))

oliver.add_task(Task(id=6, title="Feeding",
                     duration_minutes=5, priority="high",
                     category="feeding", frequency="daily"))

oliver.add_task(Task(id=7, title="Playtime",
                     duration_minutes=15, priority="low",
                     category="exercise", frequency="daily"))

oliver.add_task(Task(id=8, title="Litter Box Clean",
                     duration_minutes=10, priority="high",
                     category="hygiene", frequency="daily"))

# ---------------------------------------------------------------------------
# 3. Register pets with owner
# ---------------------------------------------------------------------------

owner.add_pet(bella)
owner.add_pet(oliver)

# ---------------------------------------------------------------------------
# 4. Print all registered pets and their tasks
# ---------------------------------------------------------------------------

print_section("Registered Pets & Tasks")

# Build a lookup: task id → pet name, used when printing the schedule later
task_pet_map: dict[int, str] = {}

for pet in owner.pets:
    print(f"\n  {pet.name} ({pet.species.capitalize()}, age {pet.age})")
    print(f"  Care needs: {', '.join(pet.care_needs) if pet.care_needs else 'None listed'}")
    print(f"  {'#':<4} {'Task':<22} {'Duration':>9}  {'Priority':<8} {'Category'}")
    print(f"  {'-'*4} {'-'*22} {'-'*9}  {'-'*8} {'-'*10}")
    for task in pet.tasks:
        print(f"  {task.id:<4} {task.title:<22} {task.duration_minutes:>7} min"
              f"  {task.priority:<8} {task.category}")
        task_pet_map[task.id] = pet.name

# ---------------------------------------------------------------------------
# 5. Generate schedule
# ---------------------------------------------------------------------------

scheduler = Scheduler(owner)
plan = scheduler.generate_daily_plan()

# ---------------------------------------------------------------------------
# 6. Print Today's Schedule
# ---------------------------------------------------------------------------

print_section("Today's Schedule")

total_budget = owner.get_available_time()
used_time    = sum(t.duration_minutes for t in plan)
remaining    = scheduler.get_remaining_time()

print(f"\n  Owner  : {owner.name}")
print(f"  Budget : {total_budget} min available")
print(f"  Planned: {used_time} min across {len(plan)} task(s)")
print(f"  Free   : {remaining} min unscheduled\n")

header = f"  {'#':<4} {'Pet':<10} {'Task':<22} {'Duration':>9}  {'Priority':<8} {'Category'}"
print(header)
print("  " + "-" * (len(header) - 2))

for i, task in enumerate(plan, start=1):
    pet_name = task_pet_map.get(task.id, "Unknown")
    print(f"  {i:<4} {pet_name:<10} {task.title:<22} "
          f"{task.duration_minutes:>7} min  {task.priority:<8} {task.category}")

# ---------------------------------------------------------------------------
# 7. Print scheduling rationale
# ---------------------------------------------------------------------------

print_section("Why This Order?")
print()
print(scheduler.explain_plan())

# ---------------------------------------------------------------------------
# 8. Demonstrate mark_complete and skipped tasks
# ---------------------------------------------------------------------------

print_section("Skipped Tasks (over budget or already done)")

all_task_ids = {t.id for t in owner.get_all_tasks()}
scheduled_ids = {t.id for t in plan}
skipped_ids = all_task_ids - scheduled_ids

if skipped_ids:
    for pet in owner.pets:
        for task in pet.tasks:
            if task.id in skipped_ids:
                print(f"  - [{pet.name}] {task.title} "
                      f"({task.duration_minutes} min, {task.priority} priority) — not scheduled")
else:
    print("  All tasks fit within today's time budget.")
