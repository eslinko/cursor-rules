# Workflow (legacy): полные промпты и операторские детали

**Назначение:** архив расширенного playbook (до сжатия в [`workflow.md`](../core/workflow.md)).  
Используйте, когда нужны **полные** самодостаточные блоки P1–P7, таблица экономии токенов, детальные P3/P6 audit, gateway-специфичные примеры путей.

**Актуальный маршрут и короткие промпты:** [`workflow.md`](../core/workflow.md) + [`session-starter.md`](../core/session-starter.md).

**Пути CLI/skill обновлены** под Builder Queue (`builder_resolve_queue.py --project …`, `builder-session`). Подставьте `builder_project: gateway` или `gpt` (см. [`profiles.yaml`](../specs/profiles.yaml)).

**Execution skill:** данные в `profiles.yaml` (`execution_skill_primary`, `execution_skill_path`); логика — [builder-session/SKILL.md](../../../../.cursor/skills/builder-session/SKILL.md) §Execution skill resolution. P1.3 epic naming — [identity-operator-contract.md](../contracts/identity-operator-contract.md) §6 / [spa-operator-contract.md](../contracts/spa-operator-contract.md) §6. Не хардкодить `python-pro` в универсальных промптах — см. [`workflow.md`](../core/workflow.md) §P1.3.

---

# Workflow: Requirement → Pipeline → Audit (полная версия)

Короткий операторский playbook для ежедневной работы в Builder Queue.  
Детали реализации не дублируются: этот файл задаёт маршрут, **полные и короткие** промпты и контрольные точки.

## Переменные пайплайна

- `$builderProject` — `gateway` | `gpt` | … (ключ `--project` в CLI).
- `$verifyCmd` — `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project $builderProject --verify`
- `$requirementDoc` — файл требования (или requirement+gaps).
- `$planFile` — план в `.cursor/plans/*.plan.md` (см. `plan_file` в profiles).
- `$storyKey` — ключ story, например `STORY-M2-14-07` (gateway).
- `$buildWindowFile` — окно задач `*-cursor-build-window--$storyKey.md` (или flat/gim slice для gpt).
- `$auditReport` — внешний аудит в `docs/analysis/*.md` фокусного проекта.
- `$tasksRoot` — каталог tasks из profiles (`doge-complaints-gateway/docs/tasks` или `GPT UI/docs/analysis/tasks`).

### Пример подстановок (gateway)

| Переменная | Значение |
|------------|----------|
| `$builderProject` | `gateway` |
| `$planFile` | `@.cursor/plans/Gateway_builder.plan.md` |
| `$buildWindowFile` | `doge-complaints-gateway/docs/tasks/run-reports/gateway-build-windows/gateway-cursor-build-window--$storyKey.md` |
| `$auditReport` | `doge-complaints-gateway/docs/analysis/*.md` |

### Пример подстановок (gpt)

| Переменная | Значение |
|------------|----------|
| `$builderProject` | `gpt` |
| `$planFile` | `@.cursor/plans/GPT_builder.plan.md` |
| `$buildWindowFile` | `GPT UI/docs/analysis/tasks/run-reports/gpt-build-windows/gpt-cursor-build-window--….md` |
| `$auditReport` | `GPT UI/docs/analysis/*.md` |

---

## Базовый маршрут

1. **Requirement → Plan**
   - Цель: декомпозировать requirement в EPIC/STORY/tasks + pkg.
   - Артефакт: `$planFile`.
2. **Plan → Package**
   - Цель: создать immutable `pkg-*.yaml` и обновить `*-active-package.current.yaml`.
   - Артефакт: `{tasksRoot}/*-active-packages/pkg-*.yaml`.
3. **Package → Build window**
   - Цель: получить окно задач на одну story / срез.
   - Команда (gateway):  
     `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key $storyKey`
   - Артефакт: `$buildWindowFile`.
4. **Build window → Execution**
   - Цель: выполнить все README из окна строго по порядку.
   - Контекст: `@$planFile` + `@$buildWindowFile`.
