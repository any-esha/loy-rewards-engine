from pydantic import BaseModel, Field

from src.shared.types import Tier, TIER_MULTIPLIERS


class TierDefinition(BaseModel):
    tier: Tier
    multiplier: float = Field(gt=0)

    @classmethod
    def for_tier(cls, tier: Tier) -> "TierDefinition":
        return cls(tier=tier, multiplier=TIER_MULTIPLIERS[tier])
