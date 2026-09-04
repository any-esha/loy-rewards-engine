import json

from mcp_server import member_lookup, members_resource


def test_member_lookup_returns_structured_member_without_email():
    result = member_lookup("MBR-001")

    assert result == {
        "id": "MBR-001",
        "name": "Amelia Hartley",
        "tier": "GOLD",
        "points_balance": 42500,
        "lifetime_points": 44000,
        "enrolled_at": "2025-01-31T00:00:00Z",
    }
    assert "email" not in result


def test_member_lookup_returns_not_found_for_unknown_member():
    assert member_lookup("UNKNOWN") == {
        "status": "NOT_FOUND",
        "id": "UNKNOWN",
    }


def test_members_resource_returns_privacy_safe_json():
    result = json.loads(members_resource())

    assert len(result) == 10
    assert result[0]["id"] == "MBR-001"
    assert "email" not in result[0]