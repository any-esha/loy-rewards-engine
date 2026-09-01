# Implementation Plan: Production-Grade Loyalty & Rewards Management Platform

**Feature ID**: `001-loyalty-rewards-platform` | **Date**: 2025-09-01 | **Spec**: [spec.md](spec.md)

**Tech Stack**: Python 3.11+ / FastAPI / SQLAlchemy 2.0+ / MySQL 8.0+ / React 18+ / Pydantic v2 / pytest / JWT/RBAC

---

## Executive Summary

Build a scalable, secure, API-first loyalty platform backend (FastAPI + SQLAlchemy + MySQL) with a responsive React frontend. Platform enables customers to earn/redeem points, progress through tiers, and access rewards while maintaining complete audit trail, idempotency, and transactional consistency. MVP prioritizes member management, earning, redemption, ledger immutability, tiers, and rewards with production-grade concurrency control and observability.

**Governance**: Follows Loyalty & Rewards Engine Constitution v1.0.0 (spec-first, test-driven, agentic with oversight, context steering, traceability, security-first, productivity-focused).

---

## Architecture Overview

### Backend Architecture (FastAPI)

```
┌─────────────────────────────────────────────────────────────┐
│                         FastAPI App                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Middleware Layer                                      │  │
│  │ - CorrelationIDMiddleware (trace requests)            │  │
│  │ - ErrorHandlingMiddleware (global exception handler) │  │
│  │ - RateLimitMiddleware (partner rate limiting)         │  │
│  │ - LoggingMiddleware (structured logging)              │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ API Routers (v1)                                      │  │
│  │ - /members (enroll, profile, status)                  │  │
│  │ - /loyalty-account (balance, summary)                 │  │
│  │ - /earn (earning events, history)                     │  │
│  │ - /redeem (redemption, tracking)                      │  │
│  │ - /rewards (catalog, eligibility)                     │  │
│  │ - /tiers (tier info, member tier)                     │  │
│  │ - /promotions (active promotions)                     │  │
│  │ - /admin (all admin operations)                       │  │
│  │ - /partners (partner transactions)                    │  │
│  │ - /health (liveness, readiness)                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Service Layer (Business Logic)                        │  │
│  │ - MemberService, LoyaltyAccountService                │  │
│  │ - EarningEngine, RedemptionEngine                      │  │
│  │ - TierCalculationEngine, PromotionEngine               │  │
│  │ - PointsLedgerService, ReconciliationService          │  │
│  │ - IdempotencyService, AuditService                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Repository Layer (Data Access)                        │  │
│  │ - MemberRepository, LoyaltyAccountRepository          │  │
│  │ - PointsTransactionRepository                         │  │
│  │ - RewardRepository, TierRepository, etc.              │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Database Layer (SQLAlchemy ORM + MySQL)               │  │
│  │ - Async session management                            │  │
│  │ - Connection pooling (asyncpg/aiomysql)               │  │
│  │ - Transaction management                              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓ (async jobs)
┌─────────────────────────────────────────────────────────────┐
│ Background Tasks (APScheduler)                              │
│ - PointExpirationJob (nightly)                              │
│ - TierRecalculationJob (daily/event-driven)                 │
│ - PromotionActivationJob (scheduled)                        │
│ - ReconciliationJob (periodic)                              │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Architecture (React)

```
┌─────────────────────────────────────────────────────────────┐
│                      React SPA (Vite)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Pages (React Components)                              │  │
│  │ - HomePage, LoginPage, DashboardPage                  │  │
│  │ - MemberProfilePage, RewardsPage                      │  │
│  │ - AdminPage, LedgerPage, etc.                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Components (Reusable UI)                              │  │
│  │ - Header, Navigation, Footer                          │  │
│  │ - EnrollmentForm, ProfileCard, BalanceWidget          │  │
│  │ - RewardCard, RedemptionForm, TierProgressBar         │  │
│  │ - AdminPanel, TransactionTable, etc.                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Context Providers (State Management)                  │  │
│  │ - AuthContext (user, token, roles)                    │  │
│  │ - MemberContext (profile, balance, tier)              │  │
│  │ - UIContext (notifications, modals, loading)          │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Custom Hooks (Reusable Logic)                         │  │
│  │ - useAuth, useMember, useAsync                        │  │
│  │ - useFetch, useLocalStorage, useNotification          │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ API Service Layer                                     │  │
│  │ - axiosInstance (interceptors for auth, errors)       │  │
│  │ - memberAPI, earningAPI, redemptionAPI, etc.          │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Utils & Helpers                                       │  │
│  │ - formatters (currency, dates), validators            │  │
│  │ - errorHandler, localStorage, constants               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓ (REST API calls)
    FastAPI Backend
```

---

## Database Design

### Core Entities & Relationships

**Tables** (MySQL 8.0+):

#### 1. **members** (10 columns)
- `member_id` (PK, CHAR(36)) - UUID
- `email` (VARCHAR(255), UNIQUE, NOT NULL) - unique enrollment identifier
- `full_name` (VARCHAR(255), NOT NULL)
- `date_of_birth` (DATE)
- `phone_number` (VARCHAR(20))
- `status` (ENUM: ACTIVE, INACTIVE, SUSPENDED) - default ACTIVE
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
- `last_activity_at` (TIMESTAMP)
- INDEX: `idx_email`, `idx_status`, `idx_created_at`

#### 2. **loyalty_accounts** (11 columns)
- `account_id` (PK, CHAR(36)) - UUID
- `member_id` (FK, CHAR(36), UNIQUE) - one account per member
- `available_balance` (BIGINT, NOT NULL, DEFAULT 0) - in smallest unit (e.g., cents if using decimal points)
- `lifetime_earned_points` (BIGINT, NOT NULL, DEFAULT 0) - cumulative
- `lifetime_redeemed_points` (BIGINT, NOT NULL, DEFAULT 0) - cumulative
- `expired_points` (BIGINT, NOT NULL, DEFAULT 0) - cumulative
- `current_tier_id` (FK, CHAR(36), NULLABLE) - current tier
- `account_status` (ENUM: ACTIVE, SUSPENDED, CLOSED) - default ACTIVE
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
- `version` (INT, NOT NULL, DEFAULT 1) - optimistic locking for balance updates
- INDEX: `idx_member_id`, `idx_available_balance`, `idx_updated_at`
- CONSTRAINT: `available_balance >= 0`, `lifetime_earned >= lifetime_redeemed + expired`

#### 3. **points_transactions** (17 columns) - IMMUTABLE LEDGER
- `transaction_id` (PK, CHAR(36)) - UUID
- `member_id` (FK, CHAR(36))
- `account_id` (FK, CHAR(36))
- `transaction_type` (ENUM: EARN, REDEEM, BONUS, EXPIRE, REVERSAL, REFUND, ADJUSTMENT)
- `amount_points` (BIGINT, NOT NULL)
- `balance_before` (BIGINT, NOT NULL)
- `balance_after` (BIGINT, NOT NULL)
- `business_transaction_id` (VARCHAR(255), NULLABLE, UNIQUE) - for idempotency
- `source` (VARCHAR(100)) - "WEB", "MOBILE", "PARTNER_X", "ADMIN", etc.
- `transaction_status` (ENUM: PENDING, SUCCESS, FAILED, REVERSED) - default SUCCESS
- `reference_data` (JSON, NULLABLE) - metadata (earning_rule_id, promotion_id, reward_id, etc.)
- `created_by` (VARCHAR(255)) - user_id or system
- `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP)
- `correlation_id` (VARCHAR(255)) - for tracing
- `notes` (TEXT)
- INDEX: `idx_member_id`, `idx_account_id`, `idx_transaction_type`, `idx_created_at`, `idx_business_transaction_id`
- CONSTRAINT: Immutable - no updates after creation, only reads
- INVARIANT: `balance_after = balance_before + amount_points` (or minus for REDEEM/EXPIRE)

