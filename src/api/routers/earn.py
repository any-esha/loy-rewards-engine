from fastapi import APIRouter, HTTPException

from src.api.repository import members, transactions
from src.api.schemas import EarnRequest, EarnResponse
from src.rules_engine.earn_rules import earn
from src.tier_recalculation_service.evaluate import recalc_tier

router = APIRouter(tags=["earn"])


@router.post("/earn", response_model=EarnResponse)
def create_earn(request: EarnRequest) -> EarnResponse:
    member = members.get(request.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    try:
        result = earn(member, request.amount_usd)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    members[request.member_id] = result.member
    transactions.append(result.transaction)
    return EarnResponse(
        earned_points=result.points_earned,
        new_balance=result.member.points_balance,
        tier=recalc_tier(result.member).value,
    )