5. **Execution → External audit**
   - Цель: получить факт-аудит и возможные gap.
   - Артефакт: `$auditReport`.
6. **Audit → Gap wave**
   - Цель: создать gap tasks внутри существующей STORY + индекс + override-run (без поломки YAML default).
   - Артефакты: обновленные STORY/task folders, `bullrun-launch-index.md`, `$planFile`.
7. **Gap wave → Re-audit**
   - Цель: подтвердить закрытие gap по фактическому коду и AC.
   - Артефакт: обновленный/новый отчет в `docs/analysis`.
8. **Finalize**
   - Цель: коммиты по правилам группировки/фильтрации.
   - Артефакт: серия commit-ов без лишних служебных файлов.

---

## Предпосылка: Phase 0 уже выполнен

В начале **project-чата** один раз вставьте [session-starter.md](../core/session-starter.md) (§2) с `builder_project: …` и дождитесь **Onboarding summary**.

Дальше в **этом же чате** используйте промпты ниже. Полный AGENT CONTRACT и инварианты агенту повторять не нужно — они уже в контексте starter + skill/rule.

### Экономия токенов — вы правы, с оговорками

| Что экономит токены | Почему |
|---------------------|--------|
| Phase 0 один раз на project-чат | Не перечитывать весь `src/` и индекс на каждой фазе |
| **Короткие промпты** (§ ниже) вместо полных | Не дублируете analysis, task-standard, списки шагов — skill/rule уже напоминают |
| `@` только 1–3 файла на фазу | Меньше вложений в контекст, чем `@bullrun` целиком |
| **Wave checkpoint** на границе story | 5–8 строк вместо повторного Phase 0 |
| SSOT на диске (`pkg`, README, req) | Агент читает актуальное с диска, а не «помнит» из старых сообщений |

**Оговорки:** токены всё равно тратятся на **чтение кода** и **артефакты тасков** при P2 — это нормально. Короткий промпт не отменяет `@$buildWindowFile` и тесты проекта. Если ответы «плывут» или смешивают story — сделайте wave checkpoint или новый чат.

### Skill и rule — как подключать через промпты

Работают **вместе** с ручным workflow; фазы P1–P7 по-прежнему **запускаете вы**.

| Механизм | Файл | Как включить в чат |
|----------|------|-------------------|
| **Skill** | `.cursor/skills/builder-session/SKILL.md` | Триггер: `pkg-`, `build window`, `builder_project`, `REQ-`, `bullrun` — или явно `@.cursor/skills/builder-session/SKILL.md` |
| **Rule** | `.cursor/rules/builder-operator-habits.mdc` | Работа в `doge-complaints-gateway/**`, `GPT UI/**`, `spa-app/**` **или** `@.cursor/rules/builder-operator-habits.mdc` |
| **Analysis** | `.cursor/rules/analysis.mdc` | В P1/P4 — явный `@`; в P2/P5/P7 — через skill/rule + факты из файлов |

**Rule** (`alwaysApply: false`, globs по проектам) подмешивается при работе в соответствующей папке. **Skill** — по триггерам или `@` в промпте. Короткие промпты ниже уже включают `@` skill + rule; повторять только если агент сбился.

### Wave checkpoint (новая story в том же project-чате)

Не обязательно новый чат. Перед P1/P2/P4 вставьте (подставьте `$storyKey`, `$builderProject`, пути):

```text
Wave checkpoint — $storyKey (builder_project: $builderProject)
@.cursor/skills/builder-session/SKILL.md @.cursor/rules/builder-operator-habits.mdc
@$tasksRoot/*-active-package.current.yaml
@$buildWindowFile
Фаза: P2 (укажи P1|P2|P4|…)
Сбрось контекст прошлой story/override. $verifyCmd из корня workspace перед execution.
```

---

## Готовые промпты — полные (без starter; self-contained)

Используйте, если **не** делали Phase 0 или нужен самодостаточный блок в новом чате.  
Для gateway в примерах ниже подставьте пути `doge-complaints-gateway/…`; для gpt — из [`profiles.yaml`](../specs/profiles.yaml).

