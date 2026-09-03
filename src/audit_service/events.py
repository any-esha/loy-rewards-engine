from src.models.audit import AuditEvent
from src.models.member import Member
from src.models.transaction import Transaction
from src.shared.types import AuditEventType


def build_earn_audit_event(
    member_before: Member,
    member_after: Member,
    transaction: Transaction,
) -> AuditEvent:
    """Create a PII-safe EARN audit event from before/after member state."""
    return AuditEvent(
        event_type=AuditEventType.EARN,
        member_id=member_before.member_id,
        transaction_id=transaction.transaction_id,
        points_delta=transaction.points,
        balance_before=member_before.points_balance,
        balance_after=member_after.points_balance,
        lifetime_before=member_before.lifetime_points,
        lifetime_after=member_after.lifetime_points,
    )
