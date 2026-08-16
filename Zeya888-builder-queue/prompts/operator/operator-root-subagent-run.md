# Operator root — subagent overnight RUN

**Категория:** operator (Phase B overnight)  
**Etalon (structure):** [`.cursor/plans/Orchestrator_Builder_Reference.plan.md`](../../../../../.cursor/plans/Orchestrator_Builder_Reference.plan.md) — **не править**; транспонировать в новый рабочий план  
**Rules SSOT:** [`../../guides/orchestrator-builder-reference.md`](../../guides/orchestrator-builder-reference.md)  
**Parent:** [`../../guides/operator-root-orchestrator.md`](../../guides/operator-root-orchestrator.md)  
**Fences:** [`../../tools/workflow-console.html`](../../tools/workflow-console.html) · [`../../core/workflow.md`](../../core/workflow.md)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

**How-to (человек):** [`../../guides/operator-how-to-run-queue.md`](../../guides/operator-how-to-run-queue.md)

## Юзкейсы (когда этот промпт)

| # | Ситуация | Действие |
|---|----------|----------|
| 1 | Нужна длинная очередь (`$queueSpec`) без paste в UI-чаты | SUBAGENT RUN: plan + process/session/wave + 2 Task overnight |
| 2 | Session уже есть с живыми `*_agent_id` | RUN: **resume тех же uuid**; Session starter не повторять |
| 3 | Session есть, ids `null`/dead | RUN: spawn Builder + Validator once → записать ids в session.yaml |
| 4 | Холодный OP (нет session) | RUN сам создаст session **или** сначала START — оба валидны |

**Вход:** `$builderProject=` + `$queueSpec=` (defaults: `mode=sequential`, `overnight=on`, `delivery=subagent`).

**Не этот промпт:**

| Ситуация | Куда |
|----------|------|
| Оператор сам paste packets в `BLD-*`/`VAL-*` UI-чаты | [`operator-root-wave.md`](./operator-root-wave.md) |
| Только bind session без очереди | [`operator-root-start.md`](./operator-root-start.md) |

### Как достоверно идентифицировать субагентов (Phase B)

| Механизм | Где | Как работает |
|----------|-----|----------------|
| **`builder_agent_id` / `validator_agent_id`** | `OP-<project>.session.yaml` **только** | Task **resume** того же uuid на каждую фазу/story ([orchestrator-builder-reference.md](../../guides/orchestrator-builder-reference.md) §4) |
| Titles `BLD-`/`VAL-` | session (label) | Удобная метка; **не** ключ resume Task |
| Имя в prompt при spawn | «Builder» / «Validator» + ROLE | Человекочитаемо; **SSOT resume = uuid в session**, не display name |
| Plan file | `.cursor/plans/OP-*.plan.md` | **Запрет** класть `*_agent_id` туда |

Новая волна **не** требует новых субагентов, если оба id живы ([reference §4](../../guides/orchestrator-builder-reference.md)). Dead id → re-spawn + переписать session.

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
@.cursor/plans/Orchestrator_Builder_Reference.plan.md
@docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md
@docs/methodology/Zeya888-builder-queue/guides/operator-root-orchestrator.md
@docs/methodology/Zeya888-builder-queue/core/workflow.md
@docs/methodology/Zeya888-builder-queue/core/session-starter.md
@docs/methodology/Zeya888-builder-queue/specs/profiles.yaml
@docs/methodology/Zeya888-builder-queue/tools/workflow-console.html
@docs/methodology/Zeya888-builder-queue/guides/fixed-builder-plan-execution.md
$builderProject=
$queueSpec=
# defaults if omitted: mode=sequential · overnight=on · delivery=subagent

Operator root SUBAGENT RUN. Follow orchestrator-builder-reference.md rules.
TRANSPOSE etalon .cursor/plans/Orchestrator_Builder_Reference.plan.md into a NEW working plan — do NOT edit the etalon.
builder_project: $builderProject
queue_spec: $queueSpec

