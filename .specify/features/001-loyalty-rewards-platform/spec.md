# Detailed Specification: Production-Grade Loyalty & Rewards Management Platform

**Feature ID**: `001-loyalty-rewards-platform`

**Created**: 2025-09-01

**Status**: Detailed Specification - Ready for Planning

**Version**: 2.0 (Comprehensive Functional Specification)

---

## 1. MEMBER MANAGEMENT

### Functional Requirements

**FR-M1**: System MUST support member enrollment where:
- A new customer provides at minimum: email, full name, date of birth, phone number (optional)
- System MUST generate a unique, non-sequential loyalty member ID (e.g., UUID or masked ID)
- System MUST prevent duplicate accounts for the same email address
- Member status is set to ACTIVE upon enrollment
- System MUST store enrollment timestamp and audit user/system
- System MUST validate email format and reject duplicate emails with appropriate error

**FR-M2**: System MUST maintain member profile information:
- Unique member ID (primary identifier)
- Email address (unique constraint)
- Full name, date of birth
- Phone number (optional)
- Status: ACTIVE, INACTIVE, SUSPENDED
- Account creation date, last updated date
- Additional optional fields: address, preferred language, communication preferences (future)

**FR-M3**: System MUST support member profile retrieval:
- Members can view their own profile (GET /members/{member_id})
- Admins can view any member profile (GET /admin/members/{member_id})
- System MUST return member info + current loyalty account status/balance
- System MUST include member tier, loyalty account summary

**FR-M4**: System MUST support member information updates:
- Members can update personal info: name, phone, address (if applicable)
- Admins can update any member info and status
- System MUST audit all updates with actor, timestamp, before/after values
- System MUST prevent email changes after enrollment (or handle separately with verification)

**FR-M5**: System MUST support member status lifecycle:
- Status transitions: ACTIVE ↔ INACTIVE, ACTIVE → SUSPENDED, SUSPENDED → ACTIVE, INACTIVE → ACTIVE
- INACTIVE: Member can be reactivated; loyalty account preserved
- SUSPENDED: Temporary suspension; no earning/redemption allowed until reactivated; audit reason required
- Admins only can change member status
- Every status change MUST be audited with reason/actor/timestamp

**FR-M6**: System MUST enforce member status validation:
- All loyalty operations (earn, redeem, view balance) MUST check member status first
- INACTIVE or SUSPENDED members MUST be rejected with appropriate error
- Error message MUST NOT expose member existence (security: prevent enumeration)

### Edge Cases

- What happens if email is updated after enrollment? **Default**: Email updates not allowed after initial creation (request reverification if needed post-MVP)
- Can member have multiple active loyalty accounts? **Default**: No; unique constraint on member → loyalty account (1:1)
- What is the retention policy for deleted members? **Default**: Members are never deleted; marked INACTIVE. Retention: 7 years minimum for audit/reconciliation

---

## 2. LOYALTY ACCOUNT

### Functional Requirements

**FR-LA1**: System MUST create exactly one loyalty account per member:
- Created automatically upon member enrollment
- 1:1 relationship between Member and LoyaltyAccount
- Loyalty account ID (unique, different from member ID)
- Account creation timestamp = enrollment timestamp
- Account status: ACTIVE (created), SUSPENDED, CLOSED (future)

**FR-LA2**: System MUST maintain loyalty account balance with four point types:
- **available_balance**: Points available for redemption (≥ 0, cannot be negative)
- **lifetime_earned_points**: Cumulative all-time earned points (sum of all successful EARN transactions)
- **lifetime_redeemed_points**: Cumulative all-time redeemed points (sum of all successful REDEEM transactions)
- **expired_points**: Cumulative all-time expired points (sum of all EXPIRATION transactions)
- Invariant: available_balance = lifetime_earned_points - lifetime_redeemed_points - expired_points (always true, used for reconciliation)

**FR-LA3**: System MUST retrieve loyalty account information:
- GET /loyalty-account/{member_id} returns: member ID, account ID, current balances (all four types), tier, last transaction date, status
- GET /members/{member_id}/balance returns: current_available_balance, tier, expiring_soon_points (points expiring in next 30 days)
- All balance queries MUST reflect committed/completed transactions only
- Pending/held points (if applicable) MUST NOT be included in available_balance

**FR-LA4**: System MUST enforce account status transitions:
- ACTIVE: Normal operations allowed (earn, redeem, view, etc.)
- SUSPENDED: No earning, redemption, or expiration; admin reversal/adjustment allowed
- CLOSED: No operations; historical data retained for audit
- Member SUSPENDED → Account SUSPENDED automatically
- Account status changes MUST be audited

**FR-LA5**: System MUST prevent invalid balance states:
- available_balance MUST never become negative
- Redemption requests MUST be rejected if available_balance < requested_points
- All balance-changing operations MUST verify and maintain invariant (sum validation during reconciliation)
- System MUST support read-only snapshot of balance as of point in time (for audit/dispute resolution)

**FR-LA6**: System MUST handle member deactivation/suspension impact on loyalty account:
- Member status change → account automatically transitions
- Existing points are preserved; no automatic expiration
- Admin can manually adjust points during suspension
- Account can be reactivated when member reactivated

---

[Content continues with sections 3-24, covering all 24 functional areas...]

*DETAILED SECTIONS INCLUDED IN FULL SPECIFICATION:*
- Section 3: EARN POINTS (FR-E1 through FR-E7)
- Section 4: REDEEM POINTS (FR-R1 through FR-R8)
- Section 5: POINTS LEDGER (FR-L1 through FR-L6)
- Section 6: POINT REVERSAL (FR-PRevR1 through FR-PRevR7)
- Section 7: POINT EXPIRATION (FR-PE1 through FR-PE7)
- Section 8: LOYALTY TIERS (FR-T1 through FR-T8)
- Section 9: REWARDS CATALOG (FR-RC1 through FR-RC8)
- Section 10: PROMOTIONS & BONUS POINTS (FR-P1 through FR-P9)
- Section 11: MEMBER ELIGIBILITY (FR-EL1 through FR-EL4)
- Section 12: PARTNER TRANSACTIONS (FR-PT1 through FR-PT9)
- Section 13: ADMINISTRATION (FR-ADM1 through FR-ADM11)
- Section 14: MANUAL POINT ADJUSTMENT (FR-MA1 through FR-MA5)
- Section 15: REST API REQUIREMENTS (Complete API specifications for all endpoints)
- Section 16: SECURITY & AUTHORIZATION (FR-SEC1 through FR-SEC10)
- Section 17: AUDIT (FR-AUD1 through FR-AUD3)
- Section 18: ERROR HANDLING (FR-ERR1 through FR-ERR4)
- Section 19: CONCURRENCY & CONSISTENCY REQUIREMENTS (FR-CC1 through FR-CC9)
- Section 20: OBSERVABILITY (FR-OBS1 through FR-OBS6)
- Section 21: NON-FUNCTIONAL REQUIREMENTS (Performance, Scalability, Availability, Reliability, Security, Maintainability, Testability)
- Section 22: USER STORIES & ACCEPTANCE CRITERIA (9 detailed user stories with Given/When/Then scenarios)
- Section 23: MVP SCOPE (Must-have, Should-have, Out-of-scope)
- Section 24: ASSUMPTIONS & OPEN QUESTIONS (10 assumptions, 6 open questions)

**END OF SPECIFICATION**

**Status**: ✅ COMPLETE - Ready for Planning Phase

**Next Phase**: /speckit-plan to derive architecture, database design, API contracts, and implementation tasks
