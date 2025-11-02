# 🚀 Zeya888 Rules with Claude — Quick Usage Guide

**For**: Using Cursor rules in Claude conversations  
**Date**: 2025-11-02

---

## 📋 Setup (2 minutes)

### Step 1: Start Claude Conversation

**Copy-paste** the contents of `Claude-Starter-Prompt.txt` at the beginning of conversation:

```
[Paste full text from Claude-Starter-Prompt.txt]
```

Claude will respond with confirmation:
```
✅ Cursor Rules Adapter Loaded
I will:
- Apply syntax adapter to every .mdc file
- Extract front matter descriptions
[... etc ...]

Ready to receive first rule. What task are we working on?
```

---

### Step 2: Attach Adapter File

**Upload** to conversation:
```
cursor-syntax-adapter.mdc
```

Claude now has a **persistent reference** — can return to adapter logic when needed.

---

### Step 3: Provide Task-Specific Rule

**Depending on task**, upload needed rule:

```yaml
testing_task: "unit-test-build.mdc"
refactoring_task: "run-task.mdc + analysis.mdc"
quality_check: "test-qualification.mdc"
documentation: "analysis.mdc"
meta_reflection: "meta.extract.mdc"
```

---

## 🎯 Usage Patterns

### Pattern 1: Unit Testing

**Files to upload**:
```
1. Claude-Starter-Prompt.txt [paste in message]
2. cursor-syntax-adapter.mdc [attach]
3. unit-test-build.mdc [attach]
4. quality-gates.mdc [attach] ← Referenced by unit-test-build
```

**Prompt**:
```
"Use @unit-test-build methodology to create production-ready tests
for my PaymentService module.

Context:
- Language: JavaScript
- Framework: Jest
- Files: src/services/PaymentService.js

Follow all phases: Infrastructure → Smoke → Real → Strategic"
```

**Expected Claude behavior**:
```
✅ Extracts description from front matter
✅ Follows progressive phases
✅ At Gate 3: "⚠️ Checkpoint. Run @test-qualification?"
✅ Uses thresholds from @quality-gates#unit
```

---

### Pattern 2: Modular Rules (Integration Testing)

**Files to upload**:
```
1. Claude-Starter-Prompt.txt [paste]
2. cursor-syntax-adapter.mdc [attach]
3. integration-test-build.core.mdc [attach]
4. integration-test-build.appendix.patterns.mdc [attach]
5. integration-test-build.appendix.contracts.mdc [attach]
6. integration-test-build.appendix.flows.mdc [attach]
7. integration-test-build.appendix.phases.mdc [attach]
8. integration-test-build.appendix.quality-gates.mdc [attach]
9. integration-test-build.appendix.examples.mdc [attach]
10. integration-test-build.appendix.scenarios.mdc [attach]
11. integration-test-build.appendix.troubleshooting.mdc [attach]
12. quality-gates.mdc [attach]
```

**OR** (easier):

**Use Claude Projects**:
```
1. Create Project: "Zeya888 Rules"
2. Upload ALL .cursor/rules/*.mdc files (52 files, one-time)
3. Start conversation in Project
4. Paste Claude-Starter-Prompt.txt
5. Done — all rules available, cross-references work
```

**Prompt**:
```
"Use @integration-test-build.core methodology to create integration tests
for ContractManager + ArweaveManager modules.

Apply minimal mocking strategy (external APIs only).
Follow all phases: Infra → Contract Validation → Flow Testing"
```

**Expected Claude behavior**:
```
✅ Detects modular rule (.core.mdc)
✅ Finds all 8 appendix references
✅ If appendix in context → uses patterns/examples
✅ If appendix missing → informs you, lists files
✅ Follows phases with minimal mocking principle
```

---

### Pattern 3: Task Decomposition

**Files to upload**:
```
1. Claude-Starter-Prompt.txt [paste]
2. cursor-syntax-adapter.mdc [attach]
3. run-task.mdc [attach]
4. listx-decomposition.mdc [attach]
5. analysis.mdc [attach] (optional)
```

**Prompt**:
```
"Use @run-task to refactor my authentication system.

Current: Session in memory (not scalable)
Goal: Move to Redis-based sessions

Apply ListX → ItemY decomposition with all 7 phases."
```

**Expected Claude behavior**:
```
✅ Applies run-task methodology
✅ Creates ListX structure
✅ For each ItemY: understanding → knowledge → acceptance → 
   planning → execution → validation → retrospective
✅ References @itemy-*.mdc (if in context) OR uses embedded logic
```

---

## ⚠️ Important Notes

### Persistence Check

**Every 10-15 messages**, verify Claude remembers adapter:

```
You: "Quick check: What should you do when you see @reference#section?"

Claude should respond:
"I check if referenced file is in context.
 If yes → find ## #section and use content
 If no → inform you about missing file"

If Claude forgot → remind: "Remember cursor-syntax-adapter instructions"
```

---

### Modular Rules

