// lib/models/inventory_item.dart

class InventoryItem {
  final String id;
  final String sku;
  final String name;
  final int quantity;
  final double unitCost;
  final DateTime lastUpdated;
  final String? description;

  const InventoryItem({
    required this.id,
    required this.sku,
    required this.name,
    required this.quantity,
    required this.unitCost,
    required this.lastUpdated,
    this.description,
  });

  InventoryItem copyWith({
    String? id,
    String? sku,
    String? name,
    int? quantity,
    double? unitCost,
    DateTime? lastUpdated,
    String? description,
  }) {
    return InventoryItem(
      id: id ?? this.id,
      sku: sku ?? this.sku,
      name: name ?? this.name,
      quantity: quantity ?? this.quantity,
      unitCost: unitCost ?? this.unitCost,
      lastUpdated: lastUpdated ?? this.lastUpdated,
      description: description ?? this.description,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'sku': sku,
        'name': name,
        'quantity': quantity,
        'unit_cost': unitCost,
        'last_updated': lastUpdated.toIso8601String(),
        'description': description,
      };

  factory InventoryItem.fromJson(Map<String, dynamic> json) => InventoryItem(
        id: json['id'] as String,
        sku: json['sku'] as String,
        name: json['name'] as String,
        quantity: json['quantity'] as int,
        unitCost: (json['unit_cost'] as num).toDouble(),
        lastUpdated: DateTime.parse(json['last_updated'] as String),
        description: json['description'] as String?,
      );

  @override
  String toString() =>
      'InventoryItem(id: $id, sku: $sku, name: $name, qty: $quantity, cost: $unitCost)';
}
