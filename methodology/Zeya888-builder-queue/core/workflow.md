# Workflow: Requirement → Pipeline → Audit

Операторский playbook для Zeya888 Builder Queue. Детали YAML/CLI — в [`input-package-spec.md`](../specs/input-package-spec.md), [`queue-manual.md`](../cli/queue-manual.md).

**Нужны полные промпты P1–P8 (self-contained), P4/P7 audit целиком, таблица «экономия токенов», wave checkpoint с деталями?** → `[workflow-legacy.md](./workflow-legacy.md)` (нумерация legacy может отличаться — см. заголовки фаз).

## Переменные пайплайна

Оператор задаёт `**builder_project`** (`gateway` | `gpt` | `identity` | …) в [starter](./session-starter.md) или в wave checkpoint.


| Переменная         | Подстановка                                                                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$builderProject`  | `gateway` / `gpt` / …                                                                                                                                      |
| `$verifyCmd`       | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project $builderProject --verify`                                                       |
| `$inputMode`       | `requirement` \| `epic_story` \| `backlog_story`                                                                                                           |
| `$requirementDoc`  | файл требования (для `input_mode=requirement`)                                                                                                             |
| `$epicFile`        | файл эпика (для `input_mode=epic_story`)                                                                                                                   |
| `$storyFile`       | для `input_mode=backlog_story` — готовая story из `backlog-stories/` (напр. `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-*.md`); для `input_mode=epic_story` — опционально одна story внутри эпика |
| `$backlogIndex`    | опционально для `input_mode=backlog_story`: `doge-identity-service/docs/tasks/backlog-stories/INDEX.md` (порядок/зависимости; не подменяет AC story)       |
| `$planFile`        | см. `plan_file` в [`profiles.yaml`](../specs/profiles.yaml)                                                                                                       |
| `$tasksRoot`       | см. `tasks_dir` в profiles                                                                                                                                 |
| `$storyKey`        | ключ story (gateway), напр. `STORY-M2-14-07`                                                                                                               |
| `$buildWindowFile` | путь к `*-cursor-build-window--*.md` в `run-reports/*-build-windows/` (строка `build_window_file:` в stdout после P2; для Cmd+click — `build_window_abs:`) |
| `$buildWindowCmd`  | см. §P2 — флаги `--write-build-window` для `$builderProject`                                                                                               |
| `$auditReport`     | `{focus_project}/docs/analysis/*.md`                                                                                                                       |


### Профили (быстрая таблица)


|               | `gateway`                                    | `gpt`                                       |
| ------------- | -------------------------------------------- | ------------------------------------------- |
| `$planFile`   | `.cursor/plans/Gateway_builder.plan.md`      | `.cursor/plans/GPT_builder.plan.md`         |
| `$tasksRoot`  | `doge-complaints-gateway/docs/tasks`         | `GPT UI/docs/analysis/tasks`                |
| Окно по story | `--write-build-window --story-key $storyKey` | часто `--window-flat-start` / `--gim-slice` |
| Bullrun index | `$tasksRoot/bullrun-launch-index.md`         | то же                                       |



|                | `identity` (epic-first / backlog intake)                                             |
| -------------- | ------------------------------------------------------------------------------------ |
| `$planFile`    | `.cursor/plans/ID_builder.plan.md`                                                   |
| `$tasksRoot`   | `doge-identity-service/docs/tasks`                                                   |
| `$epicFile`    | напр. `doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch.md` |
| `$storyFile`   | напр. `doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md` (`input_mode=backlog_story`) |
| `$backlogIndex`| `doge-identity-service/docs/tasks/backlog-stories/INDEX.md`                          |
| Окно по story  | `--write-build-window --story-key STORY-IDS-01-02`                                   |
| Окно весь эпик | `--write-build-window --window-flat-start 1 --window-flat-end K` (`K` из `--list`)   |
| Pipeline       | `doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md`                    |


---

## Базовый маршрут

