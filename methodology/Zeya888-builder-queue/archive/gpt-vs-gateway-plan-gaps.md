# GPT vs Gateway Builder plan — gap analysis

> **Deprecated (2026-06-04):** использовать [builder-plans-unification-analysis.md](./builder-plans-unification-analysis.md) для сверки **Gateway + GPT + Identity** и [builder-plan-template.md](./builder-plan-template.md) при правках plan-файлов.

**Дата сверки:** 2026-05-19 (исторический снимок GW↔GPT)  
**Планы:** [`.cursor/plans/GPT_builder.plan.md`](../../../.cursor/plans/GPT_builder.plan.md), [`.cursor/plans/Gateway_builder.plan.md`](../../../.cursor/plans/Gateway_builder.plan.md)  
**Машинный реестр:** [`profiles.yaml`](profiles.yaml)  
**Метод:** только факты с диска + `builder_resolve_queue.py --verify` (analysis.mdc).

## Контекст инцидента

При ручном переносе текста из Gateway-плана в GPT-план была замена префикса `doge-complaints-gateway` → `GPT UI` **без** смены CLI, pkg, pipeline и индексаторов. Итог: шаг 0 с `--project gateway`, `pkg-000021`, `ok 7 paths`, несуществующие пути `EPIC-M2-*` под `GPT UI/docs/tasks/`. План восстановлен; этот документ — SSOT для будущих переносов (не в теле `.plan.md`).

## Статус плана (2026-05-19)

| Проверка | Ожидание |
|----------|----------|
| Copy-paste в `GPT_builder.plan.md` | Исправлен; операционный текст — только GPT-идентификаторы |
| `builder_resolve_queue.py --project gpt --verify` | `ok 5 paths`, pkg-000001 |
| Утечки Gateway в GPT plan | Нет паттернов из §«Типичные ошибки» (допустимы осознанные строки: «Gateway Builder», gateway-only manual) |
| G1 operator manual | [`gpt-pipeline-user-manual-cursor.md`](../../../GPT%20UI/docs/analysis/tasks/gpt-pipeline-user-manual-cursor.md) |

## Проверка на диске

```bash
# из корня DOGEstonia/
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify
```

| Проект | Результат verify | Указатель `current.yaml` |
|--------|------------------|---------------------------|
| gateway | `ok 7 paths` | `gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml` |
| gpt | `ok 5 paths` | `gpt-active-packages/pkg-000001-20260520-req22-transport-wave2.yaml` |

### Регрессия GPT plan (после правок Gateway или GPT)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
grep -E 'pkg-000021|ok 7 paths|gateway-active-package|m2-epic-story|EPIC-M2-18|STORY-M2-18|python-pro/SKILL' .cursor/plans/GPT_builder.plan.md
# ожидание: пустой вывод (или только не попавшие в паттерн осознанные упоминания gateway-only)
```

## Таблица замен (при переносе из Gateway → GPT)

Не ограничиваться заменой корневой папки — менять **все** строки из колонки Gateway.

| Поле | Gateway | GPT UI |
|------|---------|--------|
| CLI `--project` | `gateway` | `gpt` |
| `tasks_dir` (profiles) | `doge-complaints-gateway/docs/tasks` | `GPT UI/docs/analysis/tasks` |
| Указатель | `gateway-active-package.current.yaml` | `gpt-active-package.current.yaml` |
| Каталог pkg | `gateway-active-packages/` | `gpt-active-packages/` |
| Активный pkg (текущая волна) | pkg-000021, **7** paths, `epic_story_tree` | pkg-000001, **5** paths, `task_list_linear` |
| Ожидание `--verify` | `ok 7 paths` | `ok 5 paths` |
| Pipeline | `m2-epic-story-execution-pipeline.md` | `gpt-story-execution-pipeline.md` |
| Run-summary поле | `gateway_input_package` | `gpt_input_package` |
| `input_origin` | `gateway_yaml_package` | `gpt_yaml_package` |
| Индексаторы волны | STORY-M2-*, task-m2-*, REQ-41 | GIM-102…106, REQ-22, `task-implement-*` / `task-refactor-*` |
| Build-window CLI | `--write-build-window --story-key <KEY>` | `--write-build-window --window-flat-start A [--window-flat-end B]` |
| Каталог окон | `run-reports/gateway-build-windows/` | `run-reports/gpt-build-windows/` |
| Next pointer | `.gateway-next-readme` | `.gpt-next-readme` |
| Skill в артефактах | `python-pro` | `openai-custom-gpt-builder` |
| Operator manual | `m2-pipeline-user-manual-cursor.md` | `gpt-pipeline-user-manual-cursor.md` |

## Типичные ошибки копипаста (FAIL / битые @-пути)

- `--project gateway` в GPT-плане
- `pkg-000021`, `ok 7 paths`, `gateway-active-*`
- Ссылки на `m2-epic-story-execution-pipeline.md` вместо `gpt-story-execution-pipeline.md`
- Пути `GPT UI/docs/tasks/epics/EPIC-M2-*` / `task-m2-*` — **дерево эпиков M2 только в gateway** (`doge-complaints-gateway/docs/tasks/epics/`)
- `22-m2-demo-story-intake-interview-ssot-v1.md` под `GPT UI/docs/requirements/` — файл есть только в `doge-complaints-gateway/docs/requirements/`
- `m2-pipeline-user-manual-cursor.md` как **единственный** operator manual для GPT — использовать `gpt-pipeline-user-manual-cursor.md`

## Gaps (продукт / документация)

| ID | Gap | Статус | Resolution |
|----|-----|--------|------------|
| G1 | Нет operator manual для Cursor (аналог gateway) | **Done** | [`gpt-pipeline-user-manual-cursor.md`](../../../GPT%20UI/docs/analysis/tasks/gpt-pipeline-user-manual-cursor.md); ссылка в `GPT_builder.plan.md` §Канон |
| G2 | Safe-override REQ-22 audit: пустой список до audit-wave | Expected | Заполнить §safe-override в плане после аудита; не выдумывать пути |
| G3 | SPA в `profiles.yaml` (`enabled: false`) | Planned | Не смешивать с GPT/Gateway до включения профиля |
| G4 | Паритет планов при изменении Gateway-эталона | Process | См. §Maintenance ниже |

## Maintenance: при изменении `Gateway_builder.plan.md`

1. Пройти [таблицу замен](#таблица-замен-при-переносе-из-gateway--gpt) для соответствующих секций в [`GPT_builder.plan.md`](../../../.cursor/plans/GPT_builder.plan.md).
2. Запустить [блок регрессии](#регрессия-gpt-plan-после-правок-gateway-или-gpt).
3. Не переносить gateway-only сущности (M2 epics tree, REQ-41 wave как default, `python-pro` как default skill).
4. Обновить дату в шапке этого файла, если менялись активные `pkg-*` или число paths.

## Связанные SSOT

- Операторский цикл: [`workflow.md`](workflow.md)
- Контракт пакетов: [`input-package-spec.md`](input-package-spec.md)
- GPT operator manual: [`gpt-pipeline-user-manual-cursor.md`](../../../GPT%20UI/docs/analysis/tasks/gpt-pipeline-user-manual-cursor.md)
- GPT план (исполнение): [`.cursor/plans/GPT_builder.plan.md`](../../../.cursor/plans/GPT_builder.plan.md)
