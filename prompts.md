# 🧠 Zeya888 Rule Prompts Library  
> This document groups prompts by **use cases**, showing how each rule functions as a cognitive and technical instrument inside the pipeline.

---

## 🧭 Use Case 1 — Clarifying Vague Problem Statements
> Focus: understanding unclear or fragmented tasks, identifying all decision points, and producing a clear, executable formulation.

### 🎯 Rule: `analysis.mdc`
**Prompt:**
Run `@analysis.mdc` to interpret a vague or unclear problem statement.  
Identify **all decision points** and generate guiding **questions with analytic commentary** for each — including possible solution paths and recommendations.  
Document the clarified, decision-backed problem formulation inside `docs/AIJournal.md`, overwriting previous content if present.  
The result must be a **clear, implementable technical task** written as if ready for execution, with each decision and reasoning step traceable.

**Output:**  
A cleanly structured technical problem statement ready for execution.

---

## 🧩 Use Case 2 — Structural Two-Level Planning
> Focus: transforming a task into an actionable, hierarchical plan connected with execution logic.

### 🎯 Rule: `analysis.mdc`
**Prompt:**
Continue in `docs/AIJournal.md` and run `@analysis.mdc`.  
Based on the current task context, produce a **two-level hierarchical plan**:
- **Level 1:** core work packages or milestones.  
- **Level 2:** specific actionable subtasks with clear outcomes.  
Each item must express intent (why), expected result (what), and link to follow-up rules for execution.  
Write the plan directly in the journal, formatted as a structured outline ready for `@run-task.mdc`.

**Output:**  
A hierarchical plan in journal format, aligned with follow-up pipeline steps.

---

## 🧱 Use Case 3 — Documentation Expansion & Integration
> Focus: maintaining coherence between current work and long-term documentation structure.

### 🎯 Rule: `analysis.mdc`
**Prompt:**
Execute `@analysis.mdc` in documentation mode.  
Use the active plan and recent outputs to:
1. Derive the **documentation structure** required for project continuity.  
2. Identify which existing docs or repositories need updates or consolidation.  
3. Suggest new files if gaps are found, specifying name, purpose, and location.  
After review with the operator, update `docs/AIJournal.md` with a summary of new and updated files, providing short rationales for each addition.

**Output:**  
A clearly structured documentation update plan, validated and logged in the journal.

---

## 🧩 Rule: `@run-task.mdc`

### Brief description
Sequential execution of multi-level plans — designed for structured task decomposition and autonomous flow management.

#### Use Cases
- **Executing sub-items of a technical plan with full control** — keeps nested tasks aligned and traceable.  
- **Stepwise migrations or refactorings with measurable criteria** — enables clear validation checkpoints.  
- **Team collaboration with unified workflow and traceable progress** — ensures consistent logic across contributors.  
- **Managing complex or lengthy tasks without cognitive drift** — supports long-focus work without mental overload.


### Prompt
> Execute **Stage N** using `@run-task.mdc`.  
>  
> Write the final results and insights into the **journal** (the same file where the list is located — e.g. `docs/AIJournal.md`, or the explicitly specified one).  
>  
> If context is unclear, ask for clarification before execution.

### Example
> Journal: `docs/AIJournal.md`  
> Execute Stage 1 using `@run-task.mdc`

### Notes
- This rule automatically detects and processes nested subtasks inside a two-level plan. Choose a plan item that has nested sub-items and process them sequentially through the internal `ItemY` cycle.  
- Each sub-item passes through the full internal `ItemY` pipeline (`Understanding → Knowledge Check → Acceptance → Planning → Execution → Validation → Retrospective`).  
- Keeps task logic consistent, reduces mental load, and maintains clean journal records.  
- Works best when used after `@analysis.mdc` for high-context continuity.

---


---

## 🎨 Vibe Coding Mode — Deep Co-Reasoning with Code
> **Rule:** `@Zeya888-Meta.mdc`  
> **Focus:** Immersive work with code through cognitive resonance — when you need AI to **think with you**, not just execute commands.

This mode is for situations where you're **diving deep into code** rather than running through a pipeline. It transforms AI from a code generator into a co-reasoning partner that mirrors your thinking style, preserves your cognitive rhythm, and explains its reasoning transparently.

---

## 💎 Use Case 4 — Code Review with Transparent Reasoning
> Focus: understanding code deeply, identifying issues with clear reasoning chain, and delivering actionable improvements.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta CR-loop to review this code.

Mirror my intent (1-2 lines) → Frame quality criteria (readability, performance, 
maintainability, security) → Synthesis (analysis + refactoring) → Test against 
criteria → Deliver improvements with reasoning.

