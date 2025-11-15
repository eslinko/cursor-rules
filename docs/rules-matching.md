# Zeya888 Rules: Task Type → Rule Stack Matrix

> **Purpose**: Quick reference guide for routing tasks to the right methodology stack in Zeya888 rules ecosystem.

---

## Overview

Zeya888 methodology uses **rule stacks** — sequential activation of specialized rules to handle complex tasks. The meta-layer (`@Zeya888-Meta.mdc`) routes work into the appropriate stack based on task type.

**Key principle:** Meta-layer frames intent and passes control; it never duplicates specialized rule steps.

---

## Rule Stack Matrix

| Task Type | Description | Recommended Stack | Notes |
|-----------|-------------|-------------------|-------|
| **Code / Refactor** | Feature implementation, refactoring, bug fixes | `@analysis` → `@run-task` → `@unit-test-build` / `@integration-test-build.core` | For backend/API changes, add `@quality-gates` validation |
| **Unit Testing** | Single module testing with isolated dependencies | `@analysis` → `@run-task` → `@unit-test-build` → `@test-qualification` | All-in-one rule; includes anti-patterns, templates, quality gates |
| **Integration Testing** | 2-4 modules together, contract validation, workflows | `@analysis` → `@run-task` → `integration-test-build suite` → `@quality-gates` → `@test-qualification` | **Suite**: core + appendix files (see below) |
| **E2E Testing / Workflows** | Complete user journeys with real infrastructure | `@analysis` → `@run-task` → `e2e-test-build suite` → `@quality-gates` → `@test-qualification` → `@test-to-success` | **Suite**: core + appendix files (see below) |
| **Ops / Deploy Playbooks** | Infrastructure setup, deployment flows, node management | `@analysis` → `@run-task` → external docs (`Deploy_Full.md`, `Deploy_Architecture.md`, `node-launch.txt`) + `@quality-gates` (infra) | No dedicated rule; reference project deployment docs |
| **Documentation / Meta** | Journals, plans, content generation, rule maintenance | `@analysis` → `@run-task` → `@Zeya888-Meta` output kits → `AIJournal` / `bridge` | For rule creation/updates: `@meta.create-rule`, `@meta.gap` |
| **Incident / Test Fixing** | Debugging failing tests, fixing test infrastructure | `@analysis` → `@run-task` → `@fix-test-failure` (if exists) → relevant build-rule suite → `@test-to-success` | Emphasize honest testing, no false positives |

---

## Complex Rule Suites

Some rules are split into **core** + **appendix** files for maintainability. When working with these suites, reference the **core** file; appendix files are automatically referenced.

### Integration Test Build Suite

**Core:** `@integration-test-build.core.mdc`

**Appendix files (automatically referenced):**
- `@integration-test-build.appendix.mdc` — extended examples, templates, anti-patterns
- `@integration-test-build.appendix.phases.mdc` — phase 1 infrastructure details
- `@integration-test-build.appendix.contracts.mdc` — contract validation (phase 2)
- `@integration-test-build.appendix.flows.mdc` — flow testing (phase 3)
- `@integration-test-build.appendix.patterns.mdc` — integration patterns, minimal mocking strategies
- `@integration-test-build.appendix.quality-gates.mdc` — quality gates specific to integration
- `@integration-test-build.appendix.scenarios.mdc` — context detection and scenarios
- `@integration-test-build.appendix.examples.mdc` — example library
- `@integration-test-build.appendix.troubleshooting.mdc` — troubleshooting reference

**Usage:**
```
"Execute Phase 2 using @integration-test-build.core.mdc"
```
AI automatically loads relevant appendix sections based on phase.

---

### E2E Test Build Suite

**Core:** `@e2e-test-build.core.mdc`

**Appendix files (automatically referenced):**
- `@e2e-test-build.appendix.mdc` — extended examples, templates, anti-patterns
- `@e2e-test-build.appendix.harness.mdc` — E2E harness pattern (infrastructure lifecycle, node management, snapshots)
- `@e2e-test-build.appendix.phases.deploy.mdc` — deployment workflows (phase 2)
- `@e2e-test-build.appendix.phases.component.mdc` — component management workflows (phase 3)
- `@e2e-test-build.appendix.phases.catalog.mdc` — catalog/pipeline workflows (phase 4)
- `@e2e-test-build.appendix.quality-gates.mdc` — E2E-specific quality gates
- `@e2e-test-build.appendix.scenarios.mdc` — context detection and scenarios
- `@e2e-test-build.appendix.reference.mdc` — quick reference, troubleshooting, DoD
- `@e2e-test-build.appendix.examples.library.mdc` — example library
- `@e2e-test-build.appendix.examples.templates.mdc` — copy-paste ready templates
- `@e2e-test-build.appendix.examples.web.mdc` — web app E2E patterns (Playwright)
- `@e2e-test-build.appendix.examples.anti-patterns.mdc` — E2E-specific anti-patterns

**Usage:**
```
"Execute Phase 1 using @e2e-test-build.core.mdc"
```
AI automatically loads relevant appendix sections based on phase.

---

## Meta-Layer Orchestration

`@Zeya888-Meta.mdc` serves as the **routing layer** that:

