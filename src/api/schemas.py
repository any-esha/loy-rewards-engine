from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class MemberResponse(BaseModel):
    member_id: str
    name: str | None = None
    tier: str
    points_balance: int
    lifetime_points: int


class MemberDetailsResponse(MemberResponse):
    enrolled_at: datetime | None = None


class EarnRequest(BaseModel):
    member_id: str = Field(min_length=1)
    amount_usd: float = Field(gt=0)


class EarnResponse(BaseModel):
    earned_points: int
    new_balance: int
    tier: str


class RedeemRequest(BaseModel):
    member_id: str = Field(min_length=1)
    reward_type: Literal["AWARD_NIGHT", "SUITE_AWARD"]


class RedeemResponse(BaseModel):
    status: Literal["SUCCESS", "PENDING_APPROVAL", "FAILED"]
    new_balance: int


class ApprovalResponse(BaseModel):
    request_id: str
    member_id: str
    member_name: str
    reward_type: str
    points: int
    status: Literal["PENDING_APPROVAL", "APPROVED", "REJECTED"]
    created_at: datetime


class PromotionResponse(BaseModel):
    id: str
    name: str
    type: str
    value: float
    start: date | None = None
    end: date | None = None
    applies_to: list[str]


class TransactionResponse(BaseModel):
    transaction_id: str
    member_id: str
    type: str
    points: int
    reference: str | None = None
    created_at: datetime


class AuditLogResponse(BaseModel):
    event_id: str
    event_type: str
    member_id: str
    transaction_id: str
    points_delta: int
    balance_before: int
    balance_after: int
    lifetime_before: int
    lifetime_after: int
    rule_version: str
    created_at: datetime