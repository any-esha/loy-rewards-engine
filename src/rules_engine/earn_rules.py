from dataclasses import dataclass

from src.audit_service.events import build_earn_audit_event
from src.audit_service.writer import write_audit_event
from src.models.audit import AuditEvent
from src.models.member import Member
from src.models.transaction import Transaction, build_earn_transaction
from src.rules_engine.determinism import round_earn_points
from src.shared.errors import InvalidEarnRequestError
from src.shared.types import BASE_POINTS_PER_USD, TIER_MULTIPLIERS


@dataclass(frozen=True)
class EarnResult:
    member: Member
    transaction: Transaction
    audit_event: AuditEvent
    points_earned: int


def calculate_earn_points(usd: float, tier_multiplier: float) -> int:
    """Pure calculation: floor(usd * base_points_per_usd * tier_multiplier)."""
    raw = usd * BASE_POINTS_PER_USD * tier_multiplier
    return round_earn_points(raw)


def earn(member: Member, usd: float, reference: str | None = None) -> EarnResult:
    """Apply earn rules for a member spending `usd`, returning updated state, txn, and audit."""
    if usd <= 0:
        raise InvalidEarnRequestError("usd must be positive")
    if member.tier not in TIER_MULTIPLIERS:
        raise InvalidEarnRequestError(f"unknown tier: {member.tier}")

    tier_multiplier = TIER_MULTIPLIERS[member.tier]
    points = calculate_earn_points(usd, tier_multiplier)

    updated_member = member.with_earn(points)
    transaction = build_earn_transaction(
        member_id=member.member_id, points=points, reference=reference
    )
    audit_event = build_earn_audit_event(
        member_before=member, member_after=updated_member, transaction=transaction
    )
    write_audit_event(audit_event)

    return EarnResult(
        member=updated_member,
        transaction=transaction,
        audit_event=audit_event,
        points_earned=points,
    )
