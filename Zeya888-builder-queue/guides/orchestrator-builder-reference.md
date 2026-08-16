# Orchestrator Builder Reference (universal)

**Версия документа:** 1.0 (methodology 1.4.26)  
**Статус:** proven Phase B overnight SSOT (из успешного OP-landing run)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent process:** [`operator-root-orchestrator.md`](./operator-root-orchestrator.md)  
**Launch prompt:** [`../prompts/operator/operator-root-subagent-run.md`](../prompts/operator/operator-root-subagent-run.md)  
**Fences SSOT:** [`../tools/workflow-console.html`](../tools/workflow-console.html) · [`../core/workflow.md`](../core/workflow.md)  
**Profiles:** [`../specs/profiles.yaml`](../specs/profiles.yaml)

**Когда:** OP-чат гонит очередь story/bug **двумя субагентами** (builder + validator), без copy-paste и без пауз mid-queue.  
**Не когда:** MVP paste в UI-чаты `BLD-*`/`VAL-*` — тогда [`operator-root-wave.md`](../prompts/operator/operator-root-wave.md).

Cursor-facing pointer: [`.cursor/plans/Orchestrator_Builder_Reference.md`](../../../../.cursor/plans/Orchestrator_Builder_Reference.md).  
Teaching snapshot (archive): [`../examples/reference-plans/Orchestrator_Builder_Reference.plan.md`](../examples/reference-plans/Orchestrator_Builder_Reference.plan.md).

---

## 1. Delivery model

| Правило | Поведение |
|---------|-----------|
| OP role | Orchestrate only: queue → wave → spawn/resume → verify disk → next. **No** product code, **no** invent AC, **no** push unless operator said |
| Claims | Read/Glob only; else Unknown ([analysis.mdc](../../../../.cursor/rules/analysis.mdc)) |
| Delivery | `delivery: subagent` — **ровно два** Task-субагента: Builder + Validator |
| UI chats | `BLD-*` / `VAL-*` **не обязательны** в этом режиме (опциональные titles в session) |
| Fences | **Дословно** из workflow-console / workflow.md — fill variables only; no paraphrase |
| Agent ids | `builder_agent_id` / `validator_agent_id` **только** в session YAML — **никогда** в `.cursor/plans/*` |
| Operator | Подтверждает queue/mode при старте; дальше **без** paste и без mid-queue approve (если `overnight: on`) |

---

## 2. Overnight non-stop (hard defaults)

Default для этого эталона: `overnight: on`, `pause_after_story: false`, `auto_approve_plan: true`.

| Правило | Поведение |
|---------|-----------|
| Стоп волны | **Только** явная команда оператора: `стоп` / `stop` / `pause` / `halt` |
| Пауза после story / mid-queue отчёт | **Запрещены** |
| P1.3a → P1.3b GATE | OP **auto-approve** сразу после PLAN_DRAFT |
| P5a → P5b GATE | OP **auto-approve** сразу после PLAN_DRAFT |
| После P8 / DONE | сразу следующая QUEUED story **в том же ходе** OP |
| BLOCKED (prod / deploy / asset / verify FAIL) | факт в wave (+ project extension log если есть) → **очередь дальше** |
| P8 | local commits, **no push** (пока оператор явно не сказал push) |
| Отчёт оператору | только на: explicit halt · queue exhausted · (опционально) итоговый summary в конце волны |

`overnight: off` (daytime) — тот же phase script, но GATE ждёт оператора `approve` на P1.3b/P5b; пауза после story всё равно не рекомендуется в этом эталоне.

---

## 3. Session + process artifacts (transpose targets)

После resolve profile OP пишет/обновляет:

| Artifact | Path |
|----------|------|
| Working Cursor plan | `.cursor/plans/OP-<project>-<slug>.plan.md` (transpose etalon; never edit `.cursor/plans/Orchestrator_Builder_Reference.plan.md`) |
| Process SSOT | `{tasksRoot}/run-reports/operator-sessions/OP-<project>.process.md` |
| Session SSOT | `{tasksRoot}/run-reports/operator-sessions/OP-<project>.session.yaml` |
| Wave MD | `{tasksRoot}/run-reports/operator-waves/wave-<YYYYMMDD>-<slug>.md` |

