from typing import List, Optional
from models.inventory_item import InventoryItem
from repositories.database import InMemoryDatabase


class InventoryRepository:
    def __init__(self, db: InMemoryDatabase):
        self._db = db

    def get_all(self) -> List[InventoryItem]:
        return self._db.items

    def find_by_id(self, id: str) -> Optional[InventoryItem]:
        return self._db.get_item_by_id(id)

    def find_by_sku(self, sku: str) -> Optional[InventoryItem]:
        return self._db.get_item_by_sku(sku)

    def get_low_stock(self, threshold: int) -> List[InventoryItem]:
        return [item for item in self._db.items if item.quantity <= threshold]

    def save(self, item: InventoryItem) -> None:
        self._db.upsert_item(item)

    def delete(self, id: str) -> bool:
        return self._db.delete_item(id)

    def exists(self, id: str) -> bool:
        return self._db.get_item_by_id(id) is not None

    def sku_exists(self, sku: str) -> bool:
        return self._db.get_item_by_sku(sku) is not None