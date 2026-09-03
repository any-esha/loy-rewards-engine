from src.models.member import Member
from src.rules_engine.tier_rules import resolve_tier
from src.shared.types import Tier


def recalc_tier(member: Member) -> Tier:
    return resolve_tier(member.lifetime_points)
