# Builder plans unification — зеркало и SSOT

**Дата сверки:** 2026-06-04  
**Планы:** [Gateway_builder.plan.md](../../../.cursor/plans/Gateway_builder.plan.md), [GPT_builder.plan.md](../../../.cursor/plans/GPT_builder.plan.md), [ID_builder.plan.md](../../../.cursor/plans/ID_builder.plan.md)  
**Шаблон:** [builder-plan-template.md](./builder-plan-template.md)  
**Машинный реестр:** [profiles.yaml](../specs/profiles.yaml)  
**Метод:** analysis.mdc — только факты с диска + `builder_resolve_queue.py --verify`.

> **Deprecated:** [gpt-vs-gateway-plan-gaps.md](../archive/gpt-vs-gateway-plan-gaps.md) — использовать этот документ для сверки всех трёх планов.

---

## Baseline verify (2026-06-04)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```

| Проект | Результат | `current.yaml` → pkg |
|--------|-----------|----------------------|
| gateway | `ok 7 paths` | `pkg-000026-20260528-req46-demo-services-intake-transparency.yaml` |
| gpt | `ok 4 paths` | `pkg-000016-20260603-req35-demo-field-population.yaml` |
| identity | `ok 15 paths` | `pkg-000008-20260602-epic-ids-06-testing-architecture.yaml` |

---

## Канонический скелет H2

Все три plan-файла после унификации:

1. `## Назначение`
2. `## Связь с unified workflow`
3. `## Поведение при Build / Execute plan (Cursor)` (+ H3 safe-override, границы, todos, шаг 0, шаблон чата)
4. `## Иерархия SSOT (что главнее при противоречии)` (+ H3 синхронизация)
5. `## ☀️☀️ INPUT SOURCE ❤️❤️` ← **эталон Gateway**
6. `## Статус внедрения правил`
7. `## Текущая точка по индексу (актуализируйте по файлу)`
8. `## Правило приоритизации и выбора эпиков`
9. `## Контракт ролей (обязательный)`
10. `## Уровни процесса`
11. `## Канон исполнения и отчётности (без дублирования pipeline)`

---

## Таблица зеркала S01–S15

| ID | Тема | Gateway (до) | GPT (до) | ID (до) | Судьба |
|----|------|--------------|----------|---------|--------|
| S01 | Порядок H2 после INPUT | Эталон | OK | Уровни→Аудит→… | Унифицировать ID |
| S02 | §Связь workflow | Есть | Есть | Нет | Добавить в ID |
| S03 | Propagation/Changelog | — | — | Есть | Удалить из ID plan |
| S04 | Три процесса / P1.3 | — | — | ~40 строк | Удалить; SSOT: workflow + operator contract |
| S05 | §Аудит P4/P4b | — | — | Есть | → operator contract §5 |
| S06 | safe-override | Ссылки без тел | 1 секция req33 | Только упоминание | H3 до Границ; GW/ID заполнить paths |
| S07 | §Режим A | 7 пунктов | 7 | Короче | = Gateway текст |
| S08 | Алгоритм резолва | 1,1b–1e,2–6 | 1,2,2b–2c | 1–6 | Единые шаги 1–6; только run_mode с телом |
| S09 | pkg drift | pkg-021/024 vs 026 | pkg-014 vs 016 | pkg-003 vs 008 | Sync с `--verify` |
| S10 | SSOT п.3 | interview 22/23 | REQ + GIM index | 3 ветки input | `{{PRODUCT_SSOT_LAYER}}` |
| S11 | build window | `--story-key` | flat window | оба | По `default_input_kind` |
| S12 | Шаблон чата | REQ-41 legacy | req33 | input_mode inline | Единый шаблон |
| S13 | frontmatter todos | 16 wave | 3 | 4 | 3 process todos |
| S14 | Skill/Git | python-pro | openai-custom-gpt | python-pro | Из profiles |
| S15 | gpt-vs-gateway doc | GW↔GPT only | — | — | Redirect сюда |

---

## Политика P1 (зафиксирована)

| Артефакт | Содержание P1 |
|----------|----------------|
| [workflow.md](../core/workflow.md) | Полные промпты P1.1 / P1.2 / P1.3 |
| [identity-operator-contract.md](../contracts/identity-operator-contract.md) | `input_mode`, backlog, session checklist |
| Build plan §Связь | ~6 строк: SSOT workflow; типичный P1.x; plan = P3/P6 runtime |
| Build plan §Синхронизация | «После P1 (workflow §P1.x) → pkg + index» без копипаста промпта |

Build plan **не** содержит: таблицу трёх режимов, P1.3 block, P4 audit table.

---

## Два режима исполнения

| Режим | Источник | Меняет current.yaml | Фаза |
|-------|----------|---------------------|------|
| YAML pkg + build window | P1→pkg; P2 `--write-build-window` | Да (новая волна) | P3 |
| safe-override | P5→§plan; `run_mode=…` | **Нет** | P6 |

Приоритет резолва: `run_mode` (если есть H3 с paths) → `ACTIVE_TASK_PATH` → `current.yaml`→pkg → режим B.

---

## P5: override vs новый pkg

| Условие | P5 output |
|---------|-----------|
| gaps ≤ 3, paths ≤ 5, 0 новых story folders, тот же эпик | §safe-override + `activation: run_mode=…` |
| иначе | task scaffold + draft pkg; `activation: none`; P1 для current.yaml |

**Checklist P5:** `exists` на каждый README; уникальный run_mode; gap-таблица; P6 чистит старые override.

---

## Плейсholders (profiles.yaml)

См. [builder-plan-template.md](./builder-plan-template.md) и таблицу в [плане унификации](../../../.cursor/plans/builder_plans_unification_86f610e0.plan.md).

---

## Регрессия после миграции

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gpt --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```

- H2 списки трёх plan совпадают (кроме числа H3 safe-override).
- Нет в plan: `Propagation / Changelog`, `Три рабочих`, `P1.3 Backlog intake`, `## Аудит (P4`.
- Каждый `run_mode` в §резолв имеет matching `### Явно прописанный safe-override`.

---

## История миграции (2026-06-04)

- Создан unified analysis + template.
- Gateway/GPT/ID приведены к каноническому скелету.
- ID: P1/P4 вынесены в operator contract.
- workflow §P5: порог override vs pkg.
