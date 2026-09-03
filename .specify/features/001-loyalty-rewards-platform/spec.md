# Specification: Dataset-Driven Loyalty & Rewards Rules

**Feature ID**: `001-loyalty-rewards-platform`
**Created**: 2026-09-03
**Status**: Updated Specification - Ready for Planning
**Version**: 2.1

---

## Overview

This specification defines a deterministic Loyalty & Rewards Engine using the provided dataset
(`.specify/capstone2_loyalty_dataset.json`) as the source of business rules and sample behavior.
The scope of this update is limited to rule extraction and acceptance behavior for earn,
redemption, tiering, promotions, and human approval gating.

## User Scenarios & Testing

### Primary User Story
As a loyalty program operator, I want the system to apply earning, redemption, tier, and promotion
rules consistently so that balances are correct, auditable, and safe to expose.

### Acceptance Scenarios Summary
1. Calculate points earned from spend using base points and tier multiplier.
2. Apply valid promotion benefits according to promotion type and date window.
3. Prevent invalid redemption and enforce points non-negativity.
4. Recalculate or validate member tier from configured thresholds.
5. Require human approval for high-value redemption requests.
6. Create an audit entry for every successful earn and redeem event.

### Edge Cases
- Promotion is active by date but does not apply to transaction category.
- Two promotions are simultaneously eligible while `promo_stackable = false`.
- Redemption request equals available balance versus exceeds available balance.
- High-value redemption at exactly 30000 points versus above 30000 points.

## Rule Extraction from Dataset

### Earn Rules
- Base earning rate is `10` points per USD.
- Tier multipliers are: BASE `1.0`, SILVER `1.1`, GOLD `1.25`, PLATINUM `1.5`.
- Earn points are calculated as `eligible_spend_usd * base_points_per_usd * tier_multiplier`.
- Deterministic rounding rule: earned points are rounded down to the nearest whole point.

### Redemption Rules
- Award night requires `15000` points.
- Suite award requires `40000` points.
- Monetary value reference is `0.007` USD per point for valuation/reporting.
- Redemption points are represented as negative deltas in the transaction ledger.
- A redemption is rejected if it would produce a negative points balance.

### Tier Rules
- Tier thresholds are configured by minimum lifetime points:
  - BASE: `0`
  - SILVER: `10000`
  - GOLD: `30000`
  - PLATINUM: `75000`
- The effective tier is the highest tier whose `min_points` is less than or equal to member
  lifetime points.

### Promotion Rules
- `PROMO-1` Double Points Weekend: type `EARN_MULTIPLIER`, multiplier `2.0`, valid
  `2026-09-20` to `2026-09-22`, applies to `ROOM`.
- `PROMO-2` 5k Bonus on 3rd Stay: type `BONUS_POINTS`, adds `5000` points on qualifying third
  stay, valid `2026-09-01` to `2026-12-31`.
- `PROMO-3` Flight Redemption -20%: type `REDEEM_DISCOUNT`, value `0.2`, valid
  `2026-10-01` to `2026-10-31`, applies to `FLIGHT`.
- Promotion stacking is disabled (`promo_stackable = false`); at most one promotion may apply per
  transaction.

### Human Approval Rule
- Any redemption request strictly greater than `30000` points requires explicit human approval
  before final commitment.
- Requests at or below `30000` follow automated policy checks only.

## Functional Requirements

- **FR-001 Earn Calculation**: The system MUST calculate earned points using base points per USD,
  member tier multiplier, and deterministic rounding.
- **FR-002 Earn Validation**: The system MUST reject earn requests with invalid amounts,
  unsupported categories, or missing member identifiers.
- **FR-003 Redemption Validation**: The system MUST reject redemptions that exceed available
  balance or violate reward policy.
- **FR-004 Redemption Commitment**: On successful redemption, the system MUST persist a single
  negative ledger entry and update available balance atomically.
- **FR-005 Tier Resolution**: The system MUST determine member tier from configured threshold
  rules and apply corresponding earn multiplier.
- **FR-006 Promotion Eligibility**: The system MUST evaluate promotions by date window, transaction
  type, and applicability scope.
- **FR-007 Promotion Exclusivity**: When multiple promotions could apply, the system MUST select
  exactly one applicable promotion because stacking is disabled.
- **FR-008 Human Gate Enforcement**: The system MUST route redemptions above 30000 points to a
  human approval state and MUST NOT finalize until approved.
