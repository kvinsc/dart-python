import uuid
from typing import Optional, List, Tuple
from datetime import datetime
from models.inventory_item import InventoryItem
from repositories.inventory_repository import InventoryRepository
from services.audit_logger import AuditLogger


class InventoryService:
    def __init__(self, repo: InventoryRepository, audit_logger: AuditLogger):
        self._repo = repo
        self._audit_logger = audit_logger

    def get_all_items(self) -> List[InventoryItem]:
        return self._repo.get_all()

    def get_by_id(self, id: str) -> Optional[InventoryItem]:
        return self._repo.find_by_id(id)

    def get_by_sku(self, sku: str) -> Optional[InventoryItem]:
        return self._repo.find_by_sku(sku)

    def get_low_stock(self, threshold: int = 5) -> List[InventoryItem]:
        return self._repo.get_low_stock(threshold)

    def create_item(
        self,
        sku: str,
        name: str,
        unit_cost: float,
        initial_quantity: int = 0,
        description: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Tuple[Optional[InventoryItem], Optional[str]]:
        if self._repo.sku_exists(sku):
            return None, f"SKU already exists: {sku}"

        item = InventoryItem(
            id=str(uuid.uuid4()),
            sku=sku,
            name=name,
            quantity=initial_quantity,
            unit_cost=unit_cost,
            last_updated=datetime.now(),
            description=description,
        )

        self._repo.save(item)
        self._audit_logger.log_item_created(item, user_id=created_by)
        return item, None

    def update_item(
        self,
        id: str,
        name: Optional[str] = None,
        unit_cost: Optional[float] = None,
        description: Optional[str] = None,
        updated_by: Optional[str] = None,
    ) -> Tuple[Optional[InventoryItem], Optional[str]]:
        existing = self._repo.find_by_id(id)
        if existing is None:
            return None, f"Item not found: {id}"

        updated = existing.copy_with(
            name=name,
            unit_cost=unit_cost,
            description=description,
            last_updated=datetime.now(),
        )

        self._repo.save(updated)
        self._audit_logger.log_item_updated(existing, updated, user_id=updated_by)
        return updated, None

    def delete_item(self, id: str, deleted_by: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        item = self._repo.find_by_id(id)
        if item is None:
            return False, f"Item not found: {id}"

        self._audit_logger.log_item_deleted(item, user_id=deleted_by)
        self._repo.delete(id)
        return True, None