# Поля `profiles.yaml`

Реестр: [`profiles.yaml`](./profiles.yaml). Ключ `--project` в CLI = ключ в `projects:`.

| Поле | Назначение |
|------|------------|
| `enabled` | `true` / `false` — профиль доступен в CLI |
| `focus_folder` | Корень кодовой базы проекта |
| `tasks_dir` | Каталог tasks/docs (pkg, index, pipeline) |
| `active_packages_dir` | Подкаталог `*-active-packages/` |
| `current_pointer` | Файл `*-active-package.current.yaml` |
| `build_windows_subdir` | Относительно `tasks_dir`: куда писать окна |
| `build_window_prefix` | Префикс имени файла окна |
| `next_readme_dotfile` | Pointer `.gateway-next-readme` и аналоги |
| `pkg_path_prefix` | Префикс путей в pkg YAML |
| `plan_file` | Operative builder plan (обычно `.cursor/plans/`) |
| `pipeline_doc` | Epic/story execution pipeline |
| `ui_visual_pipeline_doc` | Опционально (spa): полный SSOT UI Visual Pipeline (UI-0..UI-3, классификация, P1.3 fields) |
| `default_input_kind` | `epic_story_tree` \| `task_list_linear` |
| `input_package_yaml_key` | Ключ metadata в pkg |
| `artifact_kind` | Тип build window artifact |
| `build_window_title` | Заголовок в генерируемом окне |
| `test_command` | Команда тестов для Phase 0 |
| `stack_label` | Человекочитаемый стек (Python, React/JS, GPT Actions) |
| `execution_skill_primary` | Slug execution skill для P1/P3 (напр. `python-pro`, `react-expert`) |
| `execution_skill_fallback` | Опционально: запасной slug (напр. `javascript-pro` для spa) |
| `execution_skill_path` | Путь к SKILL.md от корня workspace — SSOT для `@` attach при code changes |
| `queueless` | `true` — только `--verify` (напр. `taxonomy`) |
| `verify_paths` | Список файлов для queueless verify |

**Execution skill:** данные в `profiles.yaml`; логика резолва и override task README — [builder-session/SKILL.md](../../../../.cursor/skills/builder-session/SKILL.md) §Execution skill resolution.

## Добавление нового проекта

**SSOT:** [`../guides/add-builder-profile.md`](../guides/add-builder-profile.md) — Intake Form, Checklist, Gateway clone, operative prompt.

Кратко: скопировать блок в `profiles.yaml` → bootstrap `{tasks_dir}` → operator contract → Gateway-clone plan → `--verify`.
