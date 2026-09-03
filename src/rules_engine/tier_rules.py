from src.shared.types import Tier

TIER_THRESHOLDS: tuple[tuple[int, Tier], ...] = (
    (0, Tier.BASE),
    (10000, Tier.SILVER),
    (30000, Tier.GOLD),
    (75000, Tier.PLATINUM),
)


def resolve_tier(lifetime_points: int) -> Tier:
    if lifetime_points < 0:
        raise ValueError("lifetime points must be non-negative")

    resolved_tier = Tier.BASE
    for threshold, tier in TIER_THRESHOLDS:
        if lifetime_points < threshold:
            break
        resolved_tier = tier
    return resolved_tier
