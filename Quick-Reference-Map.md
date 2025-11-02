# 🗺️ Zeya888 Rules System — Quick Reference Map

**Fast navigation through 52 rules**

---

## 📚 SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    PHILOSOPHICAL FOUNDATION                   │
│                                                              │
│  @Zeya888-Meta.mdc — Vibe Coding (co-reasoning philosophy)  │
│      ↓                                                       │
│  CR-loop: Intent → Mirror → Frame → Synthesis → Test →      │
│           Deliver                                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    UNIVERSAL WORKFLOW                         │
│                                                              │
│  @analysis.mdc — Hard analysis (no fantasies)               │
│      ↓                                                       │
│  @run-task.mdc — Universal orchestrator                     │
│      ↓                                                       │
│  @listx-decomposition.mdc — Task decomposition              │
│      ↓                                                       │
│  @itemy-*.mdc (7 phases) — Executing each ItemY:            │
│    understanding → knowledge → acceptance → planning →       │
│    execution → validation → retrospective                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                TESTING RULES ECOSYSTEM (3 LEVELS)            │
│                                                              │
│  @quality-gates.mdc ← SSOT (all metrics here)               │
│      ↓                                                       │
│  ┌──────────────┬──────────────────┬────────────────────┐  │
│  │ UNIT         │ INTEGRATION      │ E2E                │  │
│  │ (isolation)  │ (modules)        │ (workflows)        │  │
│  ├──────────────┼──────────────────┼────────────────────┤  │
│  │ 1 file       │ .core + 8 app.   │ .core + 11 app.    │  │
│  │ 2284 lines   │ modular          │ modular            │  │
│  ├──────────────┼──────────────────┼────────────────────┤  │
│  │ Phase 1:     │ Phase 1:         │ Phase 1:           │  │
│  │ Infra        │ Infra + Test DB  │ Infra + Snapshots  │  │
│  │              │                  │                    │  │
│  │ Phase 2.1:   │ Phase 2:         │ Phase 2:           │  │
│  │ Smoke (60+)  │ Contract Valid.  │ Deploy Workflows   │  │
│  │              │                  │                    │  │
│  │ Phase 2.2:   │ Phase 3:         │ Phase 3:           │  │
│  │ Real Tests   │ Flow Testing     │ Component Flows    │  │
│  │              │                  │                    │  │
│  │ Phase 2.3:   │                  │ Phase 4:           │  │
│  │ Strategic    │                  │ Full Pipeline      │  │
│  └──────────────┴──────────────────┴────────────────────┘  │
│                       ↓                                      │
│  @test-qualification.mdc ← Auto-trigger at Gate 3           │
│      ↓                                                       │
│  @test-to-success.mdc ← Hardhat-specific fixing             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    META RULES (REFLECTION)                   │
│                                                              │
│  @meta.extract.mdc — Capture MCP (6 dimensions)             │
│      ↓                                                       │
│  @meta.gap.mdc — Compare MCP vs TCP → Meta-Instructions     │
│      ↓                                                       │
│  @meta.create-rule.mdc — Transform to new persistent rule   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               SPECIALIZED RULES (DOMAIN-SPECIFIC)            │
│                                                              │
│  @mockups-to-components.mdc — UI evolution                  │
│  @transformation-starter.mdc — Prompt generation            │
│  @space-starter.mdc — Dialogue launch                       │
│  @self-identification-*.mdc — AI identity (3 variants)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 WHEN TO USE WHAT

### **Getting Started**
```
Task unclear → @analysis.mdc
Task structured → @run-task.mdc
Need prompt → @transformation-starter.mdc
```

**💡 Practical Analogy**: Think of it like cooking:
- @analysis.mdc = Reading the recipe, understanding ingredients
- @run-task.mdc = Following step-by-step cooking instructions
- @transformation-starter.mdc = Creating your own recipe template

---

### **Testing**
```
Create Unit tests → @unit-test-build.mdc
Create Integration tests → @integration-test-build.core.mdc
Create E2E tests → @e2e-test-build.core.mdc

Tests failing (Hardhat) → @test-to-success.mdc (auto-active)
Check test quality → @test-qualification.mdc
```

**💡 Practical Analogy**: Testing levels like building inspection:
- **Unit** = Checking individual bricks (isolated modules)
- **Integration** = Checking walls (modules working together)
- **E2E** = Checking entire building (full user journeys)

---

