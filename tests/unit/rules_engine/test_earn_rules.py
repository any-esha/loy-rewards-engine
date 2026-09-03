import pytest

from src.rules_engine.earn_rules import calculate_earn_points, earn
from src.shared.errors import InvalidEarnRequestError


def test_gold_member_100_usd_earns_1250_points(gold_member):
    result = earn(gold_member, usd=100.0)

    assert result.points_earned == 1250
    assert result.member.points_balance == 1250
    assert result.member.lifetime_points == 1250


@pytest.mark.parametrize(
    "tier_fixture,usd,expected",
    [
        ("base_member", 100.0, 1000),
        ("silver_member", 100.0, 1100),
        ("gold_member", 100.0, 1250),
        ("platinum_member", 100.0, 1500),
    ],
)
def test_tier_multiplier_applied(request, tier_fixture, usd, expected):
    member = request.getfixturevalue(tier_fixture)
    result = earn(member, usd=usd)
    assert result.points_earned == expected


def test_calculate_earn_points_floor_rounding():
    # $9.99 * 10 * 1.25 = 124.875 -> floor 124
    assert calculate_earn_points(9.99, 1.25) == 124


def test_invalid_usd_rejected(gold_member):
    with pytest.raises(InvalidEarnRequestError):
        earn(gold_member, usd=0)
    with pytest.raises(InvalidEarnRequestError):
        earn(gold_member, usd=-1)


def test_balance_and_lifetime_updated_together(gold_member):
    result = earn(gold_member, usd=50.0)  # 50 * 10 * 1.25 = 625
    assert result.points_earned == 625
    assert result.member.points_balance == 625
    assert result.member.lifetime_points == 625
