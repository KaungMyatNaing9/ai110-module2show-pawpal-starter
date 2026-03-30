# PawPal+ — Class Diagram

```mermaid
classDiagram
    class Owner {
        +String name
        +int dailyAvailableTime
        +List~String~ preferences
        +List~Pet~ pets
        +List~Task~ tasks
        +addPet(pet: Pet) void
        +removePet(petId: int) void
        +addTask(task: Task) void
        +removeTask(taskId: int) void
        +getAvailableTime() int
        +updatePreferences(preferences: List~String~) void
    }

    class Pet {
        +int id
        +String name
        +String species
        +int age
        +List~String~ careNeeds
        +List~Task~ tasks
        +addTask(task: Task) void
        +removeTask(taskId: int) void
        +getCareNeeds() List~String~
        +updateCareNeeds(needs: List~String~) void
    }

    class Task {
        +int id
        +String title
        +int durationMinutes
        +String priority
        +String category
        +bool isCompleted
        +markComplete() void
        +markIncomplete() void
        +updateDuration(minutes: int) void
        +updatePriority(level: String) void
        +getDetails() String
    }

    class Scheduler {
        +Owner owner
        +List~Task~ scheduledTasks
        +generateDailyPlan() List~Task~
        +organizeByPriority(tasks: List~Task~) List~Task~
        +filterByDuration(tasks: List~Task~, availableTime: int) List~Task~
        +checkConflicts(task: Task) bool
        +explainPlan() String
        +getRemainingTime() int
        +resetPlan() void
    }

    Owner "1" *-- "0..*" Pet : owns
    Pet "1" *-- "0..*" Task : has
    Owner "1" o-- "0..*" Task : manages
    Scheduler "1" --> "1" Owner : schedules for
    Scheduler ..> Pet : references
    Scheduler ..> Task : organizes
```

## Relationship Key

| Symbol | Meaning |
|--------|---------|
| `*--`  | Composition — child cannot exist without parent |
| `o--`  | Aggregation — owner holds a reference to tasks |
| `-->`  | Association — scheduler is linked to one owner |
| `..>`  | Dependency — scheduler reads pets/tasks but does not own them |

## Notes

- **Owner → Pet** (composition, 1 to 0..*): Pets belong to one owner and are removed if the owner is deleted.
- **Pet → Task** (composition, 1 to 0..*): Tasks are tied to a specific pet's care needs.
- **Owner → Task** (aggregation, 1 to 0..*): Owner also holds a master task list for cross-pet scheduling and non-pet tasks (e.g., "buy supplies").
- **Scheduler → Owner** (association): The scheduler is initialized with an owner and uses their available time and preferences to build the plan.
- **Scheduler → Pet / Task** (dependency): The scheduler reads these during `generateDailyPlan()` but does not own or store them directly.
