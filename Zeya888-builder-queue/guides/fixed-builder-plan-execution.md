# Fixed builder plans — исполнение без привязки к чату Cursor

> **SSOT:** как запускать `*_builder.plan.md` в **новом** project-чате без кнопки **Build / Execute plan**.  
> **Связано:** [session-starter.md](../core/session-starter.md) · [workflow.md](../core/workflow.md) §P3/P6 · [profiles.yaml](../specs/profiles.yaml) `plan_file`

---

## 1. Почему Build открывает «чужой» чат

Cursor хранит метаданные плана **не в** `.plan.md`, а в **локальном registry** на машине ([forum, Cursor staff](https://forum.cursor.com/t/plans-corrupt-when-save-it-to-your-repo-breaking-build-button-from-working/149598)):

> When you create a plan, Cursor stores metadata in a local registry, not in the `.plan.md` file itself.

При **Build / Execute plan** Cursor:

1. Находит план в registry → **conversation ID**, где план создавали или последний раз Build-или.
2. **Продолжает или переоткрывает** этот диалог — даже если вкладка была закрыта и другой чат активен.

**Следствия для Zeya888:**

| Факт | Вывод |
|------|--------|
| `profiles.yaml` → `plan_file` | Путь к **markdown SSOT**, не маршрутизация чата |
| `isProject: false` в frontmatter | **Не** отключает registry |
| Git-коммит `*_builder.plan.md` | **Не** переносит registry на другой чат/ПК |
| Правка плана агентом в чужом чате | Может **укрепить** привязку registry к этому чату |

Полностью «отвязать» план от диалога **из репозитория нельзя** — это ограничение продукта Cursor.

---

## 2. Два типа `.plan.md`

| Тип | Имена | Назначение | Как исполнять |
|-----|-------|------------|---------------|
| **Fixed runtime** | `Gateway_builder`, `GPT_builder`, `ID_builder`, `Spa_builder`, `Scripts_builder`… | Постоянный SSOT P3/P6 для `builder_project` | **Только @attach** + промпт из [workflow.md](../core/workflow.md); **не** Build на файле |
| **Ephemeral wave** | `p1_*_scaffold_*.plan.md`, `p5_*_gap_*.plan.md` (hash-suffix) | Одноразовая P1/P5 волна | Plan mode + Build **в том же project-чате**, где создавали план |

Fixed plans — **документация процесса** и attach-якорь, не объект Plan UI registry.

---

## 3. Запрет для fixed plans

**Не нажимать** **Build** / **Execute plan** на файлах:

- `.cursor/plans/Gateway_builder.plan.md`
- `.cursor/plans/GPT_builder.plan.md`
- `.cursor/plans/ID_builder.plan.md`
- `.cursor/plans/Spa_builder.plan.md`
- `.cursor/plans/Scripts_builder.plan.md`
- …любой `*_builder.plan.md` из `profiles.yaml` → `plan_file`

Frontmatter `todos` в fixed plans — **напоминания процесса** для людей и агентов при @attach; они **не** означают «жми Build в Plan UI».

---

## 4. Канонический поток (новый project-чат)

### Шаг A — Phase 0

Новый чат, один `builder_project` на сессию:

```text
@docs/methodology/Zeya888-builder-queue/core/session-starter.md

builder_project: scripts
workspace_root: /Users/eslinko/Development/DOGEstonia
pipeline_profile: builder_full

Выполни Phase 0 (onboarding) по AGENT CONTRACT ниже. Не меняй код.
После Onboarding summary — жди фазу (PA | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8).
```

Подставьте `gateway` | `gpt` | `identity` | `spa` | `scripts` по проекту.

### Шаг B — P2 (build window)

Copy-paste из [workflow.md](../core/workflow.md) §P2: verify + `--write-build-window`.

### Шаг C — P3 Execute

Copy-paste из [workflow.md](../core/workflow.md) §P3 + attach:

```text
@.cursor/skills/builder-session/SKILL.md
@.cursor/rules/builder-operator-habits.mdc

P3 Execute. builder_project: scripts.
@.cursor/plans/Scripts_builder.plan.md
@scripts/docs/tasks/run-reports/scripts-build-windows/<window>.md
```

`$planFile` — из [profiles.yaml](../specs/profiles.yaml) для вашего `builder_project`.

### Шаг D — P6 (audit override, safe-override)

Copy-paste из [workflow.md](../core/workflow.md) §**P6 — Execute (safe-override, `run_mode=<wave_name>`)** в **текущем** project-чате — **не** Build на файле плана.

Минимум в сообщении: `run_mode=<wave_name>` · `builder_project:` · `@$planFile` · `@<first README из §safe-override>` · строка «P6 Execute — gap closure only; … pkg unchanged».

---

## 5. Ephemeral plans (P1 / P5)

- Создавать и Build-ить **только** в **том project-чате**, где идёт волна.
- **Не** создавать и **не** выравнивать fixed `*_builder.plan.md` через Plan mode в чужом проекте (например identity-чат для `Scripts_builder.plan.md`).
- После закрытия волны ephemeral plan можно архивировать; fixed plan на диске не меняется без запроса оператора.

---

## 6. Опционально: Build in New Agent (не канон Zeya888)

Только для **ephemeral** plans, если нужен Plan UI:

- Открыть план в **dynamic plan view** (не raw markdown).
- Отметить **чекбокс** справа у нужных todos.
- Кнопка **Build in New Agent** в header ([forum](https://forum.cursor.com/t/plan-mode-was-build-using-a-new-agent-removed/161151)).

В Agents Window кнопка может отсутствовать. Для fixed `*_builder.plan.md` этот путь **не** рекомендуется.

---

## 7. Troubleshooting

| Симптом | Действие |
|---------|----------|
| Build открыл старый/закрытый чат | Закрыть; в **нужном** project-чате исполнять через §4 (P3 attach) |
| Build на fixed plan ничего не делает | Ожидаемо на другой ПК / после git clone — registry пуст; используйте §4 |
| Путаются scripts и identity | Новый чат + явный `builder_project:`; не Build на plan file |
| Нужен «чистый» контекст | Новый чат + Phase 0 + build window slice ([curriculum/00-guide-for-humans.md](../curriculum/00-guide-for-humans.md)) |

---

## 8. Ссылки

| Документ | Роль |
|----------|------|
| [session-starter.md](../core/session-starter.md) | Старт нового чата |
| [workflow.md](../core/workflow.md) | Промпты P2/P3/P6 |
| [builder-operator-habits.mdc](../../../.cursor/rules/builder-operator-habits.mdc) | Правило 12 |
| [builder-plan-template.md](../templates/builder-plan-template.md) | Каркас §Build для новых fixed plans |
