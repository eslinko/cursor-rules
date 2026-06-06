---
name: Gateway Story Builder
overview: "Оркестрация doge-complaints-gateway: active pkg-000026 (REQ-46, STORY-M2-02-12, 7 paths); шаг 0 builder_resolve_queue --project gateway --verify."
todos:
  - id: resolve-start-epic-from-index
    content: Определять стартовый эпик строго из bullrun-launch-index перед каждым batch-run
    status: completed
  - id: treat-missing-epic-as-not-decomposed
    content: Считать отсутствующий в индексе эпик не декомпозированным и запускать decomposed flow
    status: completed
  - id: sync-index-after-each-story
    content: После каждой story обновлять статус в bullrun-launch-index в той же итерации
    status: completed
isProject: false
---

# Gateway Story Builder

Проект: `doge-complaints-gateway`  
Рабочая зона: `/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/`  
Источник процесса: `[m2-epic-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md)`  
Сверка планов: [builder-plans-unification-analysis.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/analysis/builder-plans-unification-analysis.md)

## Назначение

Канонический SSOT-процесс для запуска и ведения работ Module 2 в проекте `doge-complaints-gateway`.

**Стек:** только **Python** runtime gateway (`src/core/…`). Не смешивать с планом **GPT Builder** (`GPT UI`) или **Identity Builder** (`doge-identity-service`).

## Связь с unified workflow

- SSOT промптов P1–P8: [workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md)
- Типичный P1 для gateway: **P1.2** (`input_mode=requirement`) или **P1.1** (`input_mode=epic_story`)
- **P1.3 `backlog_story`** — только identity; **не** применять к gateway
- Этот plan — **P3/P6 runtime** (pkg, build window, `run_mode`, режим A/B). Промпты P1 **не** дублировать.
- Локальный pipeline: [m2-epic-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md)

## Поведение при Build / Execute plan (Cursor)

**Как это устроено в Cursor:** кнопка **Build** / **Execute plan** подключает к сессии **этот документ**. Default-очередь задаётся активным `pkg-*.yaml` через `[gateway-active-package.current.yaml](../../doge-complaints-gateway/docs/tasks/gateway-active-package.current.yaml)` (сейчас `pkg-000026-20260528-req46-demo-services-intake-transparency.yaml`, **7** paths). Агент **обязан** прочитать YAML с диска и вести работу как **TASK_BATCH** по нормализованному списку, а не придумывать порядок из текста плана.

**Hardcoded / operator override (вне `pkg-*`):** метка `run_mode=…` в чате — **фиксированный** нумерованный список `…/README.md` из подраздела **«Явно прописанный safe-override»** с тем же именем; **не** подменяет YAML SSOT для следующих запусков (`hardcoded_override_mode = off` по умолчанию).

### Явно прописанный safe-override (REQ-46 audit follow-up)

Точечный запуск **без** смены active pkg. YAML default остаётся `pkg-000026`.

**Метка:** `run_mode=story02_12_audit_req46_followup`

**Список (от корня `DOGEstonia/`):**

1. `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/task-m2-02-12-t08-audit-gap46-01-idempotency-gpt-signals-replay-flag/README.md`
2. `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/task-m2-02-12-t09-audit-gap46-02-gpt-signals-persist-exception-test/README.md`
3. `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/task-m2-02-12-t10-audit-gap46-03-geo-lookup-order-collision-tests/README.md`

**activation:** `run_mode=story02_12_audit_req46_followup`

### Явно прописанный safe-override (REQ-46 title hint purge and cleanup)

**Метка:** `run_mode=story02_12_req46_title_hint_purge_and_cleanup`

**Список (от корня `DOGEstonia/`):**

1. `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/task-m2-02-12-t11-req46-legacy-hint-stories-purge-and-drop-columns-migration/README.md`
2. `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/task-m2-02-12-t12-req46-remove-title-hint-from-persistence-layer/README.md`
3. `doge-complaints-gateway/docs/tasks/epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-12-demo-services-enablement-intake-transparency-req46/task-m2-02-12-t13-req46-title-hint-cleanup-tests-bootstrap-parity/README.md`

**activation:** `run_mode=story02_12_req46_title_hint_purge_and_cleanup`

### Границы ответственности

- **Build в Cursor** — подача контекста **LLM-агенту**; **нет** встроенного диспетчера по каждому `README.md`.
- **Исполнение одного таска** — раздел **«Режим A»** ниже, `@.cursor/commands/bullrun-start.md`, фазы `@.cursor/commands/run-task.md`, story/epic gates — по `[m2-epic-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md)`. Эти разделы **не** дублируют YAML.

### Frontmatter todos этого `.plan.md`

Три элемента `todos` в YAML вверху — **напоминания процесса**, не чеклист активного pkg. Прогресс — артефакты тасков и `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/bullrun-launch-index.md)`.

**Шаг 0 — сразу после Build (обязательный, корень `DOGEstonia/`):**

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```

Ожидаемая строка: `ok 7 paths (project=gateway, pkg doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000026-20260528-req46-demo-services-intake-transparency.yaml)`. При `FAIL` — стоп (**analysis.mdc**).

**Каноническая нумерация очереди:** `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --list`  
**Следующий README:** `--print-next` (опционально `--skip N`); `.gateway-next-readme` — см. `[gateway-active-packages/README.md](../../doge-complaints-gateway/docs/tasks/gateway-active-packages/README.md)`.  
**Build window (производный, не SSOT):** `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key <KEY>` → `run-reports/gateway-build-windows/gateway-cursor-build-window--<KEY>.md`

### Шаблон первого сообщения в чат (после Build)

```markdown
Gateway REQ-46 (pkg-000026): шаг 0 — `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify` → ok 7 paths.

Следующий таск: `@…/gateway-cursor-build-window--STORY-M2-02-12….md` (после --write-build-window --story-key STORY-M2-02-12) или README из `--list` NN.
Audit/override: только по явному `run_mode=…` из §safe-override (без смены active pkg).
Далее bullrun-start + run-task, Режим A. Режим B — только если нет валидного pkg и пустой ACTIVE_TASK_PATH.
```

**Сразу после шага 0:**

1. Загрузить `[gateway-active-package.current.yaml](../../doge-complaints-gateway/docs/tasks/gateway-active-package.current.yaml)` → `pkg-000026-20260528-req46-demo-services-intake-transparency.yaml`.
2. По `[input-package-spec.md](../../docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)` §4.3 нормализовать очередь `README.md` — **ровно 7** paths; каждый — `exists` (**analysis.mdc**).
3. Сверить с `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/bullrun-launch-index.md)` и `STORY-M2-02-12` (anti-drift).
4. Выбрать следующий исполняемый README — по очереди pkg или указанию оператора.
5. **Режим A** по порядку; story gate после группы; epic gate после пакета.
6. До завершения пакета не переключаться на режим B без явной команды.

**Прагматика длины сессии:** допускается чекпоинт «следующий в очереди: `…/README.md`»; продолжение с того же `pkg-*.yaml`.

## Иерархия SSOT (что главнее при противоречии)

1. **Оперативный пакет** — `[pkg-000026-20260528-req46-demo-services-intake-transparency.yaml](../../doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000026-20260528-req46-demo-services-intake-transparency.yaml)` через `[gateway-active-package.current.yaml](../../doge-complaints-gateway/docs/tasks/gateway-active-package.current.yaml)`. Нормализация — `[input-package-spec.md](../../docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)`. Run metadata: `gateway_input_package`.
2. **Статусы и реестр** — `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/bullrun-launch-index.md)`.
3. **Продуктовые решения (demo M2)** — `[22-m2-demo-story-intake-interview-ssot-v1.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/requirements/22-m2-demo-story-intake-interview-ssot-v1.md)`, `[23-m2-demo-story-clustering-interview-ssot-v1.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/requirements/23-m2-demo-story-clustering-interview-ssot-v1.md)`.
4. **Техническое описание таска** — task-папка `README.md` + `acceptance-verification-*.md`.

Точка входа исполнителя: п.1 или п.4; п.2–3 — scope, не подмена порядка pkg.

**Канон порядка:** разделы **«Входные индексаторы»**, gates — в `[m2-epic-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md)`.

### Синхронизация при декомпозиции эпика (stories + task-папки)

После P1 ([workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md) §P1.1/P1.2) или изменения **STORY-M2-*** / `task-m2-*` **в одной итерации**:

1. Обновить `bullrun-launch-index.md`.
2. Новый immutable `gateway-active-packages/pkg-<NNNNNN>-<date>-<slug>.yaml` + обновить `gateway-active-package.current.yaml`. Предыдущий `pkg-*` не переписывать.
3. В `run-summary` — `gateway_input_package`, `epic_key`, ключи `story` по группам.
4. При смене operative-pkg — сброс frontmatter todos в `pending` (визуально); фактические статусы в индексе.

Правило **analysis.mdc**: каждый path после нормализации YAML → `exists`.

## ☀️☀️ INPUT SOURCE ❤️❤️

Кратко; контракт — `[input-package-spec.md](../../docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)`.

1. **Активная очередь:** `[pkg-000026-20260528-req46-demo-services-intake-transparency.yaml](../../doge-complaints-gateway/docs/tasks/gateway-active-packages/pkg-000026-20260528-req46-demo-services-intake-transparency.yaml)` — `epic_story_tree`, `epic_file` → **EPIC-M2-02**, **STORY-M2-02-12** (REQ-46), **7**×`README.md` (T01–T07).
2. `[gateway-active-package.current.yaml](../../doge-complaints-gateway/docs/tasks/gateway-active-package.current.yaml)` → pkg-000026.
3. **Build из этого плана:** очередь = нормализация п.1; режим `explicit_package`; режим B не подменять до конца пакета.
4. **Опционально `ACTIVE_TASK_PATH`:** override; в отчёте указать `gateway_input_package`.
5. **Run metadata:** `[run-reports/README.md](../../doge-complaints-gateway/docs/tasks/run-reports/README.md)` и §Run Summary в pipeline.

Битый YAML / missing README → `explicit_invalid`.

**Исключено из пакета (закрыто):** `TASK-DOMAIN-STORY-CONTRACT-INTERVIEW-01`, `TASK-CLUSTER-CRITERIA-INTERVIEW-01` — SSOT в reqs 22/23.

Однострочник для shell: `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --export-active-task-path`

### Поле запуска

- **Предпочтительно:** очередь из YAML-пакета.
- **`ACTIVE_TASK_PATH` (legacy / override):** один путь или JSON-массив; пути от корня `DOGEstonia/`.

### Режим A: explicit input (один путь или пакет)

Если очередь **не пуста** и валидация прошла:

1. Очередь `README.md` из нормализации `pkg-*.yaml` или парсинга `ACTIVE_TASK_PATH` (`[input-package-spec.md](../../docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md)` §4).
2. Для **каждого** path: `exists`; префикс `…/doge-complaints-gateway/docs/tasks/`. При `epic_story_tree` — сверить порядок групп и `paths` с индексом и `STORY-*.md`.
3. **Conflict-scan (рекомендуемый):** статусы в `bullrun-launch-index.md`.
4. При **N > 1** — **строго по порядку**; режим B запрещён до конца пакета.
5. После **каждого** таска: sync index + `run-summary`; полный bullrun/run-task; `acceptance-verification-*.md` в папке таска.
6. После последнего path в story group — **Story parent AC**; подсекция в `run-summary`.
7. После всех stories пакета — **Epic AC gate**.

### Режим B: fallback от индекса

Нет валидного pkg для default Build **и** `ACTIVE_TASK_PATH` пуст:

1. `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/bullrun-launch-index.md)`.
2. Первая `⚪` по приоритету: Story/Task в активном EPIC → cross-epic backlog → Draft EPIC.
3. **Внутри секции эпика:** первая `⚪` Story сверху вниз; порядок подтасков из `STORY-*.md`; после последнего — **Story parent AC gate**.

### Однозначный алгоритм резолва

1. Если оператор явно задал `run_mode=story02_12_audit_req46_followup` — список из §«Явно прописанный safe-override (REQ-46 audit follow-up)»; **не** менять `gateway-active-package.current.yaml`.
2. Если оператор явно задал `run_mode=story02_12_req46_title_hint_purge_and_cleanup` — список из §«Явно прописанный safe-override (REQ-46 title hint purge and cleanup)»; **не** менять `gateway-active-package.current.yaml`.
3. Любой другой `run_mode=…` — **только** если в этом плане есть одноимённый подраздел «Явно прописанный safe-override» с нумерованными путями; иначе сообщить оператору и использовать YAML default (п.5).
4. Иначе непустой `ACTIVE_TASK_PATH` → парсинг; при успехе режим A; при ошибке `explicit_invalid`.
5. Иначе `gateway-active-package.current.yaml` → `pkg-*.yaml` → нормализация; при успехе режим A (default: **pkg-000026**, **7** paths).
6. Если очередь пуста и нет валидного входа → режим B.
7. Битый YAML / missing paths при explicit-запуске → `explicit_invalid`, стоп.

## Статус внедрения правил

Очередь YAML + `builder_resolve_queue.py --project gateway`. Batch-run — `m2-epic-story-execution-pipeline.md`; Cursor manual — `m2-pipeline-user-manual-cursor.md`. Операторский цикл P1–P8 — `[workflow.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/Zeya888-builder-queue/core/workflow.md)`.

## Текущая точка по индексу (актуализируйте по файлу)

Сводка **не** задаёт порядок; порядок = **текущий `pkg-*.yaml`** или явный `run_mode`. Статусы — `[bullrun-launch-index.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/bullrun-launch-index.md)` §EPIC-M2-02 / STORY-M2-02-12.

## Правило приоритизации и выбора эпиков

Перед batch-run сверить индекс (pipeline, «Оркестрация batch-run»):

1. Эпик в файле, но не в индексе → не декомпозирован → `bullrun-epic-decompose`.
2. Эпик в индексе, есть незакрытые story/task → продолжать эпик.
3. Эпик `Done (Committed)` → следующий.

## Контракт ролей (обязательный)

- **Epic decomposition:** `@.cursor/commands/bullrun-epic-decompose.md`
- **Thinking:** `@.cursor/rules/analysis.mdc` (`@.cursor/commands/run-analysis.md`)
- **Process:** `@.cursor/commands/bullrun-start.md`, `@.cursor/commands/run-task.md`
- **Skill (Python-only):** `@.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md` — в артефактах: `Skill declared: python-pro`
- **Git:** `[docs/methodology/git-commit.md](/Users/eslinko/Development/DOGEstonia/docs/methodology/git-commit.md)`

## Уровни процесса

### 1) Epic

1. Стартовый эпик по `bullrun-launch-index.md`.
2. `EPIC-M2-*` в `Draft` / `In Progress` → `bullrun-epic-decompose` + `analysis.mdc`.
3. Результат: `stories/STORY-M2-*.md`, task-папки, sync index + новый `pkg-*` + `gateway-active-package.current.yaml`; при grouped — `epic_story_tree`.

### 2) Story или Task

1. Очередь: pkg / `ACTIVE_TASK_PATH` / fallback index (режим B).
2. Каждый `README.md` — bullrun/run-task; `Skill declared: python-pro`.
3. После подтасков story — Story parent AC; после эпика — Epic AC.

### 3) Execution

1. `BULLRUN-PHASE-LOG.md` в каждой task-папке; checkpoints на паузах.
2. `acceptance-verification-*.md` перед закрытием таска.
3. Sync index после task/story/epic gates.

## Канон исполнения и отчётности (без дублирования pipeline)

- **Фазы таска и hard gates** — `[run-task.md](/Users/eslinko/Development/DOGEstonia/.cursor/commands/run-task.md)` и pipeline §Run-task hard gates, Story/Epic AC.
- **Контракт артефактов**, batch modes, Run Summary — `[m2-epic-story-execution-pipeline.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/m2-epic-story-execution-pipeline.md)`; реестр — `[run-reports/README.md](../../doge-complaints-gateway/docs/tasks/run-reports/README.md)`.
- **Практический чеклист** — `[m2-pipeline-user-manual-cursor.md](/Users/eslinko/Development/DOGEstonia/doge-complaints-gateway/docs/tasks/m2-pipeline-user-manual-cursor.md)`.

При изменении процесса править **сначала** pipeline и `run-task.md`, затем только ссылки в этом плане.
