from fastapi import APIRouter, HTTPException

from src.api.repository import approval_requests, members, transactions
from src.api.schemas import ApprovalResponse
from src.redemption_service.approvals import approve_request, reject_request
from src.shared.types import RedemptionStatus

router = APIRouter(tags=["approvals"])


def _get_pending(request_id: str):
    request = approval_requests.get(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Approval request not found")
    if request.status != RedemptionStatus.PENDING_APPROVAL:
        raise HTTPException(status_code=409, detail="Approval request is already resolved")
    return request


@router.get("/approvals", response_model=list[ApprovalResponse])
def list_approvals() -> list[ApprovalResponse]:
    return [
        ApprovalResponse(**request.__dict__)
        for request in approval_requests.values()
        if request.status == RedemptionStatus.PENDING_APPROVAL
    ]


@router.post("/approvals/{request_id}/approve", response_model=ApprovalResponse)
def approve_approval(request_id: str) -> ApprovalResponse:
    request = _get_pending(request_id)
    member = members.get(request.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    if member.points_balance < request.points:
        raise HTTPException(status_code=400, detail="Insufficient points for approval")
    updated_member, transaction = approve_request(request, member)
    members[request.member_id] = updated_member
    transactions.append(transaction)
    return ApprovalResponse(**request.__dict__)


@router.post("/approvals/{request_id}/reject", response_model=ApprovalResponse)
def reject_approval(request_id: str) -> ApprovalResponse:
    request = _get_pending(request_id)
    member = members.get(request.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    reject_request(request, member)
    return ApprovalResponse(**request.__dict__)