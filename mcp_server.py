import json
from pathlib import Path
from typing import Any

from fastmcp import FastMCP


DATASET_PATH = Path(__file__).parent / ".specify" / "capstone2_loyalty_dataset.json"
mcp = FastMCP("Loyalty Rewards Engine")


def _load_members() -> dict[str, dict[str, Any]]:
    with DATASET_PATH.open(encoding="utf-8") as dataset_file:
        dataset = json.load(dataset_file)
    return {member["id"]: member for member in dataset["members"]}


@mcp.resource(
    "loyalty://members",
    name="Loyalty members",
    description="All loyalty members without email addresses.",
    mime_type="application/json",
)
def members_resource() -> str:
    """Provide a privacy-safe JSON resource containing all loyalty members."""
    members = _load_members().values()
    public_members = [
        {
            "id": member["id"],
            "name": member["name"],
            "tier": member["tier"],
            "points_balance": member["points_balance"],
            "lifetime_points": member["lifetime_points"],
            "enrolled_at": member["enrolled_at"],
        }
        for member in members
    ]
    return json.dumps(public_members)


@mcp.tool
def member_lookup(member_id: str) -> dict[str, Any]:
    """Look up a member without exposing email or other private fields."""
    member = _load_members().get(member_id)
    if member is None:
        return {"status": "NOT_FOUND", "id": member_id}

    return {
        "id": member["id"],
        "name": member["name"],
        "tier": member["tier"],
        "points_balance": member["points_balance"],
        "lifetime_points": member["lifetime_points"],
        "enrolled_at": member["enrolled_at"],
    }


if __name__ == "__main__":
    mcp.run()