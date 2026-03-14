// lib/repositories/inventory_repository.dart

import 'models/inventory_item.dart';
import 'database.dart';

class InventoryRepository {
  final InMemoryDatabase _db;

  InventoryRepository(this._db);

  List<InventoryItem> getAll() => _db.items;

  InventoryItem? findById(String id) => _db.getItemById(id);

  InventoryItem? findBySku(String sku) => _db.getItemBySku(sku);

  /// Returns all items with quantity at or below [threshold].
  List<InventoryItem> getLowStock(int threshold) =>
      _db.items.where((i) => i.quantity <= threshold).toList();

  void save(InventoryItem item) => _db.upsertItem(item);

  bool delete(String id) => _db.deleteItem(id);

  bool exists(String id) => _db.getItemById(id) != null;

  bool skuExists(String sku) => _db.getItemBySku(sku) != null;
}
