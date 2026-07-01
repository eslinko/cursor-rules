# Changelog — Zeya888 Builder Queue

## 1.4.8 — 2026-06-04

- [`guides/fixed-builder-plan-execution.md`](./guides/fixed-builder-plan-execution.md) — fixed `*_builder.plan.md`: @attach + workflow P3/P6; запрет Build / Execute plan (Cursor local registry)
- Propagation: `builder-plan-template.md` §Build, `workflow.md` §анти-ошибки, `session-starter.md`, `builder-operator-habits.mdc`, `builder-session/SKILL.md`, `cursor-setup.md`, `curriculum/01-first-session.md`, все `contracts/*-operator-contract.md` §1

## 1.4.7 — 2026-06-20

- Профиль **`scripts`** (Node.js / Hardhat / Web3) в [`profiles.yaml`](./specs/profiles.yaml)
- Bootstrap: `scripts/docs/tasks/` (active pkg, bullrun, backlog INDEX first)
- [`scripts-operator-contract.md`](./contracts/scripts-operator-contract.md), [`scripts-story-execution-pipeline.md`](../../../scripts/docs/tasks/scripts-story-execution-pipeline.md)
- [Scripts_builder.plan.md](../../../.cursor/plans/Scripts_builder.plan.md); propagation workflow, session-starter, queue-manual, builder-session, operator-habits

## 1.4.6 — 2026-06-20

- [`guides/builder-artifact-dates.md`](./guides/builder-artifact-dates.md) — SSOT дат артефактов (pkg, gate, run-summary, bullrun)
- [`builder_resolve_queue.py`](./cli/builder_resolve_queue.py) — `--print-utc-now`, `--verify --check-dates`, `--strict-dates`; [`date-gate-grandfather.txt`](./specs/date-gate-grandfather.txt)
- workflow §P1/P3/P5 date appendix; templates story-acceptance-gate + pkg-scaffold-snippet; sync gateway-operator-contract, builder-session, operator-habits

## 1.4.5 — 2026-06-17

- [`templates/story-ux-mockup-brief-template.md`](./templates/story-ux-mockup-brief-template.md) — UX-brief в папке materialized story
- [`core/workflow.md`](./core/workflow.md) §P1.3 п.8 + §P1.UX; sync spa-ui-visual-pipeline, spa-operator-contract, spa-story-execution-pipeline

## 1.4.4 — 2026-06-17

- Новый SSOT: [`guides/spa-ui-visual-pipeline.md`](./guides/spa-ui-visual-pipeline.md) — extract UI Visual Pipeline из Spa_builder.plan
- [Spa_builder.plan.md](../../../.cursor/plans/Spa_builder.plan.md) — каркас связки; `ui_visual_pipeline_doc` в profiles.yaml

## 1.4.3 — 2026-06-17

- Post SEARCH-02 UI pipeline patch: [`workflow.md`](./core/workflow.md) §P3 spa UI appendix — шаг 0b pre-flight Puppeteer, story-anchor model, MCP UI-0, hard STOP rules
- [`builder_resolve_queue.py`](./cli/builder_resolve_queue.py) — auto-inject UI appendix в spa build window (`--ui-appendix auto|force|off`); anchor/mockup/`puppeteer_gate` из task README
- Sync [Spa_builder.plan.md](../../../.cursor/plans/Spa_builder.plan.md), [spa-story-execution-pipeline.md](../../../spa-app/docs/tasks/spa-story-execution-pipeline.md) §P3 attach checklist, [queue-manual.md](./cli/queue-manual.md) §spa
- Источник: [methodology-spa-ui-pipeline-gaps-search-02-2026-06-17.md](../../../spa-app/docs/analysis/methodology-spa-ui-pipeline-gaps-search-02-2026-06-17.md)

## 1.4.2 — 2026-06-17

- [`core/workflow.md`](./core/workflow.md) §P3 — **spa UI appendix**: полный клон базового P3 + блок UI Visual Pipeline (`ui_gate`, `@mockup:`, UI-0..UI-3, human gate, puppeteer verify)
- Переменная `$uiPipelineDoc` в spa-таблице workflow; sync [Spa_builder.plan.md](../../../.cursor/plans/Spa_builder.plan.md) §P3 и [spa-story-execution-pipeline.md](../../../spa-app/docs/tasks/spa-story-execution-pipeline.md)

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