1. **Frames intent** — clarifies goal, format, boundaries, taboos via Handshake & Intent
2. **Recognizes mode** — determines task type (Observation / Structuring / Resonance)
3. **Routes to stack** — activates appropriate rule sequence from matrix above
4. **Synchronizes context** — checks `AIJournal`, blockers, `AI-Navigator`, confirms manual control
5. **Never duplicates** — meta-layer does not execute specialized rule steps; it only orchestrates

**Example flow:**
```
User: "create integration tests for ProductRegistry module boundaries"

@Zeya888-Meta.mdc:
  1. Handshake: clarifies scope, boundaries
  2. Mode recognition: Integration Testing task type
  3. Route: @analysis → @run-task → integration-test-build suite
  4. Context sync: checks AIJournal for related work
  5. Pass control: activates @analysis.mdc

@analysis.mdc:
  - Analyzes requirements
  - Creates structured plan (ListX → ItemY)

@run-task.mdc:
  - Executes plan items sequentially
  - For each ItemY: activates integration-test-build suite

@integration-test-build.core.mdc:
  - Executes phase-specific steps
  - Auto-loads relevant appendix files
  - Validates against quality gates

@test-qualification.mdc:
  - Final quality check
  - Ensures no false positives
```

---

## Quality Gates Flow

All testing stacks integrate with `@quality-gates.mdc` as the **Single Source of Truth** for thresholds:

- **Unit tests:** `@quality-gates#unit` (score ≥ 8.5, critical coverage ≥ 85%, runtime < 60s)
- **Integration tests:** `@quality-gates#integration` (Gate 1-4: contract compatibility, flow passing, real validation, ROI)
- **E2E tests:** `@quality-gates#e2e` (Gate 1-4: infrastructure validation, workflow passing, real E2E validation, selective coverage)

Quality gates are **auto-triggered** at Gate 3 (validation phase) for all testing rules.

---

## Common Patterns

### Pattern 1: Building Tests from Scratch

```
1. "Analyze testing requirements using @analysis.mdc method"
2. "Execute Phase 1 using @[unit|integration|e2e]-test-build.core.mdc"
3. [AI sets up infrastructure]
4. "Execute Phase 2 using @[unit|integration|e2e]-test-build.core.mdc"
5. [AI generates smoke tests]
6. "Execute Phase 3 using @[unit|integration|e2e]-test-build.core.mdc"
7. [AI creates real tests]
8. Auto-trigger: @test-qualification.mdc validates quality
```

### Pattern 2: Debugging Failing Tests

```
1. "Identify root cause using @analysis.mdc method"
2. "Fix tests using @test-to-success.mdc method"
3. [AI fixes one issue at a time with validation]
4. "Validate using @test-qualification.mdc method"
5. [AI ensures no false positives]
```

### Pattern 3: Extending Existing Test Suite

```
1. "Analyze gaps using @meta.gap.mdc method"
2. "Execute Phase [N] using @[rule]-build.core.mdc"
3. [AI extends suite with new tests]
4. Auto-trigger: @test-qualification.mdc validates additions
```

---

## Important Notes

1. **Manual activation only** — all rules have `apply: manual`, `alwaysApply: false`. Explicitly reference rules: `using @rule.mdc method`
2. **Suite loading** — when referencing `@[suite]-build.core.mdc`, AI automatically loads relevant appendix files based on phase/context
3. **Quality gates** — always validate through `@test-qualification.mdc` after test creation; auto-triggered at Gate 3
4. **External docs** — ops/deploy tasks reference project docs (`Deploy_Full.md`, etc.) rather than dedicated rules
5. **Context sync** — meta-layer always checks `AIJournal.md`, blockers, `AI-Navigator.md` before routing

---

## Quick Reference Commands

```bash
# Unit Testing
"Execute Phase 1 using @unit-test-build.mdc method"      # Infrastructure
"Execute Phase 2 using @unit-test-build.mdc method"      # Smoke tests
"Execute Phase 3 using @unit-test-build.mdc method"      # Real tests

# Integration Testing
"Execute Phase 1 using @integration-test-build.core.mdc" # Multi-module harness
"Execute Phase 2 using @integration-test-build.core.mdc" # Contract validation
"Execute Phase 3 using @integration-test-build.core.mdc" # Flow testing

# E2E Testing
"Execute Phase 1 using @e2e-test-build.core.mdc"         # E2E infrastructure
"Execute Phase 2 using @e2e-test-build.core.mdc"         # Deploy workflows
"Execute Phase 3 using @e2e-test-build.core.mdc"         # Component workflows
"Execute Phase 4 using @e2e-test-build.core.mdc"         # Full pipeline

# Quality Validation
"check tests using @test-qualification.mdc method"       # Manual quality check

# Debugging
"bring tests to 100% success using @test-to-success.mdc method"

# Analysis & Planning
"analyze requirements using @analysis.mdc method"
"execute Phase [N] using @run-task.mdc method"
```

---

**Version:** 1.0  
**Last Updated:** 2025-11-13  
**Related:** `@Zeya888-Meta.mdc`, `@analysis.mdc`, `@run-task.mdc`, `@quality-gates.mdc`

