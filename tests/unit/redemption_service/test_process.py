import pytest

from src.audit_service.writer import get_audit_log
from src.redemption_service.process import redeem_award_night, redeem_suite_award
from src.shared.errors import InsufficientBalanceError
from src.shared.types import RedemptionStatus, TransactionType


def test_redeem_award_night_deducts_points_and_creates_transaction(gold_member):
    member = gold_member.model_copy(update={"points_balance": 42500})

    result = redeem_award_night(member)

    assert result.member.points_balance == 27500
    assert result.transaction.type == TransactionType.REDEEM
    assert result.transaction.points == -15000
    assert result.transaction.reference == "AWARD-NIGHT"
    assert result.audit_event.transaction_id == result.transaction.transaction_id
    assert len(get_audit_log()) == 1


def test_redeem_award_night_rejects_insufficient_balance(gold_member):
    member = gold_member.model_copy(update={"points_balance": 10000})

    with pytest.raises(InsufficientBalanceError):
        redeem_award_night(member)

    assert member.points_balance == 10000
    assert get_audit_log() == []


def test_suite_award_requires_approval_before_commit(gold_member):
    member = gold_member.model_copy(update={"points_balance": 50000})

    result = redeem_suite_award(member)

    assert result.status == RedemptionStatus.PENDING_APPROVAL
    assert result.member.points_balance == 50000
    assert result.transaction.points == 0
    assert len(get_audit_log()) == 1
