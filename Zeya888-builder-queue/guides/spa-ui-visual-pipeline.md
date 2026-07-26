# Spa — UI Visual Pipeline

> **Runtime plan (каркас):** [`.cursor/plans/Spa_builder.plan.md`](../../../../.cursor/plans/Spa_builder.plan.md)  
> **Hard gates:** [`spa-story-execution-pipeline.md`](../../../../spa-app/docs/tasks/spa-story-execution-pipeline.md) §UI task hard gates  
> **P3 copy-paste:** [`workflow.md`](../core/workflow.md) §P3 — Execute (spa UI appendix)  
> **Post-mortem:** [`methodology-spa-ui-pipeline-gaps-search-02-2026-06-17.md`](../../../../spa-app/docs/analysis/methodology-spa-ui-pipeline-gaps-search-02-2026-06-17.md)

Применяется к **обычным** P3 task README из pkg (не к audit `run_mode` override, если таск doc-only).

**Цель:** parity качества UI-сегмента с невизуальным кодом — baseline из реального DOM, согласованный target mockup, puppeteer verify перед Done.

## Классификация (маршрутизация)

| Поле            | Значения  | Когда      |
| --------------- | --------- | ---------- |
| `ui_scope`      | `none`    | `visual`   |
| `ui_complexity` | `trivial` | `standard` |

**Порог «примитивной однозначности» (skip UI-1 interview):**

- `trivial` **и** привязка к существующему `mockup-NN-*-spec.md` **или** изменение ≤1 селектора без смены layout.
- Примеры skip: текст badge, i18n placeholder при неизменной вёрстке, doc-sync таски (T07/T08).
- Примеры **full UI pipeline:** [SEARCH-02](../../../../spa-app/docs/tasks/backlog-stories/search-and-filters/STORY-SPA-SEARCH-02-filter-panel-shell.md) (панель+чипы+drawer), [SEARCH-03](../../../../spa-app/docs/tasks/backlog-stories/search-and-filters/STORY-SPA-SEARCH-03-cross-language-search-input.md), любой новый state-screen.
- Примеры **без UI pipeline:** [SEARCH-01](../../../../spa-app/docs/tasks/backlog-stories/search-and-filters/STORY-SPA-SEARCH-01-vocabulary-alignment.md) (`ui_scope: none`), L10N telemetry без DOM.

**Эвристика без полей в README:** Scope упоминает `BoardPage`, `components/`, `mockup-`, «видно на /board», `drawer`, «чипы» → минимум `visual`.

**Включение pipeline:** `ui_scope` ∈ {`visual`, `mixed`} **и** `ui_complexity` ≥ `standard`, **или** `ui_gate: auto` в P3 ([workflow.md](../core/workflow.md) §P3 spa UI appendix).  
**Skip:** `ui_scope: none`, `ui_complexity: trivial`, или `ui_gate: off` в P3.

## Per-task артефакты (рядом с task README)

```
task-spa-<story>-tNN-<slug>/
├── README.md
├── ui-baseline/
│   ├── README.md              # route, viewport, selectors, env (FAKE-OLD)
│   ├── 01-board-default.png
│   └── 02-fragment.png        # optional element crop
├── ui-mockup-spec.md          # target: operator @mockup OR generated+approved
└── acceptance-verification-*.md   # §UI verification
```

**Правила:**

- Baseline **всегда** с текущей реализации **до** правок кода (UI-0).
- `ui-mockup-spec.md` — структура как [mockup-01-dashboard-main-spec.md](../../../../spa-app/docs/UX/mockups/mockup-01-dashboard-main-spec.md): layout-метрики, states, selectors, ссылка на baseline PNG.
- Глобальные `mockup-01..20` — SSOT эпика; task spec **extends** (`extends mockup:`) и описывает **дельту** таска.

## Story-level UI anchor (waiver)

Один **anchor task** на story wave (pkg) несёт полный UI-0..UI-1; dependent visual tasks не дублируют baseline PNG.

| Роль                               | Поля README                                                              | UI pipeline                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Anchor** (shell task, напр. T03) | `ui_anchor: true`, `ui_scope: visual`, `puppeteer_gate: test:ui:filters` | полный UI-0 (MCP) → UI-1 gate → UI-2 → UI-3                                   |
| **Dependent visual**               | `extends ui-mockup: ../task-spa-*-t03-*/ui-mockup-spec.md`               | UI-0 skip; UI-3 partial при смене DOM                                         |
| **Story gate** (T16)               | —                                                                        | `acceptance-verification` **§UI** + anchor `ui-baseline/post-implement/*.png` |

Урок SEARCH-02: [methodology-spa-ui-pipeline-gaps-search-02-2026-06-17.md](../../../../spa-app/docs/analysis/methodology-spa-ui-pipeline-gaps-search-02-2026-06-17.md).

## Puppeteer smoke ownership

