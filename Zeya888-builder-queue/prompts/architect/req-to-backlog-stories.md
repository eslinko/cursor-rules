# Requirement → backlog stories (non-UI)

**Категория:** architect (post-PA.2 / pre-P1.3)  
**Не заменяет:** PA.3 / P1.3 в [`../../core/workflow.md`](../../core/workflow.md)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

**Когда:** из **одного** per-project requirement нужно спланировать пакет backlog **STORY-*** (не UI-слои ADMIN). Типично: gateway, identity, gpt, scripts; spa/landing без visual surface (API wiring / config only).

**Не использовать**, если REQ про visual/mixed UI (spa public board, landing sections) — тогда [`req-to-ui-admin-layers.md`](./req-to-ui-admin-layers.md).

**Подстановка (только это):**

| Поле | Значение |
|------|----------|
| `$requirementDoc=` | path child REQ (напр. `doge-complaints-gateway/docs/requirements/48-….md`) |
| `$builderProject=` | `gateway` \| `identity` \| `gpt` \| `scripts` \| `spa` \| `capybara` \| … |

Пакет backlog **не** подаётся оператором — агент resolve: reuse подходящий или NEW.

**Дефолт записи:** plan + drafts **в чате**; файлы — только после «запиши» / «materialize».

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
$requirementDoc=
$builderProject=

Requirement → backlog stories (non-UI). Plan mode like P1/P5 — scaffold plan only until materialize.
@$requirementDoc
builder_project: $builderProject

MODE: plan-only. STOP after plan tables + story drafts in chat.
Do NOT: edit files; materialize STORY/pkg/epic/tasks; run P1.3/P3; create ADMIN-* / mockups.
Do NOT invent API/fields beyond @$requirementDoc (Unknown + question).
Do NOT ask operator for backlog package path — resolve it (below).
Code claims: only after Read/Grep with path:line; else Unknown.
Wait for explicit «запиши» before any disk write.
Wait for explicit go-ahead before suggesting PA.3 / P1.3 copy-paste.

Etalon: 1–2 соседних STORY-*.md в backlog-stories/ этого проекта (+ INDEX если есть).
Gateway/identity/spa naming — по конвенции проекта (STORY-GW-* / STORY-IDS-* / STORY-SPA-*).

## Phase 0 — Package resolve (обязателен)
1) List `{project}/docs/tasks/backlog-stories/` (+ root INDEX / per-package INDEX if any).
2) Reuse candidate ONLY if folder/INDEX clearly matches REQ topic (name overlap / same feature) and is not an unrelated epic package.
3) Else NEW: `backlog-stories/<kebab-slug-from-REQ-title-or-id>/`.
4) Table before stories:
| Decision (reuse|new) | Path | Why |

Do not use operator-supplied package path as input. Chat override only if operator explicitly orders a path later.

## Phase 1 — Slice
Из @$requirementDoc таблица:
| Story key | Scope slice (from REQ §§) | AC hooks | Deps | Skill | Package path (from Phase 0) |

Skills: подобрать реальный skill path из профиля проекта / jeffallan skills (как в task README Skill declared). Не выдумывать несуществующий skill.

## Phase 2 — Package plan
- Confirm Phase 0 path; INDEX rows (key | status Todo | depends).
- Proposed root backlog-stories/INDEX.md rows if that file exists.
- Proposed $dashboardFile delta (By package / Remaining / §Now) — in chat only.
  Default: `{focus}/docs/tasks/{project}-mvp-dashboard.md` (spa → spa-mvp-dashboard.md).
  Canon: docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md
- Не activate pkg-*.yaml; не трогать current.yaml; не edit dashboard until «запиши».

## Phase 3 — Story drafts (in chat only)
Для каждой story — полный markdown draft:
- Meta (key, status Draft, parent REQ path, siblings if any, skill)
- Scope / Out of scope
- Verified current state (paths or Unknown)
- Target / AC (проверяемые, из REQ)
- Точки в коде (если known)
- Dependencies

Не ADMIN layers. Не mockups.

## End of plan reply
Handoff: none until materialize.
Reply ends with: Phase 0 table + plan tables + drafts + proposed INDEX/dashboard delta + clarifying questions only.
Do not suggest «run P1.3» / «copy PA.3» until operator go-ahead.

## Materialize (только по команде «запиши»)
1) If NEW — create package folder; if reuse — write into resolved path only.
2) Create/update package INDEX.md (+ root backlog-stories/INDEX.md if exists).
3) Записать каждый STORY-*.md
4) Sync $dashboardFile for $builderProject: By package, Remaining (new keys as Todo), §Now, Updated/Last change — recount from disk only ([backlog-dashboard-maintenance.md](../../workflow/backlog-dashboard-maintenance.md)).
5) Optional note: `npm run dashboard:aggregate`. Do not activate pkg/bullrun unless operator asked.
6) Handoff: «stories + INDEX + dashboard materialized → optional PA.3 refine → P1.3 per story. No P3.»
```

---

## Примечания (не в copy-paste)

- Связанные: [`parent-requirement-to-project-reqs.md`](./parent-requirement-to-project-reqs.md) (раньше), [`req-to-ui-admin-layers.md`](./req-to-ui-admin-layers.md) (UI — всегда NEW package).
- Dashboard: [`../../workflow/backlog-dashboard-maintenance.md`](../../workflow/backlog-dashboard-maintenance.md).
- После materialize оператор сам запускает PA.3/P1.3 — этот промпт их не копирует в ответ по умолчанию.
