from dataclasses import dataclass

from src.audit_service.events import build_redeem_audit_event
from src.audit_service.writer import write_audit_event
from src.models.audit import AuditEvent
from src.models.member import Member
from src.models.transaction import Transaction, build_redeem_transaction
from src.shared.errors import InsufficientBalanceError
from src.shared.types import RedemptionStatus

AWARD_NIGHT_COST = 15000
SUITE_AWARD_COST = 40000
HUMAN_APPROVAL_THRESHOLD = 30000


@dataclass(frozen=True)
class RedemptionResult:
    member: Member
    transaction: Transaction
    audit_event: AuditEvent
    status: RedemptionStatus = RedemptionStatus.APPROVED


def redeem(member: Member, reward_cost: int, reference: str) -> RedemptionResult:
    if reward_cost <= 0:
        raise ValueError("reward cost must be positive")
    if member.points_balance < reward_cost:
        raise InsufficientBalanceError("insufficient points for redemption")

    if reward_cost > HUMAN_APPROVAL_THRESHOLD:
        transaction = build_redeem_transaction(
            member_id=member.member_id, points=0, reference=reference
        )
        audit_event = build_redeem_audit_event(
            member_before=member, member_after=member, transaction=transaction
        )
        write_audit_event(audit_event)
        return RedemptionResult(
            member=member,
            transaction=transaction,
            audit_event=audit_event,
            status=RedemptionStatus.PENDING_APPROVAL,
        )

    updated_member = member.with_redeem(reward_cost)
    transaction = build_redeem_transaction(
        member_id=member.member_id, points=reward_cost, reference=reference
    )
    audit_event = build_redeem_audit_event(
        member_before=member, member_after=updated_member, transaction=transaction
    )
    write_audit_event(audit_event)
    return RedemptionResult(
        member=updated_member, transaction=transaction, audit_event=audit_event
    )


def redeem_award_night(member: Member) -> RedemptionResult:
    return redeem(member, AWARD_NIGHT_COST, "AWARD-NIGHT")


def redeem_suite_award(member: Member) -> RedemptionResult:
    return redeem(member, SUITE_AWARD_COST, "SUITE-AWARD")