При materialize visual story task doc-sync (T15) **обязан** проверить/обновить `spa-app/tests/puppeteer/*`, если меняются селекторы, enum или DOM-контракт (урок smoke drift: legacy `VERIFIED` / inline dropdown в `filters-and-query-state-smoke.mjs`).

## UI-0 — Baseline capture (MCP primary)

1. Dev server: `cd spa-app && npm run dev` (порт `4173`, как в [board-shell-smoke.mjs](../../../../spa-app/tests/puppeteer/board-shell-smoke.mjs)).
2. Routes из task Scope / поля `UI routes:` (default `/#/board`, `/#/issue/:id`).
3. Viewport канон: `1536×1024` (EPIC-03).
4. Capture в `ui-baseline/`: **MCP `user-puppeteer`** `navigate` + `screenshot` (primary); metadata в `ui-baseline/README.md`. `npm run test:ui:*` — **не** замена UI-0; только UI-3 gate.
5. **Стоп** при недоступном dev server или отсутствии селекторов из Scope (**analysis.mdc**).

## UI-1 — Target mockup (intake OR interview)

| Path  | Условие                                   | Действие                                                                            |
| ----- | ----------------------------------------- | ----------------------------------------------------------------------------------- |
| **A** | Оператор подал `@mockup:` в P3 **или** P1.3 ready-mockups уже прописал `@mockup:` в task README (артборд в story) | Ссылки в `ui-mockup-spec.md`; interview skip при полном покрытии                    |
| **B** | Нет мокапов, `ui_complexity` ≥ `standard` | AskQuestion (1–2 раунда) → `ui-mockup-spec.md` от baseline → **human gate** до кода |
| **C** | `trivial` + `mockup-NN`                   | Baseline + ссылка на глобальный spec; короткий checkpoint «delta понятна»           |

Path B: зоны экрана, states (default/empty/error/mobile), интеракции; образец CTO-интервью — [search-filters-cto-interview-2026-06-15.md](../../../../spa-app/docs/analysis/search-filters-cto-interview-2026-06-15.md). Предпочтительно spec.md; опционально GenerateImage для фрагмента.

## UI-2 — Implement

`react-expert` + run-task по фазам; solution/decision docs ссылаются на `ui-mockup-spec.md` + baseline PNG.

## UI-3 — Verify (hard gate перед Done)

1. `cd spa-app && npm test` (Vitest).
2. **`npm run <puppeteer_gate>` обязательно** (из anchor task README, напр. `test:ui:filters`); стоп при FAIL. Дополнительно MCP spot-check при gaps. Layout-heavy — [epic03-mockup-validation.mjs](../../../../spa-app/tests/puppeteer/epic03-mockup-validation.mjs); post-screenshot в `ui-baseline/post-implement/`.
3. `acceptance-verification-*.md` — **§UI verification:** baseline path, target spec, post screenshot, pass/fail по story AC.

**Hard STOP:** story Done без story-gate §UI + anchor post-implement PNG запрещён. Retroactive — только `retroactive_closure` в `ui-baseline/README.md` + operator sign-off / `run_mode=spa_*_ui_audit_*`.

## P3 prompt appendix (spa UI)

**Copy-paste SSOT:** [workflow.md](../core/workflow.md) §P3 — Execute (spa UI appendix). **Auto-inject:** `builder_resolve_queue.py --write-build-window` вставляет UI-блок в build window для spa visual pkg (`--ui-appendix auto|force|off`). Hard gates — [spa-story-execution-pipeline.md](../../../../spa-app/docs/tasks/spa-story-execution-pipeline.md) §UI task hard gates.

**Шаг 0b (pre-flight):** после `--verify` → `npx puppeteer browsers install chrome` (if needed) + `npm run <puppeteer_gate>` — см. [frontend-run-and-environment.md](../../../../spa-app/docs/runtime-docs/frontend-run-and-environment.md) §8.

**Синтаксис (в UI-блоке промпта):**

- `@mockup: <path>` — target-референсы (0..N); пример SEARCH-like: mockup-01 + mockup-10 + mockup-13.
- `ui_gate: auto` | `off`

## P1.3 mandatory fields — UI в task README

При декомпозиции **новых** UI-стори (P1.3) — **обязательно** в task `README.md`:

```markdown
## UI routing (Builder Queue)
- **ui_scope:** visual | mixed | none
- **ui_complexity:** standard | complex | trivial
- **ui_anchor:** true   # ровно один на story wave (shell task)
- **UI routes:** `/#/board`
- **extends mockup:** mockup-01-dashboard-main-spec.md [, mockup-10-…]
- **puppeteer_gate:** test:ui:filters
```

Dependent visual task: `extends ui-mockup: <anchor-task>/ui-mockup-spec.md`

Пример anchor: SEARCH-02 T03 shell → `ui_anchor: true`, `puppeteer_gate: test:ui:filters`.  
SEARCH-01 → `ui_scope: none`.  
Badge fix → `ui_scope: visual`, `ui_complexity: trivial`, `extends mockup: mockup-03-status-badge-spec.md`.