Короткие operative промпты PA/P1–P8: [`workflow.md`](./workflow.md).

---

## PA — Intake Analysis (полные промпты)

**Когда:** сырой или неполный intake-файл; **до** P1. **Не** создавать pkg, task README, pipeline story. **Выход:** `$intakeArtifact` на диске → handoff в P1.1 / P1.2 / P1.3.

**Skip:** файл уже canonical (метаданные, verified state, AC — как соседи в `$etalonDir`).

### PA.2-full — Requirement shaping (self-contained)

Типичный кейс: GPT `REQ-42` → canonical requirement → P1.2.

```text
@.cursor/rules/analysis.mdc

PA Intake Analysis — requirement shaping. builder_project: gpt
@GPT UI/docs/requirements/REQ-42.md

Эталон стиля: папка GPT UI/docs/requirements/ — ориентир REQ-40, REQ-41 (метаданные, §1 verified state, §2 целевое, AC, dependencies).

Задача: довести @$intakeDraft до Builder-ready requirement ($intakeArtifact = тот же файл на диске после записи).

Правила:
- Analysis / shaping only — без pkg, без bullrun, без task README, без P3.
- @.cursor/rules/analysis.mdc — каждый claim о коде/instructions с path; без assumptions.
- Интерактивное интервью на КАЖДОМ decision point (scope, boundaries, AC, dependencies, verified current state).
- Язык: человечески, с расшифровкой терминов.
- Протокол Other: если оператор в «Other» задаёт встречный вопрос — сначала полный ответ, затем повтор исходного вопроса или адаптация к обновлённому контексту.
- Не переходить к декомпозиции в tasks — это P1.2.

Шаги:
1) Прочитать REQ-42 и 2 эталонных REQ из той же папки — таблица «чего не хватает» (метаданные, verified §, AC структура, парные REQ).
2) Для секций verified state — grep/read instructions и код; только facts с paths.
3) Интервью по gaps в документе; фиксировать решения оператора в тексте requirement.
4) Записать обновлённый файл на диск.
5) Handoff: «PA.2 завершён. P1.2 input_mode=requirement. @GPT UI/docs/requirements/REQ-42.md»
```

### PA.1-full — Epic shaping (self-contained)

```text
@.cursor/rules/analysis.mdc

PA Intake Analysis — epic shaping. builder_project: $builderProject
@$intakeDraft
Эталон: $tasksRoot/epics/ — 1–2 соседних EPIC-*.md

Довести epic до canonical (Goal, Stories, AC, out of scope, метаданные) для P1.1.
Analysis only — без pkg, без tasks, без P3.
Интерактивное интервью + Other-протокол (см. PA.2-full).
Verified claims — paths (analysis.mdc).
Записать @$intakeArtifact (= @$epicFile).
Handoff: «PA.1 → P1.1 epic_story. @$epicFile»
```

### PA.3-full — Backlog story shaping (self-contained)

```text
@.cursor/rules/analysis.mdc

PA Intake Analysis — backlog story. builder_project: identity
@$intakeDraft
Эталон: doge-identity-service/docs/tasks/backlog-stories/ + опционально INDEX.md

Довести story до canonical (Meta, Scope, AC, «Точки в коде», «Вне scope») для P1.3.
Analysis only — без pipeline story, без pkg, без P3.
Gap-to-code для «Точки в коде» — paths из grep/read.
Интерактивное интервью + Other-протокол (см. PA.2-full).
Записать @$intakeArtifact (= @$storyFile).
Handoff: «PA.3 → P1.3 backlog_story. @$storyFile»
```

---

### P1 — Plan mode: декомпозиция requirement

Использовать, когда стартуем новую wave.

```text
@$requirementDoc новое требование.
Собери (из идентифицированных гапов) план внедрения в task-pipeline:
1) найти (из bullrun индексатора) подходящий EPIC и создать STORY и task-папки по @docs/methodology/task-standard.md;
2) подключить новый пакет работы в @$planFile и сбросить там completed->pending в todos;
3) добавить STORY/Tasks/пакет в @$tasksRoot/bullrun-launch-index.md;
4) создать новый immutable YAML-пакет по @docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md
   (ориентируйся на последний pkg-*.yaml как пример).

Работай строго методом @.cursor/rules/analysis.mdc:
- никаких предположений;
- все claim только с подтверждением в файлах;
- в конце дай список созданных/изменённых путей.
```

