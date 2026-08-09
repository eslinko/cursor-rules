# Requirement → UI ADMIN layer package

**Категория:** architect (post-PA.2 / pre-story)  
**Не заменяет:** выполнение ADMIN «Выполни…» / P1.3  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Эталон пакета:** `spa-app/docs/tasks/backlog-stories/public-home/ADMIN-PH-01…06` (+ `PRODUCT-BRIEF.md`, `INDEX.md`)

**Когда:** spa / landing (или visual/mixed) requirement → нужна **система файлов-планов по слоям** (UX → mockups → icons → API → stories/l10n → tech), а **не** сразу финальные `STORY-*`.

**Не использовать** для чистого backend / non-UI — [`req-to-backlog-stories.md`](./req-to-backlog-stories.md).

**Подстановка (только это):**

| Поле | Значение |
|------|----------|
| `$requirementDoc=` | path REQ (напр. `spa-app/docs/requirements/15-early-signal-….md`) |
| `$builderProject=` | `spa` \| `landing` |
| `$featureSlug=` | опц. короткий префикс (напр. `ES` → `ADMIN-ES-01-…`); пусто → вывести из REQ title в plan |

Пакет backlog **не** подаётся. **Всегда NEW** `…/backlog-stories/<slug>/` (slug из `$featureSlug` или REQ). Не reuse `public-home` / чужие пакеты.

**Канон слоёв (omit только с why в plan table):**

| # | Файл | Роль |
|---|------|------|
| 0 | `PRODUCT-BRIEF.md` | locked brief из REQ (вход 01) |
| — | `INDEX.md` | статусы слоёв + порядок |
| 01 | `ADMIN-{PREFIX}-01-product-ux-prompts.md` | UX prompts / state matrix → later `UX-PROMPTS.md` |
| 02 | `ADMIN-…-02-ux-mockup-intake.md` | mockup specs intake |
| 03 | `ADMIN-…-03-icon-assets-catalog.md` | icon catalog plan |
| 04 | `ADMIN-…-04-api-requirements.md` | API needs vs verified code/docs |
| 05 | `ADMIN-…-05-backlog-stories-l10n.md` | **deliverable later:** STORY-* + l10n (не создавать STORY в этом промпте) |
| 06 | `ADMIN-…-06-tech-decomposition.md` | epic/tasks/pkg plan (scaffold later; no execute) |

Структура каждого ADMIN: Meta (Key/Status/Depends/Blocks/Skill) · Цель · Вход · Deliverable · Acceptance · Как выполнять — **как** ADMIN-PH-*.

**Дефолт записи:** plan + полные drafts в чате; диск — только «запиши».

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
$requirementDoc=
$builderProject=
$featureSlug=

Requirement → UI ADMIN layer package (plan mode).
@$requirementDoc
builder_project: $builderProject
feature_prefix: ADMIN-$featureSlug- (if $featureSlug empty — derive PREFIX from REQ title; show in plan)

MODE: plan-only. STOP after layer plan + full drafts in chat.
Do NOT: edit files until «запиши»; create STORY-*.md / pkg / epic / task README now;
      run P1.3/P3; invent gateway HTTP paths/fields (cite sibling REQ or TBD Open question);
      generate PNG mockups; propose «Выполни ADMIN-01» / Builder until operator go-ahead;
      ask operator for backlog package path; reuse existing packages (public-home, etc.).
Code claims: only after Read/Grep with path:line; else Unknown.

Etalon structure: spa-app/docs/tasks/backlog-stories/public-home/ADMIN-PH-01…06
(+ PRODUCT-BRIEF.md, INDEX.md). Match Meta/Depends/Blocks/Skill/Deliverable/Acceptance/Как выполнять.
Etalon = structure only — write into a NEW package, never into public-home.

## Phase 0 — Package path (NEW, mandatory)
Proposed path: `{spa-app|landing}/docs/tasks/backlog-stories/<kebab-slug>/`
Slug from $featureSlug (expanded) or REQ title/id.
Why: UI ADMIN set is large; always NEW; never reuse.
Table: | Decision | Path | Why |
Decision must be `new`. Override to existing path ONLY if operator explicitly orders in chat (not an input field).

## Phase 1 — Own surfaces
Из @$requirementDoc:
- surfaces / artboards / states (A–E etc.)
- API seams (consume existing vs Unknown / sibling REQ)
- l10n needs; out of scope
Таблица: | Surface / claim | REQ § | Notes |

## Phase 2 — Layer plan
| Layer | Include? (yes / omit+why) | Skill | Depends | Blocks | Proposed filename |
01…06 + BRIEF + INDEX. Default = all six ADMIN; omit only with explicit why (e.g. no new icons).
Include Phase 0 package path in the plan summary.
Proposed $dashboardFile delta (spa → spa-mvp-dashboard.md; landing → landing-mvp-dashboard.md):
By package = NEW path; Remaining = ADMIN keys Todo / «ADMIN package Todo»; §Now = package path + ADMIN-01 next.
Do not count STORY as Done (stories do not exist yet).
Canon: docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md
Dashboard edit only on «запиши».

Planned STORY keys (names only) go **inside** ADMIN-05 draft as target table — do NOT write STORY files in this prompt.

## Phase 3 — Drafts in chat
Full markdown for:
1) PRODUCT-BRIEF.md (from REQ; locked intent; out of scope; links to parent/sibling REQ)
2) INDEX.md (Todo statuses; order 01→06)
3) Each included ADMIN-0N (complete executable plan file text)

ADMIN-05 lists future STORY-* keys + l10n plan; files appear only when operator later runs ADMIN-05.
ADMIN-06 describes future epic/task/pkg scaffold; does not create them now.

## End of plan reply
Handoff: none until materialize.
Reply ends with: Phase 0 path + layer plan + drafts + proposed INDEX/dashboard delta + clarifying questions only.
Do not suggest executing ADMIN layers or P1 until operator go-ahead.

## Materialize (только по «запиши»)
1) Create the NEW package directory from Phase 0 (do not write into an unrelated existing package).
2) Write PRODUCT-BRIEF.md, INDEX.md (ADMIN statuses Todo), included ADMIN-*.md only.
3) If root backlog-stories/INDEX.md exists — add package pointer row.
4) Sync $dashboardFile: By package, Remaining (ADMIN Todo), §Now (path + next ADMIN-01), Updated/Last change — recount from disk ([backlog-dashboard-maintenance.md](../../workflow/backlog-dashboard-maintenance.md)).
5) Do NOT write STORY-*.md, pkg, epic, UX-PROMPTS.md, icon PNGs.
6) Optional note: `npm run dashboard:aggregate`.
7) Handoff: «ADMIN package + dashboard ready at <path> → operator runs layers (“Выполни ADMIN-…”);
   after ADMIN-05/06 done → P1.3 on stories. This prompt stops.»
```

---

## Примечания (не в copy-paste)

- Связанные: [`req-to-backlog-stories.md`](./req-to-backlog-stories.md) (non-UI, reuse|new), [`parent-requirement-to-project-reqs.md`](./parent-requirement-to-project-reqs.md).
- Dashboard: [`../../workflow/backlog-dashboard-maintenance.md`](../../workflow/backlog-dashboard-maintenance.md).
- Landing: те же 6 слоёв; пути mockups/icons — по `landing/docs/…` после verify exists.
- Human: [`../../curriculum/06-architect-studio-and-p1-intakes.md`](../../curriculum/06-architect-studio-and-p1-intakes.md).
