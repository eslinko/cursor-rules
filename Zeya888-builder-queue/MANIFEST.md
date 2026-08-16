# MANIFEST — Zeya888 Builder Queue

## Что это

**Zeya888 Builder Queue** — методология вайб-кодинга с жёстким контрактом между оператором и AI-агентом:

- **Requirement / Epic / Story** → декомпозиция в task tree
- **Immutable package** (`pkg-*.yaml`) — машиночитаемая очередь
- **Build window** — производный срез для одной сессии Cursor
- **Phases P0–P8** — onboarding, plan, execute, audit, gap scaffold, commits

## Три слоя SSOT

```mermaid
flowchart TB
  subgraph method [Method layer]
    wf[core/workflow.md]
    contracts[contracts/*]
    tmpl[templates/builder-plan-template.md]
  end
  subgraph tool [Tool layer]
    cli[cli/builder_resolve_queue.py]
    prof[specs/profiles.yaml]
    pkgSpec[specs/input-package-spec.md]
  end
  subgraph runtime [Project runtime]
    plans[.cursor/plans/*_builder.plan.md]
    pkgs[project *-active-packages]
    windows[run-reports/*-build-windows]
  end
  wf --> cli
  prof --> cli
  plans --> runtime
  pkgs --> cli
  cli --> windows
```

| Слой | Где править | Когда |
|------|-------------|-------|
| **Method** | `core/`, `contracts/`, `templates/`, `prompts/` | Изменение процесса, промптов, правил |
| **Tool** | `cli/`, `specs/profiles.yaml` | Новый проект, пути, CLI |
| **Runtime** | `.cursor/plans/`, `pkg-*.yaml` в проекте | Операционная работа, текущий pkg |

## Карта файлов

| Файл | Роль |
|------|------|
| [`core/session-starter.md`](./core/session-starter.md) | Phase 0 onboarding, OPERATOR CONFIG |
| [`core/workflow.md`](./core/workflow.md) | Короткие промпты **PA**, P1–P8 |
| [`core/workflow-legacy.md`](./core/workflow-legacy.md) | Полные self-contained промпты |
| [`prompts/INDEX.md`](./prompts/INDEX.md) | Индекс useful prompts по функции (architect / operator-wave / housekeeping) |
| [`prompts/architect/cross-project-system-orientation.md`](./prompts/architect/cross-project-system-orientation.md) | Pre-PA: карта 4 проектов + cross-project docs → story candidates |
| [`prompts/architect/parent-requirement-to-project-reqs.md`](./prompts/architect/parent-requirement-to-project-reqs.md) | Pre-PA.2: parent product REQ → per-project child REQs + связи |
| [`prompts/architect/req-to-backlog-stories.md`](./prompts/architect/req-to-backlog-stories.md) | Post-REQ: non-UI → backlog STORY package (plan → materialize) |
| [`prompts/architect/req-to-ui-admin-layers.md`](./prompts/architect/req-to-ui-admin-layers.md) | Post-REQ: UI → ADMIN-01…06 layer package (plan → materialize) |
| [`prompts/operator/operator-root-start.md`](./prompts/operator/operator-root-start.md) | Root OP bootstrap: project only → session bind |
| [`prompts/operator/operator-root-wave.md`](./prompts/operator/operator-root-wave.md) | Root OP: stories → wave plan + handoff packets (BLD/VAL) |
| [`prompts/operator/operator-root-subagent-run.md`](./prompts/operator/operator-root-subagent-run.md) | Root OP Phase B: profile + queueSpec → OP-*.plan.md + two subagents overnight |
| [`guides/operator-root-orchestrator.md`](./guides/operator-root-orchestrator.md) | Процесс root→субагенты + roadmap MVP/Task/SDK |
| [`guides/orchestrator-builder-reference.md`](./guides/orchestrator-builder-reference.md) | Proven overnight two-subagent SSOT (universal) |
| [`guides/operator-how-to-run-queue.md`](./guides/operator-how-to-run-queue.md) | Human how-to: запуск очереди стори/багов в OP |
| [`examples/reference-plans/Orchestrator_Builder_Reference.plan.md`](./examples/reference-plans/Orchestrator_Builder_Reference.plan.md) | Teaching snapshot: OP overnight two-subagent эталон |
| [`cli/queue-manual.md`](./cli/queue-manual.md) | Справочник CLI |
| [`specs/input-package-spec.md`](./specs/input-package-spec.md) | Контракт YAML пакета |
| [`specs/profiles.yaml`](./specs/profiles.yaml) | Реестр проектов |
| [`examples/reference-plans/`](./examples/reference-plans/) | Teaching snapshots — не runtime SSOT (`*_builder` + Orchestrator_Builder_Reference) |
| [`guides/spa-ui-visual-pipeline.md`](./guides/spa-ui-visual-pipeline.md) | Spa UI Visual Pipeline — полный SSOT UI-0..UI-3 (visual/mixed tasks) |
| [`guides/builder-artifact-dates.md`](./guides/builder-artifact-dates.md) | Дисциплина дат pkg / gate / run-summary; `--print-utc-now`, `--check-dates` |
| [`guides/fixed-builder-plan-execution.md`](./guides/fixed-builder-plan-execution.md) | Fixed `*_builder.plan.md`: @attach, не Build; отвязка от чужого чата Cursor |
| [`templates/story-acceptance-gate-template.md`](./templates/story-acceptance-gate-template.md) | Шаблон story gate с Date discipline |
| [`curriculum/00-guide-for-humans.md`](./curriculum/00-guide-for-humans.md) | Wrapping: метод для человека, роль архитектора |
| [`curriculum/06-architect-studio-and-p1-intakes.md`](./curriculum/06-architect-studio-and-p1-intakes.md) | Studio = PA chat; gap; три P1 intakes |
| [`curriculum/learning-path.md`](./curriculum/learning-path.md) | Маршрут модулей 0–6 (Human + Operative) |
| [`contracts/scripts-operator-contract.md`](./contracts/scripts-operator-contract.md) | Operator contract для `builder_project: scripts` (tooling) |
| [`contracts/capybara-operator-contract.md`](./contracts/capybara-operator-contract.md) | Operator contract для `builder_project: capybara` (Vue+Node + CLI) |
| [`contracts/landing-operator-contract.md`](./contracts/landing-operator-contract.md) | Operator contract для `builder_project: landing` (Astro+TS+Tailwind) |
| [`contracts/zeya888-operator-contract.md`](./contracts/zeya888-operator-contract.md) | Operator contract для `builder_project: zeya888` (WordPress/PHP, focus `zeya888.me`) |
| [`guides/add-builder-profile.md`](./guides/add-builder-profile.md) | SSOT bootstrap нового профиля + Gateway clone |

## Исторические пути

Артеfactы до миграции (build-windows, story gates, run-summaries) могут ссылаться на `docs/methodology/builder-queue/`. Это **исторический контекст**; операционные команды — только `Zeya888-builder-queue/cli/`.

## Propagation checklist

При изменении методологии обновить:

1. `core/workflow.md` (если меняются PA/P* промпты)
2. `prompts/` + `prompts/INDEX.md` (если меняется useful prompt вне PA/P*)
3. `.cursor/skills/builder-session/SKILL.md`
4. `.cursor/rules/builder-operator-habits.mdc`
5. Соответствующий `contracts/*-operator-contract.md`
6. `CHANGELOG.md` + bump `VERSION`

**Не** править `examples/reference-plans/` для runtime — только при обновлении учебного снимка.