### **Reflection**
```
Completed dialogue → @meta.extract.mdc (capture MCP)
Need GAP analysis → @meta.gap.mdc (compare with role)
Create new rule → @meta.create-rule.mdc
```

**💡 Practical Analogy**: Like fitness tracking:
- @meta.extract = Recording your workout (capturing cognitive profile)
- @meta.gap = Comparing with fitness goals (target vs current)
- @meta.create-rule = Creating custom workout routine (new persistent rule)

---

### **UI/Design**
```
Have PNG mockups → @mockups-to-components.mdc
```

---

## 📊 INTEGRATION PATTERNS

### **Pattern 1: Universal Task**
```
User Request
    ↓
@analysis.mdc (optional, if complex)
    ↓
@run-task.mdc
    ↓
ListX → ItemY1 → ItemY2 → ... → ItemYN
    ↓
Result + Retrospective
```

**🔧 Real-World Example**:
```
Task: "Refactor authentication system"
    ↓
@analysis (understand current auth flow)
    ↓
ListX: [
  ItemY1: Analyze current AuthService
  ItemY2: Design new AuthStrategy pattern
  ItemY3: Implement JWT validation
  ItemY4: Migrate existing users
  ItemY5: Update tests
]
    ↓
Execute each ItemY sequentially
    ↓
Retrospective: Lessons learned
```

---

### **Pattern 2: Unit Testing**
```
"Create unit tests" 
    ↓
@unit-test-build.mdc (self-orchestrating)
    ↓
Phase 1 (Infra) → Phase 2.1 (Smoke)
    ↓
Gate 3: @test-qualification.mdc (auto-trigger)
    ↓
Phase 2.2 (Real Tests) → Gate 4 (ROI)
    ↓
Production Ready (8.5+/10)
```

**🔧 Real-World Example**:
```
Project: UserService tests
    ↓
Phase 1: Setup Jest + mocks (30 min)
    ↓
Phase 2.1: 60 smoke tests (methods exist) (2 hours)
    ↓
Gate 3: Quality check → Score 6.5/10
    ↓
Phase 2.2: Transform to real tests → Score 8.7/10 (4 hours)
    ↓
Ship it! (no perfectionism)
```

---

### **Pattern 3: Meta Evolution**
```
Complete task
    ↓
@meta.extract.mdc (capture MCP)
    ↓
@meta.gap.mdc (compute gaps)
    ↓
Meta-Instructions
    ↓
@meta.create-rule.mdc (convert to rule)
    ↓
New rule in .cursor/rules/
```

**🔧 Real-World Example**:
```
After completing: "Build testing framework"
    ↓
Extract MCP: StructuralThinking=8, CognitiveDepth=7
    ↓
GAP vs CTO role: Need +2 CognitiveDepth
    ↓
Meta-Instruction: "Always analyze root cause, not symptoms"
    ↓
New rule: @root-cause-analysis.mdc
```

---

## 🔑 KEY CONCEPTS

### **Vibe Coding**
**Simple Explanation**: AI doesn't replace your style, it resonates with it.

**Practical Example**:
```
❌ Bad: AI copies generic Stack Overflow solutions
✅ Good: AI learns YOUR coding patterns and extends them

Your style: 
  - Prefer functional over OOP
  - Use descriptive variable names
  - Write comments in Russian

AI adapts:
  - Suggests functional approaches
  - Generates descriptive names
  - Writes comments in Russian
```

**Technical Detail**: 6-phase CR-loop (Intent → Mirror → Frame → Synthesis → Test → Deliver)

---

### **ListX → ItemY**
**Simple Explanation**: Break big tasks into atomic units.

**Practical Example**:
```
Task: "Add OAuth login"

❌ Bad approach:
  - Start coding immediately
  - Get lost in complexity
  - Forget edge cases

✅ Good approach (ListX → ItemY):
  ListX: OAuth Implementation
    ItemY1: Research OAuth 2.0 spec
    ItemY2: Setup OAuth provider (Google)
    ItemY3: Implement authorization flow
    ItemY4: Handle token refresh
    ItemY5: Add error handling
    ItemY6: Write tests
```

**Technical Detail**: ListX = multi-level decomposition, ItemY = atomic unit (7 phases)

---

### **Quality Gates** (4 gates)
**Simple Explanation**: Checkpoints to ensure quality at each step.

