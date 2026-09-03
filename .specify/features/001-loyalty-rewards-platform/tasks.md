# Tasks: Loyalty & Rewards Engine earn(), redeem(), and recalc_tier() implementation

**Input**: Design documents from `.specify/features/001-loyalty-rewards-platform/`

**Prerequisites**: `plan.md` (required), `spec.md` (required), `.specify/capstone2_loyalty_dataset.json`

**Tests**: Included (pytest requested)

**Organization**: Tasks are grouped by user story for independent implementation and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependency)
- **[Story]**: User story label (`[US1]` earn flow, `[US2]` redeem flow, `[US3]` tier recalculation flow)
- Every task includes explicit file path(s)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare Python/Pydantic/pytest scaffolding for rule-centric implementation.

- [ ] T001 Create package skeleton and module init files under `src/models/`, `src/rules_engine/`, `src/promotion_engine/`, `src/audit_service/`, `src/shared/`, `tests/unit/`, and `tests/integration/`
- [ ] T002 Add project dependencies for Pydantic v2 and pytest in `requirements.txt` and `requirements-dev.txt`
- [ ] T003 [P] Configure pytest discovery and defaults in `pytest.ini`
- [ ] T004 [P] Create shared pytest fixtures for tiers, members, and active promotions in `tests/conftest.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define core models and deterministic helpers required before implementing `earn()`.

**CRITICAL**: No user story work starts until this phase is complete.

- [ ] T005 [P] Define tier and promotion schema models in `src/models/tier.py` and `src/models/promotion.py`
- [ ] T006 [P] Define member balance/lifetime schema models in `src/models/member.py`
- [ ] T007 [P] Define transaction and audit schema models in `src/models/transaction.py` and `src/models/audit.py`
- [ ] T008 [P] Define shared enums and typed errors in `src/shared/types.py` and `src/shared/errors.py`
- [ ] T009 Implement deterministic rounding and stable-selection helpers in `src/rules_engine/determinism.py`

**Checkpoint**: Foundation ready for earn story implementation.

---

## Phase 3: User Story 1 - Implement `earn()` with deterministic rules (Priority: P1) 🎯 MVP

**Goal**: Implement `earn()` to compute base points (`USD * 10`), apply tier multiplier, apply one active promotion with `promo_stackable=false`, return EARN transaction + updated balances, and generate audit log payload.

**Independent Test**: Running earn tests confirms points math, promotion behavior, non-stackable selection, balance/lifetime updates, transaction creation, and audit entry creation with no PII in output payload.

### Tests for User Story 1 (pytest) ⚠️

- [ ] T010 [P] [US1] Add unit tests for base-point and tier-multiplier calculations in `tests/unit/rules_engine/test_earn_rules.py`
- [ ] T011 [P] [US1] Add unit tests for active-promotion filtering by date/category in `tests/unit/promotion_engine/test_eligibility.py`
- [ ] T012 [P] [US1] Add unit tests enforcing `promo_stackable=false` deterministic single-promo selection in `tests/unit/promotion_engine/test_selection.py`
- [ ] T013 [P] [US1] Add unit tests for earn audit payload creation and PII-safe fields in `tests/unit/audit_service/test_events.py`
- [ ] T014 [US1] Add integration test for full `earn()` flow (transaction, balance, lifetime, audit) in `tests/integration/test_earn_flow.py`

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement promotion eligibility evaluation for earn context in `src/promotion_engine/eligibility.py`
- [ ] T016 [P] [US1] Implement deterministic non-stackable promotion selection in `src/promotion_engine/selection.py`
- [ ] T017 [P] [US1] Implement promotion effect application for earn multipliers/bonus in `src/promotion_engine/application.py`
- [ ] T018 [P] [US1] Implement EARN audit payload factory and output sanitizer in `src/audit_service/events.py` and `src/audit_service/sanitizer.py`
- [ ] T019 [US1] Implement pure `earn()` composition function in `src/rules_engine/earn_rules.py` using deterministic helpers and promotion engine modules
- [ ] T020 [US1] Implement audit write orchestration contract for earn events in `src/audit_service/writer.py`
- [ ] T021 [US1] Update member state transition helpers for balance/lifetime increments in `src/models/member.py`

**Checkpoint**: User Story 1 is independently functional and testable.

---

## Phase 4: User Story 2 - Implement `redeem()` with deterministic rules (Priority: P1)

**Goal**: Implement `redeem()` to enforce fixed reward costs (Award Night `15000`, Suite Award
`40000`), reject insufficient balances, return REDEEM transaction + updated balance, and generate
audit log payload.

**Independent Test**: Running redeem tests confirms rule-cost mapping, insufficient-balance
rejection behavior, transaction creation, balance update, and audit entry creation.

### Tests for User Story 2 (pytest) ⚠️

- [ ] T022 [P] [US2] Add unit tests for fixed redemption cost lookup (Award Night and Suite Award) in `tests/unit/rules_engine/test_redemption_rules.py`
- [ ] T023 [P] [US2] Add unit tests for insufficient-balance rejection in `tests/unit/redemption_service/test_validate.py`
- [ ] T024 [P] [US2] Add unit tests for REDEEM audit payload creation in `tests/unit/audit_service/test_events.py`
- [ ] T025 [US2] Add integration test for full `redeem()` flow (transaction, balance, audit) in `tests/integration/test_redeem_flow.py`

### Implementation for User Story 2

- [ ] T026 [P] [US2] Implement fixed reward cost rules for redemption in `src/rules_engine/redemption_rules.py`
- [ ] T027 [P] [US2] Implement redemption validation (including insufficient balance check) in `src/redemption_service/validate.py`
- [ ] T028 [P] [US2] Implement REDEEM audit payload factory and sanitizer integration in `src/audit_service/events.py` and `src/audit_service/sanitizer.py`
- [ ] T029 [US2] Implement `redeem()` orchestration that emits REDEEM transaction and updated balance in `src/redemption_service/process.py`

**Checkpoint**: User Story 2 is independently functional and testable.

---

## Phase 5: User Story 3 - Implement `recalc_tier()` using lifetime points thresholds (Priority: P1)

**Goal**: Implement `recalc_tier()` to evaluate `lifetime_points` against thresholds (BASE `>=0`,
SILVER `>=10000`, GOLD `>=30000`, PLATINUM `>=75000`) and return the new tier when a threshold
crossing occurs.

**Independent Test**: Running tier tests confirms deterministic threshold mapping, boundary handling,
and changed-tier return semantics.

### Tests for User Story 3 (pytest) ⚠️

- [ ] T030 [P] [US3] Add unit tests for lifetime-point threshold mapping in `tests/unit/rules_engine/test_tier_rules.py`
- [ ] T031 [P] [US3] Add unit tests for boundary values (`0`, `9999`, `10000`, `29999`, `30000`, `74999`, `75000`) in `tests/unit/rules_engine/test_tier_rules.py`
- [ ] T032 [P] [US3] Add unit tests for "return new tier only when crossed" behavior in `tests/unit/tier_recalculation_service/test_evaluate.py`
- [ ] T033 [US3] Add integration test validating tier transition event payload from `recalc_tier()` in `tests/integration/test_tier_flow.py`

### Implementation for User Story 3

- [ ] T034 [P] [US3] Implement pure tier threshold evaluator using lifetime points in `src/rules_engine/tier_rules.py`
- [ ] T035 [P] [US3] Implement `recalc_tier()` decision function that returns prior tier when unchanged and new tier when crossed in `src/tier_recalculation_service/evaluate.py`
- [ ] T036 [US3] Implement orchestration wrapper that emits tier change payload only on change in `src/tier_recalculation_service/recalculate.py`

**Checkpoint**: User Story 3 is independently functional and testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate completeness and keep behavior explainable.

- [ ] T037 [P] Add reason-code assertions for tier recalculation outcomes in `tests/unit/tier_recalculation_service/test_evaluate.py`
- [ ] T038 [P] Add deterministic replay test for repeated identical `recalc_tier()` input in `tests/integration/test_tier_flow.py`
- [ ] T039 Document tier-recalculation behavior and assumptions in `.specify/features/001-loyalty-rewards-platform/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1 completion.
- **Phase 3 (US1)**: Depends on Phase 2 completion.
- **Phase 4 (US2)**: Depends on Phase 2 completion.
- **Phase 5 (US3)**: Depends on Phase 2 completion.
- **Phase 6 (Polish)**: Depends on Phase 3, Phase 4, and Phase 5 completion.

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational phase; no dependency on additional stories.
- **US2 (P1)**: Can start after Foundational phase; no dependency on additional stories.
- **US3 (P1)**: Can start after Foundational phase; no dependency on additional stories.

