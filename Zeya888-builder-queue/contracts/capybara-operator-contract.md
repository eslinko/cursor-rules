# Capybara Builder — operator contract

> **Plan (read-only unless operator asks):** [`.cursor/plans/Capybara_builder.plan.md`](../../../.cursor/plans/Capybara_builder.plan.md)  
> **Propagation:** [builder-session/SKILL.md](../../../.cursor/skills/builder-session/SKILL.md) · [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) · [session-starter.md](../core/session-starter.md)

Process-reminder правила для `builder_project: capybara` (Vue 3 + Node monolith + CLI). P1/PA промпты — только [workflow.md](../core/workflow.md); не дублировать в plan.

---

## 1. `resolve-start-from-index` — старт только из индекса + active pkg

**Перед** batch-run, Build window или P3 Execute:

**Fixed plan:** `@attach` [`.cursor/plans/Capybara_builder.plan.md`](../../../.cursor/plans/Capybara_builder.plan.md) + workflow §P3/P6 в **этом** чате — **не** Build / Execute plan на файле ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

1. Прочитать [`capybara/docs/tasks/bullrun-launch-index.md`](../../../capybara/docs/tasks/bullrun-launch-index.md) §«Актуальная точка».
2. Прочитать [`capybara-active-package.current.yaml`](../../../capybara/docs/tasks/capybara-active-package.current.yaml) → `package_file`, `activation`.
3. Из корня workspace:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project capybara --verify`  
   При `FAIL` — **стоп**; запустить **P1.3** (или P1.1), не выдумывать очередь.
4. Следующую волну брать **только** из индекса, pkg/`--list`, или явной команды (`run_mode=…` из plan §safe-override).

**Запрещено:**

- Брать порядок из памяти или из `scripts/docs/runtime-infrastructure/` без materialized pkg.
- Вести capybara work через `builder_project: scripts` (см. §cross-profile).
- Создавать эпики вне `EPIC-SCR-01-capybara` / `EPIC-SCR-CAPYUI` без P1.

---

## 2. `treat-missing-epic-as-not-decomposed` — эпик без индекса = не декомпозирован

Если `EPIC-SCR-01-capybara.md` или `EPIC-SCR-CAPYUI.md` существует в `capybara/docs/tasks/epics/` или backlog, но в bullrun **нет** task queue:

- Считать эпик **не декомпозированным**.
- **Не** начинать P3 Execute.
- Запустить **P1** + [`bullrun-epic-decompose.md`](../../../.cursor/commands/bullrun-epic-decompose.md) или **P1.3** для backlog story.

**Backlog story (типично capybara):** story в `capybara/docs/tasks/backlog-stories/STORY-SCR-CAPY*.md` или `STORY-SCR-CAPYUI*.md` → **P1.3** (`input_mode=backlog_story`).

---

## 3. `sync-index-after-each-task` — индекс в той же итерации

После **каждого** закрытого task или story gate:

1. Обновить `bullrun-launch-index.md` и [`backlog-stories/INDEX.md`](../../../capybara/docs/tasks/backlog-stories/INDEX.md).
2. Обновить §«Актуальная точка».
3. Не откладывать sync на конец сессии.

---

## 4. `pick-input-mode-explicitly` — один режим входа на сессию

| `input_mode` | Якорь P1/P3/P4 | Когда (capybara) |
|--------------|----------------|------------------|
| `backlog_story` | `@$storyFile` (`capybara/docs/tasks/backlog-stories/STORY-SCR-CAPY*` / `CAPYUI*`); `@$backlogIndex` | **Primary:** P1.3 для CAPY / CAPYUI |
| `epic_story` | `@$epicFile` (`EPIC-SCR-01-capybara`) | Декомпозиция готового эпика |
| `run_mode=…` | audit gap list из `Capybara_builder.plan.md` §safe-override | Post-audit; **не** менять active pkg |

**Запрещено** смешивать backlog и epic-only в одном pkg без явного решения оператора.

**PA (до P1):** workflow §PA.3 — shaping из [`scripts/docs/runtime-infrastructure/README.md`](../../../scripts/docs/runtime-infrastructure/README.md).

---

## 5. Date discipline (artifact dates)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project capybara --verify --check-dates
```