**Practical Example**:
```
Writing tests for PaymentService:

Gate 1: Existence
  ✅ Does PaymentService.test.js exist? YES
  
Gate 2: Passing
  ✅ Do all tests pass? YES (45/45 tests green)
  
Gate 3: Validation ⚠️ CRITICAL
  ❌ Do tests check REAL behavior?
  Finding: Tests only check "method exists", not actual payment logic
  Action: Transform to real tests
  
Gate 4: Strategic
  ✅ Is 8.5/10 enough or continue? YES, ship it!
```

**Technical Detail**: Gate 3 auto-triggers @test-qualification.mdc

---

### **MCP (MetaCognitive Profile)** (6 axes, 0-10)
**Simple Explanation**: Track quality of your thinking, like fitness metrics for your brain.

**Practical Example**:
```
Like tracking workout progress:

Physical Fitness:          Cognitive Fitness (MCP):
- Strength                 → StructuralThinking (organization)
- Flexibility              → Reflectivity (self-analysis)
- Endurance                → CognitiveDepth (analysis depth)
- Coordination             → CollaborativeSymmetry (AI ↔ Human balance)
- Balance                  → EmotionalRegulation (staying calm)
- Speed                    → IntentClarity (clear goals)

Your MCP score 6/10 → Target 8/10 → Train with meta-instructions
```

**Technical Detail**: Evidence-based scoring (each score backed by dialogue quotes)

---

## 📖 FILE NAVIGATION

### **Core Rules** (always relevant)
- `Zeya888-Meta.mdc` — philosophy
- `analysis.mdc` — hard analysis
- `run-task.mdc` — universal orchestrator
- `quality-gates.mdc` — SSOT for metrics

### **ItemY Ecosystem** (7 phases)
- `listx-decomposition.mdc`
- `itemy-understanding.mdc`
- `itemy-knowledge-check.mdc`
- `itemy-acceptance.mdc`
- `itemy-planning.mdc`
- `itemy-execution.mdc`
- `itemy-validation.mdc`
- `itemy-retrospective.mdc`

### **Testing Rules**

#### Unit (1 file)
- `unit-test-build.mdc` (monolithic, 2284 lines)

#### Integration (9 files)
- `integration-test-build.core.mdc` (53 lines)
- `integration-test-build.appendix.scenarios.mdc`
- `integration-test-build.appendix.patterns.mdc`
- `integration-test-build.appendix.contracts.mdc`
- `integration-test-build.appendix.flows.mdc`
- `integration-test-build.appendix.phases.mdc`
- `integration-test-build.appendix.quality-gates.mdc`
- `integration-test-build.appendix.examples.mdc`
- `integration-test-build.appendix.troubleshooting.mdc`

#### E2E (12 files)
- `e2e-test-build.core.mdc` (47 lines)
- `e2e-test-build.appendix.harness.mdc`
- `e2e-test-build.appendix.examples.web.mdc`
- `e2e-test-build.appendix.examples.templates.mdc`
- `e2e-test-build.appendix.examples.library.mdc`
- `e2e-test-build.appendix.examples.anti-patterns.mdc`
- `e2e-test-build.appendix.phases.deploy.mdc`
- `e2e-test-build.appendix.phases.component.mdc`
- `e2e-test-build.appendix.phases.catalog.mdc`
- `e2e-test-build.appendix.quality-gates.mdc`
- `e2e-test-build.appendix.reference.mdc`
- `e2e-test-build.appendix.scenarios.mdc`

#### Quality & Fixing
- `test-qualification.mdc` (critical analysis)
- `test-to-success.mdc` (Hardhat fixing)

### **Meta Rules** (3 files)
- `meta.extract.mdc` (capture MCP)
- `meta.gap.mdc` (GAP analysis)
- `meta.create-rule.mdc` (rule factory)

### **Specialized Rules**
- `mockups-to-components.mdc` (UI evolution)
- `transformation-starter.mdc` (prompt gen)
- `space-starter.mdc` (dialogue launch)
- `self-identification.mdc` (basic)
- `self-identification-cto.mdc` (technical)
- `self-identification-cosmic.mdc` (humanitarian)

---

## 🎓 LEARNING PATH

### **Beginner** (first 3 days)
1. Read `Zeya888-Meta.mdc` — understand philosophy
2. Learn `@run-task.mdc` + ListX/ItemY pattern
3. Try `@unit-test-build.mdc` on simple project

**💡 Practical Tip**: Start with something you know. If familiar with testing, start there. If familiar with refactoring, use @run-task for that.

---

### **Intermediate** (1-2 weeks)
4. Use `@analysis.mdc` for complex tasks
5. Master `@integration-test-build` and `@e2e-test-build`
6. Understand Quality Gates and @test-qualification

