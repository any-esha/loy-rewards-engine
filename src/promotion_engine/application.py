import math
from collections.abc import Iterable, Mapping

from src.models.promotion import Promotion


def apply_promotions(points: int, promotions: Iterable[Promotion | Mapping[str, object]]) -> int:
    """Apply at most one active earn multiplier promotion to points."""
    eligible = []
    for promotion in promotions:
        item = (
            promotion
            if isinstance(promotion, Promotion)
            else Promotion.model_validate(promotion)
        )
        if item.active and item.type == "EARN_MULTIPLIER":
            eligible.append(item)

    if not eligible:
        return points

    selected = min(eligible, key=lambda promotion: promotion.id)
    return math.floor(points * selected.value)
