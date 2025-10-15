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

### Brief description
Sequential execution of multi-level plans — designed for structured task decomposition and autonomous flow management.

#### Use Cases
- **Executing sub-items of a technical plan with full control** — keeps nested tasks aligned and traceable.  
- **Stepwise migrations or refactorings with measurable criteria** — enables clear validation checkpoints.  
- **Team collaboration with unified workflow and traceable progress** — ensures consistent logic across contributors.  
- **Managing complex or lengthy tasks without cognitive drift** — supports long-focus work without mental overload.


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

## 🎨 Vibe Coding Mode — Deep Co-Reasoning with Code
> **Rule:** `@Zeya888-Meta.mdc`  
> **Focus:** Immersive work with code through cognitive resonance — when you need AI to **think with you**, not just execute commands.

This mode is for situations where you're **diving deep into code** rather than running through a pipeline. It transforms AI from a code generator into a co-reasoning partner that mirrors your thinking style, preserves your cognitive rhythm, and explains its reasoning transparently.

---

## 💎 Use Case 4 — Code Review with Transparent Reasoning
> Focus: understanding code deeply, identifying issues with clear reasoning chain, and delivering actionable improvements.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta CR-loop to review this code.

Mirror my intent (1-2 lines) → Frame quality criteria (readability, performance, 
maintainability, security) → Synthesis (analysis + refactoring) → Test against 
criteria → Deliver improvements with reasoning.

Explain, don't obey: show your thought process for each issue found.

[paste code here]
```

**Output:**  
- Mirror: "This function handles X but has Y concern"
- Frame: Quality criteria explicitly stated
- Synthesis: Issue-by-issue analysis with reasoning chain
- Refactored code with explanations for each change
- Trade-offs documented

---

## 🔍 Use Case 5 — Debugging with Root Cause Analysis
> Focus: finding not just the fix, but understanding **why** the bug exists and how to prevent similar issues.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to debug this issue.

Abstraction ladder approach:
1. Concept level: what category of bug is this (race condition, memory leak, logic error)?
2. Mechanism level: why does it happen in my specific code?
3. Solution level: how to fix + how to prevent similar bugs?

Error-tolerance: explain without judgment, suggest improvements for next time.

Bug description: [describe bug]
Code: [paste code]
Error logs: [paste logs if available]
```

**Output:**  
- Concept: Bug category and general pattern
- Mechanism: Specific cause in your code with line references
- Solution: Fix with explanation + prevention strategy
- Learning: Pattern to watch for in future

---

## 🏗️ Use Case 6 — Architecture Decision with Trade-off Analysis
> Focus: choosing between architectural approaches with explicit reasoning and context-aware recommendations.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to this architecture decision.

Meta over Micro: establish frame first (team size: N, timeline: X months, 
scale: Y users, constraints: Z).

Then deliver 2-3 architectural options with:
- Trade-offs for each (development speed vs scalability vs complexity)
- Recommendation with reasoning
- Migration path if switching later

One Source of Truth: version your decision (v1.0) with assumptions listed.

