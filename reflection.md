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

The scheduler considers three constraints: time budget, priority, and conflicts. The owner's daily_available_time is the hard limit: filter_by_duration ensures the cumulative task duration never exceeds what is available, and get_remaining_time tracks what is left. Within that budget, organize_by_priority ranks tasks from "high" to "medium" to "low" so the most critical care always gets scheduled first. check_conflicts then acts as a safety gate before any task is added to the final plan. Time was treated as the most important constraint because no matter how high a task's priority is, it simply cannot be done if there is no time for it: priority only matters within the time that exists.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

From my perspective, the scheduler makes a tradeoff by using a simple greedy approach that prioritizes high-priority tasks first instead of trying to find the most optimal combination of tasks. This means it might not always maximize the number of tasks completed within a limited time, but it keeps the logic easy to understand and predictable. I think this is reasonable because, in real life, pet owners usually think in terms of urgency rather than optimization. Also, the number of tasks in this app is small, so the difference between greedy and optimal solutions is not very significant. Keeping the algorithm simple makes it easier to maintain and explain, which is important for a practical application like this.

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
