from fastapi import APIRouter, Query

from src.api.repository import audit_log
from src.api.schemas import AuditLogResponse

router = APIRouter(tags=["audit"])


@router.get("/audit-logs", response_model=list[AuditLogResponse])
def list_audit_logs(member_id: str | None = Query(default=None)) -> list[AuditLogResponse]:
    events = audit_log()
    if member_id:
        events = [event for event in events if event.member_id == member_id]
    return [AuditLogResponse(**event.model_dump()) for event in events]