#### 4. **idempotency_keys** (5 columns)
- `idempotency_key` (PK, VARCHAR(255))
- `member_id` (FK, CHAR(36))
- `operation_type` (VARCHAR(100)) - "EARN", "REDEEM", "ADJUST", etc.
- `response_data` (JSON) - cached response
- `expires_at` (TIMESTAMP) - TTL for cleanup (24 hours)
- INDEX: `idx_member_id`, `idx_expires_at`

#### 5. **earning_rules** (11 columns)
- `rule_id` (PK, CHAR(36)) - UUID
- `rule_name` (VARCHAR(255), NOT NULL, UNIQUE)
- `rule_type` (VARCHAR(100)) - "PURCHASE", "HOTEL_STAY", "REFERRAL", etc.
- `base_earning_rate` (DECIMAL(5,2)) - points per unit (e.g., 1 point per $1)
- `multiplier` (DECIMAL(3,2), DEFAULT 1.00) - tier or promotional boost
- `eligibility_criteria` (JSON) - conditions (tier_min, tier_max, category, etc.)
- `partner_id` (FK, CHAR(36), NULLABLE) - if partner-specific
- `status` (ENUM: ACTIVE, INACTIVE) - default ACTIVE
- `version` (INT, DEFAULT 1) - for rule versioning
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
- INDEX: `idx_rule_type`, `idx_status`, `idx_partner_id`

#### 6. **redemption_rules** (7 columns)
- `rule_id` (PK, CHAR(36)) - UUID
- `rule_name` (VARCHAR(255), NOT NULL)
- `min_tier_id` (FK, CHAR(36), NULLABLE)
- `min_points` (BIGINT, DEFAULT 0)
- `eligibility_criteria` (JSON) - conditions
- `status` (ENUM: ACTIVE, INACTIVE) - default ACTIVE
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- INDEX: `idx_status`, `idx_min_tier_id`

#### 7. **rewards** (14 columns)
- `reward_id` (PK, CHAR(36)) - UUID
- `reward_name` (VARCHAR(255), NOT NULL)
- `description` (TEXT)
- `category` (VARCHAR(100)) - "DISCOUNT", "FREE_ITEM", "UPGRADE", etc.
- `points_cost` (BIGINT, NOT NULL)
- `inventory_total` (INT, NULLABLE) - NULL = unlimited
- `inventory_available` (INT, NULLABLE) - current available count
- `eligibility_criteria` (JSON) - tier, status, category restrictions
- `validity_start` (TIMESTAMP)
- `validity_end` (TIMESTAMP, NULLABLE)
- `status` (ENUM: ACTIVE, INACTIVE) - default ACTIVE
- `terms_and_conditions` (TEXT)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
- INDEX: `idx_category`, `idx_status`, `idx_validity_start`, `idx_points_cost`
- CONSTRAINT: `inventory_available >= 0`, `inventory_available <= inventory_total`

#### 8. **redemptions** (12 columns)
- `redemption_id` (PK, CHAR(36)) - UUID, unique redemption reference
- `member_id` (FK, CHAR(36))
- `reward_id` (FK, CHAR(36))
- `points_spent` (BIGINT, NOT NULL)
- `redemption_status` (ENUM: PENDING, SUCCESS, FAILED, REVERSED, REFUNDED) - default PENDING
- `transaction_id` (FK, CHAR(36), NULLABLE) - link to points transaction
- `fulfilled_at` (TIMESTAMP, NULLABLE)
- `cancellation_reason` (VARCHAR(255), NULLABLE)
- `created_by` (VARCHAR(255))
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
- INDEX: `idx_member_id`, `idx_reward_id`, `idx_redemption_status`, `idx_created_at`

#### 9. **tiers** (10 columns)
- `tier_id` (PK, CHAR(36)) - UUID
- `tier_name` (VARCHAR(100), NOT NULL, UNIQUE) - "MEMBER", "SILVER", "GOLD", "PLATINUM", "VIP"
- `min_lifetime_points` (BIGINT, NOT NULL) - qualification threshold
- `max_lifetime_points` (BIGINT, NULLABLE) - exclusive upper bound (NULL = no limit)
- `earning_multiplier` (DECIMAL(3,2), DEFAULT 1.00)
- `redemption_bonus_multiplier` (DECIMAL(3,2), DEFAULT 1.00) - e.g., 10% extra value
- `benefits` (JSON) - features, perks, priority support flag
- `qualification_period_days` (INT, DEFAULT 365) - lookback period for qualification
- `status` (ENUM: ACTIVE, INACTIVE)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- INDEX: `idx_tier_name`, `idx_min_lifetime_points`, `idx_status`
- CONSTRAINT: `min_lifetime_points >= 0`, ranges don't overlap

#### 10. **member_tier_history** (7 columns)
- `history_id` (PK, INT AUTO_INCREMENT)
- `member_id` (FK, CHAR(36))
- `tier_id` (FK, CHAR(36)) - new tier
- `effective_date` (TIMESTAMP, NOT NULL)
- `end_date` (TIMESTAMP, NULLABLE) - NULL if current
- `qualification_basis` (VARCHAR(100)) - "LIFETIME_POINTS", "SPEND", "DOWNGRADE_EXPIRY"
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- INDEX: `idx_member_id`, `idx_effective_date`, `idx_end_date`

#### 11. **promotions** (14 columns)
- `promotion_id` (PK, CHAR(36)) - UUID
- `promotion_name` (VARCHAR(255), NOT NULL)
- `earning_multiplier` (DECIMAL(3,2), NULLABLE)
- `bonus_points` (BIGINT, NULLABLE)
- `eligibility_criteria` (JSON) - tier, member_segment, purchase_amount, etc.
- `member_segment` (JSON, NULLABLE) - demographic/behavioral targeting
- `transaction_criteria` (JSON, NULLABLE) - category, merchant, amount
- `start_date` (TIMESTAMP, NOT NULL)
- `end_date` (TIMESTAMP, NOT NULL)
- `usage_limit_global` (INT, NULLABLE) - total uses cap
- `usage_limit_per_member` (INT, DEFAULT 1) - per-member cap
- `priority` (INT, DEFAULT 1) - for conflict resolution (higher = higher priority)
- `status` (ENUM: ACTIVE, INACTIVE, PAUSED) - default ACTIVE
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- INDEX: `idx_status`, `idx_start_date`, `idx_end_date`, `idx_priority`

#### 12. **partners** (9 columns)
- `partner_id` (PK, CHAR(36)) - UUID
- `partner_name` (VARCHAR(255), NOT NULL, UNIQUE)
- `api_key_hash` (VARCHAR(255), NOT NULL) - bcrypt hashed
- `api_key_created_at` (TIMESTAMP)
- `api_key_rotated_at` (TIMESTAMP)
- `earning_rule_id` (FK, CHAR(36), NULLABLE) - default earning rule for partner
- `rate_limit_req_per_min` (INT, DEFAULT 1000)
- `status` (ENUM: ACTIVE, INACTIVE) - default ACTIVE
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- INDEX: `idx_partner_name`, `idx_status`

#### 13. **audit_records** (10 columns)
- `audit_id` (PK, BIGINT AUTO_INCREMENT)
- `actor` (VARCHAR(255)) - user_id or system
- `action` (VARCHAR(255)) - "MEMBER_CREATED", "POINTS_EARNED", "TIER_UPGRADED", etc.
- `entity_type` (VARCHAR(100)) - "MEMBER", "LOYALTYACCOUNT", "TRANSACTION", etc.
- `entity_id` (VARCHAR(255)) - which entity affected
- `before_state` (JSON, NULLABLE) - previous values
- `after_state` (JSON, NULLABLE) - new values
- `correlation_id` (VARCHAR(255)) - link to request
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- INDEX: `idx_actor`, `idx_action`, `idx_entity_type`, `idx_created_at`, `idx_correlation_id`