1. **Input (`requirement` | `epic/story` | `backlog_story`) → Plan** — EPIC/STORY/tasks + pkg → `$planFile`
2. **Plan → Package** — immutable `pkg-*.yaml` + `*-active-package.current.yaml`
3. **Package → Build window** — `$verifyCmd` затем `--write-build-window …` → `$buildWindowFile`
4. **Build window → Execution** — `@$planFile` + `@$buildWindowFile`, шаг 0, Режим A
5. **Execution → Audit** → `$auditReport`
6. **Audit → Gap wave** — scaffold tasks; YAML default не ломать
7. **Gap wave → Re-audit**
8. **Finalize** — `[git-commit.md](../git-commit.md)`

---

## Предпосылка: Phase 0

В начале project-чата вставьте [session-starter.md](./session-starter.md) с `builder_project: …` и дождитесь **Onboarding summary**.

Без Phase 0 — сначала starter, затем фазы ниже.

### Skill и rule


| Механизм | Файл                                        |
| -------- | ------------------------------------------- |
| Skill    | `.cursor/skills/builder-session/SKILL.md`   |
| Rule     | `.cursor/rules/builder-operator-habits.mdc` |
| Analysis | `.cursor/rules/analysis.mdc`                |


Rule подмешивается при работе в `doge-complaints-gateway/`**, `GPT UI/`**, `doge-identity-service/**`, `spa-app/**`.

### Wave checkpoint

```text
Wave checkpoint — $storyKey (builder_project: $builderProject)
@.cursor/skills/builder-session/SKILL.md @.cursor/rules/builder-operator-habits.mdc
@$tasksRoot/*-active-package.current.yaml
@$buildWindowFile
Фаза: P3 (укажи P1|P2|P3|P4|…; P2 = только build window)
Сбрось контекст прошлой story. $verifyCmd перед execution.
```

---

## Короткие промпты (после Phase 0)

**Якорь:** `@.cursor/skills/builder-session/SKILL.md` + `@.cursor/rules/builder-operator-habits.mdc`

### P1 — Plan

## P1.1 (Epic, обязательный порядок):

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P1 Plan mode. builder_project: $builderProject.
input_mode=epic_story. @$epicFile

Нужно сделать декомпозию строго из содержимого эпика:
1) взять Stories из текста эпика (внутренние разделы Story/Acceptance Criteria) как единственный источник;
2) не придумывать новые Stories вне эпика и не менять формулировки AC;
3) для каждой Story подготовить task-папки и README по @docs/methodology/task-standard.md;
4) сформировать immutable pkg (@docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md) с корректным `epic_file` и `story_groups`;
5) синхронизировать @$tasksRoot/bullrun-launch-index.md и указатель active package.

Требование analysis.mdc: каждый claim подтверждать путём к файлу. Plan only — без execution.
В конце: таблица Story -> task -> файлы -> статус + список созданных/изменённых путей.

```

## P1.2 (Requirement, обязательный порядок):

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

1) Вход только @$requirementDoc.
2) Обязательно найти подходящий существующий эпик в @$tasksRoot/epics и bullrun-launch-index.md (по домену/scope requirement); не стартовать с произвольной story.
3) На базе requirement создать 1+ Story внутри выбранного эпика (и task-папки внутри story), без создания параллельного дублирующего эпика если текущий эпик подходит.
4) Материал requirement внедрять в Story/Task артефакты как source-of-truth: AC, scope, ограничения.
5) Обновить pkg (immutable) и индекс; pkg формировать в формате, совместимом с input-package-spec.md (`epic_story_tree` или `epic_decompose_pending` по состоянию); в отчёте явно показать mapping `requirement -> epic -> story -> tasks`.

помни про то что таски внутри стори, чтобы была понятная вложенная структура
и эпик подбери из существующих

По skill: Plan only — без execution. Все claims с путями к файлам (analysis.mdc). В конце — список созданных/изменённых путей.
```

## P1.3 (Backlog story, обязательный порядок):

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P1 Plan mode. builder_project: $builderProject (типично identity).
input_mode=backlog_story. @$storyFile
Опционально для сверки зависимостей: @$backlogIndex

1) Вход — только @$storyFile. AC, Scope, «Вне scope», «Точки в коде» брать из файла; не придумывать новые stories/AC и не менять формулировки.
2) Epic из Meta.Epic story:
   - если EPIC уже есть в @$tasksRoot/epics/ → использовать;
   - если EPIC только в backlog-stories/EPIC-*.md → materialize минимальный EPIC-IDS-NN-*.md в epics/ (следующий свободный номер после EPIC-IDS-06) + строка в bullrun-launch-index;
   - если EPIC только «в коде» (AUTH-CORE/OAUTH/EID) → создать EPIC-IDS-NN-<slug>.md по Meta + runtime-docs из «Парадигма-якорь»; не дублировать EPIC-IDS-01..06.
