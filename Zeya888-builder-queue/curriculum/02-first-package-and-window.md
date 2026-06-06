# Модуль 2 — Package и build window

**Operative SSOT:** [`../specs/input-package-spec.md`](../specs/input-package-spec.md), [`../cli/queue-manual.md`](../cli/queue-manual.md)  
**Контекст:** [`00-guide-for-humans.md`](./00-guide-for-humans.md)

## Цель модуля

Понять цепочку **pkg → verify → build window** — три опоры между «планом на диске» и «одной сессией Cursor».

---

## Шаг 1 — Прочитать контракт input package

### Что происходит

Вы знакомитесь с форматом `pkg-*.yaml`: `input_kind`, `story_groups`, paths к task README, указатель `*-active-package.current.yaml`.

### Зачем это архитектору

Pkg — **immutable договор очереди**. Архитектор в P1 проектирует, *что* входит в волну и в каком порядке. Без spec агент и человек по-разному понимают «нормализацию».

### Что делает оператор

Читает [`input-package-spec.md`](../specs/input-package-spec.md) §1–§4 (назначение, файлы по профилю, meta-поля, `input_kind`).

### Что делает агент

(На этом шаге агент не обязателен — это ваше чтение.)

### Признак успеха

Вы можете объяснить: pkg хранит **paths**, index хранит **статусы**, plan хранит **как исполнять**.

### Типичная ошибка мышления

Думать, что JSON в builder plan — очередь. Очередь SSOT — YAML pkg ([`input-package-spec.md`](../specs/input-package-spec.md) §1).

---

## Шаг 2 — Запустить verify

### Что происходит

CLI читает `profiles.yaml` → active pointer → `pkg-*.yaml` → список paths → проверяет `exists` на диске.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```

### Зачем это архитектору

Verify — **диспетчерский сигнал**. Красный = контракт сломан (опечатка path, удалён task, рассинхрон pkg и дерева). Исправлять контракт, не «убеждать» агента.

### Что делает оператор

Запускает команду из **корня workspace** (не из подпапки проекта).

### Что делает агент

На P3/P6 шаг 0 — та же команда; FAIL = стоп ([`builder-operator-habits`](../../../.cursor/rules/builder-operator-habits.mdc)).

### Признак успеха

Stdout: `ok N paths (project=…, pkg …)`.

### Типичная ошибка мышления

Игнорировать FAIL и идти в P3 — агент начнёт с несуществующих README.

---

## Шаг 3 — Сгенерировать build window

### Что происходит

CLI берёт активный pkg и **вырезает slice** — одну story, flat диапазон или gim-slice — в markdown-файл в `run-reports/*-build-windows/`.

Пример (gateway):

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway \
  --write-build-window --story-key STORY-M2-14-01
```

### Зачем это архитектору

Build window — **граница контекста** одного чата. Архитектор выбирает slice (P2), не перегружая агента всем эпиком. Окно **производное**: после смены pkg перегенерировать.

### Что делает оператор

Выбирает режим slice по профилю ([`queue-manual.md`](../cli/queue-manual.md) §3): `--story-key`, `--window-flat-start/end`, `--gim-slice` (gpt).

### Что делает агент

В P2 только генерирует/фиксирует `$buildWindowFile` из stdout; в P3 attach plan + window.

### Признак успеха

Файл окна создан; в stdout есть `build_window_abs:`, `cursor_attach:`, часто symlink `latest-cursor-build-window.md` в `*-active-packages/`.

### Типичная ошибка мышления

Редактировать окно руками как SSOT — правильный путь: поправить pkg → verify → `--write-build-window` заново.

---

## Шаг 4 — Открыть окно в Cursor

### Что происходит

Вы attach файл окна в чат P3 вместе с `.cursor/plans/*_builder.plan.md`. Symlink и `quick_open_pointer` упрощают Cmd+P (см. [`queue-manual.md`](../cli/queue-manual.md) troubleshooting).

### Зачем это архитектору

Явный attach — **намеренная граница work**. Архитектор видит, по каким README идёт execution, без импlicit «вспомни прошлую story».

### Что делает оператор

Cmd+click `build_window_abs:` или Cmd+P → `latest-cursor-build-window`; копирует `cursor_attach:` в чат.

### Что делает агент

Идёт по README из окна по порядку; шаг 0 verify.

### Признак успеха

В P3 в контексте два якоря: operative plan + build window.

### Типичная ошибка мышления

Вставить полный путь с пробелами (`GPT UI/…`) в Go-to-File — IDE обрезает; использовать symlink/pointer из stdout.

---

## Ошибки (кратко)

| Симптом | Действие |
|---------|----------|
| FAIL verify | Исправить paths в pkg YAML |
| story_key not found | Точное совпадение ключа в pkg |
| IDE не находит окно | Symlink в `*-active-packages/` или `cursor_attach:` |

## Дальше

[`03-workflow-phases-explained.md`](./03-workflow-phases-explained.md) — полный цикл P0–P8 для человека.  
Operative: [`../core/workflow.md`](../core/workflow.md) §P2, §P3.
