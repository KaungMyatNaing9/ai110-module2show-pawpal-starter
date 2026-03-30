import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ---------------------------------------------------------------------------
# Session-state initialisation
#
# Streamlit reruns the entire script on every user interaction.
# Keys are only written once; subsequent reruns reuse the stored value.
# ---------------------------------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", daily_available_time=90)

if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1

if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

# Feedback messages are stored in session state so they survive the rerun
# that immediately follows a button press.
if "feedback" not in st.session_state:
    st.session_state.feedback = None   # tuple ("success"|"warning", message) or None

# Convenience reference — always points at the live Owner object.
owner: Owner = st.session_state.owner

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🐾 PawPal+")
st.caption("A daily pet care planner for busy owners.")
st.divider()

# ---------------------------------------------------------------------------
# Show any pending feedback from the previous action, then clear it.
# ---------------------------------------------------------------------------

if st.session_state.feedback:
    level, msg = st.session_state.feedback
    if level == "success":
        st.success(msg)
    else:
        st.warning(msg)
    st.session_state.feedback = None

# ---------------------------------------------------------------------------
# Section 1 — Owner settings
#
# Wrapped in st.form so that typing in the text box does NOT trigger a rerun;
# changes are only applied when the user clicks "Save".
# ---------------------------------------------------------------------------

st.subheader("Owner")

with st.form("owner_form"):
    col_name, col_time = st.columns(2)
    with col_name:
        new_name = st.text_input("Your name", value=owner.name)
    with col_time:
        new_time = st.number_input(
            "Daily time available (minutes)",
            min_value=10, max_value=480,
            value=owner.daily_available_time, step=5,
        )
    save_owner = st.form_submit_button("Save owner settings")

if save_owner:
    st.session_state.owner.name = new_name
    st.session_state.owner.daily_available_time = new_time
    owner = st.session_state.owner
    st.session_state.feedback = ("success", f"Owner updated: {new_name}, {new_time} min/day.")
    st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Section 2 — Add a Pet
#
# On submit: instantiate Pet → call owner.add_pet() → increment id counter.
# ---------------------------------------------------------------------------

st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    col_pet, col_species, col_age = st.columns(3)
    with col_pet:
        pet_name = st.text_input("Pet name", value="Bella")
    with col_species:
        species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
    with col_age:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
    add_pet_btn = st.form_submit_button("Add pet")

if add_pet_btn:
    new_pet = Pet(
        id=st.session_state.next_pet_id,
        name=pet_name,
        species=species,
        age=int(age),
    )
    st.session_state.owner.add_pet(new_pet)        # Owner.add_pet()
    st.session_state.next_pet_id += 1
    st.session_state.feedback = ("success", f"Added {pet_name} the {species}.")
    st.rerun()

# Live roster — updates immediately after add_pet rerun.
if owner.pets:
    st.caption("Current pets:")
    for pet in owner.pets:
        st.write(f"- **{pet.name}** ({pet.species.capitalize()}, age {pet.age})")
else:
    st.info("No pets added yet.")

st.divider()

# ---------------------------------------------------------------------------
# Section 3 — Add a Task
#
# On submit: instantiate Task → call pet.add_task() → increment id counter.
# The pet is looked up from owner.pets so we always work with the live object.
# ---------------------------------------------------------------------------

st.subheader("Add a Task")

if not owner.pets:
    st.info("Add at least one pet above before adding tasks.")
else:
    # Build name → Pet map from the live owner each rerun.
    pet_options: dict[str, Pet] = {p.name: p for p in owner.pets}

    with st.form("add_task_form", clear_on_submit=True):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            selected_pet_name = st.selectbox("Assign to pet", list(pet_options.keys()))
        with col_t2:
            task_title = st.text_input("Task title", value="Morning walk")

        col_t3, col_t4, col_t5 = st.columns(3)
        with col_t3:
            duration = st.number_input(
                "Duration (min)", min_value=1, max_value=240, value=20
            )
        with col_t4:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col_t5:
            category = st.selectbox(
                "Category",
                ["exercise", "feeding", "grooming", "medical", "hygiene", "other"],
            )
        add_task_btn = st.form_submit_button("Add task")

    if add_task_btn:
        new_task = Task(
            id=st.session_state.next_task_id,
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
        )
        # Retrieve the target pet from the live owner and call pet.add_task().
        target_pet: Pet = pet_options[selected_pet_name]
        target_pet.add_task(new_task)                  # Pet.add_task()
        st.session_state.next_task_id += 1
        st.session_state.feedback = (
            "success", f"Added '{task_title}' to {selected_pet_name}."
        )
        st.rerun()

st.divider()

# ---------------------------------------------------------------------------
# Section 4 — Current pets and tasks
#
# Always reads from st.session_state.owner so additions above are immediately
# reflected without any extra state copying.
# ---------------------------------------------------------------------------

st.subheader("Your Pets & Tasks")

if not owner.pets:
    st.info("No pets added yet.")
else:
    for pet in owner.pets:
        task_count = len(pet.tasks)
        label = f"{pet.name} ({pet.species.capitalize()}, age {pet.age}) — {task_count} task(s)"
        with st.expander(label, expanded=True):
            if not pet.tasks:
                st.caption("No tasks yet.")
            else:
                rows = [
                    {
                        "Task": t.title,
                        "Duration (min)": t.duration_minutes,
                        "Priority": t.priority,
                        "Category": t.category,
                        "Done": "Yes" if t.is_completed else "No",
                    }
                    for t in pet.tasks
                ]
                st.table(rows)

st.divider()

# ---------------------------------------------------------------------------
# Section 5 — Generate schedule
#
# Creates a Scheduler, calls generate_daily_plan(), and displays the result.
# The Scheduler reads all tasks from owner.get_pending_tasks() internally.
# ---------------------------------------------------------------------------

st.subheader("Generate Today's Schedule")

all_tasks = owner.get_all_tasks()
if not all_tasks:
    st.info("Add at least one task before generating a schedule.")
else:
    if st.button("Generate schedule"):
        scheduler = Scheduler(owner)                   # Scheduler(owner)
        plan = scheduler.generate_daily_plan()         # Scheduler.generate_daily_plan()

        if not plan:
            st.session_state.feedback = (
                "warning",
                "No tasks could be scheduled. Try increasing available time or reducing durations.",
            )
            st.rerun()
        else:
            used = sum(t.duration_minutes for t in plan)
            remaining = scheduler.get_remaining_time()

            st.success(
                f"Scheduled {len(plan)} task(s) — {used} min used, {remaining} min remaining."
            )

            # Build pet-name lookup from the live owner.
            task_pet_map: dict[int, str] = {
                t.id: p.name
                for p in owner.pets
                for t in p.tasks
            }

            schedule_rows = [
                {
                    "#": i,
                    "Pet": task_pet_map.get(t.id, "—"),
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Category": t.category,
                }
                for i, t in enumerate(plan, start=1)
            ]
            st.table(schedule_rows)

            with st.expander("Why this order?"):
                st.text(scheduler.explain_plan())      # Scheduler.explain_plan()
