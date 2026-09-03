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

- [X] T001 Create package skeleton and module init files under `src/models/`, `src/rules_engine/`, `src/promotion_engine/`, `src/audit_service/`, `src/shared/`, `tests/unit/`, and `tests/integration/`
- [X] T002 Add project dependencies for Pydantic v2 and pytest in `requirements.txt` and `requirements-dev.txt`
- [X] T003 [P] Configure pytest discovery and defaults in `pytest.ini`
- [X] T004 [P] Create shared pytest fixtures for tiers, members, and active promotions in `tests/conftest.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define core models and deterministic helpers required before implementing `earn()`.

**CRITICAL**: No user story work starts until this phase is complete.

- [X] T005 [P] Define tier and promotion schema models in `src/models/tier.py` and `src/models/promotion.py`
- [X] T006 [P] Define member balance/lifetime schema models in `src/models/member.py`
- [X] T007 [P] Define transaction and audit schema models in `src/models/transaction.py` and `src/models/audit.py`
- [X] T008 [P] Define shared enums and typed errors in `src/shared/types.py` and `src/shared/errors.py`
- [X] T009 Implement deterministic rounding and stable-selection helpers in `src/rules_engine/determinism.py`

**Checkpoint**: Foundation ready for earn story implementation.

---

## Phase 3: User Story 1 - Implement `earn()` with deterministic rules (Priority: P1) 🎯 MVP

**Goal**: Implement `earn()` to compute base points (`USD * 10`), apply tier multiplier, apply one active promotion with `promo_stackable=false`, return EARN transaction + updated balances, and generate audit log payload.

**Independent Test**: Running earn tests confirms points math, promotion behavior, non-stackable selection, balance/lifetime updates, transaction creation, and audit entry creation with no PII in output payload.

### Tests for User Story 1 (pytest) ⚠️

- [X] T010 [P] [US1] Add unit tests for base-point and tier-multiplier calculations in `tests/unit/rules_engine/test_earn_rules.py`
- [ ] T011 [P] [US1] Add unit tests for active-promotion filtering by date/category in `tests/unit/promotion_engine/test_eligibility.py`
- [X] T012 [P] [US1] Add unit tests enforcing `promo_stackable=false` deterministic single-promo selection in `tests/unit/promotion_engine/test_selection.py`
- [X] T013 [P] [US1] Add unit tests for earn audit payload creation and PII-safe fields in `tests/unit/audit_service/test_events.py`
- [X] T014 [US1] Add integration test for full `earn()` flow (transaction, balance, lifetime, audit) in `tests/integration/test_earn_flow.py`

### Implementation for User Story 1

- [ ] T015 [P] [US1] Implement promotion eligibility evaluation for earn context in `src/promotion_engine/eligibility.py`
- [ ] T016 [P] [US1] Implement deterministic non-stackable promotion selection in `src/promotion_engine/selection.py`
- [X] T017 [P] [US1] Implement promotion effect application for earn multipliers/bonus in `src/promotion_engine/application.py`
- [X] T018 [P] [US1] Implement EARN audit payload factory and output sanitizer in `src/audit_service/events.py` and `src/audit_service/sanitizer.py`
- [X] T019 [US1] Implement pure `earn()` composition function in `src/rules_engine/earn_rules.py` using deterministic helpers and promotion engine modules
- [X] T020 [US1] Implement audit write orchestration contract for earn events in `src/audit_service/writer.py`
- [X] T021 [US1] Update member state transition helpers for balance/lifetime increments in `src/models/member.py`

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
- [X] T023 [P] [US2] Add unit tests for insufficient-balance rejection in `tests/unit/redemption_service/test_validate.py`
- [ ] T024 [P] [US2] Add unit tests for REDEEM audit payload creation in `tests/unit/audit_service/test_events.py`
- [ ] T025 [US2] Add integration test for full `redeem()` flow (transaction, balance, audit) in `tests/integration/test_redeem_flow.py`

### Implementation for User Story 2

- [ ] T026 [P] [US2] Implement fixed reward cost rules for redemption in `src/rules_engine/redemption_rules.py`
- [ ] T027 [P] [US2] Implement redemption validation (including insufficient balance check) in `src/redemption_service/validate.py`
- [ ] T028 [P] [US2] Implement REDEEM audit payload factory and sanitizer integration in `src/audit_service/events.py` and `src/audit_service/sanitizer.py`
- [X] T029 [US2] Implement `redeem()` orchestration that emits REDEEM transaction and updated balance in `src/redemption_service/process.py`

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

- [X] T034 [P] [US3] Implement pure tier threshold evaluator using lifetime points in `src/rules_engine/tier_rules.py`
- [X] T035 [P] [US3] Implement `recalc_tier()` decision function that returns prior tier when unchanged and new tier when crossed in `src/tier_recalculation_service/evaluate.py`
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

---

## Phase 7: User Story 4 - Promotion Engine (EARN_MULTIPLIER, BONUS_POINTS, REDEEM_DISCOUNT) (Priority: P1)

**Goal**: Deliver a standalone, pure promotion evaluation module that returns exactly one applied
promotion per transaction. Support the three promotion types from the dataset (`PROMO-1`
EARN_MULTIPLIER, `PROMO-2` BONUS_POINTS, `PROMO-3` REDEEM_DISCOUNT). Enforce three invariants on
every evaluation: (1) only promotions whose `[start, end]` UTC window contains the transaction date
are active; (2) `promo_stackable=false` reduces the candidate pool to exactly one promotion via a
deterministic tie-breaker (ascending `promotion.id`); (3) at most one promotion is applied per
transaction (apply-once-per-transaction).

**Non-Impact Guarantee**: All work in this phase is additive. Task IDs T001–T039 and their file
paths are untouched. New behavior is exposed through a new public entrypoint
`evaluate_promotion(ctx, promotions, config)` in a new module `src/promotion_engine/engine.py`;
existing `earn()` (T019) and `redeem()` (T029) signatures and semantics remain unchanged. Any
extension to `src/promotion_engine/eligibility.py`, `selection.py`, or `application.py` (from
T015–T017, T027) MUST be additive (new functions only) and MUST NOT alter functions already
consumed by US1/US2.

**Independent Test**: Running `pytest tests/unit/promotion_engine/ tests/integration/test_promotion_engine_flow.py`
verifies each promotion type in isolation, the non-stackable invariant across mixed candidate
pools, and deterministic replay for identical inputs.

### Foundational Extensions for User Story 4 (additive)

- [ ] T040 [P] [US4] Extend `src/models/promotion.py` with `PromotionType` enum (`EARN_MULTIPLIER`, `BONUS_POINTS`, `REDEEM_DISCOUNT`), `Promotion` fields `type`, `value`, `start`, `end`, optional `applies_to: list[Category]`, optional `threshold_stays: int` — additive, do not remove fields relied on by earn() from T005
- [ ] T041 [P] [US4] Add `PromotionContext` (member id, `kind: Literal["EARN","REDEEM"]`, category, transaction date UTC, spend USD, completed stays count, requested redeem points) and `PromotionOutcome` (promo id or None, `effect: PromotionEffect`, `multiplier: float|None`, `bonus_points: int|None`, `discounted_cost: int|None`, `reason: PromotionReason`) Pydantic v2 models in `src/models/promotion.py`
- [ ] T042 [P] [US4] Add `PromotionConfig(promo_stackable: bool = False)` model in `src/models/promotion.py`
- [ ] T043 [P] [US4] Extend `src/shared/types.py` (additive) with `PromotionEffect` (`EARN_MULTIPLIER`, `BONUS_POINTS`, `REDEEM_DISCOUNT`, `NONE`) and `PromotionReason` (`EARN_MULTIPLIER_APPLIED`, `BONUS_POINTS_APPLIED`, `REDEEM_DISCOUNT_APPLIED`, `NO_ACTIVE_PROMOTION`, `NOT_APPLICABLE`, `STACKING_DISABLED`)
- [ ] T044 [US4] Implement dataset-backed promotion loader in `src/promotion_engine/loader.py` that reads `.specify/capstone2_loyalty_dataset.json` and returns a validated `list[Promotion]`

### Tests for User Story 4 (pytest) ⚠️

- [ ] T045 [P] [US4] Add unit tests for inclusive UTC window filtering (boundary dates 2026-09-20, 2026-09-22, 2026-09-19, 2026-09-23) in `tests/unit/promotion_engine/test_eligibility_active_window.py`
- [ ] T046 [P] [US4] Add unit tests for EARN_MULTIPLIER eligibility (ROOM match, FLIGHT non-match, out-of-window non-match) in `tests/unit/promotion_engine/test_eligibility_earn_multiplier.py`
- [ ] T047 [P] [US4] Add unit tests for BONUS_POINTS eligibility gated by `threshold_stays == ctx.completed_stays` (1st, 2nd, 3rd, 4th stay) in `tests/unit/promotion_engine/test_eligibility_bonus_points.py`
- [ ] T048 [P] [US4] Add unit tests for REDEEM_DISCOUNT eligibility (FLIGHT match inside 2026-10-01..2026-10-31, ROOM non-match, out-of-window non-match) in `tests/unit/promotion_engine/test_eligibility_redeem_discount.py`
- [ ] T049 [P] [US4] Add unit tests enforcing `promo_stackable=False` single-promo selection with deterministic ascending-id tie-breaker (two EARN_MULTIPLIER matches → one chosen; mixed EARN_MULTIPLIER + BONUS_POINTS → one chosen) in `tests/unit/promotion_engine/test_selection_single_promo.py`
- [ ] T050 [P] [US4] Add unit tests for `apply_earn_multiplier` outcome (`effect=EARN_MULTIPLIER`, `multiplier == promotion.value`, `reason=EARN_MULTIPLIER_APPLIED`) in `tests/unit/promotion_engine/test_application_earn_multiplier.py`
- [ ] T051 [P] [US4] Add unit tests for `apply_bonus_points` outcome (`effect=BONUS_POINTS`, `bonus_points == int(promotion.value)`, `reason=BONUS_POINTS_APPLIED`) in `tests/unit/promotion_engine/test_application_bonus_points.py`
- [ ] T052 [P] [US4] Add unit tests for `apply_redeem_discount` cost math (`discounted_cost == floor(ctx.requested_redeem_points * (1 - promotion.value))`, `reason=REDEEM_DISCOUNT_APPLIED`) in `tests/unit/promotion_engine/test_application_redeem_discount.py`
- [ ] T053 [P] [US4] Add unit tests for apply-once-per-transaction invariant on `evaluate_promotion` (returns exactly one `PromotionOutcome`, and `NO_ACTIVE_PROMOTION` when nothing matches) in `tests/unit/promotion_engine/test_engine_invariants.py`
- [ ] T054 [US4] Add integration test covering all three promotion types end-to-end with dataset promotions plus a deterministic replay assertion (two runs, identical outcome) in `tests/integration/test_promotion_engine_flow.py`

### Implementation for User Story 4

- [ ] T055 [P] [US4] Add (do not modify existing) helpers `is_active(promotion, ctx_date)`, `list_active_earn_multiplier_promotions(promotions, ctx)`, `list_active_bonus_points_promotions(promotions, ctx)`, and `list_active_redeem_discount_promotions(promotions, ctx)` to `src/promotion_engine/eligibility.py`
- [ ] T056 [P] [US4] Add (do not modify existing) `select_single_promotion(candidates, config)` in `src/promotion_engine/selection.py` that raises/returns empty when `candidates` is empty, returns the single element when `len == 1`, and when `config.promo_stackable is False` returns the candidate with the lexicographically smallest `id`; leave existing selection helpers used by T016 intact
- [ ] T057 [P] [US4] Add (do not modify existing) `apply_earn_multiplier(promotion, ctx)`, `apply_bonus_points(promotion, ctx)`, and `apply_redeem_discount(promotion, ctx)` returning `PromotionOutcome` in `src/promotion_engine/application.py`
- [ ] T058 [US4] Implement public entrypoint `evaluate_promotion(ctx, promotions, config)` in new file `src/promotion_engine/engine.py`: for `ctx.kind == "EARN"` combine EARN_MULTIPLIER + BONUS_POINTS candidates into one pool, then `select_single_promotion` → dispatch to matching application function; for `ctx.kind == "REDEEM"` route through REDEEM_DISCOUNT candidates only; return an outcome with `promo_id=None`, `effect=NONE`, and `reason=NO_ACTIVE_PROMOTION` (or `NOT_APPLICABLE`) when no candidate matches
- [ ] T059 [US4] Export `evaluate_promotion`, `PromotionContext`, `PromotionOutcome`, `PromotionConfig` from `src/promotion_engine/__init__.py` so downstream services can adopt it without touching existing earn()/redeem() call sites in this phase

**Checkpoint**: US4 is independently functional and testable; `earn()`, `redeem()`, and
`recalc_tier()` from US1–US3 continue to pass their existing tests unchanged.

### Dependencies within Phase 7

- Foundational extensions (T040–T044) before tests and implementation.
- Tests (T045–T054) written first and expected to fail before implementation lands.
- Eligibility (T055), selection (T056), and application (T057) can proceed in parallel after models exist.
- Engine wiring (T058) depends on T055–T057.
- Package export (T059) depends on T058.

### Parallel Opportunities within Phase 7

- Foundational: T040–T043 in parallel; T044 after models exist.
- Tests: T045–T053 in parallel; T054 after unit tests are drafted.
- Implementation: T055, T056, and T057 in parallel; T058 depends on T055–T057; T059 depends on T058.

### Parallel Example: User Story 4

```bash
Task: "T045 tests/unit/promotion_engine/test_eligibility_active_window.py"
Task: "T046 tests/unit/promotion_engine/test_eligibility_earn_multiplier.py"
Task: "T047 tests/unit/promotion_engine/test_eligibility_bonus_points.py"
Task: "T048 tests/unit/promotion_engine/test_eligibility_redeem_discount.py"
Task: "T049 tests/unit/promotion_engine/test_selection_single_promo.py"
```

```bash
Task: "T055 src/promotion_engine/eligibility.py (add per-type filters + is_active)"
Task: "T056 src/promotion_engine/selection.py (add select_single_promotion)"
Task: "T057 src/promotion_engine/application.py (add three apply_* functions)"
```

### US4 Notes

- Phase 7 depends on Phase 2 (Foundational). It does NOT depend on completion of US1, US2, or US3
  and MAY run in parallel with them because it only adds new symbols and a new module file.
- `evaluate_promotion` is a pure function; audit emission and persistence remain the
  responsibility of the earn/redeem services (T020, T029) and are out of scope here.
- Rounding for REDEEM_DISCOUNT uses `math.floor` for deterministic replay.
- Tie-breaker for non-stackable selection is ascending `promotion.id` (stable, string comparison)
  so identical inputs always yield the same outcome.

---

## Phase 8: User Story 5 - Approval Gate for High-Value Redemptions (Priority: P1)

**Goal**: Add an approval-gate decision layer for redemptions so requests strictly greater than
`30000` points enter a pending approval state, do not commit a redemption ledger entry or balance
mutation until approved, and produce an audit decision for every approval-gate outcome.

**Non-Impact Guarantee**: All work in this phase is additive around `src/redemption_service/approvals.py`
and approval-specific audit helpers. Existing `earn()`, `redeem()`, `recalc_tier()`, and promotion
engine public behavior MUST remain unchanged. The current `redeem()` orchestration from T029 is not
modified in this phase except through a new optional approval-aware wrapper that preserves the old
redemption path for requests at or below `30000` points.

**Independent Test**: Running `pytest tests/unit/redemption_service/test_approvals.py tests/unit/audit_service/test_approval_events.py tests/integration/test_approval_gate_flow.py`
verifies that `30000` points is processed without approval, `30001` and higher points are routed to
pending approval, no balance or ledger commit occurs while pending, approved decisions commit through
the existing redemption path, rejected decisions do not commit, and every decision produces an audit
payload.

### Tests for User Story 5 (pytest) ⚠️

- [ ] T060 [P] [US5] Add unit tests for approval threshold decisions (`30000` requires no approval, `30001` requires approval, `40000` requires approval) in `tests/unit/redemption_service/test_approvals.py`
- [ ] T061 [P] [US5] Add unit tests asserting pending approval decisions return `commit_allowed=False`, no ledger entry, and no balance delta in `tests/unit/redemption_service/test_approvals.py`
- [ ] T062 [P] [US5] Add unit tests asserting approved high-value decisions return `commit_allowed=True` and include the original redemption request reference in `tests/unit/redemption_service/test_approvals.py`
- [ ] T063 [P] [US5] Add unit tests asserting rejected high-value decisions return `commit_allowed=False`, preserve balance, and include rejection reason code in `tests/unit/redemption_service/test_approvals.py`
- [ ] T064 [P] [US5] Add unit tests for approval-gate audit payload creation for `AUTO_APPROVED`, `PENDING_APPROVAL`, `APPROVED`, and `REJECTED` decisions in `tests/unit/audit_service/test_approval_events.py`
- [ ] T065 [P] [US5] Add unit tests proving approval-gate audit payloads contain non-PII member identifiers only in `tests/unit/audit_service/test_approval_events.py`
- [ ] T066 [US5] Add integration test for automated redemption at exactly `30000` points that uses the existing redeem path, commits once, and audits the auto-approved decision in `tests/integration/test_approval_gate_flow.py`
- [ ] T067 [US5] Add integration test for `40000` point redemption request that enters pending approval, creates no redeem ledger entry, leaves balance unchanged, and audits the pending decision in `tests/integration/test_approval_gate_flow.py`
- [ ] T068 [US5] Add integration test for approved pending request that commits through the existing redemption process exactly once and audits both approval and commit decisions in `tests/integration/test_approval_gate_flow.py`
- [ ] T069 [US5] Add integration test for rejected pending request that never commits redemption, leaves balance unchanged, and audits the rejection in `tests/integration/test_approval_gate_flow.py`

### Implementation for User Story 5

- [ ] T070 [P] [US5] Define approval decision enums (`AUTO_APPROVED`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`) and approval reason codes (`UNDER_THRESHOLD`, `REQUIRES_HUMAN_APPROVAL`, `HUMAN_APPROVED`, `HUMAN_REJECTED`) additively in `src/shared/types.py`
- [ ] T071 [P] [US5] Define `ApprovalGateConfig(threshold_points=30000)`, `ApprovalRequest`, and `ApprovalDecision` Pydantic v2 models in `src/models/redemption.py`
- [ ] T072 [P] [US5] Implement pure `evaluate_approval_gate(request, config)` in `src/redemption_service/approvals.py` where `requested_points > threshold_points` returns pending approval and `requested_points <= threshold_points` returns auto-approved
- [ ] T073 [P] [US5] Implement pure `record_human_approval(request, approver_id, approved, reason)` in `src/redemption_service/approvals.py` that converts a pending request into an approved or rejected `ApprovalDecision` without committing redemption
- [ ] T074 [P] [US5] Implement `create_approval_audit_event(decision, before_balance, after_balance=None)` in `src/audit_service/events.py` that emits one audit payload for every approval-gate decision and never includes direct PII
- [ ] T075 [US5] Implement optional approval-aware wrapper `redeem_with_approval_gate(request, member_state, config)` in `src/redemption_service/process.py` that calls existing `redeem()` only when `commit_allowed=True` and otherwise returns a pending decision with no ledger entry or balance mutation
- [ ] T076 [US5] Export approval-gate helpers from `src/redemption_service/__init__.py` so callers can opt in without changing existing `redeem()` call sites

