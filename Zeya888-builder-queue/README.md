# Zeya888 Builder Queue

Авторская методология **Zeya888** для управляемой разработки с AI-агентом в Cursor: машиночитаемая очередь (`pkg-*.yaml`), фазы P0–P8, build windows и operator contracts.

**Бренд:** Zeya888 · **Версия:** см. [`VERSION`](./VERSION) · **Карта методологии:** [`MANIFEST.md`](./MANIFEST.md)

## Быстрый старт

1. Установите Cursor integration — [`integration/cursor-setup.md`](./integration/cursor-setup.md)
2. Настройте профиль проекта — [`specs/profiles.yaml`](./specs/profiles.yaml)
3. Новый чат: `@docs/methodology/Zeya888-builder-queue/core/session-starter.md` + `builder_project: …`
4. Verify: `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify`

## Структура

| Каталог | Назначение |
|---------|------------|
| [`core/`](./core/) | Workflow P1–P8, session starter, legacy prompts |
| [`cli/`](./cli/) | `builder_resolve_queue.py`, queue manual |
| [`specs/`](./specs/) | Контракт input package, `profiles.yaml` |
| [`contracts/`](./contracts/) | Operator contracts (gateway, gpt, identity) |
| [`templates/`](./templates/) | Шаблон builder plan |
| [`examples/`](./examples/) | Reference plans (обучение) + sample profiles |
| [`curriculum/`](./curriculum/) | Учебный маршрут |
| [`integration/`](./integration/) | Подключение к Cursor |
| [`analysis/`](./analysis/) | Сверка и unification analysis |

## Runtime vs обучение

| Слой | SSOT | Назначение |
|------|------|------------|
| Метод | `core/workflow.md`, contracts | Промпты и правила оператора |
| CLI | `cli/builder_resolve_queue.py` | Verify, list, build window |
| Проект | `.cursor/plans/*_builder.plan.md` | Operative execution (P3/P6) |
| Примеры | `examples/reference-plans/` | Снимки для курса — **не** attach для P3 |

**Cursor:** [`.cursor/skills/builder-session/SKILL.md`](../../.cursor/skills/builder-session/SKILL.md), [`.cursor/rules/builder-operator-habits.mdc`](../../.cursor/rules/builder-operator-habits.mdc).

## Профили (DOGEstonia)

| `--project` | Статус |
|-------------|--------|
| `gateway` | активен |
| `gpt` | активен |
| `identity` | активен |
| `spa` | активен |
| `taxonomy` | активен (**queueless** — только `--verify`; meta-script TC0–TC7, без `pkg-*.yaml`) |

## Обучение

**Старт (человеческий слой):** [`curriculum/00-guide-for-humans.md`](./curriculum/00-guide-for-humans.md)

Маршрут модулей 0–6: [`curriculum/learning-path.md`](./curriculum/learning-path.md) · PA + Studio: [`curriculum/06-architect-studio-and-p1-intakes.md`](./curriculum/06-architect-studio-and-p1-intakes.md) · operative §PA: [`core/workflow.md`](./core/workflow.md)
