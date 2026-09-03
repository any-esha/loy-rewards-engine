# Implementation Plan: Loyalty & Rewards Engine Architecture

**Feature ID**: `001-loyalty-rewards-platform` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)

**Input**: Updated feature specification focused on deterministic earn, redemption, tier,
promotion, human approval, and auditability rules.

## Summary

Define a Python-first modular architecture that enforces deterministic outcomes, no silent balance
changes, complete earn/redeem auditing, and no PII in standard outputs. The architecture is
organized around pure rule functions and side-effect orchestration services.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**:
- Pydantic v2 for domain and boundary validation
- pytest for unit and integration testing

**Storage**: N/A in this planning slice (persistence design deferred to implementation tasks)

**Testing**: pytest

**Target Platform**: Linux server runtime

**Project Type**: Backend domain service

**Performance Goals**: Deterministic, replay-safe rule evaluation under normal request load

**Constraints**:
- Same validated input must produce same output
- No silent balance mutations
- Every earn/redeem must emit audit entry
- Core rule logic must be pure functions where practical
- Standard outputs must avoid direct PII exposure

**Scale/Scope**: Rule-centric MVP for members, transactions, tiers, promotions, and audit trails

## Constitution Check

*Gate: Must pass before design handoff.*

- Determinism: PASS - architecture is pure-function-first.
- Auditability: PASS - explicit audit module with mandatory emit points.
- No silent mutations: PASS - balance writes are service-orchestrated with paired audit events.
- Privacy/no PII outputs: PASS - presentation boundaries enforce non-PII payloads.
- Same input same output: PASS - rules isolate state-free deterministic calculations.

## Project Structure

### Documentation (this feature)

```text
.specify/features/001-loyalty-rewards-platform/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── member.py
│   ├── transaction.py
│   ├── tier.py
│   ├── promotion.py
│   ├── redemption.py
│   └── audit.py
├── rules_engine/
│   ├── earn_rules.py
│   ├── redemption_rules.py
│   ├── tier_rules.py
│   └── determinism.py
├── promotion_engine/
│   ├── eligibility.py
│   ├── selection.py
│   └── application.py
├── redemption_service/
│   ├── validate.py
│   ├── process.py
│   └── approvals.py
├── tier_recalculation_service/
│   ├── evaluate.py
│   └── recalculate.py
├── audit_service/
│   ├── events.py
│   ├── writer.py
│   └── sanitizer.py
└── shared/
    ├── types.py
    ├── errors.py
    └── clock.py

tests/
├── unit/
│   ├── models/
│   ├── rules_engine/
│   ├── promotion_engine/
│   ├── redemption_service/
│   ├── tier_recalculation_service/
│   └── audit_service/
└── integration/
    ├── test_earn_flow.py
    ├── test_redeem_flow.py
    ├── test_tier_flow.py
    └── test_audit_integrity.py
```

## Module Responsibilities

- `Models`: Pydantic v2 models for members, tiers, promotions, transactions, requests, responses,
  and audit payload schemas.
- `Rules Engine`: Pure deterministic functions for earn math, redemption checks, and tier
  threshold evaluation.
- `Promotion Engine`: Determine promotion eligibility, choose one promotion when non-stackable,
  and apply promotion effects deterministically.
- `Redemption Service`: Orchestrate redemption flow (validate, human approval routing, commit-ready
  result) without embedding business math.
- `Tier Recalculation Service`: Recompute tier from lifetime points or replayed ledger state and
  return tier transition events.
- `Audit Service`: Generate immutable audit records for every successful earn/redeem and sanitize
  outputs to prevent direct PII exposure.

## Plan Status

Ready for task generation with architecture modules and ownership boundaries defined.

