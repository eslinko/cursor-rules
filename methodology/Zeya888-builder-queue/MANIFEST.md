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
| **Method** | `core/`, `contracts/`, `templates/` | Изменение процесса, промптов, правил |
| **Tool** | `cli/`, `specs/profiles.yaml` | Новый проект, пути, CLI |
| **Runtime** | `.cursor/plans/`, `pkg-*.yaml` в проекте | Операционная работа, текущий pkg |

## Карта файлов

| Файл | Роль |
|------|------|
| [`core/session-starter.md`](./core/session-starter.md) | Phase 0 onboarding, OPERATOR CONFIG |
| [`core/workflow.md`](./core/workflow.md) | Короткие промпты P1–P8 |
| [`core/workflow-legacy.md`](./core/workflow-legacy.md) | Полные self-contained промпты |
| [`cli/queue-manual.md`](./cli/queue-manual.md) | Справочник CLI |
| [`specs/input-package-spec.md`](./specs/input-package-spec.md) | Контракт YAML пакета |
| [`specs/profiles.yaml`](./specs/profiles.yaml) | Реестр проектов |
| [`examples/reference-plans/`](./examples/reference-plans/) | Teaching snapshots — не runtime SSOT |

## Исторические пути

Артеfactы до миграции (build-windows, story gates, run-summaries) могут ссылаться на `docs/methodology/builder-queue/`. Это **исторический контекст**; операционные команды — только `Zeya888-builder-queue/cli/`.

## Propagation checklist

При изменении методологии обновить:

1. `core/workflow.md` (если меняются промпты)
2. `.cursor/skills/builder-session/SKILL.md`
3. `.cursor/rules/builder-operator-habits.mdc`
4. Соответствующий `contracts/*-operator-contract.md`
5. `CHANGELOG.md` + bump `VERSION`

**Не** править `examples/reference-plans/` для runtime — только при обновлении учебного снимка.
