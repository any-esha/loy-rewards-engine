import json
from datetime import date, datetime, timezone
from pathlib import Path

from src.audit_service.writer import get_audit_log
from src.models.member import Member
from src.models.promotion import Promotion
from src.models.transaction import Transaction
from src.redemption_service.approvals import ApprovalRequest
from src.shared.types import Tier, TransactionType

DATASET_PATH = Path(__file__).resolve().parents[2] / ".specify" / "capstone2_loyalty_dataset.json"


def _load_dataset() -> dict:
    with DATASET_PATH.open(encoding="utf-8") as dataset_file:
        return json.load(dataset_file)


def _initial_members() -> dict[str, Member]:
    return {
        item["id"]: Member(
            member_id=item["id"],
            tier=Tier(item["tier"]),
            points_balance=item["points_balance"],
            lifetime_points=item["lifetime_points"],
        )
        for item in _load_dataset()["members"]
    }


def _initial_transactions() -> list[Transaction]:
    return [
        Transaction(
            transaction_id=item["id"],
            member_id=item["member_id"],
            type=TransactionType(item["type"]),
            points=item["points"],
            reference=item.get("reference"),
            created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
        )
        for item in _load_dataset()["transactions"]
    ]


members = _initial_members()
member_names = {
    item["id"]: item["name"] for item in _load_dataset()["members"]
}
transactions = _initial_transactions()
promotions = [Promotion.model_validate(item) for item in _load_dataset()["promotions"]]
approval_requests: dict[str, ApprovalRequest] = {}


def active_promotions() -> list[Promotion]:
    today = datetime.now(timezone.utc).date()
    return [
        promotion
        for promotion in promotions
        if promotion.active
        and (promotion.start is None or promotion.start <= today)
        and (promotion.end is None or today <= promotion.end)
    ]


def audit_log():
    return get_audit_log()