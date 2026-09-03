from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from src.shared.clock import utc_now
from src.shared.types import TransactionType


class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid4()))
    member_id: str
    type: TransactionType
    points: int
    reference: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


def build_earn_transaction(member_id: str, points: int, reference: str | None = None) -> Transaction:
    return Transaction(
        member_id=member_id,
        type=TransactionType.EARN,
        points=points,
        reference=reference,
    )


def build_redeem_transaction(
    member_id: str, points: int, reference: str | None = None
) -> Transaction:
    return Transaction(
        member_id=member_id,
        type=TransactionType.REDEEM,
        points=-points,
        reference=reference,
    )
