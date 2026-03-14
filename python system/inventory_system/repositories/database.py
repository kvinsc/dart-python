from typing import Dict, List, Optional
from models.inventory_item import InventoryItem
from models.transaction import Transaction
from models.audit_log import AuditLog


class InMemoryDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._items: Dict[str, InventoryItem] = {}
        self._transactions: List[Transaction] = []
        self._audit_logs: List[AuditLog] = []

    # Inventory Items
    @property
    def items(self) -> List[InventoryItem]:
        return list(self._items.values())

    def get_item_by_id(self, id: str) -> Optional[InventoryItem]:
        return self._items.get(id)

    def get_item_by_sku(self, sku: str) -> Optional[InventoryItem]:
        for item in self._items.values():
            if item.sku == sku:
                return item
        return None

    def upsert_item(self, item: InventoryItem) -> None:
        self._items[item.id] = item

    def delete_item(self, id: str) -> bool:
        if id in self._items:
            del self._items[id]
            return True
        return False

    # Transactions
    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions.copy()

    def get_transactions_for_item(self, item_id: str) -> List[Transaction]:
        return [t for t in self._transactions if t.item_id == item_id]

    def insert_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    # Audit Logs
    @property
    def audit_logs(self) -> List[AuditLog]:
        return self._audit_logs.copy()

    def get_logs_for_entity(self, entity_type: str, entity_id: str) -> List[AuditLog]:
        return [
            log for log in self._audit_logs
            if log.entity_type == entity_type and log.entity_id == entity_id
        ]

    def insert_audit_log(self, log: AuditLog) -> None:
        self._audit_logs.append(log)