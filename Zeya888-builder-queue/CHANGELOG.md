# Changelog — Zeya888 Builder Queue

## 1.4.1 — 2026-06-16

- Hybrid **execution skill**: `execution_skill_*` + `stack_label` в [`profiles.yaml`](./specs/profiles.yaml); резолв в [builder-session/SKILL.md](../../../../.cursor/skills/builder-session/SKILL.md) §Execution skill resolution
- Универсальные промпты [`core/workflow.md`](./core/workflow.md) §P1–P8: `$executionSkill*`, `$p13Appendix`; убран захардкоженный `python-pro` из P1.3
- §6 P1.3 appendix: [spa-operator-contract.md](./contracts/spa-operator-contract.md), [identity-operator-contract.md](./contracts/identity-operator-contract.md)
- session-starter Phase 0, curriculum/03, workflow-legacy — builder-session vs execution skill

## 1.4.0 — 2026-06-04

- Runtime SSOT [`.cursor/plans/Spa_builder.plan.md`](../../../.cursor/plans/Spa_builder.plan.md) для `builder_project: spa` (P3/P6, unified INPUT SOURCE, bootstrap pending)
- [spa-operator-contract.md](./contracts/spa-operator-contract.md) — primary `backlog_story`, paths `spa-app`
- [spa-story-execution-pipeline.md](../../../spa-app/docs/tasks/spa-story-execution-pipeline.md) + `spa-active-packages/` skeleton
- Профиль `spa` `enabled: true` в [`profiles.yaml`](./specs/profiles.yaml); обновлены SKILL, workflow §profiles, session-starter, queue-manual §5, README, curriculum 06, bullrun-launch-index
- Legacy [`DASHBOARD (SPA)_builder.plan.md`](../../../.cursor/plans/DASHBOARD%20(SPA)_builder.plan.md) — redirect в Spa_builder.plan.md

## 1.3.0 — 2026-06-07

- Фаза **PA — Intake Analysis** в [`core/workflow.md`](./core/workflow.md): PA.1/PA.2/PA.3, переменные `$intakeArtifact` / `$etalonDir`, базовый маршрут Phase 0 → PA → P1 → …
- Полные промпты PA в [`core/workflow-legacy.md`](./core/workflow-legacy.md) (пример REQ-42 shaping)
- Curriculum 06: Architect Studio = чат для PA; обновлены 00-guide, 03-workflow, learning-path, session-starter, builder-session SKILL

## 1.2.0 — 2026-06-06

- Новый модуль: `curriculum/06-architect-studio-and-p1-intakes.md` — Architect Studio (per-project диалог), gap analysis, три intake (P1.1 / P1.2 / P1.3), decision tree, handoff checklist
- Обновлены `learning-path.md` (модуль 6), `00-guide-for-humans.md` §8, cross-link в `03-workflow-phases-explained.md` §P1
- README, MANIFEST

## 1.1.0 — 2026-06-06

- Human learning layer: `curriculum/00-guide-for-humans.md` (wrapping, ценность, роль архитектора)
- Расширены модули 01–02 (шаги с «что происходит / зачем архитектору»)
- Новые модули: `03-workflow-phases-explained.md`, `04-cli-and-contracts-explained.md`, `05-connect-your-project.md`
- Обновлены `learning-path.md`, README, MANIFEST

## 1.0.0 — 2026-06-06

- Переименование `builder-queue` → `Zeya888-builder-queue`
- Реструктуризация: `core/`, `cli/`, `specs/`, `contracts/`, `examples/`, `curriculum/`, `integration/`
- Reference plans перенесены в `examples/reference-plans/` (teaching only)
- Runtime SSOT builder plans: `.cursor/plans/*_builder.plan.md`
- Добавлены: MANIFEST, curriculum skeleton, gateway operator contract, profiles-fields, cursor-setup