### Within User Story 1

- Tests (T010-T014) are written first and expected to fail before implementation.
- Promotion engine implementation (T015-T017) precedes `earn()` composition (T019).
- Audit payload factory (T018) and writer contract (T020) complete before integration assertions finalize.

### Within User Story 2

- Tests (T022-T025) are written first and expected to fail before implementation.
- Fixed-cost rules (T026) and validation (T027) precede redeem orchestration (T029).
- Audit payload factory integration (T028) completes before final integration assertions.

### Within User Story 3

- Tests (T030-T033) are written first and expected to fail before implementation.
- Threshold evaluator (T034) precedes recalc decision logic (T035).
- Orchestration wrapper (T036) follows decision logic and is validated by integration tests.

### Parallel Opportunities

- Setup: T003 and T004 can run in parallel after T002.
- Foundational: T005-T008 can run in parallel; T009 after shared types.
- US1 Tests: T010-T013 can run in parallel; T014 after unit tests are drafted.
- US1 Implementation: T015-T018 can run in parallel; T019 depends on T015-T018.
- US2 Tests: T022-T024 can run in parallel; T025 after unit tests are drafted.
- US2 Implementation: T026-T028 can run in parallel; T029 depends on T026-T028.
- US3 Tests: T030-T032 can run in parallel; T033 after unit tests are drafted.
- US3 Implementation: T034 and T035 can run in parallel after tests; T036 depends on T034-T035.
- Polish: T037 and T038 can run in parallel; T039 after tests stabilize.

