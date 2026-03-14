// lib/repositories/database.dart
// In-memory store — swap for SQLite/drift in production

import 'models/inventory_item.dart';
import 'models/transaction.dart';
import 'models/audit_log.dart';

class InMemoryDatabase {
  static final InMemoryDatabase _instance = InMemoryDatabase._internal();
  factory InMemoryDatabase() => _instance;
  InMemoryDatabase._internal();

  final Map<String, InventoryItem> _items = {};
  final List<Transaction> _transactions = [];
  final List<AuditLog> _auditLogs = [];

  // ── Inventory Items ─────────────────────────────────────────────
  List<InventoryItem> get items => List.unmodifiable(_items.values);

  InventoryItem? getItemById(String id) => _items[id];

  InventoryItem? getItemBySku(String sku) =>
      _items.values.where((i) => i.sku == sku).firstOrNull;

  void upsertItem(InventoryItem item) => _items[item.id] = item;

  bool deleteItem(String id) => _items.remove(id) != null;

  // ── Transactions ─────────────────────────────────────────────────
  List<Transaction> get transactions => List.unmodifiable(_transactions);

  List<Transaction> getTransactionsForItem(String itemId) =>
      _transactions.where((t) => t.itemId == itemId).toList();

  void insertTransaction(Transaction tx) => _transactions.add(tx);

  // ── Audit Logs ────────────────────────────────────────────────────
  List<AuditLog> get auditLogs => List.unmodifiable(_auditLogs);

  List<AuditLog> getLogsForEntity(String entityType, String entityId) =>
      _auditLogs
          .where((l) => l.entityType == entityType && l.entityId == entityId)
          .toList();

  void insertAuditLog(AuditLog log) => _auditLogs.add(log);
}
