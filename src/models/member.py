from pydantic import BaseModel, Field

from src.shared.types import Tier


class Member(BaseModel):
    member_id: str = Field(min_length=1)
    tier: Tier
    points_balance: int = Field(ge=0, default=0)
    lifetime_points: int = Field(ge=0, default=0)

    def with_earn(self, points: int) -> "Member":
        """Return a new Member with balance and lifetime incremented by earned points."""
        if points < 0:
            raise ValueError("earn points must be non-negative")
        return self.model_copy(
            update={
                "points_balance": self.points_balance + points,
                "lifetime_points": self.lifetime_points + points,
            }
        )