- **FR-009 Audit Logging**: Every successful earn and redeem operation MUST create an immutable
  audit log entry with event ID, member ID, before/after balances, rule version, and timestamp.
- **FR-010 No Silent Mutations**: The system MUST prohibit any balance mutation that lacks a
  corresponding committed ledger and audit event.
- **FR-011 Deterministic Replay**: Replaying the same ordered transaction inputs against the same
  rule set MUST produce identical balances and tiers.
- **FR-012 Privacy-Safe Outputs**: Standard outputs MUST expose non-PII identifiers only and MUST
  not include member names or email addresses unless explicitly authorized.

## Non-Functional Requirements

- **NFR-001 Determinism**: For identical validated inputs and rule versions, output balances,
  tiers, and audit payloads are identical.
- **NFR-002 Consistency**: Balance update and ledger/audit persistence for earn/redeem complete as
  one atomic unit.
- **NFR-003 Traceability**: 100% of successful earn/redeem events are queryable by transaction ID
  and include full before/after state.
- **NFR-004 Integrity**: The system never returns a committed state where available points are
  negative.
- **NFR-005 Privacy**: Default customer-visible and operational outputs avoid direct PII exposure.
- **NFR-006 Explainability**: Decision responses include machine-readable reason codes for
  acceptance/rejection and approval-gate routing.
- **NFR-007 Time Handling**: Rule windows are evaluated in UTC with ISO-8601 timestamps.

## Gherkin Acceptance Criteria

```gherkin
Feature: Loyalty and rewards rule execution

  Scenario: Calculate earn points using tier multiplier
	Given a member with tier "GOLD"
	And base points per USD is 10
	When the member earns on a qualifying 200 USD room spend
	Then earned points are 2500
	And an earn audit log is created

  Scenario: Apply earn multiplier promotion within valid window
	Given promotion "PROMO-1" is active for ROOM from 2026-09-20 to 2026-09-22
	And promotion stacking is disabled
	When a qualifying ROOM earn occurs on 2026-09-21
	Then the selected promotion is "PROMO-1"
	And points are multiplied by 2.0

  Scenario: Do not apply promotion outside category scope
	Given promotion "PROMO-1" applies only to ROOM
	When an earn transaction category is FLIGHT on 2026-09-21
	Then "PROMO-1" is not applied

  Scenario: Reject redemption when balance is insufficient
	Given a member has 12000 available points
	When the member requests an award night redemption of 15000 points
	Then the redemption is rejected
	And no balance change is committed
	And no redeem ledger entry is written

  Scenario: Allow automated redemption at threshold
	Given human approval is required for redemption over 30000 points
	And a member has 45000 available points
	When the member redeems 30000 points
	Then the redemption is processed without human approval
	And a redeem audit log is created

  Scenario: Route high-value redemption for manual approval
	Given human approval is required for redemption over 30000 points
	And a member has 90000 available points
	When the member requests 40000 points redemption
	Then the request enters pending human approval
	And no final balance change is committed until approval

  Scenario: Resolve tier from lifetime points thresholds
	Given tier thresholds include SILVER at 10000 and GOLD at 30000
	When a member has 31250 lifetime points
	Then the member tier is GOLD

  Scenario: Enforce non-stackable promotions
	Given two promotions are both eligible for the same transaction
	And promotion stacking is disabled
	When the transaction is evaluated
	Then exactly one promotion is applied
	And the choice is recorded in the audit payload

  Scenario: Guarantee deterministic replay
	Given a fixed ordered transaction list and unchanged rules
	When the engine is executed twice
	Then both runs produce identical balances, tiers, and audit entries
```

## Assumptions

- Spend amount and transaction category are provided in earn requests even though the dataset
  transaction samples already contain computed points.
- Third-stay counting for `PROMO-2` is based on completed qualifying stay events per member.
- If multiple promotions are eligible and stacking is disabled, selection uses a deterministic
  precedence policy defined in planning.
- Time windows are inclusive of start and end dates in UTC.

## Success Criteria

- 100% of successful earn and redeem operations produce exactly one corresponding audit log.
- 100% of rejected redemptions leave balances unchanged.
- Replaying the same sample dataset yields zero balance or tier drift across repeated runs.
- 100% of output payloads in standard mode use non-PII member identifiers.

---

**Status**: Ready for `/speckit-plan`
