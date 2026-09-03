<!-- Sync Impact Report -->
<!-- Version change: 1.0.0 -> 1.1.0 -->
<!-- Modified principles: -->
<!-- - I. Spec-First Development (NON-NEGOTIABLE) -> I. Deterministic Spec-First Development (NON-NEGOTIABLE) -->
<!-- - II. Test-Driven Delivery (NON-NEGOTIABLE) -> II. Test-Driven, Repeatable Delivery (NON-NEGOTIABLE) -->
<!-- - III. Agentic Implementation with Human Oversight -> III. Agentic Implementation with Human Oversight -->
<!-- - VI. Security & Data Protection (NON-NEGOTIABLE) -> VI. Security, Privacy, and No-PII Outputs (NON-NEGOTIABLE) -->
<!-- Added sections: -->
<!-- - Architecture Guardrails -->
<!-- - Canonical Domain Models -->
<!-- - Explicit Assumptions -->
<!-- Removed sections: none -->
<!-- Follow-up TODOs: none -->

# Loyalty & Rewards Engine Constitution

## Core Principles

### I. Deterministic Spec-First Development (NON-NEGOTIABLE)
Every feature begins with a comprehensive specification document created before implementation.
Specifications MUST define deterministic behavior for business logic, including explicit formulas,
rounding behavior, and event-order handling. For the same validated input, implementations MUST
produce the same output and side effects across all environments.

### II. Test-Driven, Repeatable Delivery (NON-NEGOTIABLE)
Tests are written first and MUST prove repeatability, auditability, and invariants for core logic.
At minimum, suites cover points calculations, tier transitions, promotion rules, redemption gates,
and ledger mutation semantics. Any change that can alter balances MUST include failing tests first,
then passing tests that show exact expected deltas.

### III. Agentic Implementation with Human Oversight
Agents and LLM-powered tools may implement multi-step changes, but business-critical logic
(tier rules, multipliers, promotion eligibility, redemption thresholds) requires human approval
before release. All autonomous actions MUST remain traceable through commits, tests, and
design artifacts.

### IV. Context Steering & Prompt Engineering
Custom prompts, instructions, and agent configurations guide AI behavior with project-specific
conventions and governance rules. Context is organized hierarchically: constitution -> project
guidance -> feature-specific context. All prompts are versioned and reviewed for security before
commit.

### V. Traceability & Governance
Every feature change is linked to specification -> tasks -> commits -> tests -> deployments.
Every earn and redeem operation MUST create an immutable audit log entry that captures actor,
timestamp, correlation/reference ID, before/after balances, and rule version used. No balance
change may occur without a corresponding persisted audit event.

### VI. Security, Privacy, and No-PII Outputs (NON-NEGOTIABLE)
Reward data and configuration are protected with role-based access controls. Outputs exposed to
logs, APIs, analytics, and AI tooling MUST not include direct PII unless explicitly required and
access-controlled. Default outputs MUST use non-identifying member references and masked values.
Secrets are scanned in CI/CD; no hardcoded credentials are permitted.

### VII. Productivity & Cost Efficiency
Model selection and token budgets are intentional. Reasoning-heavy models are used for complex
design decisions; faster models are used for routine implementation where risk is low. Reusable
patterns and high-signal context are preferred to reduce unnecessary compute and review cycles.

## Domain-Specific Constraints

### Points & Redemption Logic
- Points calculations MUST be deterministic, explicit, and reproducible from ledger state.
- No silent balance changes: all mutations MUST be event-backed, validated, and auditable.
- Redemption workflows include pre-approval validation and human-gated final approval above
  configured thresholds.
- All formula changes require spec updates and retroactive audit-log verification.

### Tier & Promotion Management
- Tier recalculation is triggered by defined business events and MUST be logged with timestamp,
  actor, and rule version.
- Promotion eligibility rules are versioned; historical outcomes MUST remain replayable.
- Tier downgrades require explicit business justification and audit trail.

### Integration Requirements
- Integration boundaries MUST preserve deterministic domain behavior despite transport retries.
- Mock external services MUST exist for repeatable tests.
- Third-party API calls MUST use retries with idempotency keys and circuit breakers.

### Architecture Guardrails
- Core points, tier, and promotion logic MUST be implemented as pure functions where practical;
  side effects are isolated in orchestration layers.
- Ledger write operations MUST be append-only and idempotent by transaction reference.
- Read models may be denormalized, but canonical balances are derived from validated ledger events.

### Canonical Domain Models
- `Member`: `member_id`, tier, points balance, lifetime points, enrollment metadata.
- `TierDefinition`: threshold, earn multiplier, and associated perks.
- `LedgerEntry`: transaction ID, member ID, type (`EARN` or `REDEEM`), points delta,
  reference, created timestamp, and rule version.
- `Promotion`: eligibility window, type, value, applicability scope, and stacking policy.
- `RedemptionDecision`: requested points, policy checks, human gate result, and final disposition.

### Explicit Assumptions
- Time handling uses UTC and ISO-8601 timestamps.
- Inputs are schema-validated before domain execution.
- Event ordering is stable per member using transaction timestamp then transaction ID as tiebreaker.
- Privacy-safe outputs default to non-PII identifiers unless policy-approved access is granted.

## Development Workflow

### Feature Lifecycle
1. **Specify**: Constitution → Spec with acceptance criteria → Clarification (if needed)
2. **Plan**: Design artifacts, architecture decisions, component diagrams
3. **Task Generation**: Dependency-ordered task list with traceability IDs
4. **Implement**: Agentic task execution with human oversight gates
5. **Converge**: Final validation against spec; remaining work appended as new tasks
6. **Deploy**: Test suite green + human approval + observability dashboards active

### Review & Approval Gates
- Spec changes: Product owner + technical lead approval required
- Code affecting business logic (points, tiers, promotions): Product + security review mandatory
- Infrastructure/secrets: DevOps + security review required
- All approvals logged with decision rationale

## Governance

### Amendment Procedure
Amendments to this constitution MUST:
1. Be documented with rationale and impact analysis
2. Include a migration plan if existing practices are superseded
3. Receive consensus from technical lead + product owner
4. Increment version per semantic versioning (MAJOR/MINOR/PATCH rules apply)
5. Be committed with message: `docs(constitution): amend to vX.Y.Z (<reason>)`

### Compliance Review
- Constitution compliance is reviewed at feature completion and quarterly
- All PRs reference this constitution and cite applicable principles in review comments
- Violations (skipped tests, missing spec, unapproved business logic) block merge to main
- Waivers require documented exception justification and time-bounded review

### Runtime Development Guidance
See `.github/copilot-instructions.md` for session-specific context steering and `.github/skills/` for reusable agent/skill definitions. Constitution supersedes all other practices; conflicts escalate to technical lead.

**Version**: 1.1.0 | **Ratified**: 2025-09-01 | **Last Amended**: 2026-09-03
