---
name: Orchestrator Builder Reference
overview: "Teaching snapshot — OP→two-subagent overnight queue. Runtime SSOT = guides/orchestrator-builder-reference.md"
todos: []
isProject: false
---

# Orchestrator Builder Reference — teaching snapshot

**Дата снимка:** 2026-08-13  
**Runtime SSOT (править там):** [`../../guides/orchestrator-builder-reference.md`](../../guides/orchestrator-builder-reference.md)  
**Launch prompt:** [`../../prompts/operator/operator-root-subagent-run.md`](../../prompts/operator/operator-root-subagent-run.md)  
**How-to:** [`../../guides/operator-how-to-run-queue.md`](../../guides/operator-how-to-run-queue.md)  
**Cursor pointer:** [`.cursor/plans/Orchestrator_Builder_Reference.md`](../../../../../.cursor/plans/Orchestrator_Builder_Reference.md)

Политика как у остальных файлов в этой папке: снимок для обучения / чтобы не потерять эталон; operative правки — в guide + prompts.

Ниже — полный текст эталона на дату снимка (копия guide).

---

# Orchestrator Builder Reference (universal)

**Версия документа:** 1.0 (methodology 1.4.26)  
**Статус:** proven Phase B overnight SSOT (из успешного OP-landing run)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Parent process:** [`../../guides/operator-root-orchestrator.md`](../../guides/operator-root-orchestrator.md)  
**Launch prompt:** [`../../prompts/operator/operator-root-subagent-run.md`](../../prompts/operator/operator-root-subagent-run.md)  
**Fences SSOT:** [`../../tools/workflow-console.html`](../../tools/workflow-console.html) · [`../../core/workflow.md`](../../core/workflow.md)  
**Profiles:** [`../../specs/profiles.yaml`](../../specs/profiles.yaml)

**Когда:** OP-чат гонит очередь story/bug **двумя субагентами** (builder + validator), без copy-paste и без пауз mid-queue.  
**Не когда:** MVP paste в UI-чаты `BLD-*`/`VAL-*` — тогда [`../../prompts/operator/operator-root-wave.md`](../../prompts/operator/operator-root-wave.md).

---

## 1. Delivery model

| Правило | Поведение |
|---------|-----------|
| OP role | Orchestrate only: queue → wave → spawn/resume → verify disk → next. **No** product code, **no** invent AC, **no** push unless operator said |
| Claims | Read/Glob only; else Unknown |
| Delivery | `delivery: subagent` — **ровно два** Task-субагента: Builder + Validator |
| UI chats | `BLD-*` / `VAL-*` **не обязательны** в этом режиме |
| Fences | **Дословно** из workflow-console / workflow.md — fill variables only |
| Agent ids | только в `OP-<project>.session.yaml` — **никогда** в `.cursor/plans/*` |
| Operator | queue/mode при старте; дальше без paste / mid-queue approve (`overnight: on`) |

## 2. Overnight non-stop (hard defaults)

Default: `overnight: on`, `pause_after_story: false`, `auto_approve_plan: true`.

| Правило | Поведение |
|---------|-----------|
| Стоп волны | только `стоп` / `stop` / `pause` / `halt` |
| Пауза после story | **запрещена** |
| P1.3 / P5 GATE | OP **auto-approve** сразу |
| После P8 / DONE | сразу следующая QUEUED |
| BLOCKED | факт в wave → **очередь дальше** |
| P8 | local commits, **no push** |
| Отчёт оператору | halt · queue exhausted · итоговый summary |

## 3. Artifacts

| Artifact | Path |
|----------|------|
| Process | `{tasksRoot}/run-reports/operator-sessions/OP-<project>.process.md` |
| Session | `{tasksRoot}/run-reports/operator-sessions/OP-<project>.session.yaml` |
| Wave | `{tasksRoot}/run-reports/operator-waves/wave-<YYYYMMDD>-<slug>.md` |

## 4. Bootstrap (once)

| Who | Source |
|-----|--------|
| Builder | `core/session-starter.md` + console Session starter → `builder_agent_id` |
| Validator | analysis.mdc + RO ROLE_LOCK → `validator_agent_id` |
| Resume | same ids per phase/story; dead id → re-spawn once |

## 5. Plan simulation variant 1

P1.3 и P5 = **два** вызова: `PLAN_DRAFT` (ephemeral `p1_*` / `p5_*` only) → GATE → `PLAN_APPLY`.  
Запрет: single-shot materialize; Build UI на fixed `$planFile`.

## 6. Per-story phase script

```text
P1.3a → auto → P1.3b → P2 shell → P3 → P4
→ [gaps] P5a → auto → P5b → P6 → P7
→ P8 (no push) → next story
```

Prompt sources: workflow-console / workflow.md (verbatim). P2 = OP shell verify + write-build-window.

## 7. Queue resolve

`$queueSpec`: `remaining` | exact `@paths`/ids | number range | Pri filter → ordered stories from dashboard/INDEX (facts).

## 8. Proven landing run (historical)

Facts only — not universal queue norm:

- `landing/docs/tasks/run-reports/operator-sessions/OP-landing.process.md`
- `landing/docs/tasks/run-reports/operator-sessions/OP-landing.session.yaml`

Successful pattern: two subagents, overnight on, Ready queue + asset-unlock wave, P8 local no push.

---

Полная актуальная спека с ROLE_LOCK templates и prompt source map:  
[`../../guides/orchestrator-builder-reference.md`](../../guides/orchestrator-builder-reference.md)
