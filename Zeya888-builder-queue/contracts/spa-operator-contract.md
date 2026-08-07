# Spa Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/Spa_builder.plan.md`](../../../.cursor/plans/Spa_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Три process-reminder правила из frontmatter `Spa_builder.plan.md` + §4 `input_mode` / §5 P4 — на **каждой** сессии `builder_project: spa`. P1/PA промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index` — старт только из индекса + active pkg

**Перед** batch-run, Build window или P3 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/Spa_builder.plan.md`](../../../.cursor/plans/Spa_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`spa-app/docs/tasks/bullrun-launch-index.md`](../../../spa-app/docs/tasks/bullrun-launch-index.md) §«Актуальная точка».
2. Прочитать [`spa-active-package.current.yaml`](../../../spa-app/docs/tasks/spa-active-package.current.yaml) → `package_file`, `activation`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project spa --verify`  
   При `FAIL` до bootstrap — **стоп**; запустить **P1.3** (или P1.2/P1.1), не выдумывать очередь.
4. Следующую волну брать **только** из индекса, pkg/`--list`, или явной команды (`run_mode=…` из plan §safe-override).

**Запрещено:**

- Брать порядок из legacy [`DASHBOARD (SPA)_builder.plan.md`](../../../.cursor/plans/DASHBOARD (SPA)_builder.plan.md) embedded `ACTIVE_TASK_PATH`.
- Создавать эпики вне префикса `EPIC-SPA-*` / `EPIC-DASH-*` без P1.

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без индекса = не декомпозирован

