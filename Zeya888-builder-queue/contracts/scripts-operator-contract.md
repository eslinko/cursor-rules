# Scripts Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/Scripts_builder.plan.md`](../../../.cursor/plans/Scripts_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Process-reminder правила для `builder_project: scripts` (operator tooling в `scripts/docs/tasks/`). **Capybara work** — только `builder_project: capybara`. P1/PA промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index` — старт только из индекса + active pkg

**Перед** batch-run, Build window или P3 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/Scripts_builder.plan.md`](../../../.cursor/plans/Scripts_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`scripts/docs/tasks/bullrun-launch-index.md`](../../../scripts/docs/tasks/bullrun-launch-index.md) §«Актуальная точка».
2. Прочитать [`scripts-active-package.current.yaml`](../../../scripts/docs/tasks/scripts-active-package.current.yaml) → `package_file`, `activation`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project scripts --verify`  
   При `FAIL` до bootstrap — **стоп**; запустить **P1.3** (или P1.2/P1.1), не выдумывать очередь.
4. Следующую волну брать **только** из индекса, pkg/`--list`, или явной команды (`run_mode=…` из plan §safe-override).

**Запрещено:**

- Брать порядок из памяти или из `docs/runtime-infrastructure/` без materialized pkg.
- Создавать эпики вне `EPIC-SCR-02-tooling` в scripts tree без P1.
- Вести `STORY-SCR-CAPY*` / `STORY-SCR-CAPYUI*` через `builder_project: capybara` ([capybara-operator-contract.md](./capybara-operator-contract.md)).

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без индекса = не декомпозирован

Если `EPIC-SCR-02-tooling.md` или tooling story существует в `scripts/docs/tasks/`, но в bullrun **нет** task queue:

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute.
- Запустить **P1** + [`bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md) или **P1.3** для backlog story.

**Backlog story (типично scripts):** story в `scripts/docs/tasks/backlog-stories/builder-console/STORY-SCR-WFCONSOLE*.md` → **P1.3**.

---

## 3. `sync-index-after-each-task` — индекс в той же итерации

После **каждого** закрытого task или story gate:

1. Обновить `bullrun-launch-index.md` и [`backlog-stories/INDEX.md`](../../../scripts/docs/tasks/backlog-stories/INDEX.md) при backlog story.
2. Обновить §«Актуальная точка».
3. Не откладывать sync на конец сессии.

---

## 4. `pick-input-mode-explicitly` — один режим входа на сессию

| `input_mode` | Якорь P1/P3/P4 | Когда (scripts) |
|--------------|----------------|-----------------|
| `backlog_story` | `@$storyFile` (`docs/tasks/backlog-stories/STORY-SCR-*.md`); опц. `@$backlogIndex` | **Primary:** shaping из [`runtime-infrastructure`](../../../scripts/docs/runtime-infrastructure/README.md) → P1.3 |
| `requirement` | `@$requirementDoc` (если появятся numbered REQ в `scripts/docs/requirements/`) | Инкремент по REQ |
| `epic_story` | `@$epicFile` (`EPIC-SCR-*`) | Декомпозиция готового эпика |
| `run_mode=…` | audit gap list из `Scripts_builder.plan.md` §safe-override | Post-audit; **не** менять active pkg |

**Запрещено** смешивать AC requirement, epic-only и backlog в одном pkg без явного решения оператора.

**PA (до P1):** workflow §PA.3 / PA.2 / PA.1 — shaping intake; без pkg и без P3.

---

## 5. Date discipline (artifact dates)

Перед записью `created_at`, gate `Date:`, run-summary — [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md):

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
```

После P1 scaffold или перед story Done:

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project scripts --verify --check-dates
```

---

## Session checklist

```markdown
## Scripts session resolve

- verify: ok N paths | FAIL (bootstrap → run P1.3 first)
- check-dates: ok / WARN / FAIL — `--verify --check-dates`
- index: bullrun §Актуальная точка + backlog-stories/INDEX.md
- active pkg: scripts-active-package.current.yaml → pkg-…
- input_mode: backlog_story | requirement | epic_story | run_mode=… (один)
- next work: <из --list или backlog INDEX, не из памяти>
```

---

## SSOT order (scripts)

1. `run_mode` override list (если оператор явно указал)  
2. Active `scripts-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` + `backlog-stories/INDEX.md`  
4. **Backlog mode:** `backlog-stories/` → после P1.3 pipeline story · **Epic mode:** `docs/tasks/epics/` · **Infra docs:** [`runtime-infrastructure/`](../../../scripts/docs/runtime-infrastructure/README.md) (intake only, не очередь)  
5. Task `README.md` + acceptance-verification

Pipeline: [`scripts-story-execution-pipeline.md`](../../../scripts/docs/tasks/scripts-story-execution-pipeline.md).

---

## 6. Аудит P4 / P7 (якоря по `input_mode`)

Отчёты: `scripts/docs/analysis/`. Мышление: `@.cursor/rules/analysis.mdc`. Промпты — [workflow.md](../core/workflow.md) §P4 / §P7.

| Режим | Cursor P4 | External re-audit |
|-------|-----------|-------------------|
| `backlog_story` | Факт-код vs AC в `@$storyFile` + code paths в `scripts/lib/` | workflow §P4 |
| `requirement` | Факт-код vs `$requirementDoc` + AC | workflow §P4 |
| `epic_story` | Факт-код vs AC Stories в `$epicFile` | workflow §P4 |
| `run_mode=…` | Findings audit report + AC тасков override | workflow §P7 |

Build plan **не** содержит таблицу P4 — только эта секция и workflow.

---

## 7. P1.3 `backlog_story` (scripts appendix)

Используется с [workflow.md](../core/workflow.md) §P1.3 (`$p13Appendix` для `builder_project: scripts`).

| Параметр | Значение |
|----------|----------|
| Epic prefix | `EPIC-SCR-02-tooling` |
| Story prefix | `STORY-SCR-WFCONSOLE*` |
| Materialize path | `scripts/docs/tasks/epics/EPIC-SCR-02-tooling/` |
| Execution skill | `javascript-pro` |
| Code facts anchor | `docs/methodology/Zeya888-builder-queue/tools/workflow-console.html` |

**Capybara (`STORY-SCR-CAPY*`, `STORY-SCR-CAPYUI*`):** профиль `capybara` — [capybara-operator-contract.md](./capybara-operator-contract.md) §7.

**Intake shaping:** Capybara intake — `scripts/docs/runtime-infrastructure/` via profile `capybara` only.
