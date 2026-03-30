from pawpal_system import Pet, Task


def test_mark_complete_sets_is_completed_to_true():
    task = Task(id=1, title="Morning Walk", duration_minutes=30,
                priority="high", category="exercise")

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(id=1, name="Bella", species="dog", age=3)
    task = Task(id=1, title="Breakfast", duration_minutes=10,
                priority="high", category="feeding")

    pet.add_task(task)

    assert len(pet.tasks) == 1
