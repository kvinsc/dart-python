
import 'dart:io';
import 'service_locator.dart';
import 'report.dart';

void main() async {
  final sl = ServiceLocator.instance;
  final inv = sl.inventoryService;
  final txn = sl.transactionService;
  final auditRepo = sl.auditLogRepo;
  final txnRepo = sl.transactionRepo;

  while (true) {
    print('\n=== Transaction System Menu ===');
    print('1. Add Inventory Item');
    print('2. List Inventory Items');
    print('3. Stock In');
    print('4. Stock Out');
    print('5. Adjust Inventory');
    print('6. View Low Stock');
    print('7. View Inventory Report');
    print('8. View Transaction Ledger');
    print('9. View Audit Trail');
    print('0. Exit');
    stdout.write('Select an option: ');
    final choice = stdin.readLineSync();

    switch (choice) {
      case '1':
        await _addInventoryItem(inv);
        break;
      case '2':
        _listInventoryItems(inv);
        break;
      case '3':
        await _stockIn(inv, txn);
        break;
      case '4':
        await _stockOut(inv, txn);
        break;
      case '5':
        await _adjustInventory(inv, txn);
        break;
      case '6':
        _viewLowStock(inv);
        break;
      case '7':
        ReportUtils.printInventoryReport(inv.getAllItems());
        break;
      case '8':
        await _viewTransactionLedger(inv, txnRepo);
        break;
      case '9':
        ReportUtils.printAuditTrail(auditRepo.getAll());
        break;
      case '0':
        print('Goodbye!');
        return;
      default:
        print('Invalid option. Please try again.');
    }
  }
}

Future<void> _addInventoryItem(inv) async {
  stdout.write('SKU: ');
  final sku = stdin.readLineSync() ?? '';
  stdout.write('Name: ');
  final name = stdin.readLineSync() ?? '';
  stdout.write('Unit Cost: ');
  final unitCost = double.tryParse(stdin.readLineSync() ?? '') ?? 0.0;
  stdout.write('Initial Quantity: ');
  final qty = int.tryParse(stdin.readLineSync() ?? '') ?? 0;
  stdout.write('Description (optional): ');
  final desc = stdin.readLineSync();
  stdout.write('Created By: ');
  final createdBy = stdin.readLineSync();
  final (item, err) = inv.createItem(
    sku: sku,
    name: name,
    unitCost: unitCost,
    initialQuantity: qty,
    description: desc,
    createdBy: createdBy,
  );
  if (item != null) {
    print('Item added: ${item.name} (${item.sku})');
  } else {
    print('Error: $err');
  }
}

void _listInventoryItems(inv) {
  final items = inv.getAllItems();
  if (items.isEmpty) {
    print('No inventory items found.');
    return;
  }
  print('\nInventory Items:');
  for (final item in items) {
    print('• ${item.name} (${item.sku}) — Qty: ${item.quantity}, Unit Cost: ${item.unitCost}');
  }
}

Future<void> _stockIn(inv, txn) async {
  stdout.write('Item SKU: ');
  final sku = stdin.readLineSync() ?? '';
  final item = inv.getBySku(sku);
  if (item == null) {
    print('Item not found.');
    return;
  }
  stdout.write('Quantity to add: ');
  final qty = int.tryParse(stdin.readLineSync() ?? '') ?? 0;
  stdout.write('Reference ID (optional): ');
  final ref = stdin.readLineSync();
  stdout.write('Performed By: ');
  final by = stdin.readLineSync();
  stdout.write('Notes (optional): ');
  final notes = stdin.readLineSync();
  final result = txn.stockIn(
    itemId: item.id,
    quantity: qty,
    referenceId: ref,
    performedBy: by,
    notes: notes,
  );
  print(result.success ? 'Stock in successful.' : 'Error: ${result.error}');
}

Future<void> _stockOut(inv, txn) async {
  stdout.write('Item SKU: ');
  final sku = stdin.readLineSync() ?? '';
  final item = inv.getBySku(sku);
  if (item == null) {
    print('Item not found.');
    return;
  }
  stdout.write('Quantity to remove: ');
  final qty = int.tryParse(stdin.readLineSync() ?? '') ?? 0;
  stdout.write('Reference ID (optional): ');
  final ref = stdin.readLineSync();
  stdout.write('Performed By: ');
  final by = stdin.readLineSync();
  stdout.write('Notes (optional): ');
  final notes = stdin.readLineSync();
  final result = txn.stockOut(
    itemId: item.id,
    quantity: qty,
    referenceId: ref,
    performedBy: by,
    notes: notes,
  );
  print(result.success ? 'Stock out successful.' : 'Error: ${result.error}');
}

Future<void> _adjustInventory(inv, txn) async {
  stdout.write('Item SKU: ');
  final sku = stdin.readLineSync() ?? '';
  final item = inv.getBySku(sku);
  if (item == null) {
    print('Item not found.');
    return;
  }
  stdout.write('New Quantity: ');
  final newQty = int.tryParse(stdin.readLineSync() ?? '') ?? item.quantity;
  stdout.write('Performed By: ');
  final by = stdin.readLineSync();
  stdout.write('Notes (optional): ');
  final notes = stdin.readLineSync();
  final result = txn.adjust(
    itemId: item.id,
    newQuantity: newQty,
    performedBy: by,
    notes: notes,
  );
  print(result.success ? 'Adjustment successful.' : 'Error: ${result.error}');
}

void _viewLowStock(inv) {
  stdout.write('Threshold: ');
  final threshold = int.tryParse(stdin.readLineSync() ?? '') ?? 5;
  final lowStock = inv.getLowStock(threshold: threshold);
  if (lowStock.isEmpty) {
    print('No low stock items.');
    return;
  }
  print('Low Stock Items:');
  for (final item in lowStock) {
    print('• ${item.name} (${item.sku}): ${item.quantity} units');
  }
}

Future<void> _viewTransactionLedger(inv, txnRepo) async {
  stdout.write('Item SKU: ');
  final sku = stdin.readLineSync() ?? '';
  final item = inv.getBySku(sku);
  if (item == null) {
    print('Item not found.');
    return;
  }
  final txns = txnRepo.getByItemId(item.id);
  ReportUtils.printTransactionLedger(item, txns);
}
