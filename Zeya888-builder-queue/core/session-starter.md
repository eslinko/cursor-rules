# Zeya888 Builder Queue — старт чистой сессии

Операторский playbook для **нового чата**: onboarding фокусного проекта, затем **PA** (опционально) и P1–P8.

**SSOT маршрута:** [workflow.md](./workflow.md) (короткие фазы) · [workflow-legacy.md](./workflow-legacy.md) (полные промпты)  
**Реестр путей:** [profiles.yaml](../specs/profiles.yaml)  
**Мышление:** [@.cursor/rules/analysis.mdc](../../../.cursor/rules/analysis.mdc)

---

## 1. OPERATOR CONFIG (правьте в новом чате)

```text
builder_project: gateway
workspace_root: /Users/eslinko/Development/DOGEstonia
pipeline_profile: builder_full
```

| Поле | Значение | Примечание |
|------|----------|------------|
| `builder_project` | `gateway` \| `gpt` \| `identity` \| `spa` \| `scripts` \| `capybara` | Ключ из `profiles.yaml` |
| `workspace_root` | абсолютный путь к корню workspace | где лежит `docs/methodology/Zeya888-builder-queue/` |
| `pipeline_profile` | `builder_full` \| `generic_repo` | `builder_full` — P1–P8; иначе только Phase 0 |

**Производные (агент читает `profiles.yaml`):**

- `focus_folder`, `tasks_dir`, `plan_file`, `pipeline_doc` — по ключу `builder_project`
- `focus_root` = `{workspace_root}/{focus_folder}`
- `verify_cmd` = `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project {builder_project} --verify`
- `execution_skill_primary`, `execution_skill_path`, `stack_label` — по ключу `builder_project` ([profiles.yaml](../specs/profiles.yaml)); резолв в [builder-session/SKILL.md](../../../../.cursor/skills/builder-session/SKILL.md) §Execution skill resolution

---

## 2. Вставка в новый чат

**Один project-чат на `builder_project`.** Fixed runtime plan (`profiles.yaml` → `plan_file`, например `Scripts_builder.plan.md`) — **@attach** в этом чате + промпт из [workflow.md](./workflow.md) §P3/P6. **Не** нажимать **Build / Execute plan** на файле плана: Cursor привязывает план к другому диалогу в локальном registry ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)).

```text
@docs/methodology/Zeya888-builder-queue/core/session-starter.md

builder_project: gateway
workspace_root: /Users/eslinko/Development/DOGEstonia
pipeline_profile: builder_full

Выполни Phase 0 (onboarding) по AGENT CONTRACT ниже. Не меняй код.
После Onboarding summary — жди фазу (PA | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8).
```

Для GPT — `builder_project: gpt`, [workflow.md](./workflow.md) §P1–P8 и [gpt-operator-contract.md](../contracts/gpt-operator-contract.md) (resolve from index, `run_mode`, sync index). Для **doge-identity-service** — `builder_project: identity`, [identity-operator-contract.md](../contracts/identity-operator-contract.md). Для **spa-app** — `builder_project: spa`, [spa-operator-contract.md](../contracts/spa-operator-contract.md); типичный intake **P1.3** `backlog`. Для **scripts** (operator tooling) — `builder_project: scripts`, [scripts-operator-contract.md](../contracts/scripts-operator-contract.md). Для **capybara** (Vue+Node monolith + CLI) — `builder_project: capybara`, [capybara-operator-contract.md](../contracts/capybara-operator-contract.md); типичный intake **P1.3** backlog `STORY-SCR-CAPY*` / `STORY-SCR-CAPYUI*`. В первом сообщении оператор указывает **один** режим: `input_mode: epic_story` \| `requirement` \| `backlog_story` (identity/spa/scripts/capybara) или `run_mode=…` / default pkg (gpt).

---

## 3. AGENT CONTRACT

### 3.1 Роль

Агент разработки проекта из `profiles.yaml` в workspace `{workspace_root}`. Цикл Requirement → Plan → Package → Build → Audit → Gap → Commits. Читать SSOT с диска.

### 3.2 Phase 0 — Onboarding (без изменений кода)

#### Общий чеклист

1. `focus_root`, `focus_git_root`
2. Стек: `stack_label` + `test_command` из profiles; execution skill — `execution_skill_primary` @ `execution_skill_path`
3. Layout кода и точка входа
4. `docs/requirements/` или аналог
5. Тесты — команда из `test_command` в `profiles.yaml` для профиля
6. **Не** читать все task README подряд

#### При `pipeline_profile: builder_full`

Читать обзорно:

| Артефакт | Источник |
|----------|----------|
| Pipeline | `pipeline_doc` из profiles |
| Bullrun index | `{tasks_dir}/bullrun-launch-index.md` |
| Active pkg | `{tasks_dir}/*-active-package.current.yaml` |
| Queue CLI | `docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py` |
| Build plan | `plan_file` из profiles |

В summary: `package_file`, ожидание `--verify` (или результат, если оператор просил запуск).

#### `generic_repo`

P1–P8 недоступны — локальный процесс проекта.

### 3.3 Формат после Phase 0

```markdown
## Onboarding summary — {builder_project}

- Git root: …
- Stack / tests: … (`stack_label`, `test_command`)
- Execution skill: … (`execution_skill_primary` @ `execution_skill_path`)
- Active pkg / verify: …
- Plan: …

## Ready for

P1 | P2 | … — жду указание оператора. (PA — в отдельном Studio-чате до P1; см. workflow §PA.)
```

### 3.4 Фазы PA, P1–P8

Тексты — [workflow.md](./workflow.md). Карта (синхронизирована с workflow):

| Фаза | Режим | Суть |
|------|-------|------|
| **PA** | Intake Analysis | PA.1 epic / PA.2 requirement / PA.3 backlog → `$intakeArtifact` на диске; **без pkg**; часто отдельный Studio-чат |
| P1 | Plan | P1.1 epic / P1.2 requirement / P1.3 backlog → tasks + pkg + index; **предпосылка:** canonical intake |
| P2 | Build window | verify + `--write-build-window` |
| P3 | Execute | plan + window; bullrun + run-task |
| P4 | Audit (external) | cross-audit |
| P5 | Plan | gap scaffold only |
| P6 | Execute | override или P2+P3 |
| P7 | Re-audit | |
| P8 | Commits | git-commit.md |

### 3.5 Инварианты

| Правило | Действие |
|---------|----------|
| analysis.mdc | Claim → путь к файлу |
| Шаг 0 | `builder_resolve_queue.py --project {builder_project} --verify` — FAIL = стоп |
| YAML SSOT | immutable `pkg-*.yaml`; не переписывать без оператора |
| `run_mode` | Только по явной команде |
| P4 | Scaffold only — без pytest/runtime |
| Plans | `.cursor/plans/*.plan.md` — не редактировать без запроса |
| Fixed builder plans | `*_builder.plan.md` — @attach + workflow P3/P6; **не** Build / Execute plan ([fixed-builder-plan-execution.md](../guides/fixed-builder-plan-execution.md)) |
| Commits | git-commit.md; push только по запросу |
| Execution skill | [builder-session/SKILL.md](../../../../.cursor/skills/builder-session/SKILL.md) §Execution skill resolution — profile SSOT; task README overrides |
| Gateway | [gateway-operator-contract.md](../contracts/gateway-operator-contract.md) — index §«Актуальная точка» + pkg verify; missing epic → decompose; sync index per task/story |
| Identity | [identity-operator-contract.md](../contracts/identity-operator-contract.md) — index/pkg verify; `backlog_story` → §4, P1.3 → §6 |
| Spa | [spa-operator-contract.md](../contracts/spa-operator-contract.md) — bootstrap verify FAIL до P1; `backlog_story` → §4, P1.3 → §6 |

### 3.6 SSOT при противоречии

1. Активный `pkg-*.yaml` + verify  
2. `bullrun-launch-index.md`  
3. Decision / interview requirements  
4. Task README + acceptance-verification  

---

## 4. Команды (из `workspace_root`)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --list
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --write-build-window --story-key STORY-M2-XX-YY
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --list
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-01-01
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project spa --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project spa --write-build-window --window-flat-start 1 --window-flat-end N
```

См. [queue-manual.md](../cli/queue-manual.md).

---

## 5. Propagation

| Слой | Путь |
|------|------|
| Starter | `docs/methodology/Zeya888-builder-queue/core/session-starter.md` |
| Skill | `.cursor/skills/builder-session/SKILL.md` |
| Rule | `.cursor/rules/builder-operator-habits.mdc` |
| Gateway contract | `docs/methodology/Zeya888-builder-queue/contracts/gateway-operator-contract.md` |
| Identity contract | `docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md` |
| Spa contract | `docs/methodology/Zeya888-builder-queue/contracts/spa-operator-contract.md` |

---

## 6. Связанные документы

- [workflow.md](./workflow.md)
- [queue-manual.md](../cli/queue-manual.md)
- [input-package-spec.md](../specs/input-package-spec.md)
- [profiles.yaml](../specs/profiles.yaml)
- [git-commit.md](../../git-commit.md)