### Session YAML (минимум)

```yaml
builder_project: <key>
op_chat_title: OP-<key>
builder_chat_title: BLD-<key>   # optional label when delivery=subagent
validator_chat_title: VAL-<key>
builder_agent_id: <uuid|null>
validator_agent_id: <uuid|null>
bind_mode: task
delivery: subagent
process_file: <path to OP-<project>.process.md>
overnight: on
pause_after_story: false
auto_approve_plan: true
stop_only_on: explicit operator стоп|stop|pause|halt
status: ready
queue: <comma ids or "see wave">
Updated: <ISO from live clock after write>
```

**Запрет:** класть `*_agent_id` в plan-файлы Cursor.

### Process MD (минимум)

- Model + overnight table (копия инвариантов §1–2)
- Constants table из profile (см. §6)
- Queue table (resolved stories)
- Plan simulation + ROLE_LOCK (§5)
- Phase script (§4)
- **Без** agent ids

---

## 4. Bootstrap субагентов (once на lifecycle)

| Who | Cursor mode | Prompt source | Когда |
|-----|-------------|---------------|-------|
| **Builder** | agent | [`../core/session-starter.md`](../core/session-starter.md) + console **Session starter** (variables filled) | **Один раз** на OP lifecycle → `builder_agent_id` |
| **Validator** | agent RO | Validator bootstrap (§4.1) | **Один раз** → `validator_agent_id` |
| Resume | — | тот же id | каждая фаза / каждая story |
| Dead id | — | re-spawn + starter/bootstrap once | переписать id в session.yaml |

Новая волна **не** требует нового Session starter, если оба агента живы и session.yaml валиден.

### 4.1 Validator bootstrap (template)

```text
@.cursor/rules/analysis.mdc
@docs/methodology/Zeya888-builder-queue/core/workflow.md
@docs/methodology/Zeya888-builder-queue/contracts/<project>-operator-contract.md
builder_project: <key>

ROLE: validator subagent for OP-<key>
MODE: read-only analysis — write ONLY audit/report markdown paths named in the fence.
Forbidden: product code edits, pkg invent, invent AC, git push, closing gaps without disposition.
Claims: Read/Glob only; else Unknown.
RETURN_TO_ROOT: paths + ≤5 lines facts.
Await phase fences (P4 / P7) from OP via resume.
```

### 4.2 ROLE_LOCK (каждая фаза к fence)

```text
ROLE_LOCK: Execute ONLY the fence below. RETURN_TO_ROOT: paths + ≤5 lines facts. Do not advance phases yourself.
```

---

## 5. Plan simulation (variant 1) — P1.3 и P5

Task UI не даёт native Plan switch → **два** вызова Builder.

| Подшаг | Имя | Writes |
|--------|-----|--------|
| **a** | `PLAN_DRAFT` | **Только** ephemeral `.cursor/plans/p1_<slug>_scaffold_<utc>.plan.md` или `p5_<slug>_gap_<utc>.plan.md` |
| GATE | overnight auto-approve / daytime `approve` | — |
| **b** | `PLAN_APPLY` | Materialize per fence + ephemeral plan; then `--verify` / `--check-dates` |

**Запрет:** один Agent-вызов «план + сразу materialize».  
**Запрет:** Build / Execute UI на fixed `$planFile`.  
**Промпт:** дословный console **P1.3** / **P5** (не укороченный handoff).  
Ephemeral + fixed plan rules: [`fixed-builder-plan-execution.md`](./fixed-builder-plan-execution.md).

### ROLE_LOCK — PLAN_DRAFT

```text
SIMULATED_CURSOR_MODE: plan
STEP: PLAN_DRAFT
Allowed writes: ONLY ephemeral .cursor/plans/p1_*_scaffold_*.plan.md OR p5_*_gap_*.plan.md
Forbidden: epics/**/stories/** materialize, task README, pkg-*.yaml, *-active-package.current.yaml,
  bullrun-launch-index.md edits, product source under focus_folder, $planFile body (except reading).
Output: plan file path + mapping preview (no apply).
```

