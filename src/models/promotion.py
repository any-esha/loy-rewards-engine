from datetime import date

from pydantic import BaseModel, Field


class Promotion(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    type: str
    value: float = Field(gt=0)
    start: date | None = None
    end: date | None = None
    applies_to: list[str] = Field(default_factory=list)
    active: bool = True

