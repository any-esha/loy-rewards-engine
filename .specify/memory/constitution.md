<!-- Sync Impact Report: Constitution v1.0.0 (initial) -->
<!-- - Initial constitution created for Loyalty & Rewards Engine -->
<!-- - 7 core principles established for spec-first, agentic, AI-native development -->
<!-- - Governance framework with amendment procedures and compliance review -->

# Loyalty & Rewards Engine Constitution

## Core Principles

### I. Spec-First Development (NON-NEGOTIABLE)
Every feature begins with a comprehensive specification document created before implementation. Specifications MUST include clear acceptance criteria, design rationale, and external interface contracts. Specs are written collaboratively and reviewed for completeness before task generation. This ensures all stakeholders (humans and agents) operate from a shared, traceable source of truth.

### II. Test-Driven Delivery (NON-NEGOTIABLE)
Tests are written first, validated against acceptance criteria, and MUST pass before feature implementation is considered complete. Test suites cover unit, integration, and end-to-end scenarios for core business logic: points calculations, tier transitions, promotion rules, and human-gated approval workflows. Test results are visible in CI/CD and gate all production deployments.

### III. Agentic Implementation with Human Oversight
Agents and LLM-powered tools perform multi-step implementation, refactoring, and code generation tasks autonomously, but all business-critical changes (tier rules, point multipliers, approval workflows) require human review and gate approval before deployment. Agent actions are logged with commit histories showing diff-based rationales.

### IV. Context Steering & Prompt Engineering
Custom prompts, instructions, and agent configurations guide AI behavior with project-specific conventions, domain terminology, and governance rules. Context is organized hierarchically: constitution (top-level principles) → project guidance → feature-specific context. All prompts are versioned and reviewed for security (no PII/secrets leakage) before commit.

### V. Traceability & Governance
Every feature change is linked to: specification → tasks → commits → tests → deployments. Requirement IDs are embedded in commit messages and test names. Human-gated decisions (tier recalculation triggers, promotion eligibility rules) are documented with decision rationale and approval timestamps. CodeQL and secret-scanning gates prevent PII/credential leakage.

### VI. Security & Data Protection (NON-NEGOTIABLE)
User reward data, promotion rules, and tier configurations are protected with role-based access controls. All data transformations (points, tier changes) are immutable and auditable. Secrets are scanned in CI/CD; no hardcoded API keys or database credentials in code. Human review is mandatory before any changes to sensitive business logic (points multipliers, redemption rules).

### VII. Productivity & Cost Efficiency
Model selection (fast vs. reasoning) and token budgets are intentional: reasoning models used only for complex design decisions, fast models for routine coding tasks. LLM cost is tracked and optimized. Refactoring and cleanup workflows reuse proven patterns to minimize redundant agent invocations. Productivity metrics (manual vs. AI-assisted) are captured for retrospectives.

## Domain-Specific Constraints

### Points & Redemption Logic
- Points calculations MUST be deterministic and reversible (audit trail required)
- Redemption workflows include pre-approval validation and human-gated final approval
- All formula changes require spec update and retroactive audit log verification

### Tier & Promotion Management
- Tier recalculation is triggered by defined business events and MUST be logged with timestamp and actor
- Promotion eligibility rules are versioned; historical data reflects rule version at transaction time
- Tier downgrades require explicit business justification and audit trail

### Integration Requirements
- MCP integration points are defined for external systems (loyalty partner APIs, point ledgers)
- Mock MCP servers must exist for testing; scoped access tokens required for production
- All third-party API calls are wrapped with circuit breakers and retry logic with exponential backoff

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

**Version**: 1.0.0 | **Ratified**: 2025-09-01 | **Last Amended**: 2025-09-01
