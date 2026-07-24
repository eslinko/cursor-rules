# Builder Queue — машиночитаемый input package (YAML)

**Версия:** 1.0  
**Реестр проектов:** [`profiles.yaml`](./profiles.yaml)  
**CLI:** [`builder_resolve_queue.py`](./builder_resolve_queue.py) с `--project <key>`

---

## 1. Назначение

Единый контракт input package для Story Builder во всех проектах workspace: нормализация в очередь `README.md`, immutable `pkg-*.yaml`, без мегастрок JSON в `.cursor/plans/*.plan.md`.

| Слой | Ответственность |
|------|-----------------|
| Этот файл | `input_kind`, нормализация, build-window, `ACTIVE_TASK_PATH` |
| `profiles.yaml` | Пути `tasks_dir`, префиксы, имена указателей |
| `{project}/docs/.../bullrun-launch-index.md` | Статусы, Run Reports Registry |
| `.cursor/plans/*_builder.plan.md` | Build, шаг 0, режимы A/B |

---

## 2. Файлы по профилю

| Профиль | `tasks_dir` | Указатель | Каталог пакетов |
|---------|-------------|-----------|-----------------|
| `gateway` | `doge-complaints-gateway/docs/tasks` | `gateway-active-package.current.yaml` | `gateway-active-packages/` |
| `gpt` | `GPT UI/docs/analysis/tasks` | `gpt-active-package.current.yaml` | `gpt-active-packages/` |
| `spa` | `spa-app/docs/tasks` | `spa-active-package.current.yaml` (будущее) | `spa-active-packages/` |
| `identity` | `doge-identity-service/docs/tasks` | `identity-active-package.current.yaml` | `identity-active-packages/` |
| `scripts` | `scripts/docs/tasks` | `scripts-active-package.current.yaml` | `scripts-active-packages/` |
| `capybara` | `capybara/docs/tasks` | `capybara-active-package.current.yaml` | `capybara-active-packages/` |

`package_file` в указателе — путь **относительно** `{tasks_dir}/`.

**Пример `epic_file` (identity):**

```yaml
input_kind: epic_story_tree
epic_file: doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch.md
story_groups:
  - story_key: STORY-IDS-01-02-appconfig
    paths:
      - doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-02-appconfig/task-ids-01-02-t01-schema/README.md
```

---

## 3. Обязательные мета-поля (`schema_version: 1`)

| Поле | Смысл |
|------|--------|
| `schema_version` | `1` |
| `package_sequence` | Монотонный номер пакета |
| `created_at` | ISO-8601 UTC; **date-part = scaffold session**; время из `builder_resolve_queue.py --print-utc-now`; см. [`guides/builder-artifact-dates.md`](../guides/builder-artifact-dates.md) |
| `label` | Короткое имя волны |
| `input_kind` | §4 |
| `tasks_root` | Префикс зоны тасков от корня workspace (см. `pkg_path_prefix` в `profiles.yaml`) |

Опционально: `gim_keys` (GPT), `decision_ref`, `epic_file`.

Пути — **от корня workspace** (каталог с `docs/methodology/Zeya888-builder-queue/`).

**Имя файла pkg:** `pkg-<package_sequence>-<YYYYMMDD>-<slug>.yaml` — сегмент `YYYYMMDD` **обязан** совпадать с date-part поля `created_at`.

**Проверка дат:** `--verify --check-dates` (см. guide + [`date-gate-grandfather.txt`](./date-gate-grandfather.txt)).

---

## 4. `input_kind`

### 4.1 `task_list_linear`

Плоский список (типично **gpt**, иногда gateway).

```yaml
input_kind: task_list_linear
linear_paths:
  - GPT UI/docs/analysis/tasks/task-example/README.md
```

### 4.2 `epic_decompose_pending`

Эпик без очереди README — сначала декомпозиция, затем новый `pkg` с `epic_story_tree` или `task_list_linear`.

### 4.3 `epic_story_tree`

Группы story (типично **gateway**).

```yaml
input_kind: epic_story_tree
epic_file: doge-complaints-gateway/docs/tasks/epics/EPIC-M2-14-....md
story_groups:
  - story_key: STORY-M2-14-01
    paths:
      - doge-complaints-gateway/docs/tasks/epics/.../README.md
```

### 4.4 `hybrid`

Смесь строк и `{ story_key, paths }` в `top_level` — нормализация слева направо.

---

## 5. Валидация (analysis.mdc)

Из корня workspace:

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --list
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --export-active-task-path
```

1. Каждый путь `exists`, префикс = `pkg_path_prefix` профиля, конец `README.md`.
2. Для grouped — сверка с bullrun и `STORY-*.md`.

---

## 6. `ACTIVE_TASK_PATH` (legacy export)

`--export-active-task-path` → одна строка `ACTIVE_TASK_PATH=[...]`.  
**Не** хранить во frontmatter Build plan.

---

## 7. Build-window (производный артефакт)

```bash
# gateway — по story
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway \
  --write-build-window --story-key STORY-M2-14-01

# gpt — плоский срез или gim
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt \
  --write-build-window --window-flat-start 1 --window-flat-end 3
```

Каталоги по умолчанию — `run-reports/{gateway,gpt,spa}-build-windows/`.  
Имена: `{prefix}--<StoryKey|flat-A-B>.md`. **Не SSOT** — перегенерировать после смены `pkg`.

---

## 8. Run metadata

| Профиль | Поле в run-summary |
|---------|-------------------|
| gateway | `gateway_input_package` |
| gpt | `gpt_input_package`, `task_batch_gim_keys` |
| spa | `spa_input_package` (будущее) |

Колонка **Input package** в `bullrun-launch-index.md`.

---

## 9. Deprecated

- Отдельные `gateway_resolve_queue.py` / `gpt_resolve_queue.py` — удалены; только `builder_resolve_queue.py --project`.
- `ACTIVE_TASK_PATH-*.env` — legacy; новые волны только YAML.