---

## Complete REST API Design

### 1. Authentication & Authorization

**Headers Required**:
- `Authorization: Bearer <jwt_token>` (members, admins)
- `X-API-Key: <partner_api_key>` (partners)
- `X-Correlation-ID: <uuid>` (all requests, generated if missing)
- `Idempotency-Key: <uuid>` (for earning, redemption, admin adjustments)

**Token Claims** (JWT):
```json
{
  "sub": "member_id or admin_id",
  "role": "MEMBER|ADMIN|PARTNER",
  "partner_id": "xyz (if partner)",
  "iat": 1234567890,
  "exp": 1234571490
}
```

**Roles & Permissions**:
- **MEMBER**: Can enroll, view own profile/balance, earn (via web/partner), redeem, view rewards, view tier info
- **ADMIN**: All MEMBER permissions + all admin operations (create rewards, manage promotions, adjust points, view ledger, manage partners)
- **PARTNER**: Can submit earning transactions with partner credentials

---

### 2. Member Management APIs

#### **POST /members/enroll**
- **Purpose**: New customer enrollment
- **Actor**: Unauthenticated user
- **Request**:
  ```json
  {
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_of_birth": "1990-01-15",
    "phone_number": "+1234567890"
  }
  ```
- **Response** (201):
  ```json
  {
    "member_id": "uuid-123",
    "email": "user@example.com",
    "status": "ACTIVE",
    "created_at": "2025-09-01T10:00:00Z",
    "loyalty_account": {
      "account_id": "uuid-456",
      "available_balance": 0,
      "tier": "MEMBER"
    }
  }
  ```
- **Errors**: 
  - 400: Invalid email format, missing required fields
  - 409: Email already exists (DuplicateMemberException)
- **Idempotency**: No (unique per enrollment)
- **Audit**: MEMBER_CREATED

#### **GET /members/{member_id}**
- **Purpose**: Retrieve member profile
- **Actor**: Member (self) or ADMIN (any)
- **Response** (200):
  ```json
  {
    "member_id": "uuid-123",
    "email": "user@example.com",
    "full_name": "John Doe",
    "status": "ACTIVE",
    "created_at": "2025-09-01T10:00:00Z",
    "updated_at": "2025-09-05T14:30:00Z"
  }
  ```
- **Errors**: 404: Member not found, 403: Unauthorized
- **Auth**: JWT Bearer token

#### **PUT /members/{member_id}**
- **Purpose**: Update member profile (name, phone, etc.)
- **Actor**: Member (self) or ADMIN
- **Request**:
  ```json
  {
    "full_name": "John Smith",
    "phone_number": "+1234567890"
  }
  ```
- **Response** (200): Updated member object
- **Errors**: 404, 403, 400
- **Audit**: MEMBER_UPDATED (before/after state)

#### **PUT /admin/members/{member_id}/status**
- **Purpose**: Admin status change (ACTIVE/INACTIVE/SUSPENDED)
- **Actor**: ADMIN only
- **Request**:
  ```json
  {
    "status": "SUSPENDED",
    "reason": "Verification pending"
  }
  ```
- **Response** (200): Updated member object with new status
- **Errors**: 403, 404, 400
- **Audit**: MEMBER_STATUS_CHANGED (with reason)

---

### 3. Loyalty Account & Balance APIs

#### **GET /loyalty-account/{member_id}**
- **Purpose**: Retrieve full loyalty account with all balance types
- **Actor**: Member (self) or ADMIN
- **Response** (200):
  ```json
  {
    "account_id": "uuid-456",
    "member_id": "uuid-123",
    "available_balance": 1500,
    "lifetime_earned_points": 5000,
    "lifetime_redeemed_points": 3000,
    "expired_points": 500,
    "current_tier": "SILVER",
    "account_status": "ACTIVE",
    "last_transaction_at": "2025-09-05T14:30:00Z",
    "updated_at": "2025-09-05T14:30:00Z"
  }
  ```
- **Calculation**: `available_balance = lifetime_earned - lifetime_redeemed - expired` (invariant check)
- **Errors**: 404, 403

#### **GET /members/{member_id}/balance**
- **Purpose**: Quick balance lookup (simplified version)
- **Response** (200):
  ```json
  {
    "available_balance": 1500,
    "current_tier": "SILVER",
    "next_tier_threshold": 3000,
    "points_toward_next_tier": 2500,
    "expiring_soon": [
      {
        "points": 100,
        "expires_at": "2025-10-01T00:00:00Z"
      }
    ]
  }
  ```

---

### 4. Earning Points APIs

#### **POST /members/{member_id}/earn**
- **Purpose**: Submit earning event (web/direct purchase)
- **Actor**: MEMBER or admin on behalf
- **Request**:
  ```json
  {
    "earning_rule_id": "uuid-rule-1",
    "amount": 50.00,
    "currency": "USD",
    "business_transaction_id": "order-12345",
    "source": "WEB",
    "metadata": {
      "merchant": "Acme Store",
      "category": "RETAIL"
    }
  }
  ```
- **Response** (201):
  ```json
  {
    "transaction_id": "uuid-trans-1",
    "member_id": "uuid-123",
    "points_earned": 50,
    "bonus_points": 0,
    "total_points": 50,
    "new_balance": 1550,
    "applied_multiplier": 1.0,
    "created_at": "2025-09-05T14:30:00Z"
  }
  ```
- **Idempotency**: YES - business_transaction_id (24h TTL)
  - Duplicate request returns 200 with same response, no double-earning
- **Concurrency**: 
  - Load current balance with optimistic lock (version field)
  - Calculate new balance
  - Retry with exponential backoff if version mismatch (concurrent earn)
- **Errors**:
  - 400: Invalid earning_rule, missing fields
  - 404: Member not found
  - 422: Member status not ACTIVE (MemberInactiveException)
- **Audit**: POINTS_EARNED (rule_id, amount, multiplier)

#### **POST /partners/{partner_id}/transactions**
- **Purpose**: Partner submits earning event (auth via API key)
- **Actor**: PARTNER (header: X-API-Key)
- **Request**:
  ```json
  {
    "member_email": "user@example.com",
    "business_transaction_id": "partner-trans-678",
    "amount": 100.00,
    "currency": "USD",
    "transaction_type": "HOTEL_STAY",
    "metadata": {
      "stay_nights": 3,
      "location": "NYC"
    }
  }
  ```
- **Response** (201): Same as POST /members/{id}/earn
- **Idempotency**: YES - business_transaction_id scoped to partner (24h TTL)
- **Rate Limiting**: Per-partner limit (X-RateLimit-Remaining header)
- **Errors**: 401 (bad API key), 429 (rate limit exceeded), 404 (member not found)
- **Audit**: POINTS_EARNED_PARTNER (partner_id, amount)

#### **GET /members/{member_id}/transactions**
- **Purpose**: Retrieve earning transaction history
- **Query Params**:
  - `type` (EARN, REDEEM, BONUS, etc.) - optional filter
  - `start_date`, `end_date` - date range
  - `page` (default 1), `per_page` (default 20, max 100)
- **Response** (200):
  ```json
  {
    "transactions": [
      {
        "transaction_id": "uuid-1",
        "type": "EARN",
        "amount_points": 50,
        "balance_before": 1500,
        "balance_after": 1550,
        "source": "WEB",
        "created_at": "2025-09-05T14:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_count": 150
    }
  }
  ```