Explain, don't obey: show your thought process for each issue found.

[paste code here]
```

**Output:**  
- Mirror: "This function handles X but has Y concern"
- Frame: Quality criteria explicitly stated
- Synthesis: Issue-by-issue analysis with reasoning chain
- Refactored code with explanations for each change
- Trade-offs documented

---

## 🔍 Use Case 5 — Debugging with Root Cause Analysis
> Focus: finding not just the fix, but understanding **why** the bug exists and how to prevent similar issues.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to debug this issue.

Abstraction ladder approach:
1. Concept level: what category of bug is this (race condition, memory leak, logic error)?
2. Mechanism level: why does it happen in my specific code?
3. Solution level: how to fix + how to prevent similar bugs?

Error-tolerance: explain without judgment, suggest improvements for next time.

Bug description: [describe bug]
Code: [paste code]
Error logs: [paste logs if available]
```

**Output:**  
- Concept: Bug category and general pattern
- Mechanism: Specific cause in your code with line references
- Solution: Fix with explanation + prevention strategy
- Learning: Pattern to watch for in future

---

## 🏗️ Use Case 6 — Architecture Decision with Trade-off Analysis
> Focus: choosing between architectural approaches with explicit reasoning and context-aware recommendations.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to this architecture decision.

Meta over Micro: establish frame first (team size: N, timeline: X months, 
scale: Y users, constraints: Z).

Then deliver 2-3 architectural options with:
- Trade-offs for each (development speed vs scalability vs complexity)
- Recommendation with reasoning
- Migration path if switching later

One Source of Truth: version your decision (v1.0) with assumptions listed.

