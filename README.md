# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

### Running the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the test suite covers

18 pytest functions across five areas:

| Area | Tests |
|---|---|
| **Task sorting** | Chronological order is correct for mixed `'HH:MM'` values; tasks with no time sort last |
| **Recurring tasks** | Daily tasks recur +1 day, weekly tasks recur +7 days, one-off tasks produce no follow-up; new occurrence is appended to the pet's task list |
| **Conflict detection** | Same-pet time overlaps are flagged, cross-pet overlaps are labelled `cross-pet`, tasks that exceed the daily budget are reported as unschedulable, non-overlapping tasks produce zero warnings |
| **Edge cases** | Pet with no tasks, owner with no pets, all tasks already completed, duplicate task IDs silently ignored |
| **Filtering** | `filter_by_pet` returns only the correct pet's tasks; unknown pet name returns an empty list |

### Confidence level

**★★★★☆ (4 / 5)**

The core scheduling behaviours — sorting, recurrence, conflict detection, and filtering — are each covered by multiple targeted tests, and all 18 pass. The rating stops short of 5 stars because the tests run against in-memory objects only; there is no coverage of the Streamlit UI layer, persistent storage, or inputs that arrive as raw user strings (e.g. malformed `'HH:MM'` values or out-of-range priorities). Those paths would need additional tests before the system could be considered fully reliable in production.

---

## Smarter Scheduling

PawPal+ has been extended with four intelligent scheduling features, all implemented in `pawpal_system.py` and demonstrated in `main.py`.

### Sorting tasks by time

`Scheduler.sort_by_time(tasks)` orders any list of tasks by their `time` field (`'HH:MM'` format) using Python's `sorted()` with a lambda key. Tasks without a scheduled time sort to the end of the list. This gives owners a chronological view of their day rather than an arbitrary insertion order.

### Filtering tasks

Two filter methods make it easy to query the task list without looping manually:

- `filter_by_status(completed)` — returns all tasks across every pet that match a given completion state (pending or done).
- `filter_by_pet(pet_name)` — returns all tasks belonging to a named pet (case-insensitive). Both return empty lists gracefully when nothing matches, so callers never need to guard against `None`.

### Recurring task automation

`Task` now carries optional `time` and `due_date` fields. Calling `Pet.complete_task(task_id, next_task_id)` marks a task done and, for `"daily"` or `"weekly"` tasks, automatically appends a fresh copy to the pet's task list with the next due date calculated via `datetime.timedelta`. One-off tasks (`frequency="once"`) produce no recurrence. This removes the manual work of re-adding routine care items every day.

### Conflict detection

`Scheduler.detect_conflicts()` runs automatically at the end of `generate_daily_plan()` and stores results in `scheduler.conflict_warnings` — a plain list of strings, so no exceptions are raised and the caller decides how to surface them. Three conflict types are checked:

| Conflict type | What it catches |
|---|---|
| **Budget overflow** | Total scheduled minutes exceed the owner's daily limit |
| **Unschedulable task** | A single task is longer than the entire daily budget |
| **Time overlap** | Two scheduled tasks have intersecting time windows |

Overlap warnings name both tasks and their pets (e.g. `cross-pet: Oliver / Bella` or `same pet: Bella`), making it immediately clear whether a conflict is within one animal's routine or spans multiple pets.