- **Performance**: Indexed by member_id, created_at; paginated for large datasets

---

### 5. Redemption APIs

#### **POST /members/{member_id}/redeem**
- **Purpose**: Redeem points for reward
- **Actor**: MEMBER
- **Request**:
  ```json
  {
    "reward_id": "uuid-reward-1",
    "business_transaction_id": "redemption-123"
  }
  ```
- **Response** (201):
  ```json
  {
    "redemption_id": "uuid-redemption-1",
    "member_id": "uuid-123",
    "reward_id": "uuid-reward-1",
    "points_spent": 250,
    "new_balance": 1300,
    "status": "SUCCESS",
    "created_at": "2025-09-05T14:40:00Z"
  }
  ```
- **Validation Chain**:
  1. Member exists & status ACTIVE
  2. Reward exists & status ACTIVE & within validity window
  3. Reward not expired
  4. Member eligibility (tier, balance, category restrictions)
  5. Sufficient available_balance
  6. Reward inventory available (SELECT...FOR UPDATE lock if inventory)
  7. Atomic deduction + transaction creation
- **Idempotency**: YES - business_transaction_id (24h TTL)
- **Concurrency**:
  - Pessimistic lock on reward inventory (SELECT...FOR UPDATE) if limited stock
  - Optimistic lock on member loyalty account (version field)
  - Prevent double-redemption: check redemption_status = SUCCESS in ledger
- **Errors**:
  - 400: Invalid reward_id
  - 404: Member or reward not found
  - 422: InsufficientPointsException, RewardUnavailableException, MemberIneligibleException
  - 409: Double-redemption (already processed)
- **Audit**: REDEMPTION_SUCCESS (reward_id, points_spent)

#### **GET /redemptions/{redemption_id}**
- **Purpose**: Retrieve redemption status
- **Response** (200):
  ```json
  {
    "redemption_id": "uuid-redemption-1",
    "reward_id": "uuid-reward-1",
    "reward_name": "Free Coffee",
    "points_spent": 250,
    "status": "SUCCESS",
    "fulfilled_at": "2025-09-05T15:00:00Z",
    "created_at": "2025-09-05T14:40:00Z"
  }
  ```

#### **POST /redemptions/{redemption_id}/reverse**
- **Purpose**: Reverse a redemption (admin-only, limited time window)
- **Actor**: ADMIN
- **Request**:
  ```json
  {
    "reason": "Customer requested refund"
  }
  ```
- **Response** (200):
  ```json
  {
    "redemption_id": "uuid-redemption-1",
    "new_status": "REVERSED",
    "refunded_points": 250,
    "new_balance": 1550,
    "refund_transaction_id": "uuid-trans-refund",
    "reversed_at": "2025-09-05T16:00:00Z"
  }
  ```
- **Validation**:
  - Redemption must exist & status = SUCCESS
  - Within reversal window (7 days, configurable)
  - Create REVERSAL transaction
  - Restore points to balance
- **Audit**: REDEMPTION_REVERSED (reason, refunded_points)

---

### 6. Rewards Catalog APIs

#### **GET /rewards**
- **Purpose**: List active rewards for member (with eligibility check)
- **Query Params**: `category`, `sort_by` (popularity, cost), `page`, `per_page`
- **Response** (200):
  ```json
  {
    "rewards": [
      {
        "reward_id": "uuid-1",
        "name": "Free Coffee",
        "description": "Grande coffee",
        "category": "BEVERAGE",
        "points_cost": 250,
        "inventory_available": 100,
        "eligible": true,
        "eligibility_reason": "SILVER+ eligible"
      }
    ],
    "pagination": { "page": 1, "total": 45 }
  }
  ```
- **Eligibility Check**: Apply member's tier, status, criteria; return `eligible` flag + reason

#### **GET /rewards/{reward_id}**
- **Purpose**: Detailed reward view
- **Response** (200):
  ```json
  {
    "reward_id": "uuid-1",
    "name": "Free Coffee",
    "points_cost": 250,
    "eligibility_criteria": {
      "min_tier": "SILVER",
      "allowed_categories": ["BEVERAGE"]
    },
    "inventory": {
      "total": 100,
      "available": 100
    },
    "validity": {
      "start": "2025-09-01T00:00:00Z",
      "end": "2025-12-31T23:59:59Z"
    }
  }
  ```

#### **POST /admin/rewards**
- **Purpose**: Create new reward (admin only)
- **Actor**: ADMIN
- **Request**:
  ```json
  {
    "name": "Free Coffee",
    "points_cost": 250,
    "category": "BEVERAGE",
    "eligibility_criteria": { "min_tier": "SILVER" },
    "inventory_total": 100,
    "validity_end": "2025-12-31T23:59:59Z"
  }
  ```
- **Response** (201): Created reward object
- **Audit**: REWARD_CREATED

#### **PUT /admin/rewards/{reward_id}**
- **Purpose**: Update reward
- **Audit**: REWARD_UPDATED

#### **PUT /admin/rewards/{reward_id}/status**
- **Purpose**: Activate/deactivate reward
- **Request**: `{ "status": "ACTIVE" | "INACTIVE" }`
- **Audit**: REWARD_STATUS_CHANGED

---

### 7. Tier APIs

#### **GET /tiers**
- **Purpose**: List all tiers
- **Response** (200):
  ```json
  {
    "tiers": [
      {
        "tier_id": "uuid-1",
        "name": "MEMBER",
        "min_lifetime_points": 0,
        "earning_multiplier": 1.0,
        "benefits": { "priority_support": false }
      },
      {
        "tier_id": "uuid-2",
        "name": "SILVER",
        "min_lifetime_points": 1000,
        "earning_multiplier": 1.25,
        "benefits": { "priority_support": true, "lounge_access": false }
      }
    ]
  }
  ```

#### **GET /members/{member_id}/tier**
- **Purpose**: Member's current tier + progression info
- **Response** (200):
  ```json
  {
    "current_tier": {
      "tier_id": "uuid-2",
      "name": "SILVER",
      "earning_multiplier": 1.25
    },
    "lifetime_points": 2500,
    "next_tier": {
      "tier_id": "uuid-3",
      "name": "GOLD",
      "min_lifetime_points": 5000,
      "points_to_upgrade": 2500
    }
  }
  ```

#### **POST /admin/tiers**
- **Purpose**: Create tier (admin only)
- **Request**:
  ```json
  {
    "name": "PLATINUM",
    "min_lifetime_points": 10000,
    "earning_multiplier": 1.5,
    "benefits": { "vip_support": true }
  }
  ```
- **Audit**: TIER_CREATED

---

### 8. Promotions APIs

#### **GET /promotions**
- **Purpose**: List active promotions
- **Response** (200):
  ```json
  {
    "promotions": [
      {
        "promotion_id": "uuid-1",
        "name": "2x Points Weekend",
        "earning_multiplier": 2.0,
        "start_date": "2025-09-06T00:00:00Z",
        "end_date": "2025-09-08T23:59:59Z",
        "applicable": true
      }
    ]
  }
  ```

#### **POST /admin/promotions**
- **Purpose**: Create promotion (admin only)
- **Request**:
  ```json
  {
    "name": "2x Points Weekend",
    "earning_multiplier": 2.0,
    "eligibility_criteria": { "min_tier": "MEMBER" },
    "start_date": "2025-09-06T00:00:00Z",
    "end_date": "2025-09-08T23:59:59Z",
    "usage_limit_global": 10000,
    "usage_limit_per_member": 1
  }
  ```
- **Audit**: PROMOTION_CREATED

#### **PUT /admin/promotions/{promotion_id}/status**
- **Purpose**: Activate/deactivate/pause promotion
- **Audit**: PROMOTION_STATUS_CHANGED

