# 🧠 Zeya888 Rule Prompts Library  
> This document groups prompts by **use cases**, showing how each rule functions as a cognitive and technical instrument inside the pipeline.

---

## 🧭 Use Case 1 — Clarifying Vague Problem Statements
> Focus: understanding unclear or fragmented tasks, identifying all decision points, and producing a clear, executable formulation.

### 🎯 Rule: `analysis.mdc`
**Prompt:**
Run `@analysis.mdc` to interpret a vague or unclear problem statement.  
Identify **all decision points** and generate guiding **questions with analytic commentary** for each — including possible solution paths and recommendations.  
Document the clarified, decision-backed problem formulation inside `docs/AIJournal.md`, overwriting previous content if present.  
The result must be a **clear, implementable technical task** written as if ready for execution, with each decision and reasoning step traceable.

**Output:**  
A cleanly structured technical problem statement ready for execution.

---

## 🧩 Use Case 2 — Structural Two-Level Planning
> Focus: transforming a task into an actionable, hierarchical plan connected with execution logic.

### 🎯 Rule: `analysis.mdc`
**Prompt:**
Continue in `docs/AIJournal.md` and run `@analysis.mdc`.  
Based on the current task context, produce a **two-level hierarchical plan**:
- **Level 1:** core work packages or milestones.  
- **Level 2:** specific actionable subtasks with clear outcomes.  
Each item must express intent (why), expected result (what), and link to follow-up rules for execution.  
Write the plan directly in the journal, formatted as a structured outline ready for `@run-task.mdc`.

**Output:**  
A hierarchical plan in journal format, aligned with follow-up pipeline steps.

---

## 🧱 Use Case 3 — Documentation Expansion & Integration
> Focus: maintaining coherence between current work and long-term documentation structure.

### 🎯 Rule: `analysis.mdc`
**Prompt:**
Execute `@analysis.mdc` in documentation mode.  
Use the active plan and recent outputs to:
1. Derive the **documentation structure** required for project continuity.  
2. Identify which existing docs or repositories need updates or consolidation.  
3. Suggest new files if gaps are found, specifying name, purpose, and location.  
After review with the operator, update `docs/AIJournal.md` with a summary of new and updated files, providing short rationales for each addition.

**Output:**  
A clearly structured documentation update plan, validated and logged in the journal.

---

## 🧩 Rule: `@run-task.mdc`

### Use Case
Sequential execution of multi-level plans — designed for structured task decomposition and autonomous flow management.

### Prompt
> Execute **Stage N** using `@run-task.mdc`.  
>  
> Write the final results and insights into the **journal** (the same file where the list is located — e.g. `docs/AIJournal.md`, or the explicitly specified one).  
>  
> If context is unclear, ask for clarification before execution.

### Example
> Journal: `docs/AIJournal.md`  
> Execute Stage 1 using `@run-task.mdc`

### Notes
- This rule automatically detects and processes nested subtasks inside a two-level plan. Choose a plan item that has nested sub-items and process them sequentially through the internal `ItemY` cycle.  
- Each sub-item passes through the full internal `ItemY` pipeline (`Understanding → Knowledge Check → Acceptance → Planning → Execution → Validation → Retrospective`).  
- Keeps task logic consistent, reduces mental load, and maintains clean journal records.  
- Works best when used after `@analysis.mdc` for high-context continuity.

---


---

🪶 *Next section:*  
Use Cases 4–6 → `run-task.mdc`, `test-qualification.mdc`, `test-to-success.mdc`
