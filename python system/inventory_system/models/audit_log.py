from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any


class AuditAction(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    STOCK_IN = "stockIn"
    STOCK_OUT = "stockOut"
    ADJUSTMENT = "adjustment"


class AuditLog:
    def __init__(
        self,
        id: str,
        timestamp: datetime,
        action: AuditAction,
        entity_type: str,
        entity_id: str,
        user_id: Optional[str] = None,
        before_snapshot: Optional[str] = None,
        after_snapshot: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        self.id = id
        self.timestamp = timestamp
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.user_id = user_id
        self.before_snapshot = before_snapshot
        self.after_snapshot = after_snapshot
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action.value,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "user_id": self.user_id,
            "before_snapshot": self.before_snapshot,
            "after_snapshot": self.after_snapshot,
            "notes": self.notes,
        }

    def __str__(self) -> str:
        return f"AuditLog(id={self.id}, action={self.action.value}, entity={self.entity_type}:{self.entity_id})"
