from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.audit_service.events import build_redeem_audit_event
from src.audit_service.writer import write_audit_event
from src.models.member import Member
from src.models.transaction import Transaction, build_redeem_transaction
from src.shared.types import RedemptionStatus


@dataclass
class ApprovalRequest:
    request_id: str
    member_id: str
    member_name: str
    reward_type: str
    points: int
    created_at: datetime
    status: RedemptionStatus = RedemptionStatus.PENDING_APPROVAL


def create_approval_request(
    member: Member, member_name: str, reward_type: str, points: int, created_at: datetime
) -> ApprovalRequest:
    return ApprovalRequest(
        request_id=str(uuid4()),
        member_id=member.member_id,
        member_name=member_name,
        reward_type=reward_type,
        points=points,
        created_at=created_at,
    )


def approve_request(
    request: ApprovalRequest, member: Member
) -> tuple[Member, Transaction]:
    updated_member = member.with_redeem(request.points)
    transaction = build_redeem_transaction(
        member_id=member.member_id,
        points=request.points,
        reference=request.reward_type,
    )
    audit_event = build_redeem_audit_event(
        member_before=member,
        member_after=updated_member,
        transaction=transaction,
    )
    write_audit_event(audit_event)
    request.status = RedemptionStatus.APPROVED
    return updated_member, transaction


def reject_request(request: ApprovalRequest, member: Member) -> None:
    transaction = build_redeem_transaction(
        member_id=member.member_id,
        points=0,
        reference=request.reward_type,
    )
    audit_event = build_redeem_audit_event(
        member_before=member,
        member_after=member,
        transaction=transaction,
    )
    write_audit_event(audit_event)
    request.status = RedemptionStatus.REJECTED