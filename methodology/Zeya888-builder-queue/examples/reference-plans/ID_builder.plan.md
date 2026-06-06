---
name: Identity Story Builder
overview: "Оркестрация doge-identity-service: active pkg-000014 (EPIC-IDS-08 CLEANUP-03, 6 paths); шаг 0 builder_resolve_queue --project identity --verify."
todos:
  - id: resolve-start-from-index
    content: Перед batch-run сверять bullrun-launch-index и активный pkg
    status: 
  - id: treat-missing-epic-as-not-decomposed
    content: Эпик в файле без индекса — не декомпозирован; bullrun-epic-decompose
    status: 
  - id: sync-index-after-each-task
    content: После каждого закрытого task/story обновлять bullrun-launch-index в той же итерации
    status: 
isProject: false
---

# Identity Story Builder

Проект: `doge-identity-service`  
Рабочая зона: `/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/`  
Источник процесса: `[ids-epic-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md)`  
Сверка планов: [builder-plans-unification-analysis.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/analysis/builder-plans-unification-analysis.md)  
Операторский контракт (P1 input_mode, P4): [contracts/identity-operator-contract.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md)

## Назначение

Канонический SSOT-процесс Builder Queue для `doge-identity-service` (`builder_project: identity`).

**Стек:** Python 3.11+ (`src/core/…`, FastAPI). **Не смешивать** с Gateway Builder или GPT Builder.

## Связь с unified workflow

- SSOT промптов P1–P8: [workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md)
- Типичный P1 для identity: **P1.2** / **P1.1** / **P1.3 `backlog_story`** — см. [contracts/identity-operator-contract.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md) §4 (один `input_mode` на сессию)
- Этот plan — **P3/P6 runtime** (pkg, build window, `run_mode`, режим A/B). Промпты P1 **не** дублировать.
- Локальный pipeline: [ids-epic-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md)

## Поведение при Build / Execute plan (Cursor)

**Как это устроено в Cursor:** кнопка **Build** / **Execute plan** подключает к сессии **этот документ**. Default-очередь задаётся активным `pkg-*.yaml` через `[identity-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/identity-active-package.current.yaml)` (сейчас `pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml`, **6** paths). Агент **обязан** прочитать YAML с диска и вести работу как **TASK_BATCH**.

**Hardcoded / operator override (вне `pkg-`*):** метка `run_mode=…` — фиксированный список из §«Явно прописанный safe-override»; **не** подменяет YAML SSOT (`hardcoded_override_mode = off`).

### Явно прописанный safe-override (EPIC-IDS-09 EID-01 audit 2026-06-06)

Точечный запуск **без** смены active pkg. YAML default остаётся `pkg-000015`.

**Метка:** `run_mode=epic_ids_09_eid_01_audit_2026_06_06`

**Правило:** при этой метке исполняется **только** список ниже; `**identity-active-package.current.yaml` не менять** (default = pkg-000015).

**Audit SSOT:** `[epic-ids-09-eid-01-audit-2026-06-06.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/analysis/epic-ids-09-eid-01-audit-2026-06-06.md)` (F1)

**Список (от корня `DOGEstonia/`):**

1. `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/task-ids-09-01-t07-audit-f1-backlog-story-status-sync/README.md`

**activation:** `run_mode=epic_ids_09_eid_01_audit_2026_06_06`

### Границы ответственности

- **Build в Cursor** — подача контекста **LLM-агенту**; **нет** встроенного диспетчера по каждому `README.md`.
- **Исполнение одного таска** — **Режим A** ниже, bullrun/run-task; gates — `[ids-epic-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md)`.

### Frontmatter todos этого `.plan.md`

Три элемента `todos` — **напоминания процесса**, не чеклист pkg. Прогресс — `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/bullrun-launch-index.md)`.

**Шаг 0 — сразу после Build (корень `DOGEstonia/`):**

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```

Ожидаемая строка: `ok 6 paths (project=identity, pkg doge-identity-service/docs/tasks/identity-active-packages/pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml)`. При `FAIL` — стоп (**analysis.mdc**).

**Каноническая нумерация:** `--project identity --list` · `--print-next` · `.identity-next-readme` — см. `[queue-manual.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/cli/queue-manual.md)`.

**Build window (производный):**


| Охват      | Команда                                                             |
| ---------- | ------------------------------------------------------------------- |
| Одна story | `… --write-build-window --story-key STORY-IDS-CLEANUP-03-doc-drift` |
| Flat срез  | `… --write-build-window --window-flat-start 1 --window-flat-end 6`  |


### Шаблон первого сообщения в чат (после Build)

```markdown
Identity EPIC-IDS-08 (pkg-000014): шаг 0 — `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify` → ok 6 paths.

