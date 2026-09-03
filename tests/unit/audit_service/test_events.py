from src.audit_service.writer import get_audit_log
from src.rules_engine.earn_rules import earn
from src.shared.types import AuditEventType, RULE_VERSION


def test_earn_creates_single_audit_event(gold_member):
    earn(gold_member, usd=100.0)
    log = get_audit_log()
    assert len(log) == 1
    event = log[0]
    assert event.event_type == AuditEventType.EARN
    assert event.rule_version == RULE_VERSION


def test_earn_audit_captures_before_after_balances(gold_member):
    result = earn(gold_member, usd=100.0)
    event = result.audit_event

    assert event.member_id == "M-GOLD"
    assert event.transaction_id == result.transaction.transaction_id
    assert event.points_delta == 1250
    assert event.balance_before == 0
    assert event.balance_after == 1250
    assert event.lifetime_before == 0
    assert event.lifetime_after == 1250


def test_earn_audit_payload_contains_no_pii(gold_member):
    result = earn(gold_member, usd=100.0)
    payload = result.audit_event.model_dump()

    for forbidden in ("email", "name", "phone", "address"):
        assert forbidden not in payload
