from utils.service_locator import ServiceLocator
from utils.report import ReportUtils


def main():
    sl = ServiceLocator()
    inv = sl.inventory_service
    txn = sl.transaction_service
    audit_repo = sl.audit_log_repo
    txn_repo = sl.transaction_repo

    while True:
        print("\n=== Transaction System Menu ===")
        print("1. Add Inventory Item")
        print("2. List Inventory Items")
        print("3. Stock In")
        print("4. Stock Out")
        print("5. Adjust Inventory")
        print("6. View Low Stock")
        print("7. View Inventory Report")
        print("8. View Transaction Ledger")
        print("9. View Audit Trail")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            _add_inventory_item(inv)
        elif choice == "2":
            _list_inventory_items(inv)
        elif choice == "3":
            _stock_in(inv, txn)
        elif choice == "4":
            _stock_out(inv, txn)
        elif choice == "5":
            _adjust_inventory(inv, txn)
        elif choice == "6":
            _view_low_stock(inv)
        elif choice == "7":
            ReportUtils.print_inventory_report(inv.get_all_items())
        elif choice == "8":
            _view_transaction_ledger(inv, txn_repo)
        elif choice == "9":
            ReportUtils.print_audit_trail(audit_repo.get_all())
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


def _add_inventory_item(inv):
    sku = input("SKU: ").strip()
    name = input("Name: ").strip()
    try:
        unit_cost = float(input("Unit Cost: ").strip() or "0")
    except ValueError:
        print("Invalid unit cost. Using 0.")
        unit_cost = 0.0
    
    try:
        qty = int(input("Initial Quantity: ").strip() or "0")
    except ValueError:
        print("Invalid quantity. Using 0.")
        qty = 0
    
    desc = input("Description (optional): ").strip() or None
    created_by = input("Created By: ").strip() or None

    item, err = inv.create_item(
        sku=sku,
        name=name,
        unit_cost=unit_cost,
        initial_quantity=qty,
        description=desc,
        created_by=created_by,
    )
    if item:
        print(f"Item added: {item.name} ({item.sku})")
    else:
        print(f"Error: {err}")


def _list_inventory_items(inv):
    items = inv.get_all_items()
    if not items:
        print("No inventory items found.")
        return
    print("\nInventory Items:")
    for item in items:
        print(f"• {item.name} ({item.sku}) — Qty: {item.quantity}, Unit Cost: ${item.unit_cost:.2f}")


def _stock_in(inv, txn):
    sku = input("Item SKU: ").strip()
    item = inv.get_by_sku(sku)
    if not item:
        print("Item not found.")
        return

    try:
        qty = int(input("Quantity to add: ").strip() or "0")
    except ValueError:
        print("Invalid quantity.")
        return
    
    ref = input("Reference ID (optional): ").strip() or None
    by = input("Performed By: ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    result = txn.stock_in(
        item_id=item.id,
        quantity=qty,
        reference_id=ref,
        performed_by=by,
        notes=notes,
    )
    print("Stock in successful." if result.success else f"Error: {result.error}")


def _stock_out(inv, txn):
    sku = input("Item SKU: ").strip()
    item = inv.get_by_sku(sku)
    if not item:
        print("Item not found.")
        return

    try:
        qty = int(input("Quantity to remove: ").strip() or "0")
    except ValueError:
        print("Invalid quantity.")
        return
    
    ref = input("Reference ID (optional): ").strip() or None
    by = input("Performed By: ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    result = txn.stock_out(
        item_id=item.id,
        quantity=qty,
        reference_id=ref,
        performed_by=by,
        notes=notes,
    )
    print("Stock out successful." if result.success else f"Error: {result.error}")


def _adjust_inventory(inv, txn):
    sku = input("Item SKU: ").strip()
    item = inv.get_by_sku(sku)
    if not item:
        print("Item not found.")
        return

    try:
        new_qty = int(input("New Quantity: ").strip() or str(item.quantity))
    except ValueError:
        print("Invalid quantity.")
        return
    
    by = input("Performed By: ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    result = txn.adjust(
        item_id=item.id,
        new_quantity=new_qty,
        performed_by=by,
        notes=notes,
    )
    print("Adjustment successful." if result.success else f"Error: {result.error}")


def _view_low_stock(inv):
    try:
        threshold = int(input("Threshold: ").strip() or "5")
    except ValueError:
        print("Invalid threshold. Using 5.")
        threshold = 5
    
    low_stock = inv.get_low_stock(threshold=threshold)
    if not low_stock:
        print("No low stock items.")
        return
    print("Low Stock Items:")
    for item in low_stock:
        print(f"• {item.name} ({item.sku}): {item.quantity} units")


def _view_transaction_ledger(inv, txn_repo):
    sku = input("Item SKU: ").strip()
    item = inv.get_by_sku(sku)
    if not item:
        print("Item not found.")
        return

    txns = txn_repo.get_by_item_id(item.id)
    ReportUtils.print_transaction_ledger(item, txns)


if __name__ == "__main__":
    main()