---

### 9. Admin APIs

#### **POST /admin/members/{member_id}/adjust-points**
- **Purpose**: Manually add/remove points (admin only)
- **Actor**: ADMIN
- **Request**:
  ```json
  {
    "points_adjustment": -100,
    "reason": "Duplicate transaction reversal",
    "idempotency_key": "adj-xyz"
  }
  ```
- **Response** (201):
  ```json
  {
    "transaction_id": "uuid-adj-1",
    "member_id": "uuid-123",
    "points_adjustment": -100,
    "new_balance": 1400,
    "created_at": "2025-09-05T16:00:00Z"
  }
  ```
- **Validation**: 
  - New balance never negative
  - Reason required
  - Idempotency supported
- **Idempotency**: YES (idempotency_key)
- **Audit**: POINTS_ADJUSTED (adjustment, reason, admin_id)

#### **GET /admin/ledger**
- **Purpose**: View full transaction ledger (filterable, paginated, exportable)
- **Query Params**: `member_id`, `transaction_type`, `start_date`, `end_date`, `page`, `per_page`, `export` (csv/json)
- **Response** (200): Paginated list of transactions
- **Authorization**: ADMIN only

#### **GET /admin/reconciliation**
- **Purpose**: Verify ledger consistency
- **Response** (200):
  ```json
  {
    "status": "CONSISTENT",
    "checks": [
      {
        "member_id": "uuid-123",
        "expected_balance": 1500,
        "calculated_balance": 1500,
        "match": true
      }
    ],
    "summary": {
      "members_checked": 1000,
      "matches": 1000,
      "discrepancies": 0
    }
  }
  ```
- **Logic**: For each member: sum(EARN) - sum(REDEEM) - sum(EXPIRE) + sum(ADJUSTMENT) = available_balance

#### **GET /admin/partners**
- **Purpose**: Manage partners
- **Response** (200): List partners

#### **POST /admin/partners**
- **Purpose**: Register new partner
- **Request**:
  ```json
  {
    "partner_name": "Hotel Chain XYZ",
    "earning_rule_id": "uuid-rule-1",
    "rate_limit_req_per_min": 1000
  }
  ```
- **Response** (201):
  ```json
  {
    "partner_id": "uuid-partner-1",
    "partner_name": "Hotel Chain XYZ",
    "api_key": "sk_live_abc123xyz...",
    "api_key_created_at": "2025-09-05T16:00:00Z"
  }
  ```
- **Security**: Return API key only once; hash in DB
- **Audit**: PARTNER_CREATED

#### **POST /admin/partners/{partner_id}/rotate-key**
- **Purpose**: Rotate partner API key
- **Audit**: PARTNER_KEY_ROTATED

---

### 10. Health & Status APIs

#### **GET /health**
- **Purpose**: Liveness probe (K8s readiness)
- **Response** (200):
  ```json
  {
    "status": "OK",
    "timestamp": "2025-09-05T16:00:00Z"
  }
  ```
- **No auth required**

#### **GET /health/ready**
- **Purpose**: Readiness probe (DB connection, cache, etc.)
- **Response** (200 or 503):
  ```json
  {
    "ready": true,
    "checks": {
      "database": "OK",
      "cache": "OK"
    }
  }
  ```

---

## Request/Response Schemas (Pydantic)

**Common Response Wrapper**:
```python
class SuccessResponse(BaseModel):
    success: bool
    data: dict
    correlation_id: str
    timestamp: datetime

class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str  # "MEMBER_NOT_FOUND", "INSUFFICIENT_POINTS", etc.
    message: str
    details: Optional[dict] = None
    correlation_id: str
    timestamp: datetime
```

**Example Schemas**:
```python
class MemberEnrollmentRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    date_of_birth: date
    phone_number: Optional[str] = None

class EarningRequest(BaseModel):
    earning_rule_id: UUID
    amount: Decimal = Field(..., gt=0)
    business_transaction_id: str = Field(..., min_length=1, max_length=255)
    source: str = Field(default="WEB")
    metadata: Optional[dict] = None

class RedemptionRequest(BaseModel):
    reward_id: UUID
    business_transaction_id: str

class PointsAdjustmentRequest(BaseModel):
    points_adjustment: int
    reason: str = Field(..., min_length=5)
    idempotency_key: UUID
```

---

## Services & Repository Layer

### Core Services

**MemberService**:
- enroll_member(email, full_name, dob, phone) → Member + LoyaltyAccount
- get_member(member_id) → Member
- update_member(member_id, fields) → Member
- change_member_status(member_id, status, reason) → Member
- validate_member_can_operate(member_id) → bool or raise MemberInactiveException

**LoyaltyAccountService**:
- get_account(member_id) → LoyaltyAccount
- get_balance_snapshot(member_id, as_of_date?) → dict
- update_balance(account_id, delta_points, transaction_type) → updated balance (with optimistic lock retry)
- verify_balance_consistency(member_id) → bool

**EarningService**:
- process_earning(member_id, earning_rule_id, amount, business_tx_id, source, metadata) → Transaction
- Check idempotency_key first (return cached result if found)
- Validate member, earning rule, eligibility
- Calculate points (base * multiplier + bonus)
- Apply tier multiplier
- Check active promotions, apply bonus
- Create EARN transaction atomically
- Update loyalty account balance (optimistic lock)
- Audit

**RedemptionService**:
- process_redemption(member_id, reward_id, business_tx_id) → Redemption
- Check idempotency_key first
- Validate member, reward, member eligibility
- Check available_balance >= points_cost
- If limited inventory: pessimistic lock on reward.inventory_available
- Create REDEEM transaction
- Update loyalty account balance
- Update reward inventory
- Create Redemption record
- Audit

**TierCalculationEngine**:
- calculate_tier(lifetime_points) → Tier
- check_tier_upgrade(member_id) → Tier or None
- check_tier_downgrade(member_id) → Tier or None
- apply_tier_upgrade(member_id, old_tier, new_tier) → MemberTierHistory record

**PromotionEngine**:
- get_applicable_promotions(member_id, context) → list[Promotion]
- evaluate_promotion_eligibility(member, promotion) → bool
- calculate_promotion_bonus(base_points, applicable_promotions) → bonus_points

**PointsLedgerService**:
- Immutable append-only operations
- create_transaction(member_id, type, amount, balance_before, balance_after, reference_data) → Transaction
- get_transaction_history(member_id, filters, pagination) → list[Transaction]
- get_transactions_for_reconciliation(date_range) → all transactions

**IdempotencyService**:
- check_idempotency_key(key, operation_type) → cached_response or None
- store_idempotency_key(key, operation_type, response_data, ttl=24h) → None
- Cleanup expired keys (background job)

**AuditService**:
- log_audit(actor, action, entity_type, entity_id, before, after, correlation_id) → AuditRecord
- get_audit_trail(entity_id, date_range) → list[AuditRecord]

**ReconciliationService**:
- verify_ledger_consistency(member_id) → bool
- calculate_expected_balance(member_id) → int (from ledger sum)
- detect_discrepancies() → list[member_id] with mismatches

### Repositories (SQLAlchemy)

**Pattern**: Base async repository with common CRUD + entity-specific queries

