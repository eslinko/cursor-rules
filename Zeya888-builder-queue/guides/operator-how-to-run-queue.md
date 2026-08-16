# Как запустить очередь в оркестраторе (для человека)

**Аудитория:** вы, оператор — открыли чат OP и хотите прогнать стори/баги.  
**Процесс один** для story и bug: фазы P1.3→P8 одинаковые; отличается только список файлов в очереди.  
**Режим по умолчанию:** два субагента, без ручного copy-paste, без пауз mid-queue (overnight).

| Нужен агенту | Документ |
|--------------|----------|
| Эталон плана (шаблон, не править) | [`.cursor/plans/Orchestrator_Builder_Reference.plan.md`](../../../../.cursor/plans/Orchestrator_Builder_Reference.plan.md) |
| Эталон правил | [`orchestrator-builder-reference.md`](./orchestrator-builder-reference.md) |
| Промпт вставки | [`../prompts/operator/operator-root-subagent-run.md`](../prompts/operator/operator-root-subagent-run.md) |
| Карта фаз | [`operator-root-orchestrator.md`](./operator-root-orchestrator.md) |

---

## 1. За 30 секунд

1. Откройте **новый** Cursor-чат — это ваш **OP** (оркестратор). Не пишите в нём код продукта.
2. Скопируйте fence из [`operator-root-subagent-run.md`](../prompts/operator/operator-root-subagent-run.md).
3. Заполните две строки:
   - `$builderProject=` — ключ профиля (`landing`, `gateway`, `spa`, `identity`, `gpt`, …)
   - `$queueSpec=` — **как угодно по смыслу**, что брать в очередь (см. §3)
4. Отправьте. Дальше OP сам: прочитает профиль → соберёт очередь → **запишет новый рабочий план** `.cursor/plans/OP-<project>-<slug>.plan.md` (копия структуры эталона [Orchestrator_Builder_Reference.plan.md](../../../../.cursor/plans/Orchestrator_Builder_Reference.plan.md), с этой очередью и константами профиля, как после выбора профиля в workflow-console) → process/session/wave → поднимет **двух** субагентов → гонит очередь до конца или явного «стоп». Эталон **не** правится.
5. Вы вмешиваетесь только если: нужно остановить (`стоп` / `stop` / `pause` / `halt`), или OP спросил уточнение (пустая/двусмысленная очередь).

Push в remote **по умолчанию не делается** — коммиты локальные; push когда скажете отдельно.

---

## 2. Что происходит «под капотом» (без жаргона)

На каждую задачу из очереди оркестратор делает один и тот же конвейер:

1. **Спланировать** работу (два шага: черновик плана → применение)  
2. **Проверить очередь** CLI и вырезать build window  
3. **Сделать** код (builder)  
4. **Проверить** код (validator)  
5. Если дыры — закрыть и перепроверить  
6. **Закоммитить** локально  
7. Сразу **следующая** задача — без отчёта «можно ли продолжать?»

Два субагента живут долго: один пишет/планирует, второй только аудитит. Их id лежат в файле сессии проекта, не в `.cursor/plans`.

---

## 3. Как задать очередь (`$queueSpec`)

Пишите свободно. OP обязан превратить это в список файлов стори **по фактам с диска** (дашборд / INDEX), не выдумывая.

| Что хотите | Пример `$queueSpec` |
|------------|---------------------|
| Всё Remaining / Ready с дашборда | `remaining` или `все Remaining в дашборде` |
| Точный список | `@landing/docs/tasks/backlog-stories/bugs/STORY-LAND-BUG-19-….md` (несколько строк) или `BUG-19, BUG-18` |
| Диапазон номеров | `BUG-02..BUG-14` или `11-19` |
| По приоритету | `P0-P1 Ready` |

Story и bug — **одна очередь, один процесс**. Не нужен отдельный «режим багов».

Если уже есть готовый pkg/pipeline для задачи — OP может начать не с нуля (пропустит лишний scaffold) — это нормально, если на диске это видно.

---

## 4. Примеры готового старта

**Landing — всё Remaining:**

```text
$builderProject=landing
$queueSpec=remaining
```

(+ весь copy-paste блок из `operator-root-subagent-run.md` выше этих строк или с ними).

**Gateway — три конкретных бага:**

```text
$builderProject=gateway
$queueSpec=BUG-02, BUG-05, BUG-07
```

**Spa — только P0–P1 Ready:**

```text
$builderProject=spa
$queueSpec=P0-P1 Ready
```

---

## 5. Что вы должны увидеть на диске

После старта (пути из профиля проекта):

| Файл | Зачем вам |
|------|-----------|
| `.cursor/plans/OP-<project>-<slug>.plan.md` | Рабочий план этой волны (эталон только шаблон) |
| `{tasks}/run-reports/operator-sessions/OP-<project>.process.md` | Человекочитаемый сценарий этой волны |
| `…/OP-<project>.session.yaml` | Связка субагентов + overnight флаги |
| `…/operator-waves/wave-….md` | Живой статус очереди (DONE / BLOCKED / next) |

Не правьте `*_agent_id` руками без нужды. Не кладите id агентов в plan-файлы.

---

## 6. Когда останавливать и чего ждать

| Ситуация | Что делать |
|----------|------------|
| Всё ок, пусть работает | Ничего; не пишите «continue» после каждой стори |
| Нужен перерыв | В OP-чат: `стоп` / `stop` / `pause` / `halt` |
| Задача упёрлась в деплой / нет ассета | OP пометит BLOCKED и **пойдёт дальше** — это нормально |
| Очередь кончилась | OP даст краткий итог: сколько DONE/BLOCKED, пути файлов, напоминание про push |

Не ждите, что OP будет спрашивать approve на каждый план в overnight-режиме — он сам переходит draft → apply.

---

## 7. Два режима — не путать

| Режим | Когда | Промпт |
|-------|-------|--------|
| **Субагенты (рекомендуется)** | Хотите «задал очередь и ушёл» | [`operator-root-subagent-run.md`](../prompts/operator/operator-root-subagent-run.md) |
| **Paste MVP** | Сами копируете пакеты в чаты BLD/VAL | [`operator-root-wave.md`](../prompts/operator/operator-root-wave.md) |

Холодный OP без сессии: можно сначала [`operator-root-start.md`](../prompts/operator/operator-root-start.md) (только имя проекта), либо сразу subagent-run — он сам создаст session.yaml.

---

## 8. Частые ошибки

- Писать код или «почини баг» **в OP-чате** — оркестратор не строитель.  
- Подсовывать укороченный «сделай P3» вместо дословного fence из console/workflow — ломает дисциплину.  
- Ждать подтверждения после каждой стори в overnight — его не будет; только `стоп`.  
- Путать **Build** на fixed `*_builder.plan.md` с нормальной работой — fixed plan только через `@attach` в builder.  
- Считать BLOCKED концом волны — нет, очередь идёт дальше.

---

## 9. Куда смотреть дальше

- Правила overnight / фазы: [`orchestrator-builder-reference.md`](./orchestrator-builder-reference.md)  
- Смысл метода: [`../curriculum/00-guide-for-humans.md`](../curriculum/00-guide-for-humans.md)  
- Успешный исторический прогон landing (пример, не шаблон очереди): `landing/docs/tasks/run-reports/operator-sessions/OP-landing.process.md`
