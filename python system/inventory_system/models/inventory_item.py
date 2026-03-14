from datetime import datetime
from typing import Optional, Dict, Any


class InventoryItem:
    def __init__(
        self,
        id: str,
        sku: str,
        name: str,
        quantity: int,
        unit_cost: float,
        last_updated: datetime,
        description: Optional[str] = None,
    ):
        self.id = id
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.unit_cost = unit_cost
        self.last_updated = last_updated
        self.description = description

    def copy_with(
        self,
        id: Optional[str] = None,
        sku: Optional[str] = None,
        name: Optional[str] = None,
        quantity: Optional[int] = None,
        unit_cost: Optional[float] = None,
        last_updated: Optional[datetime] = None,
        description: Optional[str] = None,
    ) -> "InventoryItem":
        return InventoryItem(
            id=id if id is not None else self.id,
            sku=sku if sku is not None else self.sku,
            name=name if name is not None else self.name,
            quantity=quantity if quantity is not None else self.quantity,
            unit_cost=unit_cost if unit_cost is not None else self.unit_cost,
            last_updated=last_updated if last_updated is not None else self.last_updated,
            description=description if description is not None else self.description,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "quantity": self.quantity,
            "unit_cost": self.unit_cost,
            "last_updated": self.last_updated.isoformat(),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InventoryItem":
        return cls(
            id=data["id"],
            sku=data["sku"],
            name=data["name"],
            quantity=data["quantity"],
            unit_cost=float(data["unit_cost"]),
            last_updated=datetime.fromisoformat(data["last_updated"]),
            description=data.get("description"),
        )

    def __str__(self) -> str:
        return f"InventoryItem(id={self.id}, sku={self.sku}, name={self.name}, qty={self.quantity}, cost={self.unit_cost})"