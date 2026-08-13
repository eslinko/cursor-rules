# Operator root — subagent overnight RUN

**Категория:** operator (Phase B overnight)  
**Reference SSOT:** [`../../guides/orchestrator-builder-reference.md`](../../guides/orchestrator-builder-reference.md)  
**Parent:** [`../../guides/operator-root-orchestrator.md`](../../guides/operator-root-orchestrator.md)  
**Fences:** [`../../tools/workflow-console.html`](../../tools/workflow-console.html) · [`../../core/workflow.md`](../../core/workflow.md)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

**How-to (человек):** [`../../guides/operator-how-to-run-queue.md`](../../guides/operator-how-to-run-queue.md)

**Когда:** в `OP-<project>` нужно прогнать очередь двумя Task-субагентами без paste и без пауз.  
**Не когда:** MVP paste packets → [`operator-root-wave.md`](./operator-root-wave.md).  
**Session cold?** optional [`operator-root-start.md`](./operator-root-start.md) first, or this prompt creates session.yaml itself.

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
@docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md
@docs/methodology/Zeya888-builder-queue/guides/operator-root-orchestrator.md
@docs/methodology/Zeya888-builder-queue/core/workflow.md
@docs/methodology/Zeya888-builder-queue/core/session-starter.md
@docs/methodology/Zeya888-builder-queue/specs/profiles.yaml
@docs/methodology/Zeya888-builder-queue/guides/fixed-builder-plan-execution.md
$builderProject=
$queueSpec=
# defaults if omitted: mode=sequential · overnight=on · delivery=subagent

Operator root SUBAGENT RUN. Follow orchestrator-builder-reference.md exactly.
builder_project: $builderProject
queue_spec: $queueSpec

MODE: orchestrate only — no product code, no invent AC, no push unless operator said.
Claims: Read/Glob only; else Unknown.
delivery=subagent: spawn/resume EXACTLY two agents (Builder + Validator). No operator paste.
overnight=on (default): no pause after story; auto-approve P1.3b/P5b GATE; wave halt ONLY on стоп|stop|pause|halt.
agent_id live ONLY in session.yaml — never in .cursor/plans/*.

## Step 1 — Resolve profile
From specs/profiles.yaml for $builderProject:
- tasks_dir → $tasksRoot, plan_file → $planFile, focus_folder, verify CLI
- contract: docs/methodology/Zeya888-builder-queue/contracts/<key>-operator-contract.md
- dashboard path: from that contract (do not invent filename)
If unknown/disabled key → Ask and STOP.

## Step 2 — Resolve queue ($queueSpec free-form)
Build ordered story @paths (facts only). Interpret $queueSpec as one of:
A) remaining / "all Remaining in dashboard" → Read dashboard §Remaining/Ready; order Pri then section order
B) exact @paths or story/BUG ids → Glob/Read; skip Product Done unless residual *b or operator forced
C) number range (e.g. BUG-02..BUG-14 or 11-19) → map via dashboard/INDEX keys
D) Pri filter (e.g. P0-P1 Ready) → intersect with Remaining
Ask ONLY if zero stories or ambiguous id. mode=sequential default.

## Step 3 — Materialize working artifacts (transpose reference → disk)
Write/update:
1) {$tasksRoot}/run-reports/operator-sessions/OP-$builderProject.process.md
   — model, overnight rules, profile constants, resolved queue, plan-sim + ROLE_LOCK, phase script
   — NO agent ids
2) {$tasksRoot}/run-reports/operator-sessions/OP-$builderProject.session.yaml
   — delivery=subagent, overnight, pause_after_story=false, auto_approve_plan=true,
     process_file, titles, builder_agent_id/validator_agent_id (keep live ids if present),
     Updated=live ISO after write
3) {$tasksRoot}/run-reports/operator-waves/wave-<YYYYMMDD>-<slug>.md
   — queue checklist + handoff log + stop-rules
Verify files exist (Read).

## Step 4 — Ensure two subagents
If builder_agent_id missing/dead:
  Task spawn Builder: Session starter (session-starter.md + console Session starter, vars filled)
  → write builder_agent_id to session.yaml
Else resume that id.
If validator_agent_id missing/dead:
  Task spawn Validator: reference §4.1 bootstrap template (analysis.mdc, RO)
  → write validator_agent_id
Else resume.
Do not use UI chat paste for fences in this mode.

## Step 5 — Run phase script per story (non-stop)
For each QUEUED story in order, follow reference §8:

Prompt sources (verbatim, fill vars only — reference §7):
- P1.3 / P3 / P5 / P6 / P8 → workflow-console / workflow.md (spa UX variants if profile+story require)
- P4 / P7 → console validator fences → Validator resume
- P2 → YOU run shell: $verifyCmd + write-build-window
- P1.3 and P5 → TWO calls: PLAN_DRAFT then (auto-approve) PLAN_APPLY + ROLE_LOCK (reference §5)
- Fixed $planFile: @attach only; never Build/Execute UI
- Each Task prompt prepend ROLE_LOCK (reference §4.2)

After each phase: verify RETURN paths on disk → update wave MD → next phase.
After P8/DONE or BLOCKED: immediately next story — no mid-queue operator report.
Skip P1.3 only if pkg/pipeline already on disk (document in wave).
BLOCKED prod/deploy/asset: facts in wave → continue queue (no invent art/AC).

Stop-rules: verify FAIL → BLOCKED + next; WAVE_STALLED_NO_DELTA → leave story, next;
P5_DISPOSITION_INCOMPLETE → re-P5; wave halt only on explicit operator stop.

## Step 6 — STOP (only when halt or queue exhausted)
Reply with ONLY:
1) wave MD path
2) DONE / BLOCKED / remaining counts (facts)
3) session.yaml path (+ whether agent ids live)
4) process.md path
5) reminder: P8 was local no-push unless operator ordered push
Do not invent next backlog; await new $queueSpec or halt.
```

---

## Примечания

- How-to для человека: [`../../guides/operator-how-to-run-queue.md`](../../guides/operator-how-to-run-queue.md).
- Reference: [`../../guides/orchestrator-builder-reference.md`](../../guides/orchestrator-builder-reference.md).
- Proven landing facts (not norm): `landing/docs/tasks/run-reports/operator-sessions/OP-landing.process.md`.
- MVP paste alternative: [`operator-root-wave.md`](./operator-root-wave.md).
