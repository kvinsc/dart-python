from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any


class TransactionType(Enum):
    STOCK_IN = "stockIn"
    STOCK_OUT = "stockOut"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"


class Transaction:
    def __init__(
        self,
        id: str,
        timestamp: datetime,
        type: TransactionType,
        item_id: str,
        item_sku: str,
        quantity_delta: int,
        quantity_before: int,
        quantity_after: int,
        unit_cost: float,
        reference_id: Optional[str] = None,
        performed_by: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        self.id = id
        self.timestamp = timestamp
        self.type = type
        self.item_id = item_id
        self.item_sku = item_sku
        self.quantity_delta = quantity_delta
        self.quantity_before = quantity_before
        self.quantity_after = quantity_after
        self.unit_cost = unit_cost
        self.reference_id = reference_id
        self.performed_by = performed_by
        self.notes = notes

    @property
    def total_value(self) -> float:
        return abs(self.quantity_delta) * self.unit_cost

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "type": self.type.value,
            "item_id": self.item_id,
            "item_sku": self.item_sku,
            "quantity_delta": self.quantity_delta,
            "quantity_before": self.quantity_before,
            "quantity_after": self.quantity_after,
            "unit_cost": self.unit_cost,
            "reference_id": self.reference_id,
            "performed_by": self.performed_by,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transaction":
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            type=TransactionType(data["type"]),
            item_id=data["item_id"],
            item_sku=data["item_sku"],
            quantity_delta=data["quantity_delta"],
            quantity_before=data["quantity_before"],
            quantity_after=data["quantity_after"],
            unit_cost=float(data["unit_cost"]),
            reference_id=data.get("reference_id"),
            performed_by=data.get("performed_by"),
            notes=data.get("notes"),
        )

    def __str__(self) -> str:
        return f"Transaction(id={self.id}, type={self.type.value}, sku={self.item_sku}, delta={self.quantity_delta})"