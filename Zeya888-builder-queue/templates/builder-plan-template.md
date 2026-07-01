# Builder plan template (унифицированный скелет)

SSOT структуры для [Gateway_builder.plan.md](../../../.cursor/plans/Gateway_builder.plan.md), [GPT_builder.plan.md](../../../.cursor/plans/GPT_builder.plan.md), [ID_builder.plan.md](../../../.cursor/plans/ID_builder.plan.md), [Scripts_builder.plan.md](../../../.cursor/plans/Scripts_builder.plan.md).

**Эталон §INPUT SOURCE и ниже:** нормализованный Gateway plan (2026-06-04).  
**Анализ зеркала:** [builder-plans-unification-analysis.md](./builder-plans-unification-analysis.md)  
**Реестр путей:** [profiles.yaml](../specs/profiles.yaml)

---

## Плейсхолдеры

| Placeholder | Источник |
|-------------|----------|
| `{{PLAN_TITLE}}` | Gateway / GPT / Identity Story Builder |
| `{{CLI_PROJECT}}` | `profiles.yaml` → `projects.<name>` key |
| `{{FOCUS_FOLDER}}` | focus_folder |
| `{{TASKS_DIR}}` | tasks_dir |
| `{{PIPELINE_DOC}}` | pipeline_doc (relative to tasks_dir) |
| `{{CURRENT_POINTER}}` | current_pointer |
| `{{PKG_DIR}}` | active_packages_dir |
| `{{INPUT_PACKAGE_KEY}}` | input_package_yaml_key |
| `{{BUILD_WINDOW_SUBDIR}}` | build_windows_subdir |
| `{{BUILD_WINDOW_PREFIX}}` | build_window_prefix |
| `{{NEXT_DOTFILE}}` | next_readme_dotfile |
| `{{SKILL}}` | python-pro / openai-custom-gpt-builder |
| `{{OTHER_BUILDERS}}` | cross-ref other products |
| `{{TYPICAL_P1}}` | project-specific P1.x line |
| `{{P13_NOTE}}` | identity-only or «не применять» |
| `{{PRODUCT_SSOT_LAYER}}` | п.3 иерархии SSOT |
| `{{ACTIVE_PKG}}` | from `--verify` / current.yaml |
| `{{PATH_COUNT}}` | from `--verify` |
| `{{EPIC_KEY}}` / `{{REQ_LABEL}}` | from active pkg yaml |
| `{{BUILD_WINDOW_CLI}}` | epic_story_tree: `--story-key`; linear: `--window-flat-start` |

---

## Frontmatter (YAML)

```yaml
---
name: {{PLAN_TITLE}}
overview: "Оркестрация {{FOCUS_FOLDER}}: active {{ACTIVE_PKG}} ({{PATH_COUNT}} paths); шаг 0 builder_resolve_queue --project {{CLI_PROJECT}} --verify."
todos:
  - id: resolve-start-from-index
    content: Перед batch-run сверять bullrun-launch-index и активный pkg
    status: completed
  - id: treat-missing-epic-as-not-decomposed
    content: Эпик в файле без индекса — не декомпозирован; bullrun-epic-decompose
    status: completed
  - id: sync-index-after-each-task
    content: После каждого закрытого task/story обновлять bullrun-launch-index
    status: completed
isProject: false
---
```

---

## §Связь с unified workflow (каркас)

```markdown
## Связь с unified workflow

- SSOT промптов P1–P8: [workflow.md](docs/methodology/Zeya888-builder-queue/core/workflow.md)
- Типичный P1 для этого проекта: {{TYPICAL_P1}}
- {{P13_NOTE}}
- Этот plan — **P3/P6 runtime** (pkg, build window, run_mode, режим A/B). Промпты P1 **не** дублировать.
- Локальный pipeline: [{{PIPELINE_DOC}}]({{PIPELINE_DOC}})
```

---

## §Поведение при Build / Execute plan (Cursor) — fixed runtime

```markdown
## Поведение при Build / Execute plan (Cursor)

**Fixed runtime plan (`*_builder.plan.md`):** markdown SSOT для **@attach** в project-чате. Исполнение — [session-starter.md](docs/methodology/Zeya888-builder-queue/core/session-starter.md) Phase 0 + промпты [workflow.md](docs/methodology/Zeya888-builder-queue/core/workflow.md) §P3/P6. Подробно: [fixed-builder-plan-execution.md](docs/methodology/Zeya888-builder-queue/guides/fixed-builder-plan-execution.md).

**Запрет:** не нажимать **Build / Execute plan** на этом файле. Cursor привязывает план к conversation ID в локальном registry; Build откроет «домашний» чат, а не активный project-чат.

**Как агент ведёт работу после @attach:** читает YAML с диска (`{{CURRENT_POINTER}}` → pkg); **TASK_BATCH** по нормализованной очереди; шаг 0 — `builder_resolve_queue.py --project {{CLI_PROJECT}} --verify`.

**Hardcoded / operator override:** метка `run_mode=…` — только из §«Явно прописанный safe-override»; **не** подменяет YAML SSOT.

### Границы ответственности

- **@attach fixed plan** — контекст LLM-агенту в **текущем** чате; нет встроенного диспетчера по каждому `README.md`.
- **Исполнение одного таска** — Режим A, bullrun/run-task; gates — `{{PIPELINE_DOC}}`.

### Frontmatter todos

Три элемента `todos` — **напоминания процесса**, не чеклист Plan UI Build. Прогресс — bullrun-launch-index в `{{TASKS_DIR}}`.

**Шаг 0 — сразу после @attach (корень workspace):**

\`\`\`bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project {{CLI_PROJECT}} --verify
\`\`\`

При missing paths — стоп. Шаг 0b: `--verify --check-dates` ([builder-artifact-dates.md](docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)).
```

---

## §safe-override (повторяемый H3)

```markdown
### Явно прописанный safe-override (<wave label>)

**Метка:** `run_mode=<wave_name>`

**Список (от корня DOGEstonia/):**
1. `…/README.md`
…

**activation:** `run_mode=<wave_name>`
```

P5 заполняет только при `exists` на каждый path. Иначе — draft pkg (см. workflow §P5).

---

## §Однозначный алгоритм резолва (унифицированный)

1. Явный `run_mode=…` — только если есть matching §safe-override с paths; **не** менять `{{CURRENT_POINTER}}`.
2. Любой другой `run_mode` без секции — сообщить оператору → YAML default (п.5).
3. Непустой `ACTIVE_TASK_PATH` → режим A или `explicit_invalid`.
4. `{{CURRENT_POINTER}}` → pkg → нормализация → режим A (default: **{{ACTIVE_PKG}}**, **{{PATH_COUNT}}** paths).
5. Пустая очередь → режим B.
6. Битый YAML / missing paths → `explicit_invalid`.

Project-specific run_mode — только как пункты 1.x **между** 1 и 2, если секции заполнены.

---

## Сборка plan из шаблона

1. `builder_resolve_queue.py --project {{CLI_PROJECT}} --verify`
2. Подставить плейсхолдеры из таблицы + verify output.
3. Скопировать §INPUT SOURCE…§Канон из нормализованного Gateway; заменить пути/`{{CLI_PROJECT}}`.
4. Добавить 0..N §safe-override (только волны с paths на диске).
5. Регрессия: H2 diff между тремя plan = ∅ (кроме safe-override H3).
