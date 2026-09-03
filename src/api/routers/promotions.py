from fastapi import APIRouter

from src.api.repository import active_promotions
from src.api.schemas import PromotionResponse

router = APIRouter(tags=["promotions"])


@router.get("/promotions", response_model=list[PromotionResponse])
def list_promotions() -> list[PromotionResponse]:
    return [PromotionResponse(**promotion.model_dump()) for promotion in active_promotions()]
