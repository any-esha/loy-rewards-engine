from fastapi import APIRouter

from src.api.repository import transactions
from src.api.schemas import TransactionResponse

router = APIRouter(tags=["transactions"])


@router.get("/transactions", response_model=list[TransactionResponse])
def list_transactions() -> list[TransactionResponse]:
    return [
        TransactionResponse(
            transaction_id=item.transaction_id,
            member_id=item.member_id,
            type=item.type.value,
            points=item.points,
            reference=item.reference,
            created_at=item.created_at,
        )
        for item in transactions
    ]