MODE: orchestrate only — no product code, no invent AC, no push unless operator said.
Claims: Read/Glob only; else Unknown.
delivery=subagent: spawn/resume EXACTLY two agents (Builder + Validator). No operator paste.
overnight=on (default): no pause after story; auto-approve P1.3b/P5b GATE; wave halt ONLY on стоп|stop|pause|halt.
agent_id live ONLY in session.yaml — never in .cursor/plans/*.

## Step 1 — Resolve profile (console fill)
From specs/profiles.yaml for $builderProject (SSOT paths). Cross-check workflow-console.html PROJECT_PROFILES:
- tasks_dir → $tasksRoot, plan_file → $planFile, focus_folder, pipeline_doc
- execution_skill_primary / execution_skill_path
- $verifyCmd = python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project <key> --verify
- contract: docs/methodology/Zeya888-builder-queue/contracts/<key>-operator-contract.md
- dashboard path: from that contract (do not invent filename)
- hasUxPipeline: true only for spa in console → P3/P4 spa UX when story is UI; else clean P1.3/P3/P4
If unknown/disabled key → Ask and STOP.
Do not copy landing hardcoded paths (Landing_builder, OP-landing.process.md) into a non-landing run.

## Step 2 — Resolve queue ($queueSpec free-form)
Build ordered story @paths (facts only). Interpret $queueSpec as one of:
A) remaining / "all Remaining in dashboard" → Read dashboard §Remaining/Ready; order Pri then section order
B) exact @paths or story/BUG ids → Glob/Read; skip Product Done unless residual *b or operator forced
C) number range (e.g. BUG-02..BUG-14 or 11-19) → map via dashboard/INDEX keys
D) Pri filter (e.g. P0-P1 Ready) → intersect with Remaining
Ask ONLY if zero stories or ambiguous id. mode=sequential default.

## Step 3 — WRITE working Cursor plan (transpose etalon)
Path:
`.cursor/plans/OP-$builderProject-<slug>.plan.md`
slug from queueSpec + UTC date (e.g. remaining-20260814). Example: .cursor/plans/OP-gateway-remaining-20260814.plan.md

Copy STRUCTURE from etalon Orchestrator_Builder_Reference.plan.md. KEEP:
- Model: 2 subagents, verbatim fences, no paste, OP does not write product code
- Overnight non-stop generic table (stop only стоп|stop|pause|halt; auto-approve P1.3/P5; BLOCKED → next; P8 no push)
- Session starter once + validator bootstrap once; resume same ids
- Plan-sim variant 1 (P1.3a/b, P5a/b, OP auto-approve overnight)
- Phase script table (same steps)

REPLACE with this run's facts:
- Frontmatter: name: OP-<project> <slug>; overview = profile + queueSpec; todos = bootstrap+run (NOT etalon write-process-ssot todos)
- Titles: OP-<project> / BLD-<project> / VAL-<project> — do NOT copy Landing / Landing V
- Constants table from Step 1 ($planFile, $tasksRoot, $verifyCmd, contract, dashboard, skill, P1.3 variant)
- Queue table = resolved $queueSpec (not the 18 landing bugs)
- process/session/wave paths under THIS $tasksRoot
- Prompt sources (filled) table: each phase → console block id / workflow.md § / session-starter.md + already-filled constants (as if operator picked profile in workflow-console)

STRIP landing-only (unless this run IS landing AND contract/wave notes require it — facts only, no invent):
- 18 Ready bug table, BUG-03b narrative, image-blockers, asset-gate 15/17/20
- OP-landing.process.md / Landing_builder.plan.md hardcoded
- «следующая QUEUED: BUG-11»

NEVER put builder_agent_id / validator_agent_id in this plan file.
Verify the new plan exists (Read) before Step 4.
After write: briefly show plan path + profile constants + queue count — then CONTINUE (do not wait for operator approve).

## Step 4 — Materialize process / session / wave
Write/update:
1) {$tasksRoot}/run-reports/operator-sessions/OP-$builderProject.process.md
   — mirror of working plan (model, overnight, constants, queue, plan-sim + ROLE_LOCK, phase script)
   — NO agent ids; link to the new .cursor/plans/OP-*.plan.md
2) {$tasksRoot}/run-reports/operator-sessions/OP-$builderProject.session.yaml
   — delivery=subagent, overnight, pause_after_story=false, auto_approve_plan=true,
     process_file, working_plan path, titles, builder_agent_id/validator_agent_id (keep live ids if present),
     Updated=live ISO after write
3) {$tasksRoot}/run-reports/operator-waves/wave-<YYYYMMDD>-<slug>.md
   — queue checklist + handoff log + stop-rules
Verify files exist (Read).

## Step 5 — Ensure two subagents (console-fill fences)
If builder_agent_id missing/dead:
  Task spawn Builder: Session starter from session-starter.md + console Session starter,
  OPERATOR CONFIG filled for this profile (builder_project, workspace_root, pipeline_profile=builder_full, $planFile)
  → write builder_agent_id to session.yaml
Else resume that id.
If validator_agent_id missing/dead:
  Task spawn Validator: orchestrator-builder-reference §4.1 bootstrap + this profile's operator-contract (analysis.mdc, RO)
  → write validator_agent_id
Else resume.
Do not use UI chat paste for fences in this mode.

## Step 6 — Run phase script per story (non-stop)
For each QUEUED story in order, follow reference §8 / working plan phase table.

Prompt sources (verbatim templates, fill same tokens as workflow-console buildPromptText):
- Session starter → session-starter.md + console Session starter
- P1.3 / P3 / P5 / P6 / P8 → console / workflow.md (spa UX P3/P4 only if hasUxPipeline AND story is UI)
- P4 / P7 → console validator fences → Validator resume
- P2 → YOU run shell: $verifyCmd + write-build-window
- P1.3 and P5 → TWO calls: PLAN_DRAFT then (auto-approve) PLAN_APPLY + ROLE_LOCK (reference §5)
- Fixed $planFile: @attach only; never Build/Execute UI
- Each Task prompt prepend ROLE_LOCK (reference §4.2)
Do NOT paraphrase phase fences.

After each phase: verify RETURN paths on disk → update wave MD → next phase.
After P8/DONE or BLOCKED: immediately next story — no mid-queue operator report.
Skip P1.3 only if pkg/pipeline already on disk (document in wave).
BLOCKED prod/deploy/asset: facts in wave → continue queue (no invent art/AC).

Stop-rules: verify FAIL → BLOCKED + next; WAVE_STALLED_NO_DELTA → leave story, next;
P5_DISPOSITION_INCOMPLETE → re-P5; wave halt only on explicit operator stop.

## Step 7 — STOP (only when halt or queue exhausted)
Reply with ONLY:
1) working Cursor plan path (.cursor/plans/OP-…)
2) wave MD path
3) DONE / BLOCKED / remaining counts (facts)
4) session.yaml path (+ whether agent ids live)
5) process.md path
6) reminder: P8 was local no-push unless operator ordered push
Do not invent next backlog; await new $queueSpec or halt.
```

---

## Примечания

- How-to для человека: [`../../guides/operator-how-to-run-queue.md`](../../guides/operator-how-to-run-queue.md).
- Etalon (не править): [`.cursor/plans/Orchestrator_Builder_Reference.plan.md`](../../../../../.cursor/plans/Orchestrator_Builder_Reference.plan.md).
- Rules: [`../../guides/orchestrator-builder-reference.md`](../../guides/orchestrator-builder-reference.md).
- Proven landing facts (not norm): `landing/docs/tasks/run-reports/operator-sessions/OP-landing.process.md`.
- MVP paste alternative: [`operator-root-wave.md`](./operator-root-wave.md).