### ROLE_LOCK — PLAN_APPLY

```text
SIMULATED_CURSOR_MODE: plan_apply
STEP: PLAN_APPLY
Approved ephemeral plan: <path>
Execute materialize per that plan + original P1.3|P5 fence checklist.
Then --verify / --verify --check-dates as fence requires.
```

---

## 6. Profile constants (transpose from profiles.yaml)

OP заполняет process constants **только** из фактов:

| Variable | Source |
|----------|--------|
| `$builderProject` | input / session |
| `workspace_root` | live workspace root |
| `$tasksRoot` | `profiles.yaml` → `tasks_dir` |
| `$planFile` | `profiles.yaml` → `plan_file` |
| `$verifyCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project <key> --verify` |
| contract | `contracts/<key>-operator-contract.md` |
| dashboard | path **из contract** (не хардкод имени) |
| P1.3 variant | console P1.3 clean **или** spa UX — по contract / story kind |
| execution skill | `profiles.yaml` + [`.cursor/skills/builder-session/SKILL.md`](../../../../.cursor/skills/builder-session/SKILL.md) |
| P8 push | default **forbidden** |

Per-story (из wave / artifacts): `$storyFile`, `$anchor`, `$buildWindowFile`, `$auditReport`, `$priorReaudit`.

---

## 7. Prompt source map (mandatory)

| Step | Куда брать текст |
|------|------------------|
| 0b Session starter | [`../core/session-starter.md`](../core/session-starter.md) + console **Session starter** |
| 0c Validator bootstrap | §4.1 этого guide |
| **P1.3** | console **P1.3** (+ PLAN_DRAFT / PLAN_APPLY locks) · [`../core/workflow.md`](../core/workflow.md) §P1.3 |
| **P2** | OP shell: `$verifyCmd` + `--write-build-window` (CLI / queue-manual) |
| **P3** | console **P3** / **P3 spa UX** · `$planFile` @attach · [`fixed-builder-plan-execution.md`](./fixed-builder-plan-execution.md) |
| **P4** | console **P4** / **P4 spa UX** → Validator |
| **P5** | console **P5** (+ PLAN_DRAFT / PLAN_APPLY) · auto-decide disposition (workflow §P5) |
| P6 prep | short note to BLD (strip stale «явно прописанные…» if present in plan) |
| **P6** | console **P6** |
| **P7** | console **P7** → Validator · no follow-up interview; `P5_DISPOSITION_INCOMPLETE` → re-P5 |
| **P8** | console **P8** · no push |

Console UI copy helper: [`../tools/workflow-console.html`](../tools/workflow-console.html) — OP fills the same variables when composing Task prompts.

---

## 8. Per-story phase script (canon)

```text
0     OP: ensure wave MD row = QUEUED/PLANNED
0b/0c OP: Session starter + validator bootstrap (once per lifecycle)
P1.3a OP→BLD  plan draft   console P1.3 + PLAN_DRAFT
GATE  OP auto-approve (overnight)
P1.3b OP→BLD  plan apply   same P1.3 + PLAN_APPLY + approved path → verify
P2    OP shell             $verifyCmd + write-build-window
P3    OP→BLD  agent        console P3 + $planFile + $buildWindowFile
P4    OP→VAL  agent RO     console P4 → $auditReport
[if gaps]
  P5a OP→BLD  plan draft   console P5 + PLAN_DRAFT
  GATE OP auto-approve
  P5b OP→BLD  plan apply   + PLAN_APPLY
  P6prep / P6 OP→BLD       console P6
  P7  OP→VAL               console P7
P8    OP→BLD  agent        console P8 (no push)
→ next QUEUED story (no pause)
```

