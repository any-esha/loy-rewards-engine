# Implementation Plan: Production-Grade Loyalty & Rewards Management Platform

**Feature ID**: `001-loyalty-rewards-platform` | **Date**: 2025-09-01 | **Spec**: [spec.md](spec.md)

**Input**: Complete feature specification from 25 capability areas covering member management, points, tiers, rewards, promotions, partners, and admin operations.

## Summary

Build a scalable, secure, API-first backend platform for comprehensive loyalty program management. Platform enables customers to earn points through eligible activities, manage loyalty tiers, redeem rewards, and track transactions while maintaining complete audit trail and business rule flexibility. Core MVP includes member enrollment, points earning/redemption, tier progression, immutable ledger, and admin configuration—all with production-grade security, observability, and concurrency handling.

## Technical Context

**Language/Version**: Python 3.11+ with FastAPI (modern, async-native, excellent for I/O-heavy transaction processing)

**Primary Dependencies**:
- FastAPI 0.104+ (async web framework, auto-OpenAPI docs)
- SQLAlchemy 2.0+ (async ORM with PostgreSQL dialect)
- Pydantic v2 (request/response validation, serialization)
- Alembic (database schema versioning and migrations)
- Passlib + python-jose (password hashing, JWT tokens)
- PyJWT (token generation/validation)
- tenacity (retry logic and circuit breaker patterns)
- structlog (structured logging with correlation IDs)
- prometheus-client (metrics and observability)
- pytest + pytest-asyncio (unit testing async code)
- httpx (async HTTP testing)
- testcontainers (integration testing with real PostgreSQL)
- greenlet (async event loop integration)
- **Frontend**: React 18+, JavaScript (ES6+), Axios/fetch for API calls, React Router for navigation, context API for state management

**Storage**: PostgreSQL 14+ (relational transactions, ACID guarantees, strong for financial ledger; native JSON support for rule evaluation)

**Testing**: pytest for unit tests; pytest + testcontainers for integration tests; Playwright/Cypress for React component/E2E tests; pytest-cov for coverage

**Target Platform**: Linux server (Docker containerized, Kubernetes-ready); React SPA served as static assets or separate frontend service

**Project Type**: RESTful web service backend (FastAPI) + React frontend SPA with internal async event processing

**Performance Goals**: 
- Earn/redeem transactions: p95 < 500ms, p99 < 1000ms
- Member profile retrieval: p95 < 200ms, p99 < 500ms
- Ledger queries (paginated): p95 < 1000ms for 10k transactions
- Promotion eligibility evaluation: < 100ms per member
- 1000 TPS sustained, 10k TPS burst capacity

**Constraints**: 
- Concurrency: zero lost updates, zero double-redemption, atomic balance updates
- Data integrity: 100% ledger reconciliation, no orphaned transactions
- Security: no PII in logs/errors, all secrets encrypted, API key rotation required, CodeQL + secret scanning gates
- Latency: immediate consistency for balance updates; eventual consistency for non-critical async (notifications, analytics)
- Availability: >= 99.9% uptime target, graceful degradation under load (queue backpressure for async)

**Scale/Scope**: 
- v1: 100k members, 10k daily active, 100 TPS peak
- Designed for 10M members, 10k TPS (horizontal scaling via stateless services, connection pooling, indexed queries)
- 25 major capability areas with P1/P2/P3 prioritization for iterative delivery

## Constitution Check

**Gate: Must pass before Phase 0 research. Re-check after Phase 1 design.**

*From `.specify/memory/constitution.md` v1.0.0 (Loyalty & Rewards Engine Constitution):*

### Principle Verification

1. **I. Spec-First Development (NON-NEGOTIABLE)** ✓
   - VERIFIED: Comprehensive spec with user stories, requirements, acceptance criteria completed before planning
   - Risk: NONE - proceeding with spec-first approach

2. **II. Test-Driven Delivery (NON-NEGOTIABLE)** ✓
   - REQUIRES: TDD strategy in Phase 1 design (repository tests, service tests, controller tests, transaction concurrency tests)
   - Risk: MITIGATED - Phase 0 research will establish test framework selection and TDD workflow

