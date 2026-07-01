# Подключение Zeya888 Builder Queue к Cursor

## 1. Методология в workspace

Скопируйте или symlink:

```
docs/methodology/Zeya888-builder-queue/
```

## 2. Skill (рекомендуется)

Файл: [`.cursor/skills/builder-session/SKILL.md`](../../../.cursor/skills/builder-session/SKILL.md)

Триггеры: `builder_project`, `pkg-`, build window, `Gateway_builder`, `GPT_builder`, `ID_builder`.

## 3. Rule

Файл: [`.cursor/rules/builder-operator-habits.mdc`](../../../.cursor/rules/builder-operator-habits.mdc)

## 4. Builder plan (runtime)

Создайте `.cursor/plans/YourProject_builder.plan.md` по шаблону [`../templates/builder-plan-template.md`](../templates/builder-plan-template.md).

## 5. profiles.yaml

Добавьте профиль в [`../specs/profiles.yaml`](../specs/profiles.yaml) или создайте отдельный файл для своего репо (скопируйте [`../examples/sample-profiles/minimal.yaml`](../examples/sample-profiles/minimal.yaml)).

Поля — [`../specs/profiles-fields.md`](../specs/profiles-fields.md).

## 6. Старт сессии

```
@docs/methodology/Zeya888-builder-queue/core/session-starter.md

builder_project: your_project
workspace_root: /path/to/repo
pipeline_profile: builder_full
```

**Fixed builder plans:** не используйте кнопку Build на `*_builder.plan.md` — см. [fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md).

## 7. Verify path

CLI ищет корень workspace по наличию:

`docs/methodology/Zeya888-builder-queue/specs/profiles.yaml`

Если методология лежит в другом месте — обновите `_repo_root()` в `builder_resolve_queue.py` или сохраните совместимую структуру каталогов.