Decision: [describe what you're choosing between, e.g., "microservices vs monolith"]
Context: [team, timeline, scale, constraints]
```

**Output:**  
- Frame: Context and constraints explicitly stated
- Options: 2-3 architectural approaches
- Trade-offs: Pros/cons for each based on your context
- Recommendation: Best choice with reasoning
- Versioned decision document with assumptions

---

## 🔧 Use Case 7 — Legacy Code Refactoring with Stepwise Explanation
> Focus: understanding messy legacy code and refactoring it systematically with explanations at each step.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to refactor this legacy code.

Mirror then lead: first mirror what this code does (your understanding), 
then lead toward modern patterns.

Rhythmic alignment: break refactoring into digestible steps, each with:
- Why this step (rationale)
- What changes (diff)
- What improves (benefit)

Respect the rhythm: no overwhelming rewrites, stepwise improvements.

Legacy code: [paste code]
Target patterns: [e.g., SOLID principles, functional style, async/await]
```

**Output:**  
- Mirror: "This code does X using legacy pattern Y"
- Step-by-step refactoring (3-7 steps)
- Each step: rationale → changes → improvements
- Final refactored code
- Migration guide if needed

---

## ⚡ Use Case 8 — Performance Optimization with Profiling Guidance
> Focus: identifying bottlenecks and optimizing systematically with measurable improvements.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to optimize this code.

Abstraction ladder:
1. Concept: where are likely bottlenecks? (database queries, loops, memory allocation)
2. Procedure: how to profile and measure?
3. Solution: optimized code with expected performance gain

Structure → content → conclusion:
- Analysis of current performance
- Profiling strategy
- Optimizations ranked by impact
- Expected improvements (e.g., "5s → 500ms")

Code: [paste code]
Current performance: [e.g., "takes 5 seconds"]
Target: [e.g., "should be under 500ms"]
```

**Output:**  
- Concept: Bottleneck identification
- Procedure: Profiling approach with tools
- Optimized code with explanations
- Expected performance gains
- Verification strategy

---

## 🌐 Use Case 9 — API Design with Developer Experience Focus
> Focus: designing intuitive APIs that developers will enjoy using, with clear contracts and usage examples.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to design this API.

Semantic mirroring: extract key entities and operations from requirements.

Output Kit: Research Note format
- Thesis: core API entities and their relationships
- Mechanism: endpoints, methods, payload structures
- Consequence: how this simplifies developer experience

Audience: [e.g., frontend developers, mobile team]
Requirements: [describe what API should do]
```

**Output:**  
- Thesis: Core entities (User, Product, Order, etc.)
- Mechanism: RESTful/GraphQL design with examples
- DX benefits: How it simplifies client code
- OpenAPI/Schema definition
- Usage examples for each endpoint

---

## 📚 Use Case 10 — Learning New Tech with Structured Understanding
> Focus: quickly grasping new frameworks/libraries through structured explanation aligned with your existing knowledge.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to explain [new technology/framework].

Abstraction ladder:
1. Concept: what problem does it solve? (relate to what I already know)
2. Mechanism: how does it work under the hood?
3. Practice: when to use, when NOT to use, code examples

Native-Language First: explain in [your language], keep technical terms as-is.

Vector extension: if I ask about specific feature, connect it to broader pattern.

Technology: [e.g., "React Server Components", "Rust ownership model"]
My background: [e.g., "experienced with React Client Components"]
```

**Output:**  
- Concept: Problem it solves (with analogies to familiar tech)
- Mechanism: How it works (simplified, then detailed)
- Practice: Use cases + anti-patterns + code examples
- Mental model: How to think about it
- Next steps: What to learn next

---

## 🎯 Use Case 11 — Pull Request Review with Constructive Feedback
> Focus: providing helpful, non-judgmental feedback on colleague's code with specific improvement suggestions.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to review this PR.

Tone: confidently calm, scientifically intuitive, without bragging.

Structure:
1. What's good (2-3 specific points)
2. What to improve (prioritized: critical → important → nice-to-have)
3. How to improve (concrete suggestions with code examples)

Error-tolerance: suggest improvements, don't criticize choices.

Deliver variants if multiple approaches are valid.

PR diff: [paste diff or describe changes]
Context: [what problem this PR solves]
```

**Output:**  
- ✅ Strengths: Specific praise with reasoning
- 🔧 Improvements: Prioritized by importance
  - Critical: [must fix before merge]
  - Important: [should fix for code quality]
  - Nice-to-have: [optional improvements]
- 💡 Suggestions: Code examples for each improvement
- Tone: Helpful, not judgmental

---

### 🧠 Why Vibe Coding Mode?

**Traditional AI:**  
"Here's the code. Here's the fix."

**Vibe Coding with @Zeya888-Meta:**  
"Let me understand your intent → mirror it → establish quality frame → explain my reasoning → deliver solution with trade-offs → suggest next steps"

**Key differences:**
- **Native language preservation** — think in your language, not forced English
- **Transparent reasoning** — see the thought process, not just results
- **Cognitive rhythm matching** — AI adapts to your thinking style
- **Reproducible quality** — same high quality across sessions through CR-loop

---

### 🔗 Integration with Pipeline Rules

For complex tasks, combine Vibe Coding with pipeline:

```
1. @Zeya888-Meta — establish intent and frame
2. @analysis.mdc — structure into plan
3. @run-task.mdc — execute with validation
4. @Zeya888-Meta — deep dive into complex sub-tasks
5. @test-qualification.mdc — validate quality
6. @meta.extract.mdc — capture learnings
```

**Use Vibe Coding when:**
- Exploring unfamiliar code
- Making architectural decisions  
- Debugging complex issues
- Learning new technologies
- Reviewing code deeply

**Use Pipeline when:**
- Executing structured plans
- Managing multi-step migrations
- Maintaining consistent workflow across team

---

🪶 *Next section:*  
Use Cases 12–14 → `test-qualification.mdc`, `test-to-success.mdc`, `meta.extract.mdc`
