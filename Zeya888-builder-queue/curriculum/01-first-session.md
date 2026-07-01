# Модуль 1 — Первая сессия (Phase 0)

**Operative SSOT:** [`../core/session-starter.md`](../core/session-starter.md)  
**Контекст:** [`00-guide-for-humans.md`](./00-guide-for-humans.md)

## Цель модуля

Научиться начинать работу **без изменений кода**: агент читает проект, фиксирует SSOT на диске и ждёт, какую фазу (P1, P2, P3…) выберете вы.

---

## Шаг 1 — Открыть новый чат и вставить starter

### Что происходит

Вы создаёте «чистый» контекст Cursor и передаёте агенту **контракт сессии**: какой проект (`builder_project`), где корень workspace, включён ли полный pipeline P1–P8.

### Зачем это архитектору

Phase 0 — **разведка без строительства**. Архитектор проверяет, что агент видит ту же реальность, что и вы: стек, тесты, active package, pipeline doc. Без этого любой P3 — лотерея.

### Что делает оператор

1. Копирует блок из [`session-starter.md`](../core/session-starter.md) §2.
2. Задаёт `builder_project` (`gateway` | `gpt` | `identity` | …).
3. Задаёт `workspace_root` — абсолютный путь к корню, где лежит `docs/methodology/Zeya888-builder-queue/`.
4. Оставляет `pipeline_profile: builder_full` для полного цикла (или `generic_repo` только для разведки).

### Что делает агент

Читает `profiles.yaml`, pipeline, bullrun index, active package pointer. Формирует **Onboarding summary** и строку **Ready for: P1|P2|…**. **Не меняет код.**

### Признак успеха

- В summary есть `focus_root`, команда тестов из profile, статус active pkg / verify.
- Нет правок в `src/`, конфигах, task README «заодно».

### Типичная ошибка мышления

«Сразу сделай story X» в первом сообщении — смешение P0 и P3. Сначала onboarding, потом **явный** выбор фазы.

---

## Шаг 2 — Дождаться Onboarding summary

### Что происходит

Агент синтезирует прочитанное в короткий отчёт и **останавливается**, не угадывая следующий шаг.

### Зачем это архитектору

Summary — **контракт на продолжение**. Вы видите, совпадает ли картина мира у агента с вашей, до траты токенов на plan или code.

### Что делает оператор

Читает summary. Если что-то неверно (не тот pkg, не тот index) — исправляет указания или файлы на диске, повторяет Phase 0.

### Что делает агент

Ждёт указания фазы. Не начинает P1/P3 без команды.

### Признак успеха

Блок вида:

```markdown
## Onboarding summary — gateway
...
## Ready for
P1 | P2 | … — жду указание оператора.
```

### Типичная ошибка мышления

Пропустить summary и сразу «давай P3» — агент мог не прочитать active pkg или bullrun index.

---

## Шаг 3 — Осознанно выбрать фазу

### Что происходит

Вы решаете: нужна декомпозиция (P1), только build window (P2), execution (P3), audit (P4) и т.д.

### Зачем это архитектору

Фазы разделены **по типу мышления**. P1 — design backlog; P3 — implementation; P4 — skeptic review. Autopilot «сделай всё» ломает traceability и pkg.

### Что делает оператор

Пишет одну фазу, например: «P1, input_mode=epic_story, @path/to/EPIC.md» или «P2 для story STORY-M2-14-01».

### Что делает агент

Переходит в режим выбранной фазы по [`workflow.md`](../core/workflow.md).

### Признак успеха

Одна фаза на сообщение (или явный wave checkpoint). Для identity — один `input_mode` на сессию ([`identity-operator-contract.md`](../contracts/identity-operator-contract.md) §4).

### Типичная ошибка мышления

«P1 и сразу код» — нарушение Plan only в P1. Сначала pkg и index, потом P2/P3.

---

## Шаг 4 — Не переходить к P3 без pkg и verify

### Что происходит

Execution (P3) опирается на immutable pkg и build window. Если pkg нет или verify FAIL — очередь не контрактна.

### Зачем это архитектору

Архитектор не запускает «строительство», пока нет **утверждённого плана работ** на диске (pkg + paths).

### Что делает оператор

Перед P3 убеждается: есть `*-active-package.current.yaml` → `pkg-*.yaml`, verify `ok N paths` (модуль 2).

### Что делает агент

На шаге 0 P3 снова запускает verify; при FAIL — стоп.

### Признак успеха

Вы не просите Execute, пока не прошли P1→P2 (или не осознанно используете override run_mode из plan).

### Типичная ошибка мышления

«Агент же уже видел эпик в Phase 0» — контекст чата не заменяет YAML SSOT.

---

## Шаг 5 — P3 через workflow attach, не Build на plan file

### Что происходит

Для fixed runtime plans (`Gateway_builder`, `Scripts_builder`, …) исполнение идёт через copy-paste [workflow.md](../core/workflow.md) §P3 + `@$planFile` + `@$buildWindowFile` в **текущем** project-чате.

### Зачем это архитектору

Кнопка **Build / Execute plan** на `*_builder.plan.md` открывает чат из локального registry Cursor — часто не тот, где вы ведёте проект. Новый чат ≠ Build на вкладке плана.

### Что делает оператор

1. Новый чат → Phase 0 ([шаг 1](#шаг-1--открыть-новый-чат-и-вставить-starter)).
2. P2 → build window.
3. P3 → промпт из workflow + attach plan и window. **Не** жать Build на `.cursor/plans/*_builder.plan.md`.

Подробно: [fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md).

### Признак успеха

P3 выполняется в чате с правильным `builder_project:`; старый «домашний» чат плана не переоткрывается.

### Типичная ошибка мышления

«Открою Scripts_builder.plan.md и нажму Build» — исполнение уйдёт в другой диалог.

---

## Проверка модуля

- [ ] Onboarding summary получен
- [ ] Код не менялся в Phase 0
- [ ] Вы явно назвали следующую фазу
- [ ] P3 — через workflow attach, не Build на `*_builder.plan.md`

## Дальше

[02-first-package-and-window.md](./02-first-package-and-window.md) — pkg, verify, build window.