3) Materialize pipeline story: @$tasksRoot/epics/<EPIC>/stories/<STORY-KEY>/STORY-*.md — перенести AC/scope из backlog verbatim; decision_ref → @$storyFile + источники из Meta.
4) Глубокая декомпозиция в task-папки (@docs/methodology/task-standard.md):
   - каждый пункт Scope → 1+ atomic task (implement/fix/tests);
   - каждый AC → traceability в task AC/DoD;
   - финальный task — story acceptance-verification;
   - naming: task-ids-NN-YY-tNN-<slug>/README.md;
   - каждый README: Purpose, Code Facts (verify exists), AC/DoD, Where to change, Verification commands;
   - Skill declared: python-pro.
   Ориентир глубины: мелкая story 3–4 tasks; средняя 4–6; крупная cleanup 5–7. Запрет: один task на всю story, если Scope содержит 3+ независимых изменений в коде.
5) Immutable pkg (@docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md):
   - input_kind: epic_story_tree;
   - epic_file → materialized epic;
   - story_groups: одна группа = STORY-KEY из backlog, paths = все task README по порядку;
   - обновить identity-active-package.current.yaml (или project-specific *-active-package.current.yaml).
6) Синхронизировать @$tasksRoot/bullrun-launch-index.md (story row, task table, «Актуальная точка»).
7) Backlog-файл @$storyFile не удалять; в pipeline-story указать source: backlog-stories/…

Не смешивать в этой волне с input_mode=requirement|epic_story без явной команды оператора.
Plan only — без execution. Claims с путями (analysis.mdc).
В конце: mapping `backlog_story -> epic -> story -> tasks -> pkg paths` + список созданных/изменённых путей.
```

### P2 — Build window (`$buildWindowFile`)

Из **корня workspace** `DOGEstonia/` (не из `GPT UI/` или `doge-complaints-gateway/` — иначе Python не найдёт скрипт). После P1, когда `*-active-package.current.yaml` указывает на нужный `pkg-*.yaml`:

1. `$verifyCmd` — при `FAIL` стоп.
2. Сгенерировать окно (ровно **один** режим из таблицы):


| `$builderProject` | Команда (подставьте `$storyKey` / диапазон по `--list`)                                                                                                                                                                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gateway`         | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key $storyKey`                                                                                                                                                                  |
| `gpt`             | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --write-build-window --window-flat-start 1 --window-flat-end 5` (или `--gim-slice GIM-102,GIM-103` для среза по GIM)                                                                                             |
| `identity`        | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 5``--story-key STORY-IDS-01-02` **или** `--window-flat-start 1 --window-flat-end K` (в зависимости от active pkg и выбранного `input_mode`) |


1. В stdout после `ok build-window`: `**build_window_abs:`** / `**vscode_file_uri:`** — открыть из терминала (Cmd+click); `**quick_open_basename:`** или `**quick_open_pointer:`** (`latest-cursor-build-window.md` в `*-active-packages/`) — для **Cmd+P**; `**cursor_attach:`** — для P3. Symlink обновляется при каждой генерации. **Не** вставлять путь в Go-to-File целиком — `GPT UI/…` обрезается до `UI/docs/…`.
2. Опционально: `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project $builderProject --list` — сверить номера README с окном.

Детали флагов: [`queue-manual.md`](../cli/queue-manual.md) §2–3.

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P2 Build window only. builder_project: $builderProject.
В терминале из корня workspace: $verifyCmd; затем команда --write-build-window (см. workflow P2).
Зафиксируй $buildWindowFile из stdout (`build_window_file:` или `cursor_attach:`). Без execution тасков.
```

