"""
pawpal_system.py
Backend logic layer for PawPal+ — a pet care planning application.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """Represents a single pet care activity."""

    id: int
    title: str
    duration_minutes: int
    priority: str          # "low" | "medium" | "high"
    category: str          # e.g. "feeding", "exercise", "grooming", "medical"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def mark_incomplete(self) -> None:
        """Reset this task to incomplete."""
        pass

    def update_duration(self, minutes: int) -> None:
        """Update the estimated duration of this task."""
        pass

    def update_priority(self, level: str) -> None:
        """Update the priority level of this task.

        Args:
            level: One of "low", "medium", or "high".
        """
        pass

    def get_details(self) -> str:
        """Return a human-readable summary of this task.

        Returns:
            A formatted string describing the task.
        """
        pass


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """Represents a pet and its associated care tasks."""

    id: int
    name: str
    species: str           # e.g. "dog", "cat", "bird"
    age: int
    care_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet.

        Args:
            task: The Task to add.
        """
        pass

    def remove_task(self, task_id: int) -> None:
        """Remove a task from this pet by its id.

        Args:
            task_id: The id of the Task to remove.
        """
        pass

    def get_care_needs(self) -> List[str]:
        """Return the list of care needs for this pet.

        Returns:
            A list of care need strings.
        """
        pass

    def update_care_needs(self, needs: List[str]) -> None:
        """Replace the current care needs list.

        Args:
            needs: New list of care need strings.
        """
        pass


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    """Represents the pet owner and their scheduling constraints."""

    def __init__(
        self,
        name: str,
        daily_available_time: int,
        preferences: List[str] | None = None,
    ) -> None:
        """Initialise an Owner.

        Args:
            name: The owner's name.
            daily_available_time: Total minutes available for pet care today.
            preferences: Optional list of scheduling preferences
                         (e.g. ["morning tasks first", "no tasks after 8pm"]).
        """
        self.name: str = name
        self.daily_available_time: int = daily_available_time
        self.preferences: List[str] = preferences if preferences is not None else []
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster.

        Args:
            pet: The Pet to add.
        """
        pass

    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet by its id.

        Args:
            pet_id: The id of the Pet to remove.
        """
        pass

    def add_task(self, task: Task) -> None:
        """Add a task to the owner's master task list.

        Args:
            task: The Task to add.
        """
        pass

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the master list by its id.

        Args:
            task_id: The id of the Task to remove.
        """
        pass

    def get_available_time(self) -> int:
        """Return the owner's total daily available time in minutes.

        Returns:
            Available minutes as an integer.
        """
        pass

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the owner's scheduling preferences.

        Args:
            preferences: New list of preference strings.
        """
        pass


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    """Generates and explains a daily pet care plan for an owner."""

    def __init__(self, owner: Owner) -> None:
        """Initialise the Scheduler for a given owner.

        Args:
            owner: The Owner whose pets and tasks will be scheduled.
        """
        self.owner: Owner = owner
        self.scheduled_tasks: List[Task] = []

    def generate_daily_plan(self) -> List[Task]:
        """Build an ordered list of tasks that fits within the owner's
        available time, ranked by priority and duration.

        Returns:
            An ordered list of Task objects representing today's plan.
        """
        pass

    def organize_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks so that higher-priority items appear first.

        Priority order (highest to lowest): "high", "medium", "low".

        Args:
            tasks: Unsorted list of Task objects.

        Returns:
            A new list sorted by descending priority.
        """
        pass

    def filter_by_duration(
        self, tasks: List[Task], available_time: int
    ) -> List[Task]:
        """Keep only tasks that fit within the remaining available time.

        Args:
            tasks: Candidate list of Task objects.
            available_time: Remaining minutes the owner has today.

        Returns:
            A subset of tasks whose cumulative duration fits the time budget.
        """
        pass

    def check_conflicts(self, task: Task) -> bool:
        """Determine whether adding a task would cause a scheduling conflict.

        Args:
            task: The Task being considered.

        Returns:
            True if a conflict exists, False otherwise.
        """
        pass

    def explain_plan(self) -> str:
        """Produce a plain-language explanation of why each task was chosen
        and how it was ordered in today's plan.

        Returns:
            A formatted string summarising the scheduling rationale.
        """
        pass

    def get_remaining_time(self) -> int:
        """Calculate how many minutes are still unscheduled.

        Returns:
            Remaining available minutes as an integer.
        """
        pass

    def reset_plan(self) -> None:
        """Clear the current scheduled plan so a new one can be generated."""
        pass
