from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.api.repository import approval_requests, member_names, members, transactions
from src.api.schemas import RedeemRequest, RedeemResponse
from src.redemption_service.approvals import create_approval_request
from src.redemption_service.process import (
    redeem_award_night,
    redeem_suite_award,
)
from src.shared.errors import InsufficientBalanceError
from src.shared.types import RedemptionStatus

router = APIRouter(tags=["redemption"])


@router.post("/redeem", response_model=RedeemResponse)
def create_redemption(request: RedeemRequest) -> RedeemResponse:
    member = members.get(request.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    redeem_operation = (
        redeem_award_night
        if request.reward_type == "AWARD_NIGHT"
        else redeem_suite_award
    )
    try:
        result = redeem_operation(member)
    except InsufficientBalanceError as error:
        return JSONResponse(
            status_code=400,
            content={
                "status": "FAILED",
                "new_balance": member.points_balance,
                "detail": str(error),
            },
        )

    members[request.member_id] = result.member
    transactions.append(result.transaction)
    status = (
        "PENDING_APPROVAL"
        if result.status == RedemptionStatus.PENDING_APPROVAL
        else "SUCCESS"
    )
    if result.status == RedemptionStatus.PENDING_APPROVAL:
        approval = create_approval_request(
            member=member,
            member_name=member_names.get(request.member_id, request.member_id),
            reward_type=request.reward_type,
            points=40000 if request.reward_type == "SUITE_AWARD" else 15000,
            created_at=result.transaction.created_at,
        )
        approval_requests[approval.request_id] = approval
    return RedeemResponse(status=status, new_balance=result.member.points_balance)