3. **III. Agentic Implementation with Human Oversight** ✓
   - REQUIRES: Business-critical operations (tier rules, point multipliers, redemption approval flows) must include human-gated approvals
   - Decision: Tier calculation, earning rules, redemption rules configured by admins (human); approval workflows for manual point adjustments by authorized admins only
   - Risk: ADDRESSED - admin operations logged with audit trail, role-based access control required

4. **IV. Context Steering & Prompt Engineering** ✓
   - REQUIRES: Feature-specific context encoding in `.github/skills/001-loyalty-rewards/` for agent behavior consistency
   - Action: Will create domain context files (entity models, business rules, concurrency patterns) for agent reference
   - Risk: DEFERRED to implementation phase

5. **V. Traceability & Governance** ✓
   - VERIFIED: Every user story mapped to requirements (FR-001 through FR-025), success criteria (SC-001 through SC-010), and edge cases
   - Requirement IDs will be embedded in task descriptions and test names
   - Audit trail requirement (FR-018) ensures compliance
   - Risk: NONE - traceability design integrated into spec

6. **VI. Security & Data Protection (NON-NEGOTIABLE)** ✓
   - VERIFIED: FR-023 specifies RBAC, input validation, secure data handling, no PII in logs, CodeQL + secret scanning gates
   - Immutable ledger design prevents data tampering
   - Risk: ADDRESSED - security requirements explicit, scanning gates enforced in CI/CD

7. **VII. Productivity & Cost Efficiency** ✓
   - REQUIRES: Model selection strategy (fast models for code generation, reasoning models for design decisions)
   - Action: Phase 0 research will evaluate framework/library choices to minimize custom code
   - Risk: MITIGATED - Spring Boot ecosystem provides rich libraries (Spring Data, Spring Security) reducing custom implementation

### Gate Result: ✅ PASS - All principles satisfied or with clear mitigation path

---

## Project Structure

### Documentation (this feature)

