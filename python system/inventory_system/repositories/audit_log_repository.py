from typing import List, Optional
from datetime import datetime
from models.audit_log import AuditLog, AuditAction
from repositories.database import InMemoryDatabase


class AuditLogRepository:
    def __init__(self, db: InMemoryDatabase):
        self._db = db

    def get_all(self) -> List[AuditLog]:
        return self._db.audit_logs

    def get_for_entity(self, entity_type: str, entity_id: str) -> List[AuditLog]:
        return self._db.get_logs_for_entity(entity_type, entity_id)

    def get_by_action(self, action: AuditAction) -> List[AuditLog]:
        return [log for log in self._db.audit_logs if log.action == action]

    def get_by_user(self, user_id: str) -> List[AuditLog]:
        return [log for log in self._db.audit_logs if log.user_id == user_id]

    def get_by_date_range(self, from_date: datetime, to_date: datetime) -> List[AuditLog]:
        return [
            log for log in self._db.audit_logs
            if from_date < log.timestamp < to_date
        ]

    def save(self, log: AuditLog) -> None:
        self._db.insert_audit_log(log)