```python
class BaseRepository:
    async def get_by_id(id) → T
    async def create(obj) → T
    async def update(id, fields) → T
    async def delete(id) → None
    async def list(filters, pagination) → list[T]

class MemberRepository(BaseRepository):
    async def get_by_email(email) → Member or None
    async def find_by_status(status) → list[Member]
    # ... entity-specific queries

class LoyaltyAccountRepository(BaseRepository):
    async def get_by_member_id(member_id) → LoyaltyAccount
    async def update_balance_with_version(account_id, delta, expected_version) → (updated, success)
    # Optimistic locking for concurrent updates

class PointsTransactionRepository(BaseRepository):
    async def get_by_business_tx_id(business_tx_id) → Transaction or None  # For idempotency
    async def sum_by_type(member_id, tx_type, date_range) → sum
    # For reconciliation

class RewardRepository(BaseRepository):
    async def get_available_for_member(member_id) → list[Reward]
    async def update_inventory_with_lock(reward_id, delta) → (updated, success)
    # Pessimistic lock for inventory

# ... other repositories
```

---

## Authentication & Authorization

### JWT Token Flow
1. Member logs in via `/auth/login` (email + password? Or OAuth? Assume JWT for MVP)
2. Backend issues JWT with claims: `sub` (member_id), `role` (MEMBER/ADMIN), `exp`, etc.
3. Frontend stores token in localStorage/sessionStorage
4. All requests include `Authorization: Bearer <token>`
5. Backend validates token signature, expiration, claims
6. Dependency injection extracts current_user from token

### API Key Flow (Partners)
1. Admin creates partner via `/admin/partners`
2. Backend generates API key (long random string), hashes it (bcrypt), stores hash
3. Return key once to partner (never again)
4. Partner includes `X-API-Key: <key>` in POST to `/partners/{partner_id}/transactions`
5. Backend hashes received key, compares to DB hash
6. Dependency injection extracts current_partner from API key

### RBAC Enforcement
```python
@app.post("/redeem")
async def redeem(
    req: RedemptionRequest,
    current_user: CurrentUser = Depends(verify_jwt)
):
    # current_user.role == "MEMBER", current_user.member_id == member_id (path param)
    if req.member_id != current_user.member_id:
        raise HTTPException(403, "Unauthorized")
    # ... process

@app.post("/admin/rewards")
async def create_reward(
    req: RewardCreateRequest,
    current_admin: CurrentAdmin = Depends(verify_admin)
):
    # current_admin.role == "ADMIN"
    # ... process

@app.post("/partners/{partner_id}/transactions")
async def submit_partner_transaction(
    partner_id: str,
    req: PartnerTransactionRequest,
    current_partner: CurrentPartner = Depends(verify_partner_api_key)
):
    # current_partner.partner_id == partner_id
    # ... process
```

---

## Concurrency & Consistency Strategy

### Balance Updates (Optimistic Locking)

**Problem**: Concurrent earn + redeem on same account → lost update

**Solution**: Optimistic locking with version column

```python
# In LoyaltyAccount table: version INT DEFAULT 1
# On every balance update, increment version

async def update_balance_atomic(account_id, delta_points, max_retries=3):
    for attempt in range(max_retries):
        account = await session.get(LoyaltyAccount, account_id)
        current_version = account.version
        new_balance = account.available_balance + delta_points
        
        if new_balance < 0:
            raise InsufficientPointsException()
        
        stmt = (
            update(LoyaltyAccount)
            .where(
                (LoyaltyAccount.account_id == account_id) &
                (LoyaltyAccount.version == current_version)
            )
            .values(
                available_balance=new_balance,
                version=current_version + 1,
                updated_at=func.now()
            )
        )
        result = await session.execute(stmt)
        
        if result.rowcount > 0:
            # Success
            return new_balance
        else:
            # Version mismatch (concurrent update)
            await asyncio.sleep(2 ** attempt * 0.1)  # Exponential backoff
    
    raise ConcurrentUpdateException()
```

### Redemption with Limited Inventory (Pessimistic Locking)

**Problem**: Two redemption requests for last 10-unit reward → only 10 can succeed

**Solution**: SELECT...FOR UPDATE on reward inventory

```python
async def redeem_with_inventory_check(reward_id, member_id):
    # Pessimistic lock on reward
    stmt = select(Reward).where(Reward.reward_id == reward_id).with_for_update()
    reward = await session.execute(stmt)
    reward = reward.scalar_one_or_none()
    
    if reward.inventory_available < 1:
        raise RewardUnavailableException()
    
    # Safe to proceed: we hold the lock
    reward.inventory_available -= 1
    await session.commit()
    # Lock released
```

### Earning Idempotency

**Problem**: Partner retries earning request → prevent duplicate points

**Solution**: Check idempotency key before processing

```python
async def process_earning_idempotent(member_id, rule_id, amount, business_tx_id, ...):
    # Check if already processed
    cached = await idempotency_service.check_key(business_tx_id, "EARN")
    if cached:
        return cached["response"]
    
    # Not processed; proceed
    transaction = await earning_service.process_earning(...)
    
    # Store idempotency key for future retries
    await idempotency_service.store_key(
        business_tx_id,
        "EARN",
        response_data=transaction.dict(),
        ttl=86400  # 24 hours
    )
    
    return transaction
```

### Balance Consistency Invariant

**Invariant**: `available_balance = lifetime_earned - lifetime_redeemed - expired` (always true)

**Enforcement**:
- Every transaction that changes available_balance also updates a dependent field
- Periodic reconciliation job verifies invariant for all members
- Audit alert if discrepancy detected

---

## Point Expiration Strategy

### Scheduled Job (Nightly)

```python
@scheduler.scheduled_job('cron', hour=2)  # 2 AM daily
async def expire_points_job():
    cutoff_date = now() - timedelta(days=365)  # Expiration policy: 365 days
    
    # Find all points eligible for expiration (EARN transactions from >365 days ago)
    expirable_transactions = await points_ledger_repo.find_expirable(cutoff_date)
    
    for tx in expirable_transactions:
        member_id = tx.member_id
        points_to_expire = tx.amount_points
        
        # Create EXPIRATION transaction
        expiration_tx = await points_ledger_service.create_expiration_transaction(
            member_id=member_id,
            amount_points=points_to_expire,
            reference_tx_id=tx.transaction_id
        )
        
        # Update balance (FIFO: expire oldest points)
        await loyalty_account_service.update_balance(
            member_id=member_id,
            delta_points=-points_to_expire,
            transaction_type="EXPIRE"
        )
        
        # Audit
        await audit_service.log_audit(
            actor="SYSTEM",
            action="POINTS_EXPIRED",
            entity_type="MEMBER",
            entity_id=member_id,
            after={"points_expired": points_to_expire}
        )
```

### Configurable Expiration Rules

Store in config or database:
- Base expiration period (days)
- Tier-specific overrides (VIP points never expire)
- Promotion-specific (e.g., promotional bonus expires 30 days after promotion end)

---

## Tier Qualification & Downgrade

### Auto-Upgrade on Earn

```python
async def process_earning_and_check_tier(member_id, ...):
    # ... earn points ...
    
    # After successful earn, check tier qualification
    new_tier = await tier_calc_engine.calculate_tier(
        lifetime_points=member.lifetime_earned_points
    )
    
    current_tier = member.current_tier
    if new_tier.tier_id != current_tier.tier_id:
        # Tier upgrade!
        await tier_calc_engine.apply_tier_upgrade(
            member_id=member_id,
            old_tier=current_tier,
            new_tier=new_tier
        )
        # Create MemberTierHistory record
        # Emit TierChangedEvent (async notification)
        # Audit
```

### Scheduled Downgrade Job (Daily)

```python
@scheduler.scheduled_job('cron', hour=3)
async def tier_downgrade_job():
    # For each member in non-MEMBER tier
    # Check if still qualified based on lookback period (e.g., last 365 days)
    
    for member in await member_repo.find_by_tier(exclude="MEMBER"):
        lookback_days = 365
        points_in_period = await points_ledger_repo.sum_earned_in_period(
            member_id=member.member_id,
            days=lookback_days
        )
        
        target_tier = await tier_calc_engine.calculate_tier(points_in_period)
        
        if target_tier.tier_id != member.current_tier.tier_id:
            # Downgrade
            await tier_calc_engine.apply_tier_downgrade(
                member_id=member.member_id,
                old_tier=member.current_tier,
                new_tier=target_tier
            )
```

