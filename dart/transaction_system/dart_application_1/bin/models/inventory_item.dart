class InventoryItem {
  final String id;
  final String sku;
  final String name;
  final int quantity;
  final double unitCost;
  final DateTime lastUpdated;
  final String? description;

  InventoryItem({
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
        'unitCost': unitCost,
        'lastUpdated': lastUpdated.toIso8601String(),
        'description': description,
      };

  factory InventoryItem.fromJson(Map<String, dynamic> json) => InventoryItem(
        id: json['id'],
        sku: json['sku'],
        name: json['name'],
        quantity: json['quantity'],
        unitCost: (json['unitCost'] as num).toDouble(),
        lastUpdated: DateTime.parse(json['lastUpdated']),
        description: json['description'],
      );
}