```text
.specify/features/001-loyalty-rewards-platform/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # Implementation plan (THIS FILE)
├── research.md          # Phase 0 output (Phase 0: PENDING)
├── data-model.md        # Phase 1 output (Phase 1: PENDING)
├── quickstart.md        # Phase 1 output (Phase 1: PENDING)
├── contracts/           # Phase 1 output (Phase 1: PENDING)
│   ├── member-api.yaml
│   ├── earning-api.yaml
│   ├── redemption-api.yaml
│   ├── tier-api.yaml
│   ├── admin-api.yaml
│   └── partner-api.yaml
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

**Selected Structure: Python FastAPI Backend (async) + React Frontend (SPA)**

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py (FastAPI app initialization, middleware, event handlers)
│   │
│   ├── core/
│   │   ├── config.py (environment variables, app settings)
│   │   ├── security.py (JWT, API key validation, RBAC)
│   │   ├── logging.py (structured logging with correlation IDs)
│   │   ├── exceptions.py (business exceptions: MemberNotFound, InsufficientPoints, etc.)
│   │   ├── constants.py (transaction types, member status enums)
│   │   └── utils.py (correlation ID, idempotency, helpers)
│   │
│   ├── db/
│   │   ├── base.py (SQLAlchemy Base, declarative registry)
│   │   ├── session.py (database session management, async connection pool)
│   │   ├── models/ (SQLAlchemy ORM models)
│   │   │   ├── __init__.py
│   │   │   ├── member.py (Member entity)
│   │   │   ├── loyalty_account.py (LoyaltyAccount entity)
│   │   │   ├── points_transaction.py (PointsTransaction, immutable)
│   │   │   ├── reward.py (Reward entity)
│   │   │   ├── redemption.py (Redemption entity)
│   │   │   ├── tier.py (Tier, MemberTierHistory entities)
│   │   │   ├── earning_rule.py (EarningRule entity, versioned)
│   │   │   ├── redemption_rule.py (RedemptionRule entity)
│   │   │   ├── promotion.py (Promotion entity)
│   │   │   ├── partner.py (Partner entity, API key management)
│   │   │   ├── audit_record.py (AuditRecord entity)
│   │   │   └── domain_event.py (event sourcing)
│   │   │
│   │   └── migrations/ (Alembic)
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │           ├── 001_initial_schema.py
│   │           ├── 002_member_tables.py
│   │           ├── 003_loyalty_account_ledger.py
│   │           └── [more migrations]
│   │
│   ├── schemas/ (Pydantic models for request/response validation)
│   │   ├── __init__.py
│   │   ├── member.py (MemberEnrollmentRequest, MemberProfileResponse)
│   │   ├── loyalty_account.py (LoyaltyAccountResponse, BalanceResponse)
│   │   ├── earning.py (EarningRequest, EarningResponse, EarningRuleRequest)
│   │   ├── redemption.py (RedemptionRequest, RedemptionResponse)
│   │   ├── reward.py (RewardRequest, RewardResponse, RewardListResponse)
│   │   ├── tier.py (TierResponse, MemberTierResponse)
│   │   ├── promotion.py (PromotionRequest, PromotionResponse)
│   │   ├── partner.py (PartnerTransactionRequest, PartnerResponse)
│   │   ├── transaction.py (TransactionHistoryResponse, PaginatedTransactionResponse)
│   │   ├── common.py (ErrorResponse, SuccessResponse, PaginationParams)
│   │   └── audit.py (AuditRecordResponse)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api.py (main router, dependency injection)
│   │   │
│   │   ├── v1/ (API version 1)
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── member.py (POST /members/enroll, GET /members/{id}, etc.)
│   │   │   │   ├── loyalty_account.py (GET /loyalty-account/{member_id})
│   │   │   │   ├── earning.py (POST /members/{id}/earn, partner POST /partners/{id}/transactions)
│   │   │   │   ├── redemption.py (POST /members/{id}/redeem, GET /redemptions/{id})
│   │   │   │   ├── reward.py (GET /rewards, POST /admin/rewards)
│   │   │   │   ├── tier.py (GET /tiers, admin CRUD, GET /members/{id}/tier)
│   │   │   │   ├── promotion.py (GET /promotions, admin CRUD)
│   │   │   │   ├── admin.py (POST /admin/members/{id}/adjust-points, rule management)
│   │   │   │   ├── partner.py (POST /partners/{id}/transactions)
│   │   │   │   ├── transaction.py (GET /members/{id}/transactions, ledger queries)
│   │   │   │   └── health.py (GET /health, /ready, /live)
│   │   │   │
│   │   │   └── dependencies.py (FastAPI Depends: auth, pagination, etc.)
│   │   │
│   │   └── deps.py (cross-version dependencies like current_user)
│   │
│   ├── services/ (business logic layer)
│   │   ├── __init__.py
│   │   ├── member_service.py (enrollment, profile updates, status management)
│   │   ├── loyalty_account_service.py (atomic balance operations, getters)
│   │   ├── earning_service.py (accept earning event, calculate points, validate)
│   │   ├── earning_engine.py (point calculation: base rate, multiplier, bonus)
│   │   ├── earning_rule_service.py (create, update, version earning rules)
│   │   ├── redemption_service.py (validate, deduct, create redemption)
│   │   ├── redemption_engine.py (eligibility check, atomic deduction, transaction)
│   │   ├── redemption_rule_service.py (create, update redemption rules)
│   │   ├── reward_service.py (CRUD, availability check, inventory management)
│   │   ├── tier_service.py (tier configuration, qualification rules)
│   │   ├── tier_calculation_engine.py (auto-upgrade/downgrade logic)
│   │   ├── tier_history_service.py (track tier changes)
│   │   ├── promotion_service.py (CRUD, status management)
│   │   ├── promotion_engine.py (evaluate eligibility per rules)
│   │   ├── partner_service.py (registration, API key management)
│   │   ├── partner_auth_service.py (API key validation)
│   │   ├── partner_rate_limit_service.py (rate limiting per partner)
│   │   ├── points_ledger_service.py (append-only ledger operations)
│   │   ├── transaction_service.py (query, history, pagination)
│   │   ├── reconciliation_service.py (ledger validation, balance verification)
│   │   ├── audit_service.py (log all operations with correlation ID)
│   │   ├── idempotency_service.py (check/store idempotency keys)
│   │   └── event_service.py (publish domain events)
│   │
│   ├── events/ (domain events for async processing)
│   │   ├── __init__.py
│   │   ├── base.py (DomainEvent base class)
│   │   ├── member_events.py (MemberCreatedEvent)
│   │   ├── earning_events.py (PointsEarnedEvent)
│   │   ├── redemption_events.py (PointsRedeemedEvent, RedemptionReversedEvent)
│   │   ├── tier_events.py (TierChangedEvent)
│   │   ├── expiration_events.py (PointsExpiredEvent)
│   │   ├── event_publisher.py (publish to queue/topic)
│   │   └── event_handlers.py (async event listener/processors)
│   │
│   ├── tasks/ (background jobs, async tasks)
│   │   ├── __init__.py
│   │   ├── point_expiration_task.py (scheduled: identify & expire points)
│   │   ├── tier_recalculation_task.py (scheduled: upgrade/downgrade tiers)
│   │   ├── promotion_activation_task.py (scheduled: activate/deactivate promotions)
│   │   └── reconciliation_task.py (scheduled: verify ledger consistency)
│   │
│   └── middleware/
│       ├── __init__.py
│       ├── correlation_id.py (add correlation ID to all requests)
│       ├── error_handler.py (global exception handling)
│       ├── logging_middleware.py (structured logging)
│       └── rate_limiting.py (API rate limiting)

tests/
├── __init__.py
├── conftest.py (pytest fixtures: async client, database, mocks)
│
├── unit/
│   ├── __init__.py
│   ├── services/
│   │   ├── test_earning_engine.py (base rate, multiplier, promotion)
│   │   ├── test_redemption_engine.py (validation, deduction, transaction)
│   │   ├── test_tier_calculation_engine.py (upgrade, downgrade logic)
│   │   ├── test_earning_rule_service.py
│   │   ├── test_promotion_engine.py (eligibility evaluation)
│   │   └── [more service tests]
│   │
│   └── utils/
│       ├── test_idempotency.py
│       └── [utility tests]
│
├── integration/
│   ├── __init__.py
│   ├── test_member_workflow.py (end-to-end: enroll → earn → balance)
│   ├── test_redemption_workflow.py (end-to-end: earn → redeem → verify)
│   ├── test_tier_progression.py (earn → tier upgrade → multiplier)
│   ├── test_idempotency.py (duplicate earn/redeem requests)
│   ├── test_concurrency.py (simultaneous earn/redeem, no lost updates)
│   ├── test_partner_transactions.py (partner earn with idempotency)
│   ├── test_point_expiration.py (expiration job, balance updates)
│   ├── test_ledger_reconciliation.py (sum validation)
│   ├── test_admin_operations.py (point adjustment, rule management)
│   ├── test_promotion_eligibility.py (rules evaluation)
│   └── [more integration tests]
│
└── fixtures/
    ├── member_fixtures.py (reusable member test data)
    ├── earning_fixtures.py (reusable earning event data)
    ├── reward_fixtures.py (reusable reward data)
    └── [more fixtures]

frontend/
├── public/
│   ├── index.html (React root)
│   ├── favicon.ico
│   └── [static assets]
│
├── src/
│   ├── index.js (React app entry point)
│   ├── App.js (main app component)
│   ├── App.css
│   │
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.js
│   │   │   ├── Footer.js
│   │   │   ├── Navigation.js
│   │   │   ├── LoadingSpinner.js
│   │   │   ├── ErrorBoundary.js
│   │   │   └── [common components]
│   │   │
│   │   ├── auth/
│   │   │   ├── Login.js
│   │   │   ├── Logout.js
│   │   │   ├── ProtectedRoute.js
│   │   │   └── [auth components]
│   │   │
│   │   ├── member/
│   │   │   ├── EnrollmentForm.js (new member enrollment)
│   │   │   ├── MemberProfile.js (view profile, KYC info)
│   │   │   ├── MemberDashboard.js (balance, tier, stats)
│   │   │   └── [member components]
│   │   │
│   │   ├── earning/
│   │   │   ├── EarningHistory.js (transaction history)
│   │   │   └── EarningStats.js (earned this period, etc.)
│   │   │
│   │   ├── redemption/
│   │   │   ├── RewardCatalog.js (browse rewards)
│   │   │   ├── RewardDetail.js (single reward details)
│   │   │   ├── RedemptionForm.js (redeem flow)
│   │   │   ├── RedemptionStatus.js (track redemption)
│   │   │   └── [redemption components]
│   │   │
│   │   ├── tier/
│   │   │   ├── TierProgressBar.js (visual tier progression)
│   │   │   ├── TierInfo.js (tier details, benefits)
│   │   │   └── TierRequirements.js (qualification criteria)
│   │   │
│   │   └── admin/
│   │       ├── AdminDashboard.js (admin panel)
│   │       ├── MemberManagement.js (view, manage members)
│   │       ├── RuleConfiguration.js (earning, redemption rules)
│   │       ├── PromotionManagement.js (create, edit promotions)
│   │       ├── RewardManagement.js (create, edit rewards)
│   │       ├── PointAdjustment.js (manual adjustments)
│   │       ├── TransactionLedger.js (view, export transactions)
│   │       ├── PartnerManagement.js (partner registration, keys)
│   │       └── [admin components]
│   │
│   ├── pages/
│   │   ├── HomePage.js
│   │   ├── DashboardPage.js
│   │   ├── RewardsPage.js
│   │   ├── AdminPage.js
│   │   ├── NotFoundPage.js
│   │   └── [page components]
│   │
│   ├── services/
│   │   ├── api.js (axios instance, base URL, interceptors)
│   │   ├── memberAPI.js (API calls: enroll, getProfile, getBalance)
│   │   ├── earningAPI.js (API calls: earn, getHistory)
│   │   ├── redemptionAPI.js (API calls: redeem, getRedemptions)
│   │   ├── rewardAPI.js (API calls: getRewards, getRewardDetail)
│   │   ├── tierAPI.js (API calls: getTiers, getMemberTier)
│   │   ├── promotionAPI.js (API calls: getPromotions)
│   │   ├── adminAPI.js (API calls: admin operations)
│   │   ├── authAPI.js (login, logout, token refresh)
│   │   └── [service files]
│   │
│   ├── context/
│   │   ├── AuthContext.js (current user, auth state)
│   │   ├── MemberContext.js (member profile, balance, tier)
│   │   ├── UIContext.js (notifications, modals, loading)
│   │   └── [context providers]
│   │
│   ├── hooks/
│   │   ├── useAuth.js (access auth context)
│   │   ├── useMember.js (access member context)
│   │   ├── useAsync.js (async data fetching)
│   │   ├── useLocalStorage.js (localStorage helper)
│   │   └── [custom hooks]
│   │
│   ├── utils/
│   │   ├── formatters.js (format currency, dates, numbers)
│   │   ├── validators.js (input validation)
│   │   ├── errorHandler.js (normalize API errors)
│   │   └── [utility functions]
│   │
│   ├── styles/
│   │   ├── index.css (global styles)
│   │   ├── variables.css (CSS variables: colors, spacing)
│   │   ├── components.css (component-specific styles)
│   │   └── [style files]
│   │
│   └── tests/
│       ├── components/ (Jest/React Testing Library tests)
│       ├── services/
│       └── [frontend tests]

requirements.txt (Python backend dependencies)
requirements-dev.txt (development dependencies: pytest, black, flake8)
package.json (React frontend dependencies and scripts)
package-lock.json

docker-compose.yml (PostgreSQL + FastAPI backend + React dev server)
Dockerfile.backend (FastAPI container)
Dockerfile.frontend (React build + serve)
.dockerignore

pytest.ini (pytest configuration)
.env.example (environment variables template)
README.md (setup and running instructions)
```

