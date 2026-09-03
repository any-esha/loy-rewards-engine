from src.shared.types import Tier
from src.tier_recalculation_service.evaluate import recalc_tier


def test_recalc_tier_upgrades_member_after_threshold_crossed(gold_member):
    member = gold_member.model_copy(
        update={"tier": Tier.SILVER, "lifetime_points": 30000}
    )

    assert recalc_tier(member) == Tier.GOLD