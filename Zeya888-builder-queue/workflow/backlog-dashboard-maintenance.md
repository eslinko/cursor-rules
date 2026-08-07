# Backlog dashboard maintenance

**Template (канон):** [`backlog-dashboard-template.md`](./backlog-dashboard-template.md)  
**Focus prompt (build/recount по `$scope`):** [`build-scope-dashboard-prompt.md`](./build-scope-dashboard-prompt.md) · [`/build-scope-dashboard`](../../../../.cursor/commands/build-scope-dashboard.md)  
**Automation layers:** [`backlog-dashboard-status-automation.md`](../analysis/backlog-dashboard-status-automation.md)  
**Aggregate:** `npm run dashboard:aggregate` → [`backlog-dashboard.html`](../tools/backlog-dashboard.html)

## Artifact path

Per **scope of work** (не «весь проект навсегда»):

```text
{profile}/docs/tasks/{project}-{scopeId}-dashboard.md
```

Примеры:

| Profile | Scope-Id | Snapshot |
|---------|----------|----------|
| gateway | `mvp` | [`gateway-mvp-dashboard.md`](../../../../doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md) |
| gpt | `mvp` | [`gpt-mvp-dashboard.md`](../../../../GPT%20UI/docs/tasks/gpt-mvp-dashboard.md) |
| landing | `mvp` | [`landing-mvp-dashboard.md`](../../../../landing/docs/tasks/landing-mvp-dashboard.md) |
| spa (legacy) | — | [`spa-backlog-dashboard.md`](../../../../spa-app/docs/tasks/spa-backlog-dashboard.md) до rename · канон [`spa-mvp-dashboard.md`](../../../../spa-app/docs/tasks/spa-mvp-dashboard.md) |

Related upstream (типично): `bullrun-launch-index.md`, `backlog-stories/INDEX.md`, package `INDEX.md`, при наличии — `requirements/` Status.

## When to update

В **той же итерации**, когда:

1. Закрыта story / post-audit gap (P6) / doc-task
2. Сменился статус в package `INDEX.md` или в REQ
3. Добавлен package / story / req / doc-task в текущий scope
4. Завершён housekeeping audit по backlog

Не обновлять из памяти — только recount с диска.

## Checklist (per close / status change)

1. Story/REQ/doc-task file: Status / AC
2. Package `INDEX.md` (если story)
3. Root `backlog-stories/INDEX.md` (если есть)
4. `bullrun-launch-index.md` registry (если профиль использует)
5. Recount **Done / Todo / Deferred** (+ REQ/doc-task в active totals)
6. Update `{project}-{scopeId}-dashboard.md`:
   - Summary: Active work items, Done, Todo, Deferred, **Overall progress (active)** + bar
   - By package (story counts)
   - **Remaining** (только активный остаток; Essence — одна ясная фраза)
   - Requirements Done (если закрыли REQ)
   - Epic rollup compact
   - `Updated:` / `Last change`
   - §Now / §Deferred
7. Optional: run-summary в bullrun §Актуальная точка
8. `npm run dashboard:aggregate`

Полный канон секций и правила % — в [`backlog-dashboard-template.md`](./backlog-dashboard-template.md).

## Progress bar format

Text bar, 12 chars:

```
100% → ████████████
 75% → █████████░░░
 25% → ███░░░░░░░░░
  0% → ░░░░░░░░░░░░
```

Formula: `filled = round(12 * done / active_total)` (clamp 0…12), где `active_total = done + todo` по **active work items** scope (stories + REQ + doc-tasks; Deferred вне %).

## SSOT order (conflicts)

1. Pipeline story gate / acceptance-verification (Done proof)
2. Package `INDEX.md` / REQ Status / doc-task file
3. Root `backlog-stories/INDEX.md`
4. `bullrun-launch-index.md` (если есть)
5. `{project}-{scopeId}-dashboard.md` (derived snapshot)
6. `backlog-dashboard.html` / embedded JSON (derived ×2 — lowest priority)

## What not to put in dashboard

- Task-level progress внутри P3 wave (pkg + build window)
- Superseded в denominator (считай 0)
- Полный dump всех stories по каждому epic (ссылки на INDEX/epics достаточно)
- Выдуманные статусы без path evidence ([analysis.mdc](../../../../.cursor/rules/analysis.mdc))

## Integration with Builder Queue

- Operator contracts §sync (`$dashboard` → scope snapshot + aggregate)
- [`workflow.md`](../core/workflow.md) post-story hygiene
- [`bug-intake-workflow.md`](./bug-intake-workflow.md) close → dashboard sync
- P8 finalize — `Updated:` совпадает с последним close в scope