Если `EPIC-SPA-NN-*.md` существует в `spa-app/docs/tasks/epics/`, но в bullrun **нет** task queue:

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute.
- Запустить **P1** + [`bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md) или **P1.3** для backlog story.

**Backlog story (типично spa):** story в `docs/tasks/backlog-stories/STORY-SPA-*.md`, epic ещё не в pipeline → **P1.3** (`input_mode=backlog_story`): materialize `EPIC-SPA-*` + pipeline story + tasks + pkg ([workflow.md](../core/workflow.md) §P1.3).

---

## 3. `sync-index-after-each-task` — индекс в той же итерации

После **каждого** закрытого task или story gate:

1. Обновить `bullrun-launch-index.md` и [`backlog-stories/INDEX.md`](../../../spa-app/docs/tasks/backlog-stories/INDEX.md) при doc-gap story.
2. Обновить package `INDEX.md` (если есть) для затронутого пакета.
3. Обновить [`spa-backlog-dashboard.md`](../../../spa-app/docs/tasks/spa-backlog-dashboard.md) — см. [backlog-dashboard-maintenance.md](../workflow/backlog-dashboard-maintenance.md).
4. Обновить §«Актуальная точка».
5. Не откладывать sync на конец сессии.

---

## 4. `pick-input-mode-explicitly` — один режим входа на сессию

| `input_mode` | Якорь P1/P3/P4 | Когда (spa) |
|--------------|----------------|-------------|
| `backlog_story` | `@$storyFile` (`docs/tasks/backlog-stories/STORY-SPA-*.md`); опц. `@$backlogIndex` | **Primary:** doc-gap G1–G8 → P1.3 |
| `requirement` | `@$requirementDoc` (`spa-app/docs/requirements/NN-*.md`) | Инкремент по numbered REQ |
| `epic_story` | `@$epicFile` (`EPIC-SPA-*`, `EPIC-DASH-*`) | Декомпозиция готового эпика |
| `run_mode=…` | audit gap list из `Spa_builder.plan.md` §safe-override | Post-audit; **не** менять active pkg |

**Запрещено** смешивать AC requirement, epic-only и backlog в одном pkg без явного решения оператора.

**PA (до P1):** workflow §PA.3 / PA.2 / PA.1 — shaping intake; без pkg и без P3.

---

## Session checklist

```markdown
## Spa session resolve

- verify: ok N paths | FAIL (bootstrap → run P1.3 first)
- index: bullrun §Актуальная точка + backlog-stories/INDEX.md
- active pkg: spa-active-package.current.yaml → pkg-…
- input_mode: backlog_story | requirement | epic_story | run_mode=… (один)
- next work: <из --list или backlog INDEX, не из памяти>
```

---

## SSOT order (spa)

1. `run_mode` override list (если оператор явно указал)  
2. Active `spa-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` + `backlog-stories/INDEX.md`  
4. **Backlog mode:** `backlog-stories/` → после P1.3 pipeline story · **Requirement mode:** `docs/requirements/` · **Epic mode:** `docs/tasks/epics/`  
5. Task `README.md` + acceptance-verification

---

## 5. Аудит P4 / P7 (якоря по `input_mode`)

Отчёты: `spa-app/docs/analysis/`. Мышление: `@.cursor/rules/analysis.mdc`. Промпты — [workflow.md](../core/workflow.md) §P4 / §P7.

| Режим | Cursor P4 | External re-audit |
|-------|-----------|-------------------|
| `backlog_story` | Факт-код vs AC в `@$storyFile` + doc touchpoints | workflow §P4 |
| `requirement` | Факт-код vs `$requirementDoc` + AC | workflow §P4 |
| `epic_story` | Факт-код vs AC Stories в `$epicFile` | workflow §P4 |
| `run_mode=…` | Findings audit report + AC тасков override | workflow §P7 |

**spa visual/mixed** (после P3 story-root `screenshots/`): использовать **P4 (spa UX)** — Phase A code + Phase B screenshots vs артборд (matrix в отчёте). Пустые/stub icon assets → `icon-asset: placeholder-ok`, если path/slot и позиционирование верны (не visual-fail).

**Post-audit P7:** читать disposition table из P5 (`CLOSED` | `TASKED` | `WAIVED reason=…` + `follow_up`) — [workflow.md](../core/workflow.md) §P5 / §P7. P5 **auto-decide** (без AskQuestion); wave complete ≠ product Story Done; `WAVE_STALLED_NO_DELTA` → STOP; неполный map → `P5_DISPOSITION_INCOMPLETE`; `follow_up=new_story` → verify backlog draft path.

Build plan **не** содержит таблицу P4 — только эта секция и workflow.

---

## 6. P1.3 `backlog_story` (spa appendix)

Используется с [workflow.md](../core/workflow.md) §P1.3 (`$p13Appendix` для `builder_project: spa`).

| Параметр | Значение |
|----------|----------|
| Epic prefix | `EPIC-SPA-*` (primary); legacy `EPIC-DASH-*` |
| Materialize path | `spa-app/docs/tasks/epics/` |
| Pipeline story | `epics/<EPIC>/stories/<STORY-KEY>/STORY-*.md` |
| Task naming | `task-spa-*` / `task-dash-*` (по домену story) |
| Active pointer | `spa-active-package.current.yaml` |
| Execution skill | `react-expert` (`execution_skill_primary`); fallback `javascript-pro` если оператор указал |
| Живой пример | `pkg-000003` / `STORY-SPA-L10N-01-locale-registry-foundation` |

**Epic materialize:**

- EPIC уже в `epics/` → использовать.
- EPIC только в `backlog-stories/EPIC-*.md` → materialize `EPIC-SPA-NN-<slug>.md` (следующий свободный номер) + bullrun.
- Не создавать `EPIC-IDS-*` или gateway epics в spa tree.

**Backlog INDEX:** обновить `backlog-stories/INDEX.md` при закрытии story.

**Visual / mixed tasks:** UI-0..UI-3 — [`guides/spa-ui-visual-pipeline.md`](../guides/spa-ui-visual-pipeline.md); hard gates — [`spa-story-execution-pipeline.md`](../../../spa-app/docs/tasks/spa-story-execution-pipeline.md) §UI task hard gates.

**P1.3 UX appendix (выбор одной ветки):**

| Условие | Appendix в [workflow.md](../core/workflow.md) |
|---------|-----------------------------------------------|
| §Артборд в backlog story + `*-spec.md` на диске | **UX ready mockups** — wire `@mockup:` в task README; **не** создавать `STORY-UX-MOCKUP-BRIEF.md` |
| UI visual/mixed, артборда нет | **UX mockup brief** — `STORY-UX-MOCKUP-BRIEF.md` → отдельный UX-чат |
| `ui_scope: none` | skip |

Console: `P1.3 (spa UX ready)` vs `P1.3 (spa UX)`.