**Structure Decision**: Selected FastAPI async backend (Python) + React frontend (JavaScript) architecture:
- ✅ Backend: FastAPI provides async I/O for high-TPS transaction processing, auto-generated OpenAPI docs, Pydantic validation
- ✅ Frontend: React SPA for responsive, interactive UI with Context API for state management
- ✅ Python/FastAPI excellent for fast prototyping, data science integrations, rule engines
- ✅ React plain JavaScript (no TypeScript initially) for simplicity; can add TypeScript later
- ✅ Separation of concerns: backend API tested independently, frontend can be tested with mock APIs
- ✅ Scales to 10k TPS with async workers, connection pooling, indexed queries
- ✅ Easy deployment: containerize backend + serve React static assets from CDN or separate nginx

---

## Complexity Tracking

No constitution violations detected. Structure is modular, testable, and aligns with constitution principles (spec-first, test-driven, security-first, agentic with oversight).

| Complexity | Rationale | Simpler Alternative Rejected Because |
|-----------|-----------|--------------------------------------|
| FastAPI async/await + SQLAlchemy async ORM | High-TPS earning/redeem requires non-blocking I/O; async prevents blocking on DB queries | Synchronous FastAPI + sync SQLAlchemy would bottleneck at 100 TPS; async scales to 10k TPS |
| Separate backend + frontend services | React frontend decoupled from Python backend; independent testing + deployment | Monolithic approach (SSR) would reduce flexibility and slow API-only development for partners |
| Multiple SQLAlchemy models per domain | Each entity requires independent CRUD + specialized queries; ORM mapping with async support | Single generic model insufficient for domain-specific queries (e.g., member by email, balance history pagination) |
| Event-driven async processing | Notifications, analytics, and non-critical tasks deferred to background; keeps critical path fast | Synchronous would bloat response time; async allows 100 TPS → 10k TPS scaling |
| Optimistic locking (SQLAlchemy version_id) + pessimistic locking (SELECT...FOR UPDATE) | Concurrent earn/redeem must prevent lost updates and double-redemption | Single locking strategy insufficient for mixed workloads (high read / moderate write) |
| Alembic migrations | Production-safe schema evolution with rollback capability | Raw SQL scripts error-prone; migrations must be versioned + reversible for safety |
| React Context API (no Redux) | Simpler state management for initial MVP; Context sufficient for member profile, balance, tier | Redux adds complexity; defer if performance bottleneck detected later |