---

## Parallel Example: User Story 1

```bash
Task: "T010 Add unit tests in tests/unit/rules_engine/test_earn_rules.py"
Task: "T011 Add eligibility tests in tests/unit/promotion_engine/test_eligibility.py"
Task: "T012 Add selection tests in tests/unit/promotion_engine/test_selection.py"
Task: "T013 Add audit event tests in tests/unit/audit_service/test_events.py"
```

```bash
Task: "T015 Implement src/promotion_engine/eligibility.py"
Task: "T016 Implement src/promotion_engine/selection.py"
Task: "T017 Implement src/promotion_engine/application.py"
Task: "T018 Implement src/audit_service/events.py and src/audit_service/sanitizer.py"
```

## Parallel Example: User Story 2

```bash
Task: "T022 Add unit tests in tests/unit/rules_engine/test_redemption_rules.py"
Task: "T023 Add validation tests in tests/unit/redemption_service/test_validate.py"
Task: "T024 Add audit event tests in tests/unit/audit_service/test_events.py"
```

```bash
Task: "T026 Implement src/rules_engine/redemption_rules.py"
Task: "T027 Implement src/redemption_service/validate.py"
Task: "T028 Implement src/audit_service/events.py and src/audit_service/sanitizer.py"
```

## Parallel Example: User Story 3

```bash
Task: "T030 Add threshold mapping tests in tests/unit/rules_engine/test_tier_rules.py"
Task: "T031 Add boundary tests in tests/unit/rules_engine/test_tier_rules.py"
Task: "T032 Add transition-behavior tests in tests/unit/tier_recalculation_service/test_evaluate.py"
```

```bash
Task: "T034 Implement src/rules_engine/tier_rules.py"
Task: "T035 Implement src/tier_recalculation_service/evaluate.py"
```

---

## Implementation Strategy

### MVP First (earn + redeem + tier recalculation)

1. Complete Phase 1 and Phase 2.
2. Complete US1 tests first (T010-T014).
3. Implement US1 logic (T015-T021).
4. Complete US2 tests first (T022-T025).
5. Implement US2 logic (T026-T029).
6. Complete US3 tests first (T030-T033).
7. Implement US3 logic (T034-T036).
8. Validate with deterministic replay and polish tasks (T037-T039).

### Incremental Delivery

1. Deliver earn points math + tier multiplier.
2. Add redeem fixed-cost rules + insufficient-balance rejection.
3. Add lifetime-point tier recalculation with threshold crossing detection.
4. Add transaction/audit payload generation for earn and redeem.
5. Finalize replay and reason-code hardening.

---

## Notes

- All task paths align with `plan.md` module boundaries.
- `earn()` remains pure by returning computed state and event payloads; side-effect persistence is handled by orchestration adapters.
- `redeem()` applies fixed reward-point costs and returns commit-ready state + events.
- `recalc_tier()` uses deterministic lifetime-point thresholds and returns changed-tier outcomes.
- Task list is scoped to requested earn/redeem/tier-recalc slices with pytest coverage.