### P1-short — Plan: декомпозиция requirement

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P1 Plan mode. builder_project: $builderProject. @$requirementDoc
Декомпозиция в task-pipeline: EPIC/STORY/tasks (@docs/methodology/task-standard.md), immutable pkg (@docs/methodology/Zeya888-builder-queue/specs/input-package-spec.md), @$planFile, @$tasksRoot/bullrun-launch-index.md.
По skill: Plan only — без execution. Все claims с путями к файлам (analysis.mdc). В конце — список созданных/изменённых путей.
```

### P2 — Execute mode: выполнение через build-window

Использовать, когда plan уже утвержден и есть `$buildWindowFile`.

```text
@$planFile выполняй план полностью запуская процесс с контекстным окном @$buildWindowFile
исходное требование (для состыковочного референса) — gaps в документе @$requirementDoc
используй описание процесса работы над каждым таском из плана и выполняй строго по таскам с полной отчетной документацией как все указано в процессах
```

### P2-short — Execute: build window

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P2 Execute. builder_project: $builderProject. @$planFile + @$buildWindowFile
Ref: @$requirementDoc
По skill/rule: шаг 0 — $verifyCmd из корня workspace; при FAIL — стоп. Очередь YAML default (immutable pkg не переписывать). Все README из окна по порядку; bullrun-start + run-task; полные артефакты тасков. Claims из кода, не из памяти чата.
```

### P2-minimal — Build (только исполнение)

```text
Контекст: @$planFile и @$buildWindowFile.

builder_project: $builderProject.
Выполни **весь** план: $verifyCmd, затем **Режим A** — подряд все README из окна (порядок только из окна), `bullrun-start` + фазы `run-task`, без остановок между README и без вопроса «продолжить?». Режим B не включать, пока план не отпускает.

@.cursor/rules/analysis.mdc: не выдумывай пути; при ошибке шага 0 — стоп.

После последнего README в окне — Story parent AC по pipeline эпика; не пропускай gate.
```

### P3 — Claude audit: факт-аудит после выполнения

Использовать после завершения wave.

```text
выполнила работу по @$requirementDoc
проведи фактический аудит кода на соответствие требованиям и критериям приемки
проверь не появилось ли регрессий
сделай подробный итоговый отчет в {focus_project}/docs/analysis
если есть гапы, четко пропиши каждый гап и как его закрыть
для каждого гапа укажи индикаторы сложности и важности
мышление @.cursor/rules/analysis.mdc
```

По итогу получаем отчет: `$auditReport`

### P4 — Plan mode: обработка gap-ов из внешнего аудита

Использовать, когда в `$auditReport` есть незакрытые gap.

```text
@$auditReport изучи внешний аудит.
На базе найденных gap:
1) создай task-папки внутри существующей STORY по @docs/methodology/task-standard.md;
2) добавь задачи в @$tasksRoot/bullrun-launch-index.md;
3) добавь их в @$planFile как явно прописанный override-run,
   но не ломай YAML SSOT-режим (YAML должен оставаться режимом по умолчанию).

Метод: @.cursor/rules/analysis.mdc
В конце: таблица "gap -> task -> файлы -> статус".

P.S. Не выполняй план! только создаешь!
```

### P4-short — Plan: gap scaffolding only

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@.cursor/rules/analysis.mdc