---

## Frontend Architecture (React)

### Pages

1. **HomePage**: Landing, call-to-action, feature highlights
2. **SignupPage**: Enrollment form (email, name, DOB, phone)
3. **LoginPage**: Email + password (or SSO, future)
4. **DashboardPage**: Member's home screen (balance, tier, recent transactions, recommended rewards)
5. **RewardsPage**: Reward catalog with search, filter by category, cost; eligibility check
6. **RewardDetailPage**: Single reward details, redeem button
7. **RedemptionStatusPage**: Redemption history, status tracking
8. **TierPage**: Tier info, progression to next tier, tier benefits
9. **TransactionHistoryPage**: Earning/redemption ledger, download CSV
10. **ProfilePage**: Member profile edit, account settings
11. **AdminPage**: Admin dashboard (partner management, create rewards, manage promotions, view ledger, reconciliation)
12. **NotFoundPage**: 404

### Components

**Common**:
- Header (logo, nav menu, user dropdown, logout)
- Navigation (sidebar or horizontal)
- Footer
- LoadingSpinner
- ErrorBoundary
- ConfirmDialog (confirmation modals)
- Toast (notifications)

**Member/Profile**:
- EnrollmentForm (multi-step form)
- ProfileCard (display member info)
- ProfileEditForm
- BalanceWidget (large card showing available, tier, next_tier_points)
- TierProgressBar (visual progress to next tier)

**Earning**:
- TransactionHistoryTable (paginated ledger, filter by type/date)
- EarningStatsCard (total earned this month, etc.)

**Redemption/Rewards**:
- RewardCard (image, name, cost, eligible?, redeem button)
- RewardGrid (gallery of rewards)
- RewardDetailView (full details, eligibility info, redeem form)
- RedemptionForm (select reward, confirm, submit)
- RedemptionStatusCard (PENDING/SUCCESS/etc.)
- RedemptionHistory (list of past redemptions)

**Admin**:
- AdminPanel (main dashboard)
- MemberManagementTable (search members, view profile, change status)
- RuleConfigurationForm (create earning/redemption rules)
- PromotionManagementTable (list promotions, create/edit/deactivate)
- RewardManagementTable (create/edit rewards, set inventory)
- PointAdjustmentForm (admin adjustment + reason)
- TransactionLedgerTable (full ledger, export)
- PartnerManagementTable (list partners, create, rotate API key)
- ReconciliationStatus (run reconciliation, show results)

### State Management (Context API)

```javascript
// AuthContext
{
  user: { member_id, email, role },
  token: "jwt...",
  isAuthenticated: bool,
  login(email, password),
  logout(),
  setUser(user)
}

// MemberContext
{
  profile: { member_id, email, full_name, status },
  balance: { available: 1500, lifetime_earned: 5000, tier: "SILVER" },
  tier: { tier_id, name, multiplier, benefits },
  nextTierInfo: { name, points_needed, points_progress },
  refreshBalance(),
  refreshProfile()
}

// UIContext
{
  notification: { type, message },
  showNotification(type, message),
  modal: { open, title, content },
  openModal(title, content),
  closeModal(),
  isLoading: bool,
  setLoading(bool)
}
```

### Custom Hooks

```javascript
// useAuth() - access AuthContext
// useMember() - access MemberContext
// useAsync(fn) - wraps async operations, handles loading/error/data states
// useFetch(url, options) - wrapper around fetch/axios with interceptors
// useLocalStorage(key) - typed localStorage access
// useNotification() - quick access to toast notifications
// useFormValidation(initialValues, validate) - form handling
```

### API Service Layer

```javascript
// services/api.js - axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  headers: {
    'X-Correlation-ID': generateUUID()
  }
});

// Interceptor: Add Authorization header
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor: Handle 401, refresh token, retry
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error);
  }
);

// services/memberAPI.js
export const memberAPI = {
  enroll: (data) => api.post('/members/enroll', data),
  getProfile: (memberId) => api.get(`/members/${memberId}`),
  getBalance: (memberId) => api.get(`/members/${memberId}/balance`),
  getTransactions: (memberId, filters) => api.get(`/members/${memberId}/transactions`, { params: filters }),
  // ...
};

// Usage in component:
const { data: balance, loading, error } = useAsync(
  () => memberAPI.getBalance(memberId),
  [memberId]
);
```

---

## Testing Strategy

### Backend (pytest)

**Unit Tests**:
- `tests/unit/services/test_earning_engine.py`: Calculate points with multipliers, promotions
- `tests/unit/services/test_redemption_engine.py`: Validation, eligibility checks
- `tests/unit/services/test_tier_calculation_engine.py`: Tier logic
- `tests/unit/services/test_idempotency_service.py`: Key storage/retrieval
- `tests/unit/repositories/test_loyalty_account_repo.py`: Optimistic locking

**Integration Tests**:
- `tests/integration/test_member_workflow.py`: Enroll → get profile → update (end-to-end)
- `tests/integration/test_earning_workflow.py`: Submit earning → verify balance → check ledger
- `tests/integration/test_redemption_workflow.py`: Submit redemption → verify points deducted → inventory updated
- `tests/integration/test_idempotency.py`: Duplicate earn/redeem requests return same response
- `tests/integration/test_concurrency.py`: Simultaneous earn/redeem on same account (optimistic lock retry)
- `tests/integration/test_reward_inventory.py`: Concurrent redemptions against limited inventory (pessimistic lock)
- `tests/integration/test_tier_progression.py`: Earn → reach tier threshold → auto-upgrade → new multiplier on next earn
- `tests/integration/test_point_expiration.py`: Schedule job → points expire → balance updates → audit logged
- `tests/integration/test_ledger_reconciliation.py`: Verify sum(EARN) - sum(REDEEM) - sum(EXPIRE) = balance

**Fixtures** (`conftest.py`):
- Database session (testcontainers MySQL)
- Sample members, accounts, rewards, tiers, promotions
- Mock partner

### Frontend (Jest + React Testing Library)

**Component Tests**:
- `src/components/__tests__/BalanceWidget.test.js`: Renders balance, tier, next_tier_points
- `src/components/__tests__/RewardCard.test.js`: Shows reward, cost, eligibility, redeem button
- `src/components/__tests__/RedemptionForm.test.js`: Form submission, idempotency_key handling
- `src/pages/__tests__/DashboardPage.test.js`: Fetches member data, displays balance

**Hook Tests**:
- `src/hooks/__tests__/useAuth.test.js`: Login, logout, token persistence
- `src/hooks/__tests__/useMember.test.js`: Fetch profile, balance, tier

**Integration Tests** (Cypress/Playwright):
- Enroll member → Login → View dashboard → Redeem reward → See updated balance
- Admin create promotion → Member earns with multiplier

---

## Configuration

### Environment Variables

`.env`:
```
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_ENV=development

# Backend (.env for FastAPI)
DATABASE_URL=mysql+aiomysql://user:pass@localhost:3306/loyalty_db
JWT_SECRET_KEY=<random-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

PARTNER_API_KEY_ROTATION_DAYS=90
POINTS_EXPIRATION_DAYS=365

ADMIN_EMAIL=admin@loyaltyengine.local
LOG_LEVEL=INFO

SCHEDULER_ENABLED=true
SCHEDULER_TIMEZONE=UTC
```

### Database Migrations

Alembic setup:
```
alembic init alembic
# Create migration: alembic revision --autogenerate -m "Initial schema"
# Upgrade: alembic upgrade head
```

