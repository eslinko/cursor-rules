# Учебный маршрут — Zeya888 Builder Queue

**Старт для человека:** [`00-guide-for-humans.md`](./00-guide-for-humans.md)

## Модули

| # | Тема | Human (объяснения) | Operative (промпты / spec) | Результат |
|---|------|--------------------|----------------------------|-----------|
| 0 | Обзор методологии | [00-guide-for-humans.md](./00-guide-for-humans.md) | [MANIFEST.md](../MANIFEST.md) | Зачем метод, роль архитектора, три слоя SSOT |
| 1 | Первая сессия | [01-first-session.md](./01-first-session.md) | [session-starter.md](../core/session-starter.md) | Phase 0 onboarding |
| 2 | Package + window | [02-first-package-and-window.md](./02-first-package-and-window.md) | [input-package-spec.md](../specs/input-package-spec.md) | verify + build window |
| 3 | Workflow P0–P8 | [03-workflow-phases-explained.md](./03-workflow-phases-explained.md) | [workflow.md](../core/workflow.md) | Полный цикл |
| 4 | CLI и contracts | [04-cli-and-contracts-explained.md](./04-cli-and-contracts-explained.md) | [queue-manual.md](../cli/queue-manual.md) | Команды и operator rules |
| 5 | Свой проект | [05-connect-your-project.md](./05-connect-your-project.md) | [cursor-setup.md](../integration/cursor-setup.md) | profiles + plan |
| 6 | Architect Studio + P1 intakes | [06-architect-studio-and-p1-intakes.md](./06-architect-studio-and-p1-intakes.md) | [workflow.md](../core/workflow.md) §P1 | Studio vs Builder; три `input_mode`; handoff |

## Для инструктора

- Демо-профиль: [`../examples/sample-profiles/minimal.yaml`](../examples/sample-profiles/minimal.yaml)
- Reference plans — только разбор структуры: [`../examples/reference-plans/`](../examples/reference-plans/)
- Полные self-contained промпты: [`../core/workflow-legacy.md`](../core/workflow-legacy.md)

## Предпосылки

- Cursor IDE
- Python 3.11+
- Базовое понимание git и YAML

## Порядок прохождения

1. Модуль 0 целиком (wrapping).  
2. Модули 1–2 с практикой verify на своём или demo `--project`.  
3. Модуль 6 **до** первого P1, если входите через gap analysis или backlog story (типично identity).  
4. Модуль 3 параллельно с первым реальным P1→P3.  
5. Модули 4–5 при переносе на свой репозиторий.
