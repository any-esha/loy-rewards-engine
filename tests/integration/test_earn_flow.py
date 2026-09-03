from src.audit_service.writer import get_audit_log
from src.rules_engine.earn_rules import earn
from src.shared.types import TransactionType


def test_earn_flow_updates_member_creates_transaction_and_audit(gold_member):
    result = earn(gold_member, usd=100.0, reference="STAY-1")

    assert result.points_earned == 1250
    assert result.member.points_balance == 1250
    assert result.member.lifetime_points == 1250

    assert result.transaction.type == TransactionType.EARN
    assert result.transaction.points == 1250
    assert result.transaction.reference == "STAY-1"
    assert result.transaction.member_id == gold_member.member_id

    log = get_audit_log()
    assert len(log) == 1
    assert log[0].transaction_id == result.transaction.transaction_id


def test_repeated_earn_accumulates_balance_and_lifetime(gold_member):
    first = earn(gold_member, usd=100.0)
    second = earn(first.member, usd=200.0)  # 200 * 10 * 1.25 = 2500

    assert second.member.points_balance == 1250 + 2500
    assert second.member.lifetime_points == 1250 + 2500
    assert len(get_audit_log()) == 2
