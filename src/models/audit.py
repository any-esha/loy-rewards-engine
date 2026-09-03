from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from src.shared.clock import utc_now
from src.shared.types import AuditEventType, RULE_VERSION


class AuditEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: AuditEventType
    member_id: str
    transaction_id: str
    points_delta: int
    balance_before: int
    balance_after: int
    lifetime_before: int
    lifetime_after: int
    rule_version: str = RULE_VERSION
    created_at: datetime = Field(default_factory=utc_now)
