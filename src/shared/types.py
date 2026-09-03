from enum import Enum

RULE_VERSION = "1.0.0"


class Tier(str, Enum):
    BASE = "BASE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class TransactionType(str, Enum):
    EARN = "EARN"
    REDEEM = "REDEEM"


class AuditEventType(str, Enum):
    EARN = "EARN"
    REDEEM = "REDEEM"


TIER_MULTIPLIERS: dict[Tier, float] = {
    Tier.BASE: 1.0,
    Tier.SILVER: 1.1,
    Tier.GOLD: 1.25,
    Tier.PLATINUM: 1.5,
}

BASE_POINTS_PER_USD: int = 10