Decision: [describe what you're choosing between, e.g., "microservices vs monolith"]
Context: [team, timeline, scale, constraints]
```

**Output:**  
- Frame: Context and constraints explicitly stated
- Options: 2-3 architectural approaches
- Trade-offs: Pros/cons for each based on your context
- Recommendation: Best choice with reasoning
- Versioned decision document with assumptions

---

## 🔧 Use Case 7 — Legacy Code Refactoring with Stepwise Explanation
> Focus: understanding messy legacy code and refactoring it systematically with explanations at each step.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to refactor this legacy code.

Mirror then lead: first mirror what this code does (your understanding), 
then lead toward modern patterns.

Rhythmic alignment: break refactoring into digestible steps, each with:
- Why this step (rationale)
- What changes (diff)
- What improves (benefit)

Respect the rhythm: no overwhelming rewrites, stepwise improvements.

Legacy code: [paste code]
Target patterns: [e.g., SOLID principles, functional style, async/await]
```

**Output:**  
- Mirror: "This code does X using legacy pattern Y"
- Step-by-step refactoring (3-7 steps)
- Each step: rationale → changes → improvements
- Final refactored code
- Migration guide if needed

---

## ⚡ Use Case 8 — Performance Optimization with Profiling Guidance
> Focus: identifying bottlenecks and optimizing systematically with measurable improvements.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to optimize this code.

Abstraction ladder:
1. Concept: where are likely bottlenecks? (database queries, loops, memory allocation)
2. Procedure: how to profile and measure?
3. Solution: optimized code with expected performance gain

Structure → content → conclusion:
- Analysis of current performance
- Profiling strategy
- Optimizations ranked by impact
- Expected improvements (e.g., "5s → 500ms")

Code: [paste code]
Current performance: [e.g., "takes 5 seconds"]
Target: [e.g., "should be under 500ms"]
```

**Output:**  
- Concept: Bottleneck identification
- Procedure: Profiling approach with tools
- Optimized code with explanations
- Expected performance gains
- Verification strategy

---

## 🌐 Use Case 9 — API Design with Developer Experience Focus
> Focus: designing intuitive APIs that developers will enjoy using, with clear contracts and usage examples.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to design this API.

Semantic mirroring: extract key entities and operations from requirements.

Output Kit: Research Note format
- Thesis: core API entities and their relationships
- Mechanism: endpoints, methods, payload structures
- Consequence: how this simplifies developer experience

Audience: [e.g., frontend developers, mobile team]
Requirements: [describe what API should do]
```

**Output:**  
- Thesis: Core entities (User, Product, Order, etc.)
- Mechanism: RESTful/GraphQL design with examples
- DX benefits: How it simplifies client code
- OpenAPI/Schema definition
- Usage examples for each endpoint

---

## 📚 Use Case 10 — Learning New Tech with Structured Understanding
> Focus: quickly grasping new frameworks/libraries through structured explanation aligned with your existing knowledge.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to explain [new technology/framework].

Abstraction ladder:
1. Concept: what problem does it solve? (relate to what I already know)
2. Mechanism: how does it work under the hood?
3. Practice: when to use, when NOT to use, code examples

Native-Language First: explain in [your language], keep technical terms as-is.

Vector extension: if I ask about specific feature, connect it to broader pattern.

Technology: [e.g., "React Server Components", "Rust ownership model"]
My background: [e.g., "experienced with React Client Components"]
```

**Output:**  
- Concept: Problem it solves (with analogies to familiar tech)
- Mechanism: How it works (simplified, then detailed)
- Practice: Use cases + anti-patterns + code examples
- Mental model: How to think about it
- Next steps: What to learn next

---

## 🎯 Use Case 11 — Pull Request Review with Constructive Feedback
> Focus: providing helpful, non-judgmental feedback on colleague's code with specific improvement suggestions.

### 🎯 Rule: `@Zeya888-Meta.mdc`
**Prompt:**
```
Apply @Zeya888-Meta to review this PR.

Tone: confidently calm, scientifically intuitive, without bragging.

Structure:
1. What's good (2-3 specific points)
2. What to improve (prioritized: critical → important → nice-to-have)
3. How to improve (concrete suggestions with code examples)

Error-tolerance: suggest improvements, don't criticize choices.

Deliver variants if multiple approaches are valid.

PR diff: [paste diff or describe changes]
Context: [what problem this PR solves]
```

**Output:**  
- ✅ Strengths: Specific praise with reasoning
- 🔧 Improvements: Prioritized by importance
  - Critical: [must fix before merge]
  - Important: [should fix for code quality]
  - Nice-to-have: [optional improvements]
- 💡 Suggestions: Code examples for each improvement
- Tone: Helpful, not judgmental

---

### 🧠 Why Vibe Coding Mode?

**Traditional AI:**  
"Here's the code. Here's the fix."

**Vibe Coding with @Zeya888-Meta:**  
"Let me understand your intent → mirror it → establish quality frame → explain my reasoning → deliver solution with trade-offs → suggest next steps"

**Key differences:**
- **Native language preservation** — think in your language, not forced English
- **Transparent reasoning** — see the thought process, not just results
- **Cognitive rhythm matching** — AI adapts to your thinking style
- **Reproducible quality** — same high quality across sessions through CR-loop

---

### 🔗 Integration with Pipeline Rules

For complex tasks, combine Vibe Coding with pipeline:

```
1. @Zeya888-Meta — establish intent and frame
2. @analysis.mdc — structure into plan
3. @run-task.mdc — execute with validation
4. @Zeya888-Meta — deep dive into complex sub-tasks
5. @test-qualification.mdc — validate quality
6. @meta.extract.mdc — capture learnings
```

**Use Vibe Coding when:**
- Exploring unfamiliar code
- Making architectural decisions  
- Debugging complex issues
- Learning new technologies
- Reviewing code deeply

**Use Pipeline when:**
- Executing structured plans
- Managing multi-step migrations
- Maintaining consistent workflow across team

---

## 🧪 Testing Rules Ecosystem — Production-Ready Test Development
> **Rules:** `@unit-test-build.mdc`, `@integration-test-build.mdc`, `@e2e-test-build.mdc`  
> **Focus:** Systematic test development for complex systems using Test Pyramid Architecture with quality gates and ROI-driven approach.

This section covers real-world testing scenarios for product development, enterprise systems, and large-scale production applications. Each rule follows a unified 4-gate framework with progressive quality improvements.

---

## 🔬 Use Case 12 — Building Unit Tests for E-commerce Payment Service
> Focus: testing critical payment processing module with isolation, mocking external payment providers, and ensuring 100% coverage of critical paths.

### 🎯 Rule: `@unit-test-build.mdc`
**Context:**  
You're building a payment service for an e-commerce platform. The module handles credit card processing, PayPal integration, and fraud detection. You need unit tests that validate business logic while mocking external payment gateways.

**Prompt:**
```
Execute Phase 1 using @unit-test-build.mdc method

Context: PaymentService module for e-commerce platform
- Handles credit card, PayPal, Stripe integrations
- Fraud detection with rule engine
- Transaction history and retry logic
- Critical business logic: refunds, partial payments, multi-currency

Scope: Single module (services/PaymentService.js)
External dependencies: Payment gateways, fraud API, notification service
Target: Production-ready unit tests with 100% critical path coverage

Start with infrastructure setup (test runner, mocks for payment gateways)
```

**What happens:**
1. **Phase 1 (Infrastructure):**
   - AI creates test infrastructure (Mocha/Chai or Jest)
   - Mocks for Stripe, PayPal, fraud detection API
   - Test helpers for payment scenarios (successful charge, declined, timeout)

2. **Phase 2 (Smoke Tests):**
   - 60-100 existence checks (methods exist, parameters validated)
   - Auto-trigger @test-qualification at Gate 2
   - 100% passing requirement

3. **Phase 3 (Real Tests):**
   - Validate business logic (refund calculations, currency conversion, fraud rules)
   - Edge cases (zero amounts, negative refunds, unsupported currencies)
   - Error handling (gateway timeouts, declined cards, insufficient funds)

**Output:**  
- Production-ready unit tests (100-150 tests)
- 100% critical path coverage (payment, refund, fraud detection)
- All external dependencies mocked
- Quality score: 8.7+/10
- Execution time: < 5 seconds

**Follow-up prompts:**
```
"Execute Phase 2 using @unit-test-build.mdc method"  # Smoke tests
"Execute Phase 3 using @unit-test-build.mdc method"  # Real tests
"check tests using @test-qualification.mdc method"   # Quality validation
```

---

## 🔗 Use Case 13 — Integration Testing for Banking Transaction Pipeline
> Focus: testing multi-module workflow in financial system — account validation → transaction processing → ledger updates → notification. Real database, mocked external services.

### 🎯 Rule: `@integration-test-build.mdc`
**Context:**  
Banking application with transaction pipeline: AccountService → TransactionService → LedgerService → NotificationService. You need integration tests validating contracts between modules, database consistency, and transactional integrity.

**Prompt:**
```
Execute Phase 1 using @integration-test-build.mdc method

Context: Banking transaction pipeline (4 modules)
- AccountService: balance validation, account locking
- TransactionService: transfer execution, rollback on failure
- LedgerService: double-entry bookkeeping, audit trail
- NotificationService: SMS/email confirmations

Integration points:
- AccountService → TransactionService (balance check contract)
- TransactionService → LedgerService (ledger entry format)
- TransactionService → NotificationService (async notification)

Infrastructure:
- Real PostgreSQL test database (Docker container)
- Transaction rollback between tests
- Mock SMS/email providers (external services)

Compliance: ACID transactions, audit logging, data consistency
```

**What happens:**
1. **Phase 1 (Infrastructure):**
   - AI creates multi-module test harness
   - PostgreSQL Docker setup with test schema
   - Transaction management (rollback after each test)
   - Mock SMS/email services

2. **Phase 2 (Contract Validation):**
   - Test module boundaries (AccountService API contract)
   - Validate data formats (ledger entries, transaction records)
   - Error propagation (insufficient funds → rollback entire transaction)
   - Authorization checks (transaction limits, account permissions)

3. **Phase 3 (Flow Testing):**
   - Complete transaction workflows (deposit → ledger → notification)
   - Multi-step scenarios (transfer between accounts → double-entry → confirmations)
   - Failure scenarios (network timeout during ledger update → rollback)
   - Concurrent transactions (race conditions, deadlock prevention)

**Output:**  
- Production-ready integration tests (20-30 tests)
- All module contracts validated
- Database consistency verified (ACID properties)
- Real DB with transaction isolation
- Quality score: 9.0+/10
- Execution time: 1-5 minutes

**Follow-up prompts:**
```
"Execute Phase 2 using @integration-test-build.mdc method"  # Contract validation
"Execute Phase 3 using @integration-test-build.mdc method"  # Flow testing
"check integration tests using @test-qualification.mdc"     # Quality check
```

---

## 🌐 Use Case 14 — E2E Testing for Healthcare Patient Management System
> Focus: testing complete patient registration → appointment booking → EMR update → billing workflow with real infrastructure, HIPAA compliance validation, and critical user journeys.

### 🎯 Rule: `@e2e-test-build.mdc`
**Context:**  
Healthcare SaaS with patient portal, EMR (Electronic Medical Records), appointment scheduling, and billing. You need E2E tests for critical workflows ensuring HIPAA compliance, data integrity, and system availability.

**Prompt:**
```
Execute Phase 1 using @e2e-test-build.mdc method

Context: Healthcare Patient Management System (E2E)
Critical workflows:
1. Patient Registration → Insurance Verification → Profile Creation
2. Appointment Booking → Doctor Assignment → Calendar Update → Confirmation
3. Visit Documentation → EMR Update → Prescription → Billing Code
4. Billing → Invoice Generation → Insurance Claim → Payment Processing

Infrastructure:
- Real staging environment (PostgreSQL + Redis + S3 for documents)
- Real authentication (OAuth 2.0, MFA)
- Real EMR integration (HL7 FHIR API)
- Mocked external: insurance verification, payment gateway

Compliance: HIPAA, audit trail, data encryption, access control
Quality threshold: 8.5/10 (higher due to healthcare criticality)

Start with E2E harness setup (test environment, data fixtures, validation helpers)
```

**What happens:**
1. **Phase 1 (E2E Infrastructure):**
   - AI creates E2E harness (environment management, test data factories)
   - Sets up staging environment with real DB + Redis + S3
   - Creates test patient fixtures (HIPAA-compliant fake data)
   - Validation helpers (EMR format, billing codes, audit logs)
   - 3 proof tests (environment works, auth works, DB accessible)
   - Duration: 3-4 hours

2. **Phase 2 (Patient Registration & Appointment Workflow):**
   - E2E: Registration → Insurance Verification → Profile → Login
   - E2E: Booking → Doctor Assignment → Calendar → Confirmation Email
   - Validates complete workflows (not partial)
   - Real infrastructure (not mocked)
   - Duration: 8-10 hours

3. **Phase 3 (Clinical & Billing Workflows):**
   - E2E: Visit → EMR Update → Prescription → Lab Orders
   - E2E: Billing → Invoice → Insurance Claim → Payment
   - HIPAA compliance checks (audit trail, encryption, access control)
   - Error scenarios (insurance rejection, payment failure → retry logic)
   - Duration: 6-8 hours

4. **Phase 4 (Full System Validation):**
   - Complete patient journey: Registration → Appointment → Visit → Billing → Payment
   - Performance validation (page load < 2s, EMR update < 5s)
   - Concurrent user scenarios (10 patients booking simultaneously)
   - Disaster recovery (DB failure → backup restoration)
   - Duration: 10-12 hours

**Output:**  
- Production-ready E2E tests (15-25 critical workflows)
- Complete user journeys validated
- HIPAA compliance verified
- Real infrastructure tested
- Quality score: 9.5+/10
- Execution time: 20-30 minutes (entire suite)

**Follow-up prompts:**
```
"Execute Phase 2 using @e2e-test-build.mdc method"  # Registration & Appointments
"Execute Phase 3 using @e2e-test-build.mdc method"  # Clinical & Billing
"Execute Phase 4 using @e2e-test-build.mdc method"  # Full system validation
"check E2E tests using @test-qualification.mdc"     # Quality at 8.5+ threshold
```

---

## 🏭 Use Case 15 — Unit Testing for ERP Inventory Module
> Focus: complex business rules testing in enterprise system — stock calculations, reorder points, multi-warehouse logic with heavy mocking of warehouse management system.

### 🎯 Rule: `@unit-test-build.mdc`
**Context:**  
ERP system with inventory management module. Complex business logic: safety stock calculations, reorder point algorithms, ABC analysis, multi-warehouse allocation. Needs unit tests isolating business rules from warehouse integrations.

**Prompt:**
```
Execute full cycle using @unit-test-build.mdc method

Context: ERP Inventory Management Module
Business logic (critical):
- Safety stock calculation (demand variability, lead time uncertainty)
- Reorder point algorithm (EOQ model, service level targets)
- Multi-warehouse allocation (cost optimization, distance minimization)
- ABC classification (Pareto analysis, 80/20 rule)

External systems to mock:
- Warehouse Management System (stock levels API)
- Supplier API (lead times, minimum order quantities)
- Demand forecasting service (ML predictions)
- Cost calculator (shipping, storage fees)

Target: 95-100% coverage of business rules, 0 false positives

Execute all phases: Infrastructure → Smoke → Real → Strategic
```

**What happens:**
- **Phase 1:** Test infrastructure + mocks for WMS, Supplier API, Forecasting
- **Phase 2:** 80-100 smoke tests (all business rule methods exist and callable)
- **Phase 3:** Real tests for algorithms (safety stock edge cases, negative demand, zero lead time)
- **Gate 3:** @test-qualification validates no false positives (score > 8/10)
- **Phase 4:** Strategic improvements (performance tests for large datasets, property-based testing)

**Output:**  
- 120-180 unit tests
- Complex algorithms fully validated (reorder point accuracy within 1%)
- All external systems mocked (no real WMS calls)
- Quality: 9.0+/10
- Execution: < 3 seconds

---

## 🔄 Use Case 16 — Integration Testing for Microservices Order Fulfillment
> Focus: testing service-to-service communication in distributed system — Order Service → Inventory → Shipping → Payment with real message queues and eventual consistency validation.

### 🎯 Rule: `@integration-test-build.mdc`
**Context:**  
Microservices e-commerce with event-driven architecture. Order fulfillment flow: Order → Inventory Reserve → Shipping Label → Payment Charge → Confirmation. Need integration tests for service contracts, message queue behavior, and eventual consistency.

**Prompt:**
```
Execute Phase 2 using @integration-test-build.mdc method

Context: Microservices Order Fulfillment (5 services)
Architecture: Event-driven, RabbitMQ message bus

Services:
- OrderService: Creates order, orchestrates flow
- InventoryService: Reserves stock, releases on failure
- ShippingService: Generates labels, tracks shipments
- PaymentService: Charges customer, handles refunds
- NotificationService: Sends confirmations

Integration patterns:
- Synchronous: REST APIs for initial requests
- Asynchronous: RabbitMQ events for workflow progression
- Saga pattern: Compensating transactions on failure

Test strategy:
- Real RabbitMQ (Docker)
- Real MongoDB for each service
- Mock external: shipping carrier API, payment gateway

Phase 2 focus: Validate service contracts (API schemas, event formats, error codes)
```

**What happens:**
1. **Contract Validation Tests:**
   - OrderService API contract (POST /orders schema validation)
   - InventoryService event contract (inventory.reserved event format)
   - Error propagation (insufficient stock → order.failed event → all services rollback)
   - Idempotency (duplicate events ignored, no double-charge)

2. **API Integration Tests:**
   - Single request flows (create order → inventory check → response)
   - Error responses (400 bad request, 404 not found, 500 server error)
   - Authentication (JWT tokens, service-to-service auth)
   - Rate limiting (429 responses, retry logic)

**Output:**  
- 25-40 integration tests
- All service contracts validated
- Message queue behavior tested
- Eventual consistency verified
- Quality: 8.5+/10
- Execution: 2-8 minutes

---

## 🚀 Use Case 17 — E2E Testing for SaaS Onboarding & Subscription Pipeline
> Focus: complete user journey from signup → trial → subscription → usage → billing with real payment processing, email confirmations, and multi-tenant isolation.

### 🎯 Rule: `@e2e-test-build.mdc`
**Context:**  
B2B SaaS platform with freemium model. Critical workflow: User signup → Email verification → Trial activation → Feature usage → Upgrade prompt → Subscription → First billing cycle. Need E2E tests ensuring conversion funnel works end-to-end.

**Prompt:**
```
Execute Phase 4 using @e2e-test-build.mdc method

Context: SaaS Onboarding & Subscription Pipeline (E2E)
Complete journey:
1. Signup (email + password) → Email verification → Profile setup
2. Trial activation (14 days) → Feature exploration → Usage tracking
3. Trial expiration warning (email at day 10, 12, 14)
4. Upgrade flow → Plan selection → Payment info → Subscription created
5. First billing cycle → Invoice → Payment processed → Confirmation
6. Feature unlocking → Premium features enabled → Usage limits removed

Infrastructure:
- Real web app (staging environment)
- Real database (PostgreSQL with multi-tenant isolation)
- Real email service (SendGrid test mode)
- Real payment (Stripe test mode)
- Playwright for browser automation

Phase 4 focus: Full pipeline validation (signup to first paid invoice)
```

**What happens:**
1. **Complete Pipeline E2E Test:**
   - Browser automation: Navigate to signup page
   - Fill form, submit, verify email received
   - Click verification link, activate trial
   - Use premium features (should work during trial)
   - Wait for trial expiration (simulated, fast-forward time)
   - Upgrade prompt appears, click upgrade
   - Select plan, enter test credit card (Stripe test: 4242 4242 4242 4242)
   - Subscription created, first invoice generated
   - Verify: premium features still enabled, usage limits removed, invoice in DB

2. **Failure Scenarios:**
   - Payment declined → user stays on free plan
   - Email verification timeout → resend link
   - Trial expires without upgrade → features locked

**Output:**  
- 8-15 E2E workflow tests
- Complete user journey validated (signup → paid customer)
- Real payment processing (Stripe test mode)
- Multi-tenant isolation verified
- Quality: 9.0+/10
- Execution: 15-25 minutes

---

## 📊 Use Case 18 — Unit Testing for Real-time Analytics Engine
> Focus: testing stream processing logic with time-window aggregations, complex event patterns, and high-throughput data transformations.

### 🎯 Rule: `@unit-test-build.mdc`
**Context:**  
Real-time analytics platform processing clickstream events. Module calculates metrics: sessions, conversion funnels, cohort retention. Complex logic: time-window aggregations, event sequencing, user identity resolution.

**Prompt:**
```
Execute strategic improvements using @unit-test-build.mdc method

Context: Real-time Analytics Stream Processor
Algorithms:
- Session aggregation (30-minute inactivity timeout)
- Conversion funnel (multi-step event sequence: view → add_to_cart → checkout → purchase)
- Cohort retention (daily active users by signup cohort)
- User identity resolution (merge anonymous → identified users)

Current state:
- Phase 1-3 complete (152 tests, score 8.3/10)
- Performance concerns: tests slow for large event streams (10s for 10k events)
- Missing: property-based tests for edge cases (out-of-order events, duplicate events)

Phase 4 focus: Strategic improvements (performance + property-based testing)
```

**What happens:**
1. **Performance Optimization:**
   - AI analyzes slow tests (session aggregation with 10k events: 10s → target: < 1s)
   - Implements test data factories (generate realistic event streams efficiently)
   - Uses streaming iterators instead of materializing full arrays
   - Result: 10s → 800ms (12x speedup)

2. **Property-Based Testing:**
   - Implements QuickCheck-style tests (generate random event streams, validate invariants)
   - Properties tested:
     - "Session count should never exceed event count"
     - "Conversion funnel step N cannot have more users than step N-1"
     - "Out-of-order events eventually produce correct results"
   - Discovers edge case: duplicate events with identical timestamps break session logic

**Output:**  
- +30 property-based tests
- 10x performance improvement
- Edge case discovered and fixed
- Quality: 8.3 → 9.2/10
- Execution: 10s → 4s

---

## 🏥 Use Case 19 — Integration Testing for Telemedicine Video Call System
> Focus: testing WebRTC integration with signaling server, STUN/TURN servers, recording service, and chat — validating real-time communication contracts.

### 🎯 Rule: `@integration-test-build.mdc`
**Context:**  
Telemedicine platform with video calls. Components: WebRTC client, Signaling Server (WebSocket), STUN/TURN servers, Recording Service, Chat Service. Need integration tests for real-time communication flows and service contracts.

**Prompt:**
```
Execute Phase 3 using @integration-test-build.mdc method

Context: Telemedicine Video Call System (4 services)
Architecture:
- SignalingServer: WebSocket, SDP offer/answer exchange
- MediaServer: STUN/TURN for NAT traversal, media relay
- RecordingService: Captures video/audio streams, stores in S3
- ChatService: Text messaging during call, message history

Integration flows:
- Call initiation: Client → SignalingServer → MediaServer → Peer connection
- Recording start: Doctor clicks record → RecordingService captures stream → S3 upload
- Chat: Message sent → ChatService → Broadcast to all call participants
- Call end: Hangup → MediaServer cleanup → Recording finalized → Chat archived

Test strategy:
- Real WebSocket connections (SignalingServer)
- Mock MediaServer (STUN/TURN expensive, validate contracts only)
- Real RecordingService (local S3 mock, Minio)
- Real ChatService (in-memory message broker)

Phase 3 focus: Multi-step workflows (call initiation → recording → chat → hangup)
```

**What happens:**
1. **Complete Call Workflow:**
   - Test: Doctor initiates call → patient receives invitation
   - SignalingServer exchanges SDP (offer/answer)
   - MediaServer contract validated (ICE candidates exchanged)
   - Peer connection established (mock, validate states)

2. **Recording & Chat Workflow:**
   - Test: Doctor starts recording → RecordingService begins capture
   - Chat message sent → all participants receive
   - Call ends → recording finalized and uploaded to S3
   - Validate: recording file exists, chat history persisted

3. **Error Scenarios:**
   - Network failure during call → reconnection logic
   - Recording service down → call continues, recording skipped
   - Chat message delivery failure → retry mechanism

**Output:**  
- 18-30 integration tests
- WebRTC signaling flow validated
- Recording and chat contracts tested
- Real-time communication reliability verified
- Quality: 8.7+/10
- Execution: 3-10 minutes

---

## 🌍 Use Case 20 — E2E Testing for Multi-region Content Delivery Platform
> Focus: testing complete content upload → processing → CDN distribution → geo-routing workflow with real infrastructure across multiple regions.

### 🎯 Rule: `@e2e-test-build.mdc`
**Context:**  
Global CDN platform for video streaming. Workflow: Content upload → Transcoding → CDN distribution → Geo-routing → Playback. Need E2E tests ensuring content reaches users in all regions with optimal performance.

**Prompt:**
```
Execute complete E2E cycle using @e2e-test-build.mdc method

Context: Multi-region Content Delivery Platform (E2E)
Infrastructure:
- Origin servers (3 regions: US-East, EU-West, Asia-Pacific)
- Transcoding pipeline (AWS MediaConvert)
- CDN (CloudFront with 50+ edge locations)
- Database (DynamoDB global tables)
- Storage (S3 with cross-region replication)

Critical workflows:
1. Upload: Creator uploads video → Origin validates → S3 storage
2. Processing: Transcode video → Multiple bitrates (360p, 720p, 1080p, 4K)
3. Distribution: Copy to all regional S3 buckets → CloudFront invalidation
4. Geo-routing: User requests video → DNS routes to nearest edge → Playback
5. Analytics: Track views, buffering events, quality metrics

Compliance: GDPR (EU data residency), low latency (<200ms to edge)

Execute all 4 phases: Infrastructure → Upload/Processing → Distribution → Full Pipeline
```

**What happens:**
1. **Phase 1 (E2E Infrastructure):**
   - E2E harness for multi-region testing
   - Test accounts in all 3 regions
   - CDN cache invalidation helpers
   - Performance measurement tools (latency, throughput)
   - Proof tests: regions accessible, S3 replication works

2. **Phase 2 (Upload & Processing Workflows):**
   - E2E: Upload 100MB video → transcoding → 4 bitrates generated
   - Validate: all bitrates playable, metadata correct
   - Performance: upload <30s, transcoding <2 minutes

3. **Phase 3 (Distribution Workflows):**
   - E2E: Trigger distribution → S3 replication to 3 regions
   - CDN invalidation → edge locations serve new content
   - Validate: content accessible from all regions, latency <200ms

4. **Phase 4 (Full Pipeline):**
   - Complete journey: Upload → Transcode → Distribute → Playback from 3 regions
   - Simulate users in US, EU, Asia requesting same video
   - Validate: correct edge served, low latency, no buffering
   - Failure scenarios: S3 region down → fallback to nearest region

**Output:**  
- 12-20 E2E tests
- Multi-region infrastructure validated
- Complete content pipeline tested
- Performance SLAs verified (latency <200ms)
- Quality: 9.5+/10
- Execution: 25-40 minutes (due to transcoding time)

---

## 🎯 Testing Rules Decision Matrix

**When to use each rule:**

| Scenario | Use This Rule | Why |
|----------|---------------|-----|
| Testing payment calculation logic | @unit-test-build.mdc | Isolated business rules, mock payment gateways |
| Testing 3 microservices together | @integration-test-build.mdc | Module contracts, real message queue |
| Testing complete signup → paid customer | @e2e-test-build.mdc | Complete user journey, real infrastructure |
| Complex algorithm (reorder point) | @unit-test-build.mdc | Fast feedback, edge cases, property-based tests |
| Service API contracts | @integration-test-build.mdc | Validate schemas, error codes, auth |
| Multi-region content delivery | @e2e-test-build.mdc | Infrastructure complexity, geo-routing, CDN |
| 100+ unit tests taking 10 seconds | @unit-test-build.mdc Phase 4 | Strategic performance optimization |
| Service integration failing | @integration-test-build.mdc + @test-to-success | Fix contract violations, validate flows |
| E2E tests flaky (50% pass rate) | @e2e-test-build.mdc + @test-qualification | Identify false positives, fix timing issues |

---

## 🔗 Testing Rules Integration Pattern

**Complete testing workflow:**

```bash
# Step 1: Build unit tests (foundation)
"Execute all phases using @unit-test-build.mdc method"
# Result: 100-200 unit tests, 100% critical path coverage, <5s execution

# Step 2: Add integration tests (contracts)
"Execute all phases using @integration-test-build.mdc method"
# Result: 20-50 integration tests, module contracts validated, <5min execution

# Step 3: Add E2E tests (critical journeys)
"Execute all phases using @e2e-test-build.mdc method"
# Result: 10-30 E2E tests, complete workflows validated, <30min execution

# Step 4: Quality validation (all levels)
"check all tests using @test-qualification.mdc method"
# Result: 0 false positives, P0/P1 criteria met, production-ready

# Step 5: Fix failures (if any)
"bring tests to 100% success using @test-to-success.mdc method"
# Result: Systematic debugging, root cause analysis, all tests passing
```

**ROI Analysis:**
- Unit: High ROI (fast, cheap, comprehensive)
- Integration: Medium ROI (selective, contracts only)
- E2E: Low ROI (expensive, selective, critical workflows only)

---

🪶 *Next section:*  
Use Cases 21–23 → `test-qualification.mdc`, `test-to-success.mdc`, `meta.extract.mdc`
