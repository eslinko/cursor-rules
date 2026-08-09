# Parent requirement → project child requirements

**Категория:** architect (pre-PA.2)  
**Не заменяет:** PA.2 (один REQ) / P1.2 в [`../../core/workflow.md`](../../core/workflow.md)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — только verified claims; без assumptions.

**Когда:** есть высокоуровневый product/UX requirement (часто в `docs/requirements backlog/` или `docs/modules/`) и нужно вывести **дочерние** per-project requirements на уровне **pre-story** (ещё не STORY/pkg), со связями parent↔child и sibling↔sibling.

**Пример parent:** `docs/requirements backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md` → типично children в `gateway` + `spa`.

**Подстановка оператором:**

| Поле | Значение |
|------|----------|
| `$parentReq=` | path parent product requirement |
| `$targetProjects=` | CSV: `gateway,spa` (или `identity,gpt,landing…`); пусто → агент предлагает owners и спрашивает |
| `$slice=` | опц. сужение (§§ / blocks parent) |

**Дефолт записи:** план + полные drafts **в чате**; файлы на диск — только после явной команды («запиши» / «materialize»).

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
@docs/modules/dashboard/search-matching-interviews/00-architecture-primer.md
$parentReq=
$targetProjects=
$slice=

Parent → project child requirements (Architect Studio, pre-PA.2).
@$parentReq
@$slice (если задан — только эти §§/blocks)

Жёстко (analysis.mdc):
- Только факты из parent / прочитанных REQ / кода. Нет assumptions, нет silent invent API/полей.
- Code/doc claim — с path (и line для кода). Иначе Unknown + вопрос оператору.
- Не создавать EPIC / STORY / pkg / task folders. Не запускать P3.
- Не копировать весь parent в каждый child — только scope этого проекта + ссылки.
- UX-only куски parent без backend-контракта → spa-only (+ Open question на gateway), не выдумывать endpoint.
- Файлы на диск — ТОЛЬКО после явной команды оператора («запиши» / «materialize»).

Projects map (paths; @ только нужные после $targetProjects):
- gateway → doge-complaints-gateway/docs/requirements/ (+ README-index.md); эталон стиля: соседние NN-*.md (напр. 24-tallinn-issues-read-api.md)
- spa → spa-app/docs/requirements/ (+ README-index.md)
- identity → doge-identity-service/docs/requirements/
- gpt → GPT UI/docs/requirements/ (REQ-*.md)
- landing → landing/docs/… (verify exists)

Если $targetProjects пуст: предложи owners по Phase A и STOP до подтверждения оператора.

Ownership heuristics (primer trust boundaries; refine by parent text):
- API / aggregates / signals / clustering / projections → gateway
- Public UI / discovery UX / dashboard blocks → spa
- Auth / PII / verification → identity
- Interview / taxonomy extraction → gpt

## Phase A — Own & slice
Таблица (каждая существенная § / claim из parent, с учётом $slice):
| Parent § / claim | Owning project(s) | Why | Out-of-scope projects | Unknown |

Выход Phase A: proposed child set (1+ draft IDs per owning project) + вопросы, если Unknown блокирует.

## Phase B — Child REQ drafts (pre-story, в чате)
Для каждого child — полный markdown draft в стиле эталона проекта (прочитай 1–2 соседних файла из etalon dir).

Обязательный header в каждом child:
Parent: <$parentReq> §<sections>
Parent-id: <stable slug from parent title or operator>
Siblings: <other-project/path or proposed-filename> (contract: <API/field/event or TBD-question>)
Status: Draft — awaiting PA.2

Тело child (минимум):
1) Goal
2) Scope / Out of scope
3) Verified current state (paths или Unknown)
4) Target behavior
5) Acceptance criteria (проверяемые)
6) Open questions
7) Dependencies (parent §§ + sibling children)

Не materialize. Покажи все drafts в ответе.

## Phase C — Link matrix (обязателен до materialize)
| Parent § | Child (project / proposed path) | Sibling deps | Contract seam (API/field/event) |

Правила связей:
- Каждый child → Parent path + §§.
- Siblings с общим швом → двусторонние Siblings: + одна строка Contract seam.
- Нет шва → не выдумывать зависимость.

После Phase C: краткий план materialize (proposed filenames NN-slug.md = next free number из listing/README-index) + таблица dashboard sync и STOP, пока оператор не скажет «запиши».

## Phase D — Dashboard sync plan (in chat only; no edit yet)
Канон: docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md (+ template).
Default scope mvp:
| Project | $dashboardFile |
| gateway | doge-complaints-gateway/docs/tasks/gateway-mvp-dashboard.md |
| spa | spa-app/docs/tasks/spa-mvp-dashboard.md |
| landing | landing/docs/tasks/landing-mvp-dashboard.md |
| identity/gpt | {project}-mvp-dashboard.md if exists |

Таблица: | Project | Dashboard path | Proposed delta (Requirements/Remaining/§Now) |
Draft child REQ = active Todo work item, **not** Done. Recount from disk only after materialize.
Do not invent counts from memory.

## Materialize (только по команде)
1) Записать каждый child в {project}/docs/requirements/{NN}-{slug}.md (NN = следующий свободный).
2) Обновить README-index.md строкой на новый файл.
3) В parent добавить секцию ## Derived project requirements со списком путей
   — если parent read-only / оператор запретил правку: спросить один раз и при отказе создать рядом
     <parent-stem>-derived-index.md со списком.
4) For each owning project: update $dashboardFile (Summary/Remaining/Requirements/§Now/Updated/Last change) per backlog-dashboard-maintenance — Draft REQs as Todo/active; never mark Done.
5) Optional: note `npm run dashboard:aggregate` (operator).
6) Handoff: «decomposition materialized + dashboards synced → PA.2 на каждый Draft child → P1.2».

Product Story Done ≠ наличие Draft children.
```

---

## Примечания (не в copy-paste)

- После materialize каждый child проходит **отдельный** PA.2 (стиль/AC/verified state), затем P1.2.
- Dashboard: [`../../workflow/backlog-dashboard-maintenance.md`](../../workflow/backlog-dashboard-maintenance.md).
- Связанный pre-PA: [`cross-project-system-orientation.md`](./cross-project-system-orientation.md) — если система ещё не разобрана.
- Human layer: [`../../curriculum/06-architect-studio-and-p1-intakes.md`](../../curriculum/06-architect-studio-and-p1-intakes.md).
