from src.audit_service.writer import get_audit_log
from src.models.promotion import Promotion
from src.promotion_engine.application import apply_promotions
from src.redemption_service.process import redeem, redeem_award_night, redeem_suite_award
from src.rules_engine.earn_rules import earn
from src.shared.types import RedemptionStatus, Tier, TransactionType
from src.tier_recalculation_service.evaluate import recalc_tier


def test_ac_earn_calculates_points_and_updates_state(gold_member):
    result = earn(gold_member, usd=100.0)

    assert result.points_earned == 1250
    assert result.member.points_balance == 1250
    assert result.member.lifetime_points == 1250
    assert result.transaction.type == TransactionType.EARN


def test_ac_apply_promotions_applies_active_multiplier_once():
    promotions = [
        Promotion(
            id="PROMO-1",
            name="Double Points Weekend",
            type="EARN_MULTIPLIER",
            value=2.0,
            active=True,
        ),
        Promotion(
            id="PROMO-2",
            name="Inactive multiplier",
            type="EARN_MULTIPLIER",
            value=3.0,
            active=False,
        ),
    ]

    assert apply_promotions(1250, promotions) == 2500


def test_ac_redeem_deducts_cost_and_creates_transaction(gold_member):
    member = gold_member.model_copy(update={"points_balance": 42500})

    result = redeem_award_night(member)

    assert result.member.points_balance == 27500
    assert result.transaction.type == TransactionType.REDEEM
    assert result.transaction.points == -15000


def test_ac_recalc_tier_upgrades_on_lifetime_threshold(gold_member):
    member = gold_member.model_copy(
        update={"tier": Tier.SILVER, "lifetime_points": 30000}
    )

    assert recalc_tier(member) == Tier.GOLD


def test_ac_audit_log_records_successful_earn_and_redeem(gold_member):
    earned = earn(gold_member, usd=100.0)
    redeem_award_night(earned.member.model_copy(update={"points_balance": 15000}))

    audit_log = get_audit_log()

    assert len(audit_log) == 2
    assert audit_log[0].transaction_id == earned.transaction.transaction_id
    assert audit_log[1].balance_after == 0


def test_ac_approval_gate_holds_suite_award_before_commit(gold_member):
    member = gold_member.model_copy(update={"points_balance": 50000})

    result = redeem(member, reward_cost=40000, reference="SUITE-AWARD")

    assert result.status == RedemptionStatus.PENDING_APPROVAL
    assert result.member.points_balance == 50000
    assert result.transaction.points == 0
    assert len(get_audit_log()) == 1
