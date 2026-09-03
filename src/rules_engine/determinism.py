import math


def round_earn_points(raw_points: float) -> int:
    """Deterministic rounding for earned points: floor to whole points."""
    return math.floor(raw_points)
