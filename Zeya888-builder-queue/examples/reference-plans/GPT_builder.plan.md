---
name: GPT Builder
overview: "Оркестрация GPT UI: active pkg-000018 (REQ-38, 3 paths); audit follow-up GIM-166 via run_mode=req38_audit_followup; шаг 0 builder_resolve_queue --project gpt --verify."
todos:
  - id: resolve-start-item-from-index
    content: Определять стартовую сущность строго из bullrun-launch-index перед каждым batch-run
    status: completed
  - id: treat-missing-epic-as-not-decomposed
    content: Считать отсутствующий в индексе эпик не декомпозированным и запускать decomposed flow
    status: completed
  - id: sync-index-after-each-item
    content: После каждой story/task обновлять статус в bullrun-launch-index в той же итерации
    status: completed
isProject: false
---

# GPT Builder

Проект: `GPT UI`  
Рабочая зона: `/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/`  
Источник исполнения: `[gpt-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-story-execution-pipeline.md)`  
Сверка планов: [builder-plans-unification-analysis.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/analysis/builder-plans-unification-analysis.md)

## Назначение

Канонический SSOT-процесс для запуска и ведения работ в проекте `GPT UI` (инструкции, OpenAPI Actions, requirements).

**Стек:** markdown / YAML / Custom GPT — **не** смешивать с **Gateway Builder** или **Identity Builder**.

## Связь с unified workflow

- SSOT промптов P1–P8: [workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md)
- Типичный P1 для GPT: **P1.2** (REQ → tasks, primary) или **P1.1** при декомпозиции `EPIC-M1-*`
- **P1.3 `backlog_story`** — только identity; **не** применять к GPT
- Этот plan — **P3/P6 runtime** (pkg, build window, `run_mode`, режим A/B). Промпты P1 **не** дублировать.
- Локальный pipeline: [gpt-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-story-execution-pipeline.md)

## Поведение при Build / Execute plan (Cursor)

**Как это устроено в Cursor:** кнопка **Build** / **Execute plan** подключает к сессии **этот документ**. Default-очередь задаётся активным `pkg-*.yaml` через `[gpt-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-package.current.yaml)` (сейчас `pkg-000017-20260604-req36-civic-taxonomy-expansion.yaml`, **5** paths). Агент **обязан** прочитать YAML с диска и вести работу как **TASK_BATCH** по нормализованному списку.

**Hardcoded / operator override (вне `pkg-`*):** метка `run_mode=…` — фиксированный список из §«Явно прописанный safe-override»; **не** подменяет YAML SSOT (`hardcoded_override_mode = off`).

### Явно прописанный safe-override (REQ-40 audit follow-up)

Точечный запуск **без** смены active pkg. YAML default остаётся `pkg-000020` (immutable).

**Метка:** `run_mode=req40_audit_followup`

**Список (от корня `DOGEstonia/`):**

1. `GPT UI/docs/analysis/tasks/epics/EPIC-M1-06-orchestrator-openapi-web2/stories/STORY-M1-06-16-req40-evidence-severity-sidecar/task-fix-req40-evidence-summary-flag-nesting/README.md`

**Порядок P6:** GIM-174.

**activation:** `run_mode=req40_audit_followup`

### Границы ответственности

- **Build в Cursor** — подача контекста **LLM-агенту**; **нет** встроенного диспетчера по каждому `README.md`.
- **Исполнение одного таска** — **Режим A** ниже, `@.cursor/commands/bullrun-start.md`, `@.cursor/commands/run-task.md`, gates — `[gpt-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-story-execution-pipeline.md)`.

### Frontmatter todos этого `.plan.md`

Три элемента `todos` — **напоминания процесса**, не чеклист pkg. Прогресс — `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/bullrun-launch-index.md)`.

**Шаг 0 — сразу после Build (корень `DOGEstonia/`):**

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify
```

Ожидаемая строка: `ok 3 paths (project=gpt, pkg GPT UI/docs/analysis/tasks/gpt-active-packages/pkg-000018-20260602-req38-ecosystem-deficit-detection.yaml)`. При `FAIL` — стоп (**analysis.mdc**).

**Каноническая нумерация:** `--project gpt --list` · `--print-next` · `.gpt-next-readme` — `[gpt-active-packages/README.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-packages/README.md)`.  
**Build window (flat, производный):** `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --write-build-window --window-flat-start 1 --window-flat-end 5` → `run-reports/gpt-build-windows/gpt-cursor-build-window--flat-1-5.md`

### Шаблон первого сообщения в чат (после Build)

```markdown
GPT REQ-38 (pkg-000018): шаг 0 — `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify` → ok 3 paths.