---

## Phase 0: Outline & Research

**PHASE STATUS**: Pending (will be executed next via `/speckit-plan` or manual research tasks)

### Unknowns Requiring Research

1. **FastAPI async/await + SQLAlchemy async ORM for high-TPS transaction loads**
   - Task: Research SQLAlchemy async session management, connection pooling (asyncpg), best practices for concurrent operations
   
2. **PostgreSQL advisory locks vs. row-level locking for optimistic/pessimistic concurrency patterns**
   - Task: Research SELECT...FOR UPDATE in async SQLAlchemy, optimistic locking with version columns, deadlock prevention strategies
   
3. **Idempotency implementation patterns in FastAPI (async context)**
   - Task: Research idempotency key storage strategies (in-memory cache with TTL, Redis, database table with expiration), FastAPI Depends for idempotency middleware
   
4. **Background job scheduling in FastAPI (APScheduler vs. Celery)**
   - Task: Research APScheduler integration with FastAPI for point expiration, tier recalculation; distribution in clustered environment
   
5. **Event sourcing / event store with FastAPI and PostgreSQL**
   - Task: Research append-only event table design, event handlers, async event listener patterns, event replay for reconciliation
   
6. **API rate limiting for partner integration (Slowapi vs. custom Redis-based)**
   - Task: Research rate limiting implementation in FastAPI, token bucket algorithm, per-partner limits tracking
   
