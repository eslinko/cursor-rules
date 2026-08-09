# Cross-project system orientation

**Категория:** architect (pre-PA)  
**Не заменяет:** PA.1–PA.3 / P1.x в [`../../core/workflow.md`](../../core/workflow.md)  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — только verified claims; без assumptions.

**Когда:** нужно понять верхнюю архитектуру и концепт четырёх приложений и поработать с фрагментированным cross-project docs-слоем: карта + analytics + candidates **in chat**; дальше (Studio/Builder) — только по явному go-ahead оператора.

**Подстановка оператором:**

| Поле | Значение |
|------|----------|
| `$topic=` | тема аналитики (опц.; иначе Phase B спросит) |
| `$focusModule=` | путь под `docs/modules/…` (опц.) |

---

## Copy-paste

```text
@.cursor/rules/analysis.mdc
@docs/modules/dashboard/search-matching-interviews/00-architecture-primer.md
@docs/analysis/
@docs/modules/
$topic=
$focusModule=

Cross-project system orientation (Architect Studio pre-PA).
Projects in scope: doge-complaints-gateway, doge-identity-service, spa-app, GPT UI (+ root docs).

MODE: read-only orientation + code verify only.
STOP after Phase A–C tables in chat.
Do NOT: materialize EPIC/STORY/REQ/pkg; do NOT copy PA/P1; do NOT edit files;
      do NOT propose next actions beyond clarifying questions.
Code claims: only after Read/Grep with path:line; else Unknown.
Wait for my explicit go-ahead before any Studio/Builder step.

Жёстко (analysis.mdc + MODE):
- Только факты из прочитанных файлов / кода. Нет assumptions, нет silent invent.
- Code claim — только после Read/Grep с path:line; иначе Unknown. Doc claim — с path.
- Не edit файлов; не materialize EPIC/STORY/REQ/pkg; не копировать PA/P1 в ответ.
- Product Story Done ≠ «нашли gaps» / ≠ таблица candidates.

Reading order (не «весь монорепо»):
1) @docs/modules/dashboard/search-matching-interviews/00-architecture-primer.md — SoT system map для текущего stack.
2) @docs/modules/ (+ $focusModule если задан) — product/concept modules.
3) @docs/analysis/ — сквозная integration analytics.
4) Опц. concept: docs/network-architecture/; docs/DOGEstonia.md — помечай legacy/возможно устаревшее.
5) Per-project one-pagers только после primer, по необходимости:
   - doge-complaints-gateway/docs/high-level-description.md
   - GPT UI/docs/concept-and-goals.md
   - identity / spa: architecture или runtime-docs (пути — только после verify exists)
6) Descent-канон (для сверки, не как единственный SSOT):
   {gateway|identity|spa|GPT UI}/docs/requirements/ и соответствующий docs/tasks/

Единого docs/requirements/ в корне НЕТ — слой фрагментирован; опиши карту «где искать FR» как есть.

## Phase A — System orientation (карта, не stories)
Выход:
1) Один абзац product concept (DOGEstonia / civic signals).
2) Таблица 4 компонентов: роль | стек | trust boundary | ключевые inbound/outbound.
3) Сквозной data flow: GPT UI → gateway → Issues → spa-app; identity поперёк.
4) Privacy invariant (gateway без PII vs identity) — из primer, со ссылкой на path.
5) Раздел Verified vs Unknown (Unknown → вопросы, не выдумки).

## Phase B — Cross-project requirements analytics
1) Карта слоёв: docs/modules (product FR) | docs/analysis (integration) | per-project docs/requirements (исполнение Builder).
2) Для $topic или выбранного модуля / $focusModule:
   - кандидаты в modules + analysis (read/grep);
   - сверка с per-project REQ / backlog stories (exists? overlap?).
3) Gap table:
| Claim | Source path | Status (in-docs / in-code-unverified / missing) | Owning project(s) |

Code status = in-code-unverified, пока нет path:line verify. Не утверждай «есть в коде» без Read/Grep.

## Phase C — Descending story candidates (in chat only)
Таблица (только в чате; не materialize; не запускай Studio/Builder):
| Candidate | Why | Primary project | Deps | Suggested intake label (PA.2 / PA.3 / P1.1) |

Suggested intake = метка типа intake, НЕ инструкция «скопируй PA.x» / «открой Builder».
Не предлагай copy PA/P1 и не предлагай следующие шаги Studio/Builder, пока оператор не дал explicit go-ahead.

## End of reply
Handoff: none.
Reply ends with: (1) Verified code facts (path:line only) (2) clarifying questions only.
Do not suggest next Studio/Builder steps.
```

---

## Примечания (не в copy-paste)

- Studio PA / Builder P1 — **не** часть этого промпта; только после явной команды оператора (go-ahead) с выбранным candidate.
- Не путать с P4/P5 gap wave: здесь продуктовый/архитектурный intake над docs, не post-build audit.
- Human layer: [`../../curriculum/06-architect-studio-and-p1-intakes.md`](../../curriculum/06-architect-studio-and-p1-intakes.md).
