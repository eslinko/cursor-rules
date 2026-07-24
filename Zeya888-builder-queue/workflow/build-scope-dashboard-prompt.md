# Build scope dashboard — prompt (focus dialog)

> **Канон секций / %:** [`backlog-dashboard-template.md`](./backlog-dashboard-template.md)  
> **Housekeeping:** [`backlog-dashboard-maintenance.md`](./backlog-dashboard-maintenance.md)  
> **Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
> **Команда:** [`/build-scope-dashboard`](../../../../.cursor/commands/build-scope-dashboard.md)

Self-contained промпт для **фокусного проектного диалога**. Скопируй в чат профиля или вызови команду. Не меняй статусы story/REQ без path evidence.

---

## Роль

Ты собираешь Layer-2 **per-scope backlog dashboard** (derived snapshot для `npm run dashboard:aggregate`).  
Ты **не** SSOT статусов: только recount с диска → markdown snapshot по канону template.

---

## Входные параметры

Оператор задаёт на старте (или в команде):

| Параметр | Обязателен | Пример | Смысл |
|----------|------------|--------|--------|
| `$scope` | **да** | `MVP` | Display-label в шапке `Scope:` |
| `$builderProject` | да (из сессии) | `gateway` / `gpt` / … | Ключ профиля в [`profiles.yaml`](../specs/profiles.yaml) |

### Derive (сделай сам, не спрашивай)

1. `$scopeId` = lowercase slug от `$scope`  
   - `MVP` → `mvp`  
   - `post-MVP` / `Post MVP` → `post-mvp`  
   - пробелы → `-`; только `[a-z0-9-]`
2. `$focusFolder` = `focus_folder` профиля (`doge-complaints-gateway`, `GPT UI`, …)
3. `$project` = обычно = `$builderProject` (имя файла: `gateway`, `gpt`, …)
4. `$dashboardFile` = `{focusFolder}/docs/tasks/{project}-{scopeId}-dashboard.md`  
   **Всегда** `docs/tasks/`, даже если `tasks_dir` профиля = `…/docs/analysis/tasks` (gpt).

Примеры:

- `$builderProject=gateway`, `$scope=MVP` → `doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md`
- `$builderProject=gpt`, `$scope=MVP` → `GPT UI/docs/tasks/gpt-mvp-dashboard.md`

### Hard stop (до Discover)

- Нет `$scope` → спроси **один** вопрос: «Задай `$scope=` (напр. MVP)» и жди.
- Нет `$builderProject` и нельзя вывести из сессии/плана → спроси один раз.

---

## Промпт (исполняй по фазам)

```text
@.cursor/rules/analysis.mdc
@docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-template.md
@docs/methodology/Zeya888-builder-queue/specs/profiles.yaml

$builderProject = <from session>
$scope = <operator, e.g. MVP>

# Derive: $scopeId, $focusFolder, $dashboardFile (см. выше)

Задача: собрать материал с диска и создать/обновить $dashboardFile
по канону backlog-dashboard-template.md для Scope=$scope / Scope-Id=$scopeId.
```

### Phase A — Discover (read-only)

Прочитай с диска (только то, что существует; не выдумывай пути):

1. Profile: `focus_folder`, `tasks_dir` из `profiles.yaml` для `$builderProject`.
2. Backlog:
   - `{focus}/docs/tasks/backlog-stories/INDEX.md` (или под `$tasksRoot`, если backlog там)
   - каждый package `…/backlog-stories/*/INDEX.md`
3. Bullrun / launch index: `{tasks_dir}/bullrun-launch-index.md` или `{focus}/docs/tasks/bullrun-launch-index.md`
4. Requirements: `{focus}/docs/requirements/**` — поле **Status** в каждом REQ (если каталог есть)
5. Doc-tasks: файлы `DOC-TASK-*` в backlog packages / analysis audit scope (если есть)
6. Epics: Meta Status в epic md (compact) — **не** разворачивай все stories
7. Существующий `$dashboardFile`; иначе legacy `{project}-backlog-dashboard.md`
8. Эталоны (при сомнении в формате):  
   `doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md`,  
   `GPT UI/docs/tasks/gpt-mvp-dashboard.md`

Зафиксируй кратко inventory: packages, story counts by status, REQ done/open/deferred, doc-tasks, path целевого файла.

### Phase B — Recount

По [`backlog-dashboard-template.md`](./backlog-dashboard-template.md) §Правила цифр:

| В active % | Вне % |
|------------|-------|
| Stories Done + Todo в scope | Deferred / post-scope |
| REQ Done + open в scope | Baseline SoT / vacant без файла |
| Doc-tasks Done + Todo | Superseded (0) |

```
active_total = done + todo
pct = round(100 * done / active_total)   # active_total=0 → 100%
filled = round(12 * done / active_total) # bar █/░, clamp 0…12
```

- **By package** — только product stories пакета.
- **Remaining** — одна таблица активных Todo: `Type | Key | Title | Package/Epic | Status | Priority | Essence`  
  Essence: одна ясная фраза; без канцелярита и без метафор.
- **Deferred** — только §Deferred + колонка Deferred; не в Remaining.
- Omit секции, которых нет смысла (нет REQ → нет Requirements Done).

Конфликт INDEX vs gate/acceptance без evidence → **стоп**, спроси оператора; статус не меняй.

### Phase C — Write

1. Дата:  
   `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now`  
   → `Updated: YYYY-MM-DD` (UTC date).
2. Запиши **полный** `$dashboardFile` (create или update in place) с обязательными секциями template:
   - Header: Scope-Id, Scope, SSOT links, Updated, Last change
   - Summary (Active work items, Done, Todo, Deferred, Overall progress (active) + bar)
   - By package
   - Remaining
   - Requirements Done (если есть)
   - Epic rollup (compact)
   - Roadmap → 100%
   - §Now / §Deferred
   - Mermaid pie (Done/Todo active)
   - How to refresh
3. Если создаёшь новый scope-файл, а есть legacy `{project}-backlog-dashboard.md` с полным содержимым: замени legacy на **redirect stub** (5–10 строк → ссылка на `$dashboardFile`), как у gateway/gpt.
4. Если `$dashboardFile` уже в [`snapshot-paths.js`](../../../../scripts/lib/backlog-dashboard/snapshot-paths.js) — ок. Если профиль ещё на legacy path и ты создал `{scopeId}` файл — **сообщи** оператору, что registry нужно обновить отдельно (не ломай чужие проекты молча, кроме явного legacy→scope rename для этого профиля).

### Phase D — Verify

```bash
npm run dashboard:aggregate
```

Spot-check: в embedded JSON / HTML accordion есть проект; `progress_pct` и counts согласованы с Summary.

**Отчёт оператору (кратко):**

```text
dashboard: $dashboardFile
scope: $scope ($scopeId)
active: done/todo → pct%
Remaining: N rows
aggregate: ok | WARN
```

---

## Запрещено

- Угадывать Done / менять Status в INDEX или REQ без evidence на диске
- Писать snapshot в `docs/analysis/tasks/`
- Полный story-by-story dump внутри Epic rollup
- Править `DASHBOARD_DATA` в `backlog-dashboard.html` вручную
- Редактировать plan-файлы без явной команды оператора

---

## Быстрый копипаст (минимальный)

```text
$builderProject = gateway
$scope = MVP

Исполни @docs/methodology/Zeya888-builder-queue/workflow/build-scope-dashboard-prompt.md
с @.cursor/rules/analysis.mdc
```