7. **JSON-based rule evaluation in Python (jsonschema, json-logic, or custom evaluator)**
   - Task: Research rule engines for eligibility, promotion criteria evaluation; performance implications for high-TPS
   
8. **OpenAPI/Swagger documentation generation with FastAPI (Pydantic integration)**
   - Task: Research FastAPI auto-generated OpenAPI, request/response model documentation, Swagger UI configuration

9. **Testing async FastAPI with pytest + pytest-asyncio + testcontainers**
   - Task: Research async fixture setup, transactional rollback in async context, async mock objects, testcontainers PostgreSQL

10. **React state management with Context API for member data (balance, tier, transactions)**
    - Task: Research useContext patterns, performance implications for frequent updates, when to upgrade to Redux/Zustand

11. **Security: GitHub Actions CodeQL scanning for Python + JavaScript**
    - Task: Research Python-specific CodeQL rules, JavaScript/React security scanning, SAST best practices

12. **Deployment: Docker containerization, Kubernetes readiness, frontend asset serving (static vs. separate nginx)**
    - Task: Research FastAPI Docker best practices, multi-stage builds, React production build optimization, CORS configuration

### Research Output Location

Will be consolidated into `.specify/features/001-loyalty-rewards-platform/research.md` (Phase 0 deliverable)

