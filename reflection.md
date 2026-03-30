# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My UML design includes four main classes: Owner, Pet, Task, and Scheduler. 
Task - the atomic unit of work. It represents a single pet care activity (e.g., feeding, grooming) and holds data like duration, priority, category, and completion status. Its methods manage its own state: marking itself complete/incomplete, updating duration or priority, and producing a human-readable summary via get_details().

Pet - models an individual pet and owns the tasks specific to that animal's care. It holds the pet's identity (name, species, age) and a care_needs list describing what the pet requires. Its methods let you attach or detach tasks and read or replace care needs. Because tasks are stored directly on the pet, a pet's task list is removed if the pet is removed (composition).

Owner - the central actor in the domain. It holds a daily_available_time budget, scheduling preferences, a roster of Pet objects, and a master tasks list for cross-pet or non-pet tasks (e.g., "buy supplies"). It manages its own collections with add_pet/remove_pet and add_task/remove_task, and exposes get_available_time() for the scheduler to read.

Scheduler - the planning engine. It is initialized with an Owner and generates a daily plan that fits within the owner's time budget. It sorts tasks by priority (organize_by_priority), trims the list to what fits (filter_by_duration), detects conflicts (check_conflicts), and produces a plain-language rationale (explain_plan). It does not own pets or tasks — it only reads them, keeping its responsibility focused on scheduling logic rather than data management.

The separation of concerns is deliberate: Task and Pet manage their own data, Owner aggregates everything the user controls, and Scheduler is the only class responsible for decision-making logic.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
There is no design change from UML design to implementation. It might be due to me using design as reference while leting AI code the skeleton.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
