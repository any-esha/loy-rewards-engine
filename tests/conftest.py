import pytest

from src.audit_service.writer import clear_audit_log
from src.models.member import Member
from src.shared.types import Tier


@pytest.fixture(autouse=True)
def reset_audit_log():
    clear_audit_log()
    yield
    clear_audit_log()


@pytest.fixture
def base_member() -> Member:
    return Member(member_id="M-BASE", tier=Tier.BASE, points_balance=0, lifetime_points=0)


@pytest.fixture
def silver_member() -> Member:
    return Member(member_id="M-SILVER", tier=Tier.SILVER, points_balance=0, lifetime_points=0)


@pytest.fixture
def gold_member() -> Member:
    return Member(member_id="M-GOLD", tier=Tier.GOLD, points_balance=0, lifetime_points=0)


@pytest.fixture
def platinum_member() -> Member:
    return Member(member_id="M-PLAT", tier=Tier.PLATINUM, points_balance=0, lifetime_points=0)