| Step | Who | mode | Prompt |
|------|-----|------|--------|
| 0 | OP | — | wave MD |
| 0b | OP→BLD | agent | Session starter (once) |
| 0c | OP→VAL | agent RO | validator bootstrap (once) |
| P1.3a | OP→BLD | plan draft | console P1.3 + PLAN_DRAFT |
| GATE | OP | — | auto-approve if overnight |
| P1.3b | OP→BLD | plan apply | P1.3 + PLAN_APPLY |
| P2 | OP shell | shell | CLI verify + build window |
| P3 | OP→BLD | agent | console P3 |
| P4 | OP→VAL | agent RO | console P4 |
| P5a | OP→BLD | plan draft | console P5 + PLAN_DRAFT |
| GATE | OP | — | auto-approve if overnight |
| P5b | OP→BLD | plan apply | P5 + PLAN_APPLY |
| P6 prep | OP→BLD | agent | note |
| P6 | OP→BLD | agent | console P6 |
| P7 | OP→VAL | agent RO | console P7 |
| P8 | OP→BLD | agent | console P8 |

**Skip rules (facts only):** if pipeline/pkg already materialize for story → skip P1.3a/b; enter at P2 or later task entry (document in wave). Asset/prod gates that cannot pass without external deploy/art → **BLOCKED**, continue queue (no invent).

### Stop-rules (per story, not wave)

| Condition | Action |
|-----------|--------|
| verify FAIL | story **BLOCKED** → next story |
| `WAVE_STALLED_NO_DELTA` | stop P5→P7 loop on **that** story → next |
| `P5_DISPOSITION_INCOMPLETE` | re-P5 (auto) |
| Single-shot Agent on P1.3/P5 | abort call → retry two-step |
| Explicit operator halt | **wave** stop |

Advance phase **only** after `RETURN_TO_ROOT.paths` exist on disk (Read/Glob).

---

## 9. Queue resolve (for launch prompt)

`$queueSpec` free-form → упорядоченный список story paths (facts):

| Форма | Резолв |
|-------|--------|
| `remaining` / all Remaining in dashboard | Read dashboard path from **operator-contract** → §Remaining / Ready; order Pri then section order |
| Exact `@paths` / story ids | Glob/Read; skip Product Done unless residual `*b` / operator forced |
| Number range (`BUG-02..BUG-14`, `11-19`) | Map via dashboard / backlog INDEX keys |
| Pri filter (`P0-P1 Ready`) | Intersect with Remaining |

Ask operator **only** if zero stories or ambiguous id. Default `mode: sequential`.

---

## 10. Project extensions (not universal core)

Domain extras live in contract / wave notes / process appendix — **не** в core phase script:

- Image / asset blockers log
- Prod-verify residual stories (`*b`)
- Asset-unlock re-entry (skip P1.3, start at T0x)
- Spa UX console variants
- GPT `run_mode` / index sync

OP may append an «Extensions» section to `OP-<project>.process.md` when contract requires it.

---

## 11. Proven run (historical pointer)

Successful overnight landing run (2026-08): two subagents, full Ready queue, asset-unlock wave — **facts** in:

- [`landing/docs/tasks/run-reports/operator-sessions/OP-landing.process.md`](../../../../landing/docs/tasks/run-reports/operator-sessions/OP-landing.process.md)
- [`landing/docs/tasks/run-reports/operator-sessions/OP-landing.session.yaml`](../../../../landing/docs/tasks/run-reports/operator-sessions/OP-landing.session.yaml)

Не копировать landing queue tables как норму для других профилей.

---

## 12. Related

| Doc | Role |
|-----|------|
| [`operator-root-orchestrator.md`](./operator-root-orchestrator.md) | Parent OP model (MVP paste + roadmap) |
| [`../prompts/operator/operator-root-subagent-run.md`](../prompts/operator/operator-root-subagent-run.md) | Launch: profile + queueSpec → execute |
| [`./operator-how-to-run-queue.md`](./operator-how-to-run-queue.md) | Human how-to: как задать очередь и запустить |
| [`../prompts/operator/operator-root-start.md`](../prompts/operator/operator-root-start.md) | Optional bootstrap if no session |
| [`../prompts/operator/operator-root-wave.md`](../prompts/operator/operator-root-wave.md) | MVP paste packets (not this mode) |
| [`../workflow/backlog-dashboard-maintenance.md`](../workflow/backlog-dashboard-maintenance.md) | Dashboard recount after closes |
