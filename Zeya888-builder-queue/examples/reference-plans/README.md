# Reference builder plans — teaching snapshots

**Дата снимка:** 2026-06-06 (Gateway/GPT/ID) · Taxonomy: 2026-06-16  
**Runtime SSOT:** [`.cursor/plans/`](../../../../.cursor/plans/) — `Gateway_builder.plan.md`, `GPT_builder.plan.md`, `ID_builder.plan.md`, `Taxonomy_builder.plan.md`

## Политика

| Правило | Действие |
|---------|----------|
| P3/P6 Execute | Attach **только** `.cursor/plans/*_builder.plan.md` |
| Обучение / обзор структуры | Можно читать файлы здесь |
| Правки runtime | Только в `.cursor/plans/`; затем при необходимости обновить снимок здесь |
| Drift | Ожидаем — снимок не обязан совпадать с operative plan |

## Файлы

- [`Gateway_builder.plan.md`](./Gateway_builder.plan.md) — epic/story tree, story-key windows
- [`GPT_builder.plan.md`](./GPT_builder.plan.md) — flat/GIM slices, run_mode overrides
- [`ID_builder.plan.md`](./ID_builder.plan.md) — epic-first, backlog_story, P4b
- [`Taxonomy_builder.plan.md`](./Taxonomy_builder.plan.md) — queueless meta-script TC0–TC7 (gateway + spa), `--project taxonomy --verify`

Шаблон для новых планов: [`../../templates/builder-plan-template.md`](../../templates/builder-plan-template.md)
