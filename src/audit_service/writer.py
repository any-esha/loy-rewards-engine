from src.models.audit import AuditEvent

_audit_log: list[AuditEvent] = []


def write_audit_event(event: AuditEvent) -> AuditEvent:
    """In-memory audit sink; production adapters can replace this."""
    _audit_log.append(event)
    return event


def get_audit_log() -> list[AuditEvent]:
    return list(_audit_log)


def clear_audit_log() -> None:
    _audit_log.clear()
