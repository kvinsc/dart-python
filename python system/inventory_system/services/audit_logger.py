import json
import uuid
from typing import Optional
from datetime import datetime
from models.audit_log import AuditLog, AuditAction
from models.inventory_item import InventoryItem
from repositories.audit_log_repository import AuditLogRepository


class AuditLogger:
    def __init__(self, repo: AuditLogRepository):
        self._repo = repo

    def log_item_created(self, item: InventoryItem, user_id: Optional[str] = None) -> None:
        self._log(
            action=AuditAction.CREATED,
            entity_type="InventoryItem",
            entity_id=item.id,
            user_id=user_id,
            before_snapshot=None,
            after_snapshot=json.dumps(item.to_dict()),
        )

    def log_item_updated(
        self,
        before: InventoryItem,
        after: InventoryItem,
        user_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        self._log(
            action=AuditAction.UPDATED,
            entity_type="InventoryItem",
            entity_id=after.id,
            user_id=user_id,
            before_snapshot=json.dumps(before.to_dict()),
            after_snapshot=json.dumps(after.to_dict()),
            notes=notes,
        )

    def log_item_deleted(self, item: InventoryItem, user_id: Optional[str] = None) -> None:
        self._log(
            action=AuditAction.DELETED,
            entity_type="InventoryItem",
            entity_id=item.id,
            user_id=user_id,
            before_snapshot=json.dumps(item.to_dict()),
            after_snapshot=None,
        )

    def log_stock_in(
        self,
        before: InventoryItem,
        after: InventoryItem,
        user_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        self._log(
            action=AuditAction.STOCK_IN,
            entity_type="InventoryItem",
            entity_id=after.id,
            user_id=user_id,
            before_snapshot=json.dumps(before.to_dict()),
            after_snapshot=json.dumps(after.to_dict()),
            notes=notes,
        )

    def log_stock_out(
        self,
        before: InventoryItem,
        after: InventoryItem,
        user_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        self._log(
            action=AuditAction.STOCK_OUT,
            entity_type="InventoryItem",
            entity_id=after.id,
            user_id=user_id,
            before_snapshot=json.dumps(before.to_dict()),
            after_snapshot=json.dumps(after.to_dict()),
            notes=notes,
        )

    def log_adjustment(
        self,
        before: InventoryItem,
        after: InventoryItem,
        user_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        self._log(
            action=AuditAction.ADJUSTMENT,
            entity_type="InventoryItem",
            entity_id=after.id,
            user_id=user_id,
            before_snapshot=json.dumps(before.to_dict()),
            after_snapshot=json.dumps(after.to_dict()),
            notes=notes,
        )

    def _log(
        self,
        action: AuditAction,
        entity_type: str,
        entity_id: str,
        user_id: Optional[str] = None,
        before_snapshot: Optional[str] = None,
        after_snapshot: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        log = AuditLog(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
            before_snapshot=before_snapshot,
            after_snapshot=after_snapshot,
            notes=notes,
        )
        self._repo.save(log)