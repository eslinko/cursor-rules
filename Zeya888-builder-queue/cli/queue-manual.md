# Мануал: Builder Queue и `builder_resolve_queue.py`

Коротко: **очередь из YAML**, **команды**, **сессия в Cursor**. Контракт — [`input-package-spec.md`](../specs/input-package-spec.md); реестр путей — [`profiles.yaml`](../specs/profiles.yaml).

---

## 0. Откуда всё читается

1. Выберите `--project` (`gateway`, `gpt`, `identity`, `spa`, `taxonomy`, …).
2. Скрипт читает `{tasks_dir}/*-active-package.current.yaml` → `package_file` → `pkg-*.yaml`.
3. Запуск **из корня workspace** (где есть `docs/methodology/Zeya888-builder-queue/specs/profiles.yaml`).

```bash
cd /путь/к/DOGEstonia
```

---

## 1. Обычная сессия (пошагово)

### Шаг 1 — verify

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```

Успех: `ok N paths (project=gateway, pkg …)`.

### Шаг 2 — build window

**Gateway (по story):**

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway \
  --write-build-window --story-key STORY-M2-14-01
```

**GPT (плоский срез):**

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt \
  --write-build-window --window-flat-start 1 --window-flat-end 3
```

**Stdout (пример для gpt):** `ok build-window` → `build_window_abs:` (Cmd+click в терминале) → `quick_open_basename:` / `quick_open_pointer:` (для **Cmd+P**, без обрезки `GPT UI` → `UI`) → symlink `gpt-active-packages/latest-cursor-build-window.md` → `cursor_attach: @…`. **Не** вставляйте полный путь в Go-to-File — IDE обрезает на пробеле.

### Шаг 3 — Cursor

Подключите `@.cursor/plans/{Gateway|GPT}_builder.plan.md` и сгенерированное окно из `run-reports/*-build-windows/`. См. [workflow.md](../core/workflow.md) P2 (окно) и P3 (execution).

### Шаг 4 — после story

Story parent AC / epic AC по pipeline проекта. Следующая story — снова шаг 2.

### Шаг 5 — смена pkg

Снова verify + write-build-window.

---

## 2. Команды (копипаст)

Замените `{proj}` на `gateway` или `gpt`.

| Задача | Команда |
|--------|---------|
| Verify | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project {proj} --verify` |
| List | `… --project {proj} --list` |
| ACTIVE_TASK_PATH | `… --project {proj} --export-active-task-path` |
| Next path | `… --project {proj} --print-next` |
| Next + skip N | `… --print-next --skip N` |
| Next pointer file | `… --project {proj} --write-next-pointer` |
| Window by story-key | `… --write-build-window --story-key STORY-…` |
| Window by story-index | `… --write-build-window --story-index 2` |
| Flat slice | `… --write-build-window --window-flat-start A --window-flat-end B` |
| GPT gim slice | `… --project gpt --write-build-window --gim-slice GIM-102,GIM-103` |
| Custom out path | добавить `--build-window-out path/from/repo/root.md` |

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --help
```

---

## 3. Режимы `--write-build-window`

Ровно **один** из: `--story-key`, `--story-index`, `--window-flat-start`, `--gim-slice` (gpt).

Окна **не SSOT** — перегенерировать после смены pkg.

---

## 4. Профиль `identity` (epic-first)

**Вход:** `input_mode=epic_story` → `EPIC-IDS-*.md`; `input_mode=requirement` → `docs/requirements/NN-*.md` (эпик подбирается из индекса). Операторский контракт — [identity-operator-contract.md](../contracts/identity-operator-contract.md). Маршрут — [workflow.md](../core/workflow.md) §P1/P2/P3.

**Перед run:** `bullrun-launch-index.md` + `identity-active-package.current.yaml` + `--verify`. Эпик без строки в индексе → decompose, не execute.

### Verify / list

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --list
```

До первого P1 (нет `package_file` в `identity-active-package.current.yaml`) **verify и list ожидаемо FAIL** — норма.

### Build window

**Одна Story:**

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity \
  --write-build-window --story-key STORY-IDS-01-02-appconfig
```

**Весь эпик** (все README в активном pkg, flat `1..K`):

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity \
  --write-build-window --window-flat-start 1 --window-flat-end K
```

`K` — из `--list`. Execution: `@$epicFile` + build window; pipeline — `doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md`.

---

## 5. Профиль `spa`

`--project spa` — активен. До первого **P1.3** `pkg-bootstrap-pending.yaml` даёт пустую очередь; `--verify` → **FAIL** (ожидаемо). После P1 — flat window: `--write-build-window --window-flat-start 1 --window-flat-end N`. Контракт: [spa-operator-contract.md](../contracts/spa-operator-contract.md). Runtime plan: `.cursor/plans/Spa_builder.plan.md`.

---

## 6. Профиль `taxonomy` (queueless meta-script)

**Taxonomy Cycle Builder** — ручной цикл обновления меток (телеметрия → решения → патчи gateway + spa). **Не** pkg-очередь: нет `--list`, `--write-build-window`, `pkg-*.yaml`.

Runtime plan: [`.cursor/plans/Taxonomy_builder.plan.md`](../../../../.cursor/plans/Taxonomy_builder.plan.md)  
Runbook: `doge-complaints-gateway/docs/runtime-docs/appendix/taxonomy-update-process-ru.md`

### Verify (единственная CLI-команда для профиля)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project taxonomy --verify
```

Успех: `ok taxonomy verify (N paths)` — plan + scripts + schema + `taxonomy-cycles/README.md` на диске.

Любой другой флаг → ошибка: *«Профиль taxonomy (queueless) поддерживает только --verify»*.

### Запуск цикла в Cursor

```text
@.cursor/plans/Taxonomy_builder.plan.md
@doge-complaints-gateway/docs/runtime-docs/appendix/taxonomy-update-process-ru.md
Taxonomy cycle TC0–TC7. cycle_id=YYYYMMDD. Claims из кода.
```

**Зависимости:** GW-L10N-03 (`POST /telemetry/label-misses`); SPA-отправитель telemetry (GL-5) — отдельная spa-задача. До GL-5 operational cycle (TC1+) ждёт живых misses или ручного POST.

---

## 7. Troubleshooting

| Симптом | Действие |
|---------|----------|
| Нет указателя / пакета | Проверить `*-active-package.current.yaml` |
| FAIL verify | Исправить пути в pkg |
| IDE не находит окно после `write-build-window` | **Cmd+P:** `latest-cursor-build-window` или `gpt-cursor-build-window--flat-…`; либо Cmd+click `build_window_abs:` / `vscode_file_uri:`; либо открыть `gpt-active-packages/latest-cursor-build-window.md` (symlink). Не вставлять `UI/docs/…` — это обрезанный путь |
| story_key не найден | Точное совпадение с YAML |
| Неизвестный --project | Список ключей в `profiles.yaml` |

---

## 8. Override в Build plan

YAML — default. Hardcoded override в `*_builder.plan.md` — только по **явной** команде оператора в чате. После mini-wave — убрать override, снова verify + list.

---

## 9. Связанные файлы

| Файл | Зачем |
|------|-------|
| [`profiles.yaml`](../specs/profiles.yaml) | Пути per project |
| [`builder_resolve_queue.py`](./builder_resolve_queue.py) | CLI |
| [`session-starter.md`](../core/session-starter.md) | Phase 0 |
