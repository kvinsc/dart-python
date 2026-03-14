// lib/utils/report.dart

import 'models/audit_log.dart';
import 'models/inventory_item.dart';
import 'models/transaction.dart';

class ReportUtils {
  /// Prints a summary table of all inventory items.
  static void printInventoryReport(List<InventoryItem> items) {
    print('\n══════════════════════════════════════════════');
    print('  INVENTORY REPORT  (${DateTime.now().toLocal()})');
    print('══════════════════════════════════════════════');
    print('${'SKU'.padRight(15)} ${'Name'.padRight(20)} ${'Qty'.padLeft(6)} ${'Unit Cost'.padLeft(10)}');
    print('─' * 56);
    for (final item in items) {
      print(
        '${item.sku.padRight(15)} '
        '${item.name.padRight(20)} '
        '${item.quantity.toString().padLeft(6)} '
        '\$${item.unitCost.toStringAsFixed(2).padLeft(9)}',
      );
    }
    print('══════════════════════════════════════════════\n');
  }

  /// Prints a transaction ledger for a specific item.
  static void printTransactionLedger(
    InventoryItem item,
    List<Transaction> transactions,
  ) {
    print('\n══════════════════════════════════════════════════════════');
    print('  LEDGER: ${item.name} (${item.sku})');
    print('══════════════════════════════════════════════════════════');
    print(
      '${'Date'.padRight(20)} ${'Type'.padRight(12)} ${'Delta'.padLeft(7)} ${'After'.padLeft(7)}',
    );
    print('─' * 52);
    for (final tx in transactions) {
      final delta = tx.quantityDelta > 0 ? '+${tx.quantityDelta}' : '${tx.quantityDelta}';
      print(
        '${tx.timestamp.toLocal().toString().substring(0, 19).padRight(20)} '
        '${tx.type.name.padRight(12)} '
        '${delta.padLeft(7)} '
        '${tx.quantityAfter.toString().padLeft(7)}',
      );
    }
    print('══════════════════════════════════════════════════════════\n');
  }

  /// Prints the audit trail for a specific entity.
  static void printAuditTrail(List<AuditLog> logs) {
    print('\n══════════════════════════════════════════════════════════');
    print('  AUDIT TRAIL');
    print('══════════════════════════════════════════════════════════');
    for (final log in logs) {
      print(
        '[${log.timestamp.toLocal().toString().substring(0, 19)}] '
        '${log.action.name.toUpperCase().padRight(12)} '
        '${log.entityType}[${log.entityId.substring(0, 8)}…] '
        'by: ${log.userId ?? 'system'}',
      );
      if (log.notes != null) print('  → ${log.notes}');
    }
    print('══════════════════════════════════════════════════════════\n');
  }
}