---

## Phase 1: Design & Contracts

**PHASE STATUS**: Pending (will be executed after Phase 0 research completes)

### Phase 1 Deliverables

1. **data-model.md**: Detailed entity definitions with fields, relationships, validation rules, state transitions
2. **quickstart.md**: End-to-end validation guide (setup, earn, redeem, verify)
3. **contracts/** (6 API contract files):
   - member-api.yaml (enrollment, profile, balance)
   - earning-api.yaml (earn, transaction history)
   - redemption-api.yaml (redeem, track redemption)
   - tier-api.yaml (tier config, member tier status)
   - admin-api.yaml (configuration, point adjustment)
   - partner-api.yaml (partner transactions, rate limiting)

### Design Decisions to Finalize in Phase 1

1. **Idempotency key scope**: Transaction-level (earn unique only on {partner_id, business_tx_id}) or global?
2. **Balance updates**: Optimistic (version column in LoyaltyAccount) or pessimistic (SELECT...FOR UPDATE in async SQLAlchemy)?
3. **Event storage**: Separate event table or embedded in transaction table?
4. **Tier recalculation**: Nightly batch job (APScheduler) or real-time on earn event?
5. **Rule evaluation**: JSON logic library (json-logic) or custom evaluator in Python?
6. **Rate limiting**: In-application (Slowapi) or external (Redis-backed)?
7. **Frontend state management**: React Context API sufficient for MVP or start with Zustand/Redux?
8. **Async background tasks**: APScheduler with in-process scheduler or Celery with separate worker processes?
9. **React component testing**: Jest with React Testing Library or Vitest?
10. **Frontend asset hosting**: Serve React build from FastAPI static files or separate nginx/CDN?

---

## Next Steps

Upon user approval of this plan:

1. **Execute Phase 0**: Run research tasks to resolve unknowns → produce `research.md`
2. **Execute Phase 1**: Generate data model, API contracts, and quickstart → produce design artifacts
3. **Execute Phase 2**: Run `/speckit-tasks` to generate dependency-ordered task list for implementation
4. **Execute Phase 3**: `/speckit-implement` to execute tasks with agentic + human oversight

**Estimated Timeline**:
- Phase 0 (Research): 1-2 days
- Phase 1 (Design): 2-3 days
- Phase 2 (Tasks): 1 day
- Phase 3 (Implementation): 3-4 weeks (Backend: 2-3 weeks, Frontend: 1-2 weeks, Integration: 1 week)

---

**Plan Status**: ✅ READY FOR PHASE 0 RESEARCH

---

*Plan created by speckit-plan workflow on 2025-09-01. Constitution check: PASS. All design principles aligned. Proceeding to Phase 0 research.*