**💡 Practical Tip**: Pick ONE rule per week. Overuse it intentionally to deeply learn patterns.

---

### **Advanced** (1+ month)
7. Run `@meta.extract` after tasks
8. Use `@meta.gap` for cognitive growth
9. Create your own rules via `@meta.create-rule`

**💡 Practical Tip**: At this stage, you'll naturally feel when to use what. Trust your intuition, it's now trained.

---

## 🚀 QUICK STARTS

### **Create Unit tests**
```
"Create production-ready unit tests for src/ project
Method: @unit-test-build.mdc"
```

### **Check test quality**
```
"Check test quality in tests/unit/
If < 8/10, bring to production ready
Method: @unit-test-build.mdc"
```

### **Fix failing tests (Hardhat)**
```
"Fix errors in contracts/tests/SpiralEngine.test.js
Method: @test-to-success.mdc"
```

### **Create Integration tests**
```
"Create integration tests for modules:
- ContractManager + ArweaveManager
- UserService + Database
Method: @integration-test-build.core.mdc"
```

### **Capture MCP after dialogue**
```
"Create meta extract for this dialogue
dialog_id: 'test-refactoring-001'
Method: @meta.extract.mdc"
```

### **GAP Analysis for role**
```
"Perform GAP analysis for CTO role
Use last 3 extracts
Method: @meta.gap.mdc"
```

---

## 📊 METRICS REFERENCE

### **Quality Thresholds** (from @quality-gates.mdc)

#### Unit Tests
- Score: `>= 8.5/10`
- Critical Coverage: `>= 85%`
- Runtime: `< 60s`
- Real Tests Ratio: `>= 60%`

**💡 What this means**:
```
Score 8.5/10:
  ✅ Tests validate REAL behavior (not just "method exists")
  ✅ Critical paths covered
  ❌ NOT perfect (9.5/10 = diminishing returns)
  
Critical Coverage 85%:
  ✅ All payment logic tested
  ✅ All auth flows tested
  ❌ NOT 100% (getters/setters can be skipped)
  
Runtime < 60s:
  ✅ Fast feedback loop
  ✅ Developers run tests frequently
  ❌ NOT < 1s (that's unit level expectation)
```

---

#### Integration Tests
- Score: `>= 8.5/10`
- Contract Coverage: `>= 80%`
- Flow Coverage: `>= 70%`
- Runtime: `< 5m`

---

#### E2E Tests
- Score: `>= 8.5/10`
- Workflow Coverage: `>= 70%`
- Runtime: `< 30m`
- Flakiness: `< 5%`

---

### **MCP Scoring** (0-10 scale)
- `0-3`: Problem area (needs work)
- `4-6`: Average level (functional)
- `7-8`: Good level (professional)
- `9-10`: Master level (expert)

**💡 Real-World Interpretation**:
```
StructuralThinking = 6:
  "I can break down tasks, but sometimes miss dependencies"
  
StructuralThinking = 8:
  "I naturally use ListX → ItemY, spot all dependencies"
  
StructuralThinking = 9:
  "I design multi-level architectures effortlessly"
```

---

## 🔗 USEFUL LINKS

- **Detailed analysis**: `docs/Zeya888-Rules-System.en.md`
- **Conceptual questions**: see Q1-Q9 section in analysis
- **GitHub repo**: https://github.com/eslinko/cursor-rules

---

## 🎯 ACCESSIBILITY TIPS FOR ENGINEERS

### **If you're a Backend Developer**
Start with: `@unit-test-build.mdc` (familiar territory)
Then: `@integration-test-build.core.mdc` (API testing)
Skip: UI-related rules until needed

### **If you're a Frontend Developer**
Start with: `@mockups-to-components.mdc` (UI evolution)
Then: `@unit-test-build.mdc` (component testing)
Later: `@e2e-test-build.core.mdc` (user flows)

### **If you're a DevOps Engineer**
Start with: `@e2e-test-build.core.mdc` (full pipeline)
Then: `@integration-test-build.core.mdc` (service integration)
Use: `@analysis.mdc` for infrastructure planning

### **If you're new to AI-assisted coding**
Start with: `Zeya888-Meta.mdc` (understand philosophy)
Then: Simple tasks with `@run-task.mdc`
Gradually: Add specialized rules as needed

---

**Version**: 1.0  
**Date**: 2025-11-02  
**Updated**: When new rules added  
**Language**: English (original: Russian)