P4 Plan mode — scaffold only. builder_project: $builderProject. @$auditReport
По skill/rule: не выполняй код и pytest; не закрывай gap implementation. Gap → task-папки (@docs/methodology/task-standard.md), @$tasksRoot/bullrun-launch-index.md, override-run в @$planFile; YAML остаётся режимом по умолчанию.
В конце: таблица gap -> task -> файлы -> статус. Claims с путями к файлам.
```

### P5 — Запустить Builder (после P4)

Перед запуском: почистить в `$planFile` лишние «явно прописанные таски», оставить только свежие override.

```text
P5: запусти Builder по @$planFile
builder_project: $builderProject
Контекст: @$buildWindowFile, ref @$requirementDoc
Почисти в плане устаревшие override; активная очередь — YAML default, если оператор не указал run_mode=…
```

### P5-short — Builder (после P4)

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P5 Execute override-wave. builder_project: $builderProject. @$planFile + @$buildWindowFile
Ref: @$requirementDoc
По skill/rule: $verifyCmd перед стартом; run_mode=… только если я указала явно в этом сообщении; убери в плане устаревшие override. Далее как P2 — README по порядку, bullrun-start + run-task.
```

### P6 — Claude audit: факт-аудит после gap wave

Использовать после завершения gap wave.

```text
правки выполнены
проведи подробный аудит по найденным гапам по фактическому коду
@.cursor/rules/analysis.mdc
```

По итогу получаем новый отчет: `$auditReport`

### P7 — Коммиты

После отработки циклами всех гапов и когда audit даст «зелёный свет», запускаем коммиты.

```text
выполни теперь по $reqX план коммитов по @docs/methodology/git-commit.md 
можешь коммитить, только не коммить лишнее, внимательно изучи файлы методологии коммитов!!!
пуш не делаешь
```

### P7-short — Коммиты

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc
@docs/methodology/git-commit.md

P7 Commits для scope REQ-XX (подставь номер, напр. REQ-24).
По skill/rule и git-commit.md: группы feat → test → docs; не коммить docs/tasks/**, BULLRUN, acceptance-verification, run-summary без моей явной команды; push не делать.
```

---

## Готовые промпты — короткие (после Phase 0 + skill/rule)

**Предпосылка:** в чате уже был [session-starter.md](../core/session-starter.md).

**Якорь (в каждом коротком промпте):** `@.cursor/skills/builder-session/SKILL.md` + `@.cursor/rules/builder-operator-habits.mdc` — verify, YAML SSOT, режимы фаз.

**P3 и P6 (audit)** — полные блоки в §«Готовые промпты — полные» выше (или кратко P3/P6 в [`workflow.md`](../core/workflow.md)).

---

## Чек-лист перед запуском

- [ ] `*-active-package.current.yaml` указывает на нужный `pkg-*.yaml`.
- [ ] `$verifyCmd` возвращает `ok N paths`.
- [ ] `$buildWindowFile` соответствует нужному `$storyKey` / срезу.
- [ ] В запуске не смешан override-run и обычный YAML режим.
- [ ] В контексте execution есть и `$planFile`, и `$buildWindowFile`.
- [ ] Ожидаемый формат финального отчета зафиксирован заранее (таблица gap->task->files->status).

## Анти-ошибки

- **Ошибка:** Запуск без verify.  
  **Действие:** сначала `$verifyCmd`, потом execution.
- **Ошибка:** Окно не совпадает с активным pkg.  
  **Действие:** перегенерировать `$buildWindowFile` из текущего pkg.
- **Ошибка:** Override-run используется как постоянный режим.  
  **Действие:** вернуть YAML default и оставить override только для точечной mini-wave.
- **Ошибка:** Коммитятся task-артефакты без явной команды.  
  **Действие:** фильтровать по `docs/methodology/git-commit.md`.
- **Ошибка:** Формулировки «по памяти».  
  **Действие:** проверять claims по файлам через `analysis.mdc`.

## Старт чистой сессии

- [`session-starter.md`](../core/session-starter.md) — onboarding + AGENT CONTRACT; propagation через skill/rule.

## Подробности смотри в

- [`queue-manual.md`](../cli/queue-manual.md)
- [`input-package-spec.md`](../specs/input-package-spec.md)
- [`profiles.yaml`](../specs/profiles.yaml)
- [`git-commit.md`](../git-commit.md)
- [`analysis.mdc`](../../../.cursor/rules/analysis.mdc)
