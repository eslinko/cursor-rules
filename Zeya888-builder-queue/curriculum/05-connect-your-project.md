# Модуль 5 — Подключить свой проект

**Operative SSOT:** [`../integration/cursor-setup.md`](../integration/cursor-setup.md)  
**Контекст:** [`00-guide-for-humans.md`](./00-guide-for-humans.md)

Метод переносится в **ваш** репозиторий без привязки к DOGEstonia — архитектор настраивает три опоры: Method layer, Tool layer, Runtime layer.

---

## Шаг 1 — Скопировать методологию

### Что происходит

В workspace появляется каталог `docs/methodology/Zeya888-builder-queue/` (или symlink на отдельный clone [`docs/methodology`](../../) git).

### Зачем архитектору

Method layer (workflow, curriculum, contracts templates) **версионируется отдельно** от продуктового кода — можно учить команду и обновлять процесс без merge в `src/`.

### Признак успеха

CLI находит корень:

`docs/methodology/Zeya888-builder-queue/specs/profiles.yaml`

**Operative:** [`cursor-setup.md`](../integration/cursor-setup.md) §1.

---

## Шаг 2 — Cursor skill и rule

### Что происходит

Подключаются [`.cursor/skills/builder-session/SKILL.md`](../../../.cursor/skills/builder-session/SKILL.md) и [`.cursor/rules/builder-operator-habits.mdc`](../../../.cursor/rules/builder-operator-habits.mdc) — триггеры `builder_project`, pkg, verify.

### Зачем архитектору

Skill/rule — **автоматическое напоминание** дисциплины без копирования длинного starter каждый раз (starter всё равно нужен для Phase 0 нового чата).

### Типичная ошибка

Только skill без profiles — агент не знает `tasks_dir` и `plan_file`.

**Operative:** cursor-setup §2–3.

---

## Шаг 3 — Профиль в `profiles.yaml`

### Что происходит

Добавляется блок `projects.your_key` с путями: `focus_folder`, `tasks_dir`, `active_packages_dir`, `current_pointer`, `plan_file`, `test_command`, …

### Зачем архитектору

Profile — **карта репозитория** для CLI и Phase 0. Архитектор один раз проектирует layout task tree и build windows.

### Учебный пример без production

[`../examples/sample-profiles/minimal.yaml`](../examples/sample-profiles/minimal.yaml) — профиль `demo` с `enabled: false`; скопируйте структуру, подставьте свои пути.

Поля: [`profiles-fields.md`](../specs/profiles-fields.md).

### Checklist нового профиля

**SSOT:** [`../guides/add-builder-profile.md`](../guides/add-builder-profile.md) §0 Intake + §1 Checklist + §3 Operative prompt.

Учебный пример без production: [`../examples/sample-profiles/minimal.yaml`](../examples/sample-profiles/minimal.yaml).

---

## Шаг 4 — Runtime builder plan

### Что происходит

Operative plan живёт в **`.cursor/plans/*_builder.plan.md`** — attach для P3/P6.

Reference copies в [`../examples/reference-plans/`](../examples/reference-plans/) — **только обучение**, не runtime. Drift возможен; SSOT execution — `.cursor/plans/`.

### Зачем архитектору

Plan — **как исполнять** (шаг 0, bullrun, run_mode overrides). P1 промпты **не** дублировать в plan — они в [`workflow.md`](../core/workflow.md).

### Типичная ошибка

Attach reference plan из examples для P3 — устаревшие paths/commands.

**Operative:** [`reference-plans/README.md`](../examples/reference-plans/README.md).

---

## Шаг 5 — Первая волна на своём репо

### Что происходит

1. P0 — session starter, ваш `builder_project`.  
2. P1 — один вход (epic / requirement / backlog).  
3. P2 — verify + build window.  
4. P3 — plan + window.

### Зачем архитектору

Проверка, что **ваши** paths в pkg, index и profiles согласованы — метод «прижился» к репо.

### Solo builder tip

Даже один человек ведёт bullrun index как «доску статусов» — иначе через неделю вы сами не вспомните, какая story следующая.

---

## Шаг 3 vs Runtime — таблица

| Вопрос | Method | Runtime |
|--------|--------|---------|
| Где учиться? | `curriculum/`, `core/workflow.md` | — |
| Где промпты P1–P8? | `core/workflow.md` | — |
| Где очередь work? | spec | `pkg-*.yaml` в проекте |
| Где execution attach? | — | `.cursor/plans/` + build window |
| Где учебный пример plan? | `examples/reference-plans/` | не использовать в P3 |

---

## Дальше

Вы прошли human-layer curriculum 0–5. Для production держите под рукой:

- [`../core/workflow.md`](../core/workflow.md)  
- [`../cli/queue-manual.md`](../cli/queue-manual.md)  
- Contract вашего `builder_project` в [`../contracts/`](../contracts/)

Версия метода: [`../VERSION`](../VERSION), изменения: [`../CHANGELOG.md`](../CHANGELOG.md).
