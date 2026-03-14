import uuid
from typing import Optional, Tuple
from datetime import datetime
from models.inventory_item import InventoryItem
from models.transaction import Transaction, TransactionType
from repositories.inventory_repository import InventoryRepository
from repositories.transaction_repository import TransactionRepository
from services.audit_logger import AuditLogger


class TransactionException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class TransactionResult:
    def __init__(
        self,
        success: bool,
        error: Optional[str] = None,
        transaction: Optional[Transaction] = None,
        updated_item: Optional[InventoryItem] = None,
    ):
        self.success = success
        self.error = error
        self.transaction = transaction
        self.updated_item = updated_item

    @classmethod
    def ok(cls, transaction: Transaction, updated_item: InventoryItem) -> "TransactionResult":
        return cls(success=True, transaction=transaction, updated_item=updated_item)

    @classmethod
    def fail(cls, error: str) -> "TransactionResult":
        return cls(success=False, error=error)


class TransactionService:
    def __init__(
        self,
        inventory_repo: InventoryRepository,
        transaction_repo: TransactionRepository,
        audit_logger: AuditLogger,
    ):
        self._inventory_repo = inventory_repo
        self._transaction_repo = transaction_repo
        self._audit_logger = audit_logger

    def stock_in(
        self,
        item_id: str,
        quantity: int,
        reference_id: Optional[str] = None,
        performed_by: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> TransactionResult:
        if quantity <= 0:
            return TransactionResult.fail("Quantity must be greater than zero.")

        item = self._inventory_repo.find_by_id(item_id)
        if item is None:
            return TransactionResult.fail(f"Item not found: {item_id}")

        updated_item = item.copy_with(
            quantity=item.quantity + quantity,
            last_updated=datetime.now(),
        )

        tx = Transaction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            type=TransactionType.STOCK_IN,
            item_id=item.id,
            item_sku=item.sku,
            quantity_delta=quantity,
            quantity_before=item.quantity,
            quantity_after=updated_item.quantity,
            unit_cost=item.unit_cost,
            reference_id=reference_id,
            performed_by=performed_by,
            notes=notes,
        )

        self._inventory_repo.save(updated_item)
        self._transaction_repo.save(tx)
        self._audit_logger.log_stock_in(item, updated_item, user_id=performed_by, notes=notes)

        return TransactionResult.ok(tx, updated_item)

    def stock_out(
        self,
        item_id: str,
        quantity: int,
        reference_id: Optional[str] = None,
        performed_by: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> TransactionResult:
        if quantity <= 0:
            return TransactionResult.fail("Quantity must be greater than zero.")

        item = self._inventory_repo.find_by_id(item_id)
        if item is None:
            return TransactionResult.fail(f"Item not found: {item_id}")

        if item.quantity < quantity:
            return TransactionResult.fail(
                f"Insufficient stock. Available: {item.quantity}, Requested: {quantity}"
            )

        updated_item = item.copy_with(
            quantity=item.quantity - quantity,
            last_updated=datetime.now(),
        )

        tx = Transaction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            type=TransactionType.STOCK_OUT,
            item_id=item.id,
            item_sku=item.sku,
            quantity_delta=-quantity,
            quantity_before=item.quantity,
            quantity_after=updated_item.quantity,
            unit_cost=item.unit_cost,
            reference_id=reference_id,
            performed_by=performed_by,
            notes=notes,
        )

        self._inventory_repo.save(updated_item)
        self._transaction_repo.save(tx)
        self._audit_logger.log_stock_out(item, updated_item, user_id=performed_by, notes=notes)

        return TransactionResult.ok(tx, updated_item)

    def adjust(
        self,
        item_id: str,
        new_quantity: int,
        performed_by: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> TransactionResult:
        if new_quantity < 0:
            return TransactionResult.fail("Quantity cannot be negative.")

        item = self._inventory_repo.find_by_id(item_id)
        if item is None:
            return TransactionResult.fail(f"Item not found: {item_id}")

        delta = new_quantity - item.quantity
        updated_item = item.copy_with(
            quantity=new_quantity,
            last_updated=datetime.now(),
        )

        tx = Transaction(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            type=TransactionType.ADJUSTMENT,
            item_id=item.id,
            item_sku=item.sku,
            quantity_delta=delta,
            quantity_before=item.quantity,
            quantity_after=new_quantity,
            unit_cost=item.unit_cost,
            performed_by=performed_by,
            notes=notes or "Manual adjustment",
        )

        self._inventory_repo.save(updated_item)
        self._transaction_repo.save(tx)
        self._audit_logger.log_adjustment(item, updated_item, user_id=performed_by, notes=notes)

        return TransactionResult.ok(tx, updated_item)