Следующий таск: build-window `@GPT UI/docs/analysis/tasks/run-reports/gpt-build-windows/gpt-cursor-build-window--flat-….md` или README из `--list` NN.
Audit follow-up: `run_mode=req40_audit_followup` — только §safe-override (GIM-174), без смены active pkg.
Audit follow-up: `run_mode=req39_audit_followup` — только §safe-override (GIM-170), без смены active pkg.
Audit follow-up: `run_mode=req38_audit_followup` — только §safe-override (GIM-166), без смены active pkg.
Audit follow-up: `run_mode=req36_audit_followup` — только §safe-override (GIM-161→162), без смены active pkg.
Audit follow-up (legacy): `run_mode=req33_audit_followup` — только §safe-override (GIM-147→148), без смены active pkg.
Далее bullrun-start + run-task, Режим A. Режим B — только если нет валидного pkg и пустой ACTIVE_TASK_PATH.
```

**Сразу после шага 0:**

1. `[gpt-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-package.current.yaml)` → `pkg-000018-20260602-req38-ecosystem-deficit-detection.yaml`.
2. Нормализация по `[input-package-spec.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)` §4 — **3** paths; каждый — `exists`.
3. Сверка с `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/bullrun-launch-index.md)` (GIM-163…165).
4. Следующий README — по очереди pkg или указанию оператора.
5. **Режим A** по порядку; story/epic gates — pipeline.
6. До завершения пакета не переключаться на режим B.

**Прагматика длины сессии:** чекпоинт «следующий в очереди: `…/README.md`»; продолжение с того же `pkg-*.yaml`.

## Иерархия SSOT (что главнее при противоречии)

1. **Оперативный пакет** — `[pkg-000018-20260602-req38-ecosystem-deficit-detection.yaml](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-packages/pkg-000018-20260602-req38-ecosystem-deficit-detection.yaml)` через `[gpt-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-package.current.yaml)`. Run metadata: `gpt_input_package`.
2. **Статусы и реестр** — `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/bullrun-launch-index.md)` (+ `[gpt-interview-module1-tasks-index.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-interview-module1-tasks-index.md)` при дубле GIM).
3. **Требования** — `GPT UI/docs/requirements/REQ-*.md` (текущая волна: REQ-38 по pkg-000018; audit follow-up GIM-166 via `run_mode=req38_audit_followup`).
4. **Техническое описание таска** — `task-*/README.md` + `acceptance-verification-*.md`.

Точка входа исполнителя: п.1 или п.4; п.2–3 — scope, не подмена порядка pkg.

**Канон порядка:** pipeline §«Входные индексаторы»`, gates.

### Синхронизация при декомпозиции эпика (stories + task-папки)

После P1 ([workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md) §P1.1/P1.2) или изменения **EPIC-M1-*** / **STORY-*** / `task-`* **в одной итерации**:

1. Обновить `bullrun-launch-index.md` (+ gpt-interview index при необходимости).
2. Новый immutable `gpt-active-packages/pkg-*.yaml` + обновить `gpt-active-package.current.yaml`.
3. В `run-summary` — `gpt_input_package`, `gim_keys` / `epic_key`.
4. При смене operative-pkg — сброс frontmatter todos в `pending`.

Правило **analysis.mdc**: каждый path → `exists`.

## ☀️☀️ INPUT SOURCE ❤️❤️

Кратко; контракт — `[input-package-spec.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)`.

1. **Активная очередь:** `[pkg-000018-20260602-req38-ecosystem-deficit-detection.yaml](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-packages/pkg-000018-20260602-req38-ecosystem-deficit-detection.yaml)` — `task_list_linear`, **EPIC-M1-08**, **3**×`README.md` (GIM-163…165).
2. `[gpt-active-package.current.yaml](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-active-package.current.yaml)` → pkg-000018.
3. **Build из этого плана:** очередь = нормализация п.1; режим `explicit_package`; режим B не подменять.
4. **Опционально `ACTIVE_TASK_PATH`:** override; указать `gpt_input_package`.
5. **Run metadata:** `[run-reports/README.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/run-reports/README.md)` и §Run Summary в pipeline.

Битый YAML / missing README → `explicit_invalid`.

Однострочник: `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --export-active-task-path`

### Поле запуска

- **Предпочтительно:** очередь из YAML-пакета.
- `**ACTIVE_TASK_PATH` (legacy / override):** один путь или JSON / grouped JSON; пути от корня `DOGEstonia/`.

### Режим A: explicit input (один путь или пакет)

Если очередь **не пуста** и валидация прошла:

1. Очередь `README.md` из нормализации `pkg-*.yaml` или `ACTIVE_TASK_PATH` (`[input-package-spec.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)` §4).
2. Для **каждого** path: `exists`; префикс `…/GPT UI/docs/analysis/tasks/`. При `epic_story_tree` — сверить порядок с индексом и `STORY-*.md`.
3. **Conflict-scan (рекомендуемый):** GIM / статусы в `bullrun-launch-index.md`.
4. При **N > 1** — **строго по порядку**; режим B запрещён до конца пакета.
5. После **каждого** таска: sync index + `run-summary`; bullrun/run-task; `acceptance-verification-*.md`.
6. После группы story — **Story parent AC**; подсекция в `run-summary`.
7. После всех stories — **Epic AC gate**.

### Режим B: fallback от индекса

Нет валидного pkg **и** `ACTIVE_TASK_PATH` пуст:

1. `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/bullrun-launch-index.md)`.
2. Первая `⚪` по приоритету (см. `[GPT-BUILDER-PROCESS-SSOT.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/GPT-BUILDER-PROCESS-SSOT.md)` §1).
3. Первая `⚪` Story сверху вниз; порядок подтасков из `STORY-*.md`; Story parent AC после группы.

### Однозначный алгоритм резолва

1. Если оператор явно задал `run_mode=req40_audit_followup` — список из §«Явно прописанный safe-override (REQ-40 audit follow-up)»; **не** менять `gpt-active-package.current.yaml`.
2. Если оператор явно задал `run_mode=req39_audit_followup` — список из §«Явно прописанный safe-override (REQ-39 audit follow-up)»; **не** менять `gpt-active-package.current.yaml`.
3. Если оператор явно задал `run_mode=req38_audit_followup` — список из §«Явно прописанный safe-override (REQ-38 audit follow-up)»; **не** менять `gpt-active-package.current.yaml`.
4. Если оператор явно задал `run_mode=req36_audit_followup` — список из §«Явно прописанный safe-override (REQ-36 audit follow-up)»; **не** менять `gpt-active-package.current.yaml`.
5. Если оператор явно задал `run_mode=req33_audit_followup` — список из §«Явно прописанный safe-override (REQ-33 audit follow-up)»; **не** менять `gpt-active-package.current.yaml`.
6. Любой другой `run_mode=…` — **только** если есть одноимённый §safe-override с paths; иначе сообщить оператору → YAML default (п.9).
7. Непустой `ACTIVE_TASK_PATH` → режим A или `explicit_invalid`.
8. `gpt-active-package.current.yaml` → pkg → нормализация → режим A (default: **pkg-000020**, **3** paths).
9. Пустая очередь → режим B.
10. Битый YAML / missing paths → `explicit_invalid`, стоп.

## Статус внедрения правил

Очередь YAML + `builder_resolve_queue.py --project gpt`. Batch/runtime — `[gpt-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-story-execution-pipeline.md)`; Cursor — `[gpt-pipeline-user-manual-cursor.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-pipeline-user-manual-cursor.md)`. P1–P8 — `[workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md)`.

## Текущая точка по индексу (актуализируйте по файлу)

Сводка **не** задаёт порядок; порядок = **текущий `pkg-*.yaml*`* или `run_mode`. Статусы — `bullrun-launch-index.md` §EPIC-M1-08 (GIM-163…165 pkg-000018 Done; audit follow-up GIM-166 via `run_mode=req38_audit_followup`).

## Правило приоритизации и выбора эпиков

1. Эпик в файле, но не в индексе → не декомпозирован → `bullrun-epic-decompose`.
2. Эпик в индексе, незакрытые story/task → продолжать эпик.
3. Эпик `Done (Committed)` → следующий.

## Контракт ролей (обязательный)

- **Epic decomposition:** `@.cursor/commands/bullrun-epic-decompose.md`
- **Thinking:** `@.cursor/rules/analysis.mdc` (`@.cursor/commands/run-analysis.md`)
- **Process:** `@.cursor/commands/bullrun-start.md`, `@.cursor/commands/run-task.md`
- **Skill (GPT):** `@.cursor/skills/openai-custom-gpt-builder/SKILL.md` — в артефактах: `Skill declared: openai-custom-gpt-builder`
- **Git:** `[docs/methodology/git-commit-prompt.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/git-commit-prompt.md)`; сводка — `[git-commit.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/git-commit.md)`

## Уровни процесса

### 1) Epic

1. Стартовый эпик по `bullrun-launch-index.md`.
2. `EPIC-M1-`* → `bullrun-epic-decompose` + `analysis.mdc`.
3. Результат: `epics/`, `stories/`, `task-*/`; sync index + новый `pkg-`* + `gpt-active-package.current.yaml`.

### 2) Story или Task

1. Очередь: pkg / `ACTIVE_TASK_PATH` / fallback index.
2. Каждый `README.md` — bullrun/run-task; skill **openai-custom-gpt-builder**.
3. Story parent AC; Epic AC — pipeline.

### 3) Execution

1. `BULLRUN-PHASE-LOG.md`; checkpoints.
2. `acceptance-verification-*.md` перед закрытием таска.
3. Sync index после gates.

## Канон исполнения и отчётности (без дублирования pipeline)

- **Фазы и gates** — `[run-task.md](/Users/eslinko/Development/DOGEstonia/.cursor/commands/run-task.md)` + `[gpt-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-story-execution-pipeline.md)`.
- **Run Summary**, batch modes — pipeline; реестр — `[run-reports/README.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/run-reports/README.md)`.
- **Практический чеклист** — `[gpt-pipeline-user-manual-cursor.md](/Users/eslinko/Development/DOGEstonia/GPT UI/docs/analysis/tasks/gpt-pipeline-user-manual-cursor.md)`.

При изменении процесса править **сначала** pipeline и `run-task.md`, затем ссылки в этом плане.