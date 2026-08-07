# Landing Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/Landing_builder.plan.md`](../../../.cursor/plans/Landing_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Process-reminder правила для `builder_project: landing` (Astro + TypeScript + Tailwind marketing landing). P1/PA промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index` — старт только из индекса + active pkg

**Перед** batch-run, Build window или P3 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/Landing_builder.plan.md`](../../../.cursor/plans/Landing_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`landing/docs/tasks/bullrun-launch-index.md`](../../../landing/docs/tasks/bullrun-launch-index.md) §«Актуальная точка».
2. Прочитать [`landing-active-package.current.yaml`](../../../landing/docs/tasks/landing-active-package.current.yaml) → `package_file`, `activation`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project landing --verify`  
   При `FAIL` — **стоп**; запустить **P1.1** (или P1.3), не выдумывать очередь.
4. Следующую волну брать **только** из индекса, pkg/`--list`, или явной команды (`run_mode=…` из plan §safe-override).

**Запрещено:**

- Брать порядок из памяти или исполнять raw `epics/**/story.md` без materialized task `README.md` + pkg.
- Смешивать landing work с `builder_project: spa` без явной команды.

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без task queue = не декомпозирован

Если legacy `epic-0N-*` / `EPIC-LAND-*` есть в `landing/docs/tasks/epics/`, но в bullrun **нет** Builder Queue task queue:

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute.
- Запустить **P1.1** + [`bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md) или **P1.3** для backlog story.

**Primary intake:** **P1.1** `epic_story` from living map [bullrun-landing-index.md](../../../landing/docs/tasks/bullrun-landing-index.md).

---

## 3. `sync-index-after-each-task` — индекс в той же итерации

После **каждого** закрытого task или story gate (и при **emit / добавлении** новых `STORY-*`):

1. Обновить `bullrun-launch-index.md` и при необходимости [bullrun-landing-index.md](../../../landing/docs/tasks/bullrun-landing-index.md) + [`backlog-stories/INDEX.md`](../../../landing/docs/tasks/backlog-stories/INDEX.md) + package `INDEX.md`.
2. Обновить §«Актуальная точка».
3. Recount [`landing-mvp-dashboard.md`](../../../landing/docs/tasks/landing-mvp-dashboard.md): Summary / By package / Remaining (keys = links) / Epic rollup / §Now / `Updated` / `Last change` — только с диска (см. [backlog-dashboard-maintenance.md](../workflow/backlog-dashboard-maintenance.md)).
4. Не откладывать sync на конец сессии.

---

## 4. `pick-input-mode-explicitly` — один режим входа на сессию

| `input_mode` | Якорь P1/P3/P4 | Когда (landing) |
|--------------|----------------|-----------------|
| `epic_story` | `@$epicFile` (`epics/epic-0N-*` or `EPIC-LAND-*`) | **Primary:** materialize INFRA…QA |
| `backlog_story` | `@$storyFile` (`STORY-LAND-*`); опц. `@$backlogIndex` | Когда появятся backlog stories |
| `requirement` | `@$requirementDoc` (architecture / analysis) | Инкремент по арх. REQ |
| `run_mode=…` | audit gap list из `Landing_builder.plan.md` §safe-override | Post-audit; **не** менять active pkg |

**PA (до P1):** workflow §PA.1 / PA.2 / PA.3 — shaping; без pkg и без P3.

---

## 5. Date discipline (artifact dates)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project landing --verify --check-dates
```

SSOT: [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md).

---

## Session checklist

```markdown
## Landing session resolve

- verify: ok N paths | FAIL (→ P1.1 first)
- check-dates: ok / WARN / FAIL
- index: bullrun-launch-index §Актуальная точка (+ living bullrun-landing-index)
- active pkg: landing-active-package.current.yaml → pkg-…
- input_mode: epic_story | backlog_story | requirement | run_mode=… (один)
- stack: Astro + TS + Tailwind; skill typescript-pro
- next work: <из --list или living map, не из памяти>
```

---

## SSOT order (landing)

1. `run_mode` override list (если оператор явно указал)  
2. Active `landing-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` + living `bullrun-landing-index.md`  
4. **Epic mode:** `docs/tasks/epics/` · **Backlog:** `backlog-stories/` · **Arch:** `landing/docs/architecture/`  
5. Task `README.md` + acceptance-verification

Pipeline: [`landing-story-execution-pipeline.md`](../../../landing/docs/tasks/landing-story-execution-pipeline.md).

---

## 6. Аудит P4 / P7 (якоря по `input_mode`)

Отчёты: `landing/docs/analysis/`. Мышление: `@.cursor/rules/analysis.mdc`. Промпты — [workflow.md](../core/workflow.md) §P4 / §P7 (P5 auto-decide disposition + follow_up; без AskQuestion).

| Режим | Cursor P4 | External re-audit |
|-------|-----------|-------------------|
| `epic_story` | Факт-код vs AC Stories в `$epicFile` | workflow §P4 |
| `backlog_story` | Факт-код vs AC в `@$storyFile` | workflow §P4 |
| `requirement` | Факт-код vs `$requirementDoc` + AC | workflow §P4 |
| `run_mode=…` | Findings + AC тасков override | workflow §P7 |

Build plan **не** содержит таблицу P4 — только эта секция и workflow.

---

## 7. P1.1 / P1.3 appendix (landing)

| Параметр | Значение |
|----------|----------|
| Epic prefix (target) | `EPIC-LAND-*` (primary after materialize); legacy `epic-0N-*` folders OK with source link |
| Story prefix | `STORY-LAND-*` / legacy keys INFRA-*, DS-*, … |
| Materialize path | `landing/docs/tasks/epics/` |
| Execution skill | `typescript-pro` (`execution_skill_primary`); fallback `javascript-pro` |
| Living map | [`bullrun-landing-index.md`](../../../landing/docs/tasks/bullrun-landing-index.md) |
| Wireframe / images | `landing/public/images/`; architecture `07-image-inventory.md` |

**hasUxPipeline:** false — не spa UI-0..UI-3; visual evidence via screenshots/build as task AC when needed.