**ALWAYS** either:
- Upload ALL appendix files (tedious)
- OR use Claude Projects (recommended)

**Don't**: Upload only .core.mdc → will be incomplete

---

### Auto-Triggers

**Expect** manual confirmation:
```
Claude: "⚠️ Gate 3 checkpoint. Run @test-qualification?"
You: "Yes"
Claude: [applies qualification]
```

**Don't expect**: Automatic transitions (Claude can't)

---

## 🎯 Recommended Setup

### Option A: Claude Projects (⭐⭐⭐⭐⭐ BEST)

**One-time setup** (15 minutes):
```
1. Create Claude Project: "Zeya888 Development"
2. Upload entire .cursor/rules/ directory (52 files)
3. Claude indexes all rules
```

**Every conversation**:
```
1. Start conversation in Project
2. Paste Claude-Starter-Prompt.txt
3. Say task: "Use @unit-test-build for PaymentService"
4. Claude auto-loads rule from Project ✅
```

**Pros**: 
- All rules available
- Cross-references work
- No repeated uploads

---

### Option B: Per-Conversation Upload (⭐⭐⭐ GOOD)

**Every conversation**:
```
1. Paste Claude-Starter-Prompt.txt
2. Upload cursor-syntax-adapter.mdc
3. Upload task-specific rule(s)
4. Upload dependencies (@quality-gates if needed)
```

**Pros**: 
- Works without Projects
- Explicit file control

**Cons**: 
- Repeat uploads
- Must remember dependencies

---

## 📊 Troubleshooting

### Issue: Claude Forgot Adapter

**Symptom**: Claude treats front matter as code, doesn't detect modular

**Fix**:
```
"Remember: Apply cursor-syntax-adapter.mdc instructions.
 When you see front matter → extract description.
 When you see .core.mdc → check for appendix."
```

---

### Issue: Missing Dependencies Not Detected

**Symptom**: Claude uses incomplete rule without warning

**Fix**:
```
"Check: Does this rule reference other files?
 Apply adapter STEP 2 (scan for @references)."
```

---

### Issue: Auto-Triggers Skipped

**Symptom**: Claude proceeds without checkpoint

**Fix**:
```
"We reached Phase 2.1 completion.
 According to rule, this should trigger Gate 3.
 Apply adapter auto-trigger pattern — remind me."
```

---

## ✅ Validation Checklist

Before starting work with Claude:

```yaml
setup:
  - [ ] Claude-Starter-Prompt.txt pasted
  - [ ] cursor-syntax-adapter.mdc uploaded
  - [ ] Task-specific rule uploaded
  - [ ] Dependencies uploaded (check @references in rule)

during_conversation:
  - [ ] Claude extracts descriptions from front matter
  - [ ] Claude detects modular rules (.core.mdc)
  - [ ] Claude reminds at AUTO-TRIGGER points
  - [ ] Claude asks for missing dependencies

if_issues:
  - [ ] Remind about adapter instructions
  - [ ] Re-paste relevant adapter section
  - [ ] Check file availability in conversation
```

---

## 📖 Quick Reference

### Files You Need

**Always**:
- `Claude-Starter-Prompt.txt` (paste at start)
- `cursor-syntax-adapter.mdc` (attach once)

**Task-Specific** (choose based on task):
```
Testing:
  - unit-test-build.mdc + quality-gates.mdc
  - integration-test-build.core.mdc + 8 appendix + quality-gates.mdc
  - e2e-test-build.core.mdc + 11 appendix + quality-gates.mdc
  - test-qualification.mdc (for quality check)
  - test-to-success.mdc (for fixing Hardhat tests)

Workflow:
  - run-task.mdc + listx-decomposition.mdc
  - analysis.mdc (for documentation/understanding)
  - Zeya888-Meta.mdc (for content creation)

Meta:
  - meta.extract.mdc (capture cognitive profile)
  - meta.gap.mdc (gap analysis)
  - meta.create-rule.mdc (create new rules)
```

---

## 🎯 Success Indicators

**Claude working correctly with adapter**:
- ✅ Mentions "extracting description from front matter"
- ✅ Says "checking context for @referenced-file"
- ✅ Lists missing appendix when .core.mdc uploaded alone
- ✅ Pauses at AUTO-TRIGGER: "⚠️ Checkpoint. Run @rule?"
- ✅ Uses thresholds from @quality-gates#unit when referenced

**Claude forgot adapter**:
- ❌ Treats front matter as code block
- ❌ Ignores @references (doesn't mention checking context)
- ❌ Proceeds past AUTO-TRIGGER without reminding
- ❌ Uses .core.mdc as complete without mentioning appendix

**Fix**: Remind about Claude-Starter-Prompt instructions

---

**Version**: 1.0  
**Date**: 2025-11-02  
**Compatible**: Claude Sonnet 3.5/4.5  
**Related**: cursor-syntax-adapter.mdc, Claude-Starter-Prompt.txt