**Checkpoint**: US5 is independently functional and testable; existing earn, redeem, tier, and
promotion tests continue to pass unchanged.

### Dependencies within Phase 8

- Models and enums (T070-T071) before approval service implementation.
- Tests (T060-T069) written first and expected to fail before implementation lands.
- Approval gate (T072), human decision recording (T073), and audit event creation (T074) can proceed
  in parallel after models exist.
- Approval-aware wrapper (T075) depends on T072-T074 and the existing redeem orchestration from T029.
- Package export (T076) depends on T075.

### Parallel Opportunities within Phase 8

- Tests: T060-T065 in parallel; T066-T069 after unit tests are drafted.
- Implementation: T070 and T071 in parallel; T072, T073, and T074 in parallel after models exist;
  T075 after T072-T074; T076 after T075.

### Parallel Example: User Story 5

```bash
Task: "T060 tests/unit/redemption_service/test_approvals.py (threshold boundaries)"
Task: "T061 tests/unit/redemption_service/test_approvals.py (pending no-commit)"
Task: "T064 tests/unit/audit_service/test_approval_events.py (decision audit payloads)"
Task: "T065 tests/unit/audit_service/test_approval_events.py (PII-safe audit payloads)"
```

```bash
Task: "T072 src/redemption_service/approvals.py (evaluate approval gate)"
Task: "T073 src/redemption_service/approvals.py (record human approval)"
Task: "T074 src/audit_service/events.py (approval audit events)"
```

### US5 Notes

- The approval rule is strict: only `requested_points > 30000` requires human approval; exactly
  `30000` points remains automated.
- Pending or rejected approval decisions MUST NOT create a redeem ledger entry and MUST NOT mutate
  member balance.
- Approved decisions commit by reusing the existing redemption path to avoid duplicate redemption
  logic and preserve current insufficient-balance validation.
- Every approval-gate decision, including automated under-threshold approval, pending approval,
  human approval, and human rejection, MUST produce one audit payload.

