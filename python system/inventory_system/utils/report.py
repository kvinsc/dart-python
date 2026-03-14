from typing import List
from models.inventory_item import InventoryItem
from models.transaction import Transaction
from models.audit_log import AuditLog


class ReportUtils:
    @staticmethod
    def print_inventory_report(items: List[InventoryItem]) -> None:
        print("\n=== Inventory Report ===")
        if not items:
            print("No items in inventory.")
            return
        total_value = sum(item.quantity * item.unit_cost for item in items)
        print(f"{'SKU':<15} {'Name':<25} {'Qty':>8} {'Unit Cost':>12} {'Total Value':>14}")
        print("-" * 78)
        for item in items:
            val = item.quantity * item.unit_cost
            print(f"{item.sku:<15} {item.name:<25} {item.quantity:>8} ${item.unit_cost:>11.2f} ${val:>13.2f}")
        print("-" * 78)
        print(f"{'Total Inventory Value:':>63} ${total_value:>13.2f}")

    @staticmethod
    def print_transaction_ledger(item: InventoryItem, transactions: List[Transaction]) -> None:
        print(f"\n=== Transaction Ledger: {item.name} ({item.sku}) ===")
        if not transactions:
            print("No transactions found.")
            return
        print(f"{'Date':<22} {'Type':<14} {'Delta':>8} {'Before':>8} {'After':>8} {'Value':>12}")
        print("-" * 76)
        for t in sorted(transactions, key=lambda x: x.timestamp):
            date_str = t.timestamp.strftime("%Y-%m-%d %H:%M")
            print(f"{date_str:<22} {t.type.value:<14} {t.quantity_delta:>+8} {t.quantity_before:>8} {t.quantity_after:>8} ${t.total_value:>11.2f}")

    @staticmethod
    def print_audit_trail(logs: List[AuditLog]) -> None:
        print("\n=== Audit Trail ===")
        if not logs:
            print("No audit logs found.")
            return
        for log in sorted(logs, key=lambda x: x.timestamp):
            ts = log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            user = log.user_id or "system"
            notes = f" | {log.notes}" if log.notes else ""
            print(f"[{ts}] {log.action.value.upper():<12} {log.entity_type}:{log.entity_id[:8]}... by {user}{notes}")
