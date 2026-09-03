from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_members_response_hides_email_and_supports_details():
    response = client.get("/members")

    assert response.status_code == 200
    assert response.json()
    assert "email" not in response.json()[0]
    assert response.json()[0]["name"]
    assert client.get("/members/MBR-001").status_code == 200


def test_earn_returns_points_balance_and_tier():
    response = client.post(
        "/earn", json={"member_id": "MBR-002", "amount_usd": 100}
    )

    assert response.status_code == 200
    assert response.json() == {
        "earned_points": 1100,
        "new_balance": 19300,
        "tier": "SILVER",
    }


def test_redeem_returns_success_and_failed_statuses():
    success = client.post(
        "/redeem", json={"member_id": "MBR-001", "reward_type": "AWARD_NIGHT"}
    )
    failed = client.post(
        "/redeem", json={"member_id": "MBR-001", "reward_type": "SUITE_AWARD"}
    )

    assert success.status_code == 200
    assert success.json()["status"] == "SUCCESS"
    assert failed.status_code == 400
    assert failed.json()["status"] == "FAILED"


def test_redeem_suite_award_requires_approval():
    response = client.post(
        "/redeem", json={"member_id": "MBR-004", "reward_type": "SUITE_AWARD"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "PENDING_APPROVAL"


def test_collection_endpoints_return_json():
    for path in ("/promotions", "/transactions", "/audit-logs"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("application/json")


def test_unknown_member_returns_not_found():
    response = client.get("/members/UNKNOWN")

    assert response.status_code == 404