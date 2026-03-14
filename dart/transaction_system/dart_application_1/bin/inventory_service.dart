import 'package:uuid/uuid.dart';
// lib/services/inventory_service.dart

import 'models/inventory_item.dart';
import 'inventory_repository.dart';
import 'audit_logger.dart';

class InventoryService {
  final InventoryRepository _repo;
  final AuditLogger _auditLogger;
  final Uuid _uuid;

  InventoryService({
    required InventoryRepository repo,
    required AuditLogger auditLogger,
  })  : _repo = repo,
        _auditLogger = auditLogger,
        _uuid = const Uuid();

  List<InventoryItem> getAllItems() => _repo.getAll();

  InventoryItem? getById(String id) => _repo.findById(id);

  InventoryItem? getBySku(String sku) => _repo.findBySku(sku);

  List<InventoryItem> getLowStock({int threshold = 5}) =>
      _repo.getLowStock(threshold);

  /// Creates a new item. Returns null and a message if SKU already exists.
  (InventoryItem?, String?) createItem({
    required String sku,
    required String name,
    required double unitCost,
    int initialQuantity = 0,
    String? description,
    String? createdBy,
  }) {
    if (_repo.skuExists(sku)) {
      return (null, 'SKU already exists: $sku');
    }

    final item = InventoryItem(
      id: _uuid.v4(),
      sku: sku,
      name: name,
      quantity: initialQuantity,
      unitCost: unitCost,
      lastUpdated: DateTime.now(),
      description: description,
    );

    _repo.save(item);
    _auditLogger.logItemCreated(item, userId: createdBy);
    return (item, null);
  }

  /// Updates item metadata (not quantity — use TransactionService for that).
  (InventoryItem?, String?) updateItem(
    String id, {
    String? name,
    double? unitCost,
    String? description,
    String? updatedBy,
  }) {
    final existing = _repo.findById(id);
    if (existing == null) return (null, 'Item not found: $id');

    final updated = existing.copyWith(
      name: name,
      unitCost: unitCost,
      description: description,
      lastUpdated: DateTime.now(),
    );

    _repo.save(updated);
    _auditLogger.logItemUpdated(existing, updated, userId: updatedBy);
    return (updated, null);
  }

  /// Soft-archives an item. Returns false if not found.
  (bool, String?) deleteItem(String id, {String? deletedBy}) {
    final item = _repo.findById(id);
    if (item == null) return (false, 'Item not found: $id');

    _auditLogger.logItemDeleted(item, userId: deletedBy);
    _repo.delete(id);
    return (true, null);
  }
}