SSOT: [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md).

---

## Session checklist

```markdown
## Capybara session resolve

- verify: ok N paths | FAIL → run P1.3 first
- check-dates: ok / WARN / FAIL
- index: bullrun §Актуальная точка + backlog-stories/INDEX.md
- active pkg: capybara-active-package.current.yaml → pkg-…
- input_mode: backlog_story | epic_story | run_mode=… (один)
- next work: <из --list или backlog INDEX>
- cross-profile: capybara work НЕ через scripts
```

---

## SSOT order (capybara)

1. `run_mode` override list (если оператор явно указал)  
2. Active `capybara-active-packages/pkg-*.yaml` + `--verify`  
3. `bullrun-launch-index.md` + `backlog-stories/INDEX.md`  
4. **Derived snapshot:** [`capybara-backlog-dashboard.md`](../../../capybara/docs/tasks/capybara-backlog-dashboard.md) — после story close / housekeeping; затем `npm run dashboard:aggregate`  
5. **Backlog:** `capybara/docs/tasks/backlog-stories/` · **Epic:** `capybara/docs/tasks/epics/` · **Intake:** `scripts/docs/runtime-infrastructure/` (shaping only)  
6. Task `README.md` + acceptance-verification

Pipeline: [`capybara-story-execution-pipeline.md`](../../../capybara/docs/tasks/capybara-story-execution-pipeline.md).

---

## 6. Аудит P4 / P7 (якоря по `input_mode`)

Отчёты: `scripts/docs/analysis/`. Мышление: `@.cursor/rules/analysis.mdc`. Промпты — [workflow.md](../core/workflow.md) §P4 / §P7.

| Режим | Cursor P4 | External re-audit |
|-------|-----------|-------------------|
| `backlog_story` | Факт-код vs AC в `@$storyFile` + code paths | workflow §P4 |
| `epic_story` | Факт-код vs AC Stories в `$epicFile` | workflow §P4 |
| `run_mode=…` | Findings audit report + AC тасков override | workflow §P7 |

---

## 7. P1.3 `backlog_story` (capybara appendix)

Используется с [workflow.md](../core/workflow.md) §P1.3 (`$p13Appendix` для `builder_project: capybara`).

| Параметр | Значение |
|----------|----------|
| Epic prefix | `EPIC-SCR-01-capybara`, `EPIC-SCR-CAPYUI` |
| Story prefix | `STORY-SCR-CAPY*`, `STORY-SCR-CAPYUI*` |
| Materialize path | `capybara/docs/tasks/epics/` |
| Task naming | `task-scr-capybara-tNN-*` / `task-scr-capyui-tNN-*` |
| Active pointer | `capybara-active-package.current.yaml` |
| Execution skill | `vue-expert` (UI) / `javascript-pro` (CLI, server) — см. pipeline §Skill routing |
| Code zones | CLI: `scripts/lib/capybara/`; UI: `capybara-ui/`; tests: `scripts/tests/unit/capybara/` |

**Backlog INDEX:** обновить `capybara/docs/tasks/backlog-stories/INDEX.md` при закрытии story.

---

## 8. Cross-profile (capybara ↔ scripts)

| Work | Profile |
|------|---------|
| `EPIC-SCR-01-capybara`, `STORY-SCR-CAPY*`, `STORY-SCR-CAPYUI*` | **`capybara`** |
| `EPIC-SCR-02-tooling`, `STORY-SCR-WFCONSOLE*` | **`scripts`** |

Capybara tasks SSOT: `capybara/docs/tasks/`. Tooling tasks SSOT: `scripts/docs/tasks/`.