input_mode / run_mode: один на сессию — см. [contracts/identity-operator-contract.md](docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md) §4.
Следующий таск: build-window или README из `--list` NN.
Далее bullrun-start + run-task, Режим A. Режим B — только если нет валидного pkg и пустой ACTIVE_TASK_PATH.
```

**Сразу после шага 0:**

1. `identity-active-package.current.yaml` → `pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml`.
2. Нормализация по `[input-package-spec.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)` — **6** paths; каждый — `exists`.
3. Сверка с `bullrun-launch-index.md`.
4. Следующий README — по очереди pkg или указанию оператора.
5. **Режим A** по порядку; story/epic gates — pipeline.
6. До завершения пакета не переключаться на режим B.

**Прагматика длины сессии:** чекпоинт «следующий в очереди: `…/README.md`».

## Иерархия SSOT (что главнее при противоречии)

1. **Оперативный пакет** — `[pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/identity-active-packages/pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml)` через `[identity-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/identity-active-package.current.yaml)`. Run metadata: `identity_input_package`.
2. **Статусы и реестр** — `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/bullrun-launch-index.md)`.
3. **Продуктовые решения** — `docs/requirements/`, `docs/tasks/epics/`, `docs/tasks/backlog-stories/` (порядок по `input_mode` — [operator contract](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md) §SSOT order).
4. **Техническое описание таска** — `README.md` + `acceptance-verification-*.md`.

Точка входа исполнителя: п.1 или п.4; п.2–3 — scope, не подмена порядка pkg.

**Канон порядка:** pipeline §gates.

### Синхронизация при декомпозиции эпика (stories + task-папки)

После P1 ([workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md) §P1.1/P1.2/P1.3) или изменения **STORY-IDS-*** / `task-ids-*` **в одной итерации**:

1. Обновить `bullrun-launch-index.md`.
2. Новый immutable `identity-active-packages/pkg-*.yaml` + обновить `identity-active-package.current.yaml`.
3. В `run-summary` — `identity_input_package`, `epic_file` / `decision_ref`.
4. При смене operative-pkg — сброс frontmatter todos в `pending`.

Правило **analysis.mdc**: каждый path → `exists`.

## ☀️☀️ INPUT SOURCE ❤️❤️

Кратко; контракт — `[input-package-spec.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)`.

1. **Активная очередь:** `[pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/identity-active-packages/pkg-000014-20260605-epic-ids-08-cleanup-03-doc-drift.yaml)` — `epic_story_tree`, **EPIC-IDS-08** CLEANUP-03, **6**×`README.md` (1 story group, 🟢 Done).
2. `[identity-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/identity-active-package.current.yaml)` → pkg-000014.
3. **Build из этого плана:** очередь = нормализация п.1; режим `explicit_package`; режим B не подменять.
4. **Опционально `ACTIVE_TASK_PATH`:** override; указать `identity_input_package`.
5. **Run metadata:** `doge-identity-service/docs/tasks/run-reports/` (реестр run-summary).

Битый YAML / missing README → `explicit_invalid`.

### Поле запуска

- **Предпочтительно:** очередь из YAML-пакета.
- `**ACTIVE_TASK_PATH` (legacy):** JSON / один путь; пути от корня `DOGEstonia/`.

### Режим A: explicit input (один путь или пакет)

Если очередь **не пуста** и валидация прошла:

1. Очередь `README.md` из нормализации `pkg-*.yaml` или `ACTIVE_TASK_PATH` (`[input-package-spec.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)` §4).
2. Для **каждого** path: `exists`; префикс `…/doge-identity-service/docs/tasks/`. При `epic_story_tree` — сверить порядок с индексом и `STORY-*.md`.
3. **Conflict-scan (рекомендуемый):** статусы в `bullrun-launch-index.md`.
4. При **N > 1** — **строго по порядку**; режим B запрещён до конца пакета.
5. После **каждого** таска: sync index + `run-summary`; bullrun/run-task; `acceptance-verification-*.md`.
6. После последнего path в story group — **Story parent AC**.
7. После всех stories пакета — **Epic AC gate**.

### Режим B: fallback от индекса

Нет валидного pkg **и** `ACTIVE_TASK_PATH` пуст:

1. `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/bullrun-launch-index.md)`.
2. Первая `⚪` в активном `EPIC-IDS-*`.
3. Порядок подтасков из story markdown / индекса; Story parent AC после группы.

### Однозначный алгоритм резолва

1. Если оператор явно задал `run_mode=epic_ids_06_audit_2026_06_02` — список из §«Явно прописанный safe-override (EPIC-IDS-06 audit 2026-06-02)»; **не** менять `identity-active-package.current.yaml`.
2. Если оператор явно задал `run_mode=epic_ids_08_cleanup_02_audit_2026_06_05` — список из §«Явно прописанный safe-override (EPIC-IDS-08 CLEANUP-02 audit 2026-06-05)»; **не** менять `identity-active-package.current.yaml` (default = pkg-000013).
3. Если оператор явно задал `run_mode=epic_ids_09_eid_01_audit_2026_06_06` — список из §«Явно прописанный safe-override (EPIC-IDS-09 EID-01 audit 2026-06-06)»; **не** менять `identity-active-package.current.yaml` (default = pkg-000015).
4. Любой другой `run_mode=…` — **только** если есть одноимённый §safe-override с paths; иначе сообщить оператору → YAML default (п.7).
5. Непустой `ACTIVE_TASK_PATH` → режим A или `explicit_invalid`.
6. `identity-active-package.current.yaml` → pkg → нормализация → режим A (default: **pkg-000015**, **6** paths).
7. Пустая очередь → режим B.
8. Битый YAML / missing paths → `explicit_invalid`, стоп.

## Статус внедрения правил

Очередь YAML + `builder_resolve_queue.py --project identity`. Pipeline — `ids-epic-execution-pipeline.md`. P1–P8 — `[workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md)`; onboarding — `[session-starter.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/session-starter.md)`.

## Текущая точка по индексу (актуализируйте по файлу)

Сводка **не** задаёт порядок; порядок = **текущий `pkg-*.yaml`** или `run_mode`. **pkg-000014** (CLEANUP-03) 🟢 Done — 6 tasks docs-only. Post-audit `[epic-ids-08-cleanup-03-audit-2026-06-06.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/analysis/epic-ids-08-cleanup-03-audit-2026-06-06.md)`: **zero-gap**, P5 **activation: none** (без нового `run_mode`). **Next:** EPIC-IDS-08 epic gate (отдельная P1). Исторические override: `run_mode=epic_ids_06_audit_2026_06_02`, `run_mode=epic_ids_08_cleanup_02_audit_2026_06_05`.

## Правило приоритизации и выбора эпиков

1. Эпик в файле, но не в индексе → не декомпозирован → `bullrun-epic-decompose`.
2. Эпик в индексе, незакрытые story/task → продолжать эпик.
3. Эпик `Done (Committed)` → следующий.

Только префикс `EPIC-IDS-`* в `docs/tasks/epics/` (см. operator contract).

## Контракт ролей (обязательный)

- **Epic decomposition:** `@.cursor/commands/bullrun-epic-decompose.md`
- **Thinking:** `@.cursor/rules/analysis.mdc`
- **Process:** `@.cursor/commands/bullrun-start.md`, `@.cursor/commands/run-task.md`
- **Skill:** `@.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md` — в артефактах: `Skill declared: python-pro`
- **Git:** `[docs/methodology/git-commit.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/git-commit.md)`; scope по EPIC-IDS / requirement

## Уровни процесса

### 1) Epic

1. Стартовый эпик по `bullrun-launch-index.md`.
2. `EPIC-IDS-`* → `bullrun-epic-decompose` + `analysis.mdc`.
3. Результат: `stories/STORY-IDS-*.md`, `task-ids-`*; sync index + новый `pkg-*` + `identity-active-package.current.yaml`.

### 2) Story или Task

1. Очередь: pkg / `ACTIVE_TASK_PATH` / fallback index.
2. Каждый `README.md` — bullrun/run-task; `Skill declared: python-pro`.
3. Story parent AC; Epic AC — pipeline.

### 3) Execution

1. `BULLRUN-PHASE-LOG.md`; checkpoints.
2. `acceptance-verification-*.md` перед закрытием таска.
3. Sync index после gates.

## Канон исполнения и отчётности (без дублирования pipeline)

- **Фазы и gates** — `[run-task.md](/Users/eslinko/Development/DOGEstonia/.cursor/commands/run-task.md)` + `[ids-epic-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md)`.
- **Run Summary**, batch modes — pipeline; отчёты аудита — `doge-identity-service/docs/analysis/`.
- P4/P4b якоря по `input_mode` — [operator contract](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md) §5.

При изменении процесса править **сначала** pipeline и `run-task.md`, затем ссылки в этом плане.