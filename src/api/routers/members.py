from fastapi import APIRouter, HTTPException

from src.api.repository import member_names, members
from src.api.schemas import MemberDetailsResponse, MemberResponse

router = APIRouter(tags=["members"])


def _member_response(member) -> MemberResponse:
    return MemberResponse(
        member_id=member.member_id,
        name=member_names.get(member.member_id),
        tier=member.tier.value,
        points_balance=member.points_balance,
        lifetime_points=member.lifetime_points,
    )


@router.get("/members", response_model=list[MemberResponse])
def list_members() -> list[MemberResponse]:
    return [_member_response(member) for member in members.values()]


@router.get("/members/{member_id}", response_model=MemberDetailsResponse)
def get_member(member_id: str) -> MemberDetailsResponse:
    member = members.get(member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberDetailsResponse(**_member_response(member).model_dump())