### P3 — Execute

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P3 Execute. builder_project: $builderProject. @$planFile + @$buildWindowFile
Ref: input_mode=requirement -> @$requirementDoc; input_mode=epic_story -> @$epicFile / @$storyFile; input_mode=backlog_story -> @$storyFile
По skill/rule: шаг 0 — $verifyCmd из корня workspace; при FAIL — стоп. Очередь YAML default (immutable pkg не переписывать). Все README из окна по порядку; bullrun-start + run-task; полные артефакты тасков. Claims из кода, не из памяти чата.
```

### P4 — Claude external (cross-audit)

Оператор вставляет в **Claude.ai / Claude Code** (не второй Cursor-чат):

```text
проведи жесткий аудит по фактическому коду отностельно исполнения $стори или req

и актуализируй каждый таск и стори в отчете

выбрать из:
doge-identity-service/docs/tasks/bullrun-launch-index.md
GPT UI/docs/analysis/tasks/bullrun-launch-index.md

мышление @.cursor/rules/analysis.mdc  

Правила: только проверяемые claims с путями; регрессии; gaps с severity + как закрыть.
Не предлагай реализацию — только findings.

по итогу отчет в анализ зоне текущего проекта (*/docs/analysis)
```

Перед **P5**: если нужен двойной аудит — выполнить P4b до scaffold.

Если gaps точечные и небольшие — оформить в project-specific builder plan подраздел
`Явно прописанный safe-override (<wave>)` (по образцу GPT), где:

- override включается только по явной метке `run_mode=...`;
- default остаётся YAML SSOT;
- список путей в override — нумерованный и проверяемый, без выдумывания.

### P5 — Plan: Gap scaffold only

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P5 Plan mode — scaffold only. builder_project: $builderProject. @$auditReport
По skill/rule: не выполняй код и pytest; не закрывай gap implementation. Gap → task-папки (@docs/methodology/task-standard.md), @$tasksRoot/bullrun-launch-index.md; YAML остаётся режимом по умолчанию для P3.

Порог P5 (override в `$planFile` vs новый pkg):
- safe-override в plan: gaps ≤ 3, README paths ≤ 5, 0 новых story folders, тот же эпик (post-audit).
- иначе: scaffold task-папок + черновик pkg + `activation: none`; отдельная P1 для обновления current.yaml.

Если порог override: добавь/обнови в `$planFile` подраздел `Явно прописанный safe-override (<wave>)` с:
1) `run_mode=<wave_name>`,
2) нумерованным списком `README.md` (каждый path — exists на диске),
3) правилом: при `run_mode` исполняется **только** этот список, без смены active pkg.
P5 checklist: уникальный run_mode; нет мёртвых run_mode без секции; gap-таблица; `activation: run_mode=…` или `activation: none`.
В конце: таблица `gap -> task -> файлы -> status`. Claims с путями к файлам.
```

### P6 — Builder после P5

Перед запуском: почистить в $planFile лишние «явно прописанные таски», оставить только свежие override.
Если в волне задан `run_mode=<wave_name>` — исполняй список из safe-override как source-of-truth (build-window из YAML не обязателен).
Если `run_mode` не задан — стандартно повторить **P2** (verify + `--write-build-window`) и работать по YAML окну.

### P7 — Claude: Re-audit

```text
правки по gap-листу выполнены
проведи подробный re-audit по закрытию каждого gap по фактическому коду
@.cursor/rules/analysis.mdc
```

### P8 — Commits

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@docs/methodology/git-commit.md

Commits для scope anchor (`REQ-XX`, `EPIC/STORY` или `STORY-IDS-*` из backlog intake — по input_mode).
feat → test → docs; не коммить: docs/tasks/**, BULLRUN, acceptance-verification, run-summary без явной команды; push не делать.

```

---

## Чек-лист перед запуском

- `*-active-package.current.yaml` → нужный `pkg-*.yaml`
- `$verifyCmd` → `ok N paths`
- `$buildWindowFile` соответствует активному pkg
- Не смешаны override-run и YAML default
- В execution: `$planFile` + `$buildWindowFile`

## Анти-ошибки

- Запуск без verify → сначала `$verifyCmd`
- Окно устарело → перегенерировать `--write-build-window`
- Override как постоянный режим → вернуть YAML default
- Claims «по памяти» → analysis.mdc

## Старт сессии

- [session-starter.md](./session-starter.md)
- [queue-manual.md](../cli/queue-manual.md)
- [input-package-spec.md](../specs/input-package-spec.md)
- [git-commit.md](../../git-commit.md)

