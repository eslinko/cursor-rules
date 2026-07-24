# Add Builder Profile — SSOT bootstrap

> **Reusable plan:** [`.cursor/plans/add_builder_profile.plan.md`](../../../.cursor/plans/add_builder_profile.plan.md)  
> **Structural reference for `*_builder.plan.md`:** [`.cursor/plans/Gateway_builder.plan.md`](../../../.cursor/plans/Gateway_builder.plan.md) (полный клон H2, не template-only)  
> **Analysis:** [builder-plans-unification-analysis.md](../analysis/builder-plans-unification-analysis.md)

Единый operative guide: как добавить профиль в `profiles.yaml`, workflow-console, bootstrap task SSOT, operator contract, runtime plan, propagation.

Заменяет разрозненные checklist в [`profiles-fields.md`](../specs/profiles-fields.md), [`05-connect-your-project.md`](../curriculum/05-connect-your-project.md) §3, [`cursor-setup.md`](../integration/cursor-setup.md) §5.

---

## §0 Intake Form

### Обязательное поле

```yaml
profile_key: your_project   # = имя директории проекта в корне workspace = focus_folder = CLI --project
```

**Правило:** `profile_key` **всегда** совпадает с именем папки проекта (`capybara/`, `scripts/`, `spa-app/` → ключ `spa` — исключения только через явный override в `profiles.yaml`).

### Derived defaults (если не переопределено)

| Поле | Правило |
|------|---------|
| `focus_folder` | `{profile_key}` |
| `tasks_dir` | `{profile_key}/docs/tasks` |
| `plan_file` | `.cursor/plans/{TitleCase(profile_key)}_builder.plan.md` |
| `pipeline_doc` | `{tasks_dir}/{profile_key}-story-execution-pipeline.md` |
| `active_packages_dir` | `{profile_key}-active-packages` |
| `current_pointer` | `{profile_key}-active-package.current.yaml` |
| `pkg_path_prefix` | `{tasks_dir}/` |
| `input_package_yaml_key` | `{profile_key}_input_package` |
| `operator_contract` | `contracts/{profile_key}-operator-contract.md` |
| `builder_plan_reference` | **всегда** `.cursor/plans/Gateway_builder.plan.md` |

`TitleCase` — первая буква заглавная. Исключения (`gpt` → `GPT`) — через override.

### Optional overrides

```yaml
stack_label: "…"
execution_skill_primary: python-pro | vue-expert | javascript-pro | …
execution_skill_fallback: …  # опционально
test_command: "…"
default_input_kind: epic_story_tree | task_list_linear
source_profile: …           # если split
source_split: full | partial
```

---

## §1 Checklist (13 шагов)

1. [ ] **Intake** — `profile_key` + overrides (§0)
2. [ ] **`profiles.yaml`** — блок `projects.{profile_key}` ([`profiles-fields.md`](../specs/profiles-fields.md))
3. [ ] **`input-package-spec.md`** — строка в таблице §2
4. [ ] **`workflow-console.html`** — `BUILDER_PROJECTS` + `PROJECT_PROFILES.{profile_key}` (§1.1)
5. [ ] **Tasks SSOT** в `{tasks_dir}/`:
   - `{profile_key}-active-packages/` + `pkg-bootstrap-pending.yaml` или migrated pkg
   - `{profile_key}-active-package.current.yaml`
   - `bullrun-launch-index.md`
   - `backlog-stories/INDEX.md`
   - `{profile_key}-story-execution-pipeline.md`
   - `run-reports/{profile_key}-build-windows/README.md`
6. [ ] **Split** (если `source_profile`) — migrate pkg paths, narrow source bullrun/INDEX/contract
7. [ ] **`{profile_key}-operator-contract.md`** — по образцу scripts/identity + fixed-plan §1
8. [ ] **`.cursor/plans/{TitleCase(profile_key)}_builder.plan.md`** — **Gateway structural clone** (§2 ниже)
9. [ ] **Propagation:** `workflow.md` §profiles, `session-starter.md`, `queue-manual.md` §5x, `MANIFEST.md`, `builder-session/SKILL.md`, `builder-operator-habits.mdc`
10. [ ] **`--verify`** — `python3 …/builder_resolve_queue.py --project {profile_key} --verify`
11. [ ] **VERSION / CHANGELOG** — bump methodology
12. [ ] **Не** Build на `*_builder.plan.md` — @attach + workflow §P3/P6
13. [ ] **Не** коммитить `docs/tasks/**` без явной команды оператора

### §1.1 workflow-console propagation

Файл: [`tools/workflow-console.html`](../tools/workflow-console.html)

После `profiles.yaml` добавить профиль в operator UI:

1. `{profile_key}` в массив `BUILDER_PROJECTS`
2. Блок `PROJECT_PROFILES.{profile_key}` — поля синхронны с YAML:

| Console key | YAML / derived |
|-------------|----------------|
| `project` | `{profile_key}` |
| `tasks_dir` | `tasks_dir` |
| `current_pointer` | `current_pointer` |
| `plan_file` | `plan_file` |
| `pipeline_doc` | `pipeline_doc` (если задан) |
| `execution_skill_primary` | `execution_skill_primary` |
| `execution_skill_path` | `execution_skill_path` |
| `backlog_index` | `{tasks_dir}/backlog-stories/INDEX.md` |
| `hasUxPipeline` | `true` только для spa-like UX; иначе `false` |

3. Bump version pill консоли
4. Ручная проверка: dropdown → `planFile`, `$verifyCmd` (`--project {profile_key}`), backlog в P1.3

---

## §2 Gateway structural clone (runtime plan)

### Правило

**`*_builder.plan.md` = полный структурный клон** [`Gateway_builder.plan.md`](../../../.cursor/plans/Gateway_builder.plan.md).

[`builder-plan-template.md`](../templates/builder-plan-template.md) — только плейсхолдеры; **не** укороченный SSOT.

### Канон H2 (11 разделов)

1. `## Назначение`
2. `## Связь с unified workflow`
3. `## Поведение при Build / Execute plan` (+ safe-override, шаг 0/0b, шаблон чата)
4. `## Иерархия SSOT` (+ sync H3)
5. `## ☀️☀️ INPUT SOURCE ❤️❤️` (+ Режим A/B, алгоритм резолва)
6. `## Статус внедрения правил`
7. `## Текущая точка по индексу`
8. `## Правило приоритизации`
9. `## Контракт ролей`
10. `## Уровни процесса`
11. `## Канон исполнения`

Опционально из Scripts-планов: `## Тесты` (таблица команд).

### Алгоритм генерации

1. Прочитать Gateway plan целиком.
2. Скопировать все H2/H3; сохранить порядок, нумерацию резолва, формат safe-override.
3. Подставить значения из §0 Intake + `--verify` (pkg file, path count).
4. При split — перенести `run_mode` секции из source plan с rewrite путей.
5. Сверить каждый path → `exists` (**analysis.mdc**).
6. §Шаг 0 должен совпадать с реальным выводом `--verify`.

### Reference instance: `capybara`

- `profile_key: capybara` (= директория `capybara/`)
- Split от `scripts`; tasks SSOT → `capybara/docs/tasks/`
- Stack: Vue 3 + Node monolith + CLI в `scripts/lib/capybara/`
- Plan: [`.cursor/plans/Capybara_builder.plan.md`](../../../.cursor/plans/Capybara_builder.plan.md)
- Contract: [`capybara-operator-contract.md`](../contracts/capybara-operator-contract.md)
- Console: `PROJECT_PROFILES.capybara` в workflow-console.html

---

## §3 Operative prompt (copy-paste)

```markdown
@docs/methodology/Zeya888-builder-queue/guides/add-builder-profile.md
@.cursor/plans/Gateway_builder.plan.md
@docs/methodology/Zeya888-builder-queue/specs/profiles.yaml
@docs/methodology/Zeya888-builder-queue/tools/workflow-console.html
@.cursor/rules/analysis.mdc

Создай Builder Queue профиль по guide §1 Checklist.

profile_key: {profile_key}
# optional: stack_label, execution_skill_primary, test_command, source_profile, source_split

Runtime plan: полный клон Gateway_builder.plan.md (guide §2), не template-only.
После profiles.yaml: workflow-console.html — BUILDER_PROJECTS + PROJECT_PROFILES.{profile_key}
После bootstrap: python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project {profile_key} --verify

НЕ Build на *_builder.plan.md — @attach + workflow §P3/P6.
```

---

## §4 Validation matrix

| Check | Expected |
|-------|----------|
| `profile_key` = directory name | match (или documented override) |
| `profiles.yaml` key = CLI `--project` | match |
| `workflow-console.html` | `{profile_key}` в dropdown; fields 1:1 с YAML |
| `pkg_path_prefix` = paths in pkg YAML | prefix match |
| `current_pointer` → existing pkg | exists |
| `--verify` | `ok N paths` |
| bullrun §Актуальная точка | same pkg as pointer |
| plan §Шаг 0 | same N paths |
| cross-profile (if split) | documented in both contracts |

---

## §5 Split-from-existing

1. Migrate pkg YAML: rewrite `{source}/docs/tasks/` → `{target}/docs/tasks/`
2. Copy/adapt bullrun history (remove unrelated epics)
3. Narrow source: delete duplicated task tree, update pointer to remaining pkg
4. Cross-ref in both operator contracts §cross-profile
5. **Не** править source `*_builder.plan.md` без явной команды

Пример: `profile_key: capybara` ← `source_profile: scripts` (CAPY-* → capybara; WFCONSOLE → scripts).