### Logging & Observability

**Structured Logging** (structlog):
```python
logger.info(
    "points_earned",
    member_id=member_id,
    points=100,
    tier=tier_name,
    correlation_id=correlation_id,
    transaction_id=transaction_id
)
```

**Metrics** (Prometheus):
- `earn_transaction_total` (counter: success/failure by rule)
- `redeem_transaction_total` (counter: success/failure by reward)
- `balance_update_duration_seconds` (histogram)
- `idempotency_cache_hit_rate` (gauge)
- `tier_upgrade_total` (counter)

**Health Checks**:
- `/health` - liveness (always 200)
- `/health/ready` - readiness (database, cache connectivity)

---

## MVP Scope

### Must-Have (MVP v1)

1. ✅ Member enrollment (FR-M1 through FR-M6)
2. ✅ Loyalty account creation & balance tracking (FR-LA1 through FR-LA6)
3. ✅ Points earning (FR-E1 through FR-E7) - basic earning + partner earning + idempotency
4. ✅ Points redemption (FR-R1 through FR-R8) - validation + atomic deduction + inventory
5. ✅ Immutable points ledger (FR-L1 through FR-L6) - EARN/REDEEM/BONUS transactions
6. ✅ Loyalty tiers (FR-T1 through FR-T8) - tier config + auto-upgrade, basic downgrade logic
7. ✅ Rewards catalog (FR-RC1 through FR-RC8) - create, activate, list, eligibility check
8. ✅ REST APIs for above (FR-API subset)
9. ✅ Security & RBAC (FR-SEC1 through SEC10) - JWT + API keys, role-based access
10. ✅ Audit logging (FR-AUD1 through AUD3) - all balance-changing operations logged
11. ✅ Concurrency & consistency (FR-CC1 through FR-CC9) - optimistic/pessimistic locking, idempotency
12. ✅ Error handling & validation (FR-ERR1 through ERR4)
13. ✅ Basic UI (React): Enrollment, Dashboard, Rewards, Redeem, Admin basic
14. ✅ Test coverage: Unit + integration tests for above

### Should-Have (MVP v2 / Post-MVP)

1. 🟡 Point reversal/refund (FR-PRevR1 through FR-PRevR7) - depends on FR-R (redemption)
2. 🟡 Point expiration (FR-PE1 through FR-PE7) - scheduled job + EXPIRATION transaction type
3. 🟡 Promotions/bonus points (FR-P1 through FR-P9) - earning multiplier boosts, bonus points
4. 🟡 Advanced admin features (FR-ADM7 through FR-ADM11) - tier management, rule versioning
5. 🟡 Manual point adjustments (FR-MA1 through FR-MA5) - admin-only with audit
6. 🟡 Advanced UI: Tier page, Transaction history export, Admin ledger, Reconciliation
7. 🟡 Observability enhancements: Metrics, distributed tracing, analytics dashboard
8. 🟡 Performance optimization: Caching (Redis), read replicas for ledger queries

### Out-of-Scope (v2+)

- 🚫 Multi-currency support
- 🚫 Mobile app (native iOS/Android)
- 🚫 Gamification (badges, achievements)
- 🚫 ML-based tier prediction / personalized recommendations
- 🚫 International compliance (GDPR, China-specific, etc.)
- 🚫 Real-time analytics / streaming events
- 🚫 Bulk member imports/exports
- 🚫 OAuth2 / social login (MVP uses email/password or phone OTP)
- 🚫 SMS/Email notifications (built into platform but not in MVP frontend)

---

## Implementation Roadmap (Task Ordering)

**Phase 0: Setup & Infrastructure**
1. Database schema (13 tables, indexes, migrations)
2. FastAPI project structure, dependencies, config
3. React project setup (Vite, routing, context)
4. CI/CD pipeline (GitHub Actions, tests, linting)

**Phase 1: Core Member & Account (Week 1-2)**
1. MemberRepository + MemberService (create, update, status validation)
2. LoyaltyAccountRepository + LoyaltyAccountService (creation, balance tracking)
3. POST /members/enroll + GET /members/{id} APIs
4. Member & LoyaltyAccount models (Pydantic)
5. Unit + integration tests
6. React: Enrollment form, Dashboard component (mock data)

**Phase 2: Earning (Week 2-3)**
1. EarningRuleRepository + EarningRuleService
2. EarningEngine (calculate points, apply multiplier)
3. PointsTransactionRepository + PointsLedgerService
4. IdempotencyService (check/store keys)
5. POST /members/{id}/earn API
6. POST /partners/{id}/transactions API
7. Concurrency test: Multiple concurrent earns
8. React: Transaction history page

**Phase 3: Redemption (Week 3-4)**
1. RewardRepository + RewardService (create, activate, list)
2. RedemptionRuleRepository + RedemptionRuleService
3. RedemptionEngine (validate eligibility, check balance, check inventory)
4. Redemption model + repository
5. POST /members/{id}/redeem API
6. GET /rewards + GET /rewards/{id} APIs
7. Concurrency test: Concurrent redemptions with limited inventory
8. React: Reward catalog, Redemption form, Status tracking

**Phase 4: Tiers & Audit (Week 4-5)**
1. TierRepository + TierService
2. MemberTierHistory + TierCalculationEngine
3. TierCalculationEngine (auto-upgrade logic)
4. Scheduled job: TierRecalculationJob (daily downgrade check)
5. GET /tiers + GET /members/{id}/tier APIs
6. AuditRepository + AuditService (all balance-changing operations)
7. GET /admin/ledger API
8. React: Tier page, Admin ledger page

**Phase 5: Advanced Features & Admin (Week 5-6)**
1. PromotionRepository + PromotionEngine (eligibility, bonus calculation)
2. Earning logic: Apply applicable promotions, add bonus points
3. POST /admin/promotions + PUT status APIs
4. Partner management: PartnerRepository, PartnerAuthService, PartnerRateLimitService
5. GET /admin/partners + POST /admin/partners APIs
6. Point reversal: POST /redemptions/{id}/reverse API
7. Point expiration: Scheduled job + EXPIRATION transaction type
8. React: Admin panels (rewards, promotions, partners, adjustments)

**Phase 6: Testing & Polish (Week 6-7)**
1. Complete test coverage (aim for >90%)
2. Performance testing (load test earning/redeem at 1000 TPS)
3. Security audit (no PII in logs, API key handling, RBAC testing)
4. Frontend: Responsive design, error handling, toast notifications
5. Documentation (API docs, runbook, troubleshooting)
6. Staging deployment, end-to-end testing

---

## Critical Unresolved Decisions

**None at this point**. All critical ambiguities were resolved in `/speckit-clarify`:
- Idempotency: database-backed with 24h TTL ✅
- Balance updates: optimistic locking with version ✅
- Concurrent redemptions: pessimistic lock on inventory ✅
- Point expiration: FIFO by transaction date, configurable policy ✅
- Tier downgrade: lookback period + scheduled job ✅
- Reversal: 7-day window, admin-only ✅
- MVP scope: Enroll, Earn, Redeem, Tiers, Rewards (core) ✅

---

## Next Steps

1. ✅ Plan complete - ready for `/speckit-tasks` (task generation)
2. Create dependency-ordered task list
3. Execute `/speckit-implement` with agentic + human oversight
4. Phase 0: Database & infrastructure setup
5. Phase 1-6: Feature-by-feature implementation (6 weeks estimated)

---

**Plan Version**: 1.0  
**Status**: ✅ COMPLETE & IMPLEMENTATION-READY  
**Created**: 2025-09-01  
**Last Updated**: 2025-09-01  
**Approved**: YES (follows Constitution, Shape, Specify, all clarifications integrated)
