// lib/models/transaction.dart

enum TransactionType { stockIn, stockOut, adjustment, transfer }

class Transaction {
  final String id;
  final DateTime timestamp;
  final TransactionType type;
  final String itemId;
  final String itemSku;
  final int quantityDelta; // positive = added, negative = removed
  final int quantityBefore;
  final int quantityAfter;
  final double unitCost;
  final String? referenceId;  // e.g. PO number, invoice number
  final String? performedBy;
  final String? notes;

  const Transaction({
    required this.id,
    required this.timestamp,
    required this.type,
    required this.itemId,
    required this.itemSku,
    required this.quantityDelta,
    required this.quantityBefore,
    required this.quantityAfter,
    required this.unitCost,
    this.referenceId,
    this.performedBy,
    this.notes,
  });

  double get totalValue => quantityDelta.abs() * unitCost;

  Map<String, dynamic> toJson() => {
        'id': id,
        'timestamp': timestamp.toIso8601String(),
        'type': type.name,
        'item_id': itemId,
        'item_sku': itemSku,
        'quantity_delta': quantityDelta,
        'quantity_before': quantityBefore,
        'quantity_after': quantityAfter,
        'unit_cost': unitCost,
        'reference_id': referenceId,
        'performed_by': performedBy,
        'notes': notes,
      };

  factory Transaction.fromJson(Map<String, dynamic> json) => Transaction(
        id: json['id'] as String,
        timestamp: DateTime.parse(json['timestamp'] as String),
        type: TransactionType.values.byName(json['type'] as String),
        itemId: json['item_id'] as String,
        itemSku: json['item_sku'] as String,
        quantityDelta: json['quantity_delta'] as int,
        quantityBefore: json['quantity_before'] as int,
        quantityAfter: json['quantity_after'] as int,
        unitCost: (json['unit_cost'] as num).toDouble(),
        referenceId: json['reference_id'] as String?,
        performedBy: json['performed_by'] as String?,
        notes: json['notes'] as String?,
      );

  @override
  String toString() =>
      'Transaction(id: $id, type: ${type.name}, sku: $itemSku, delta: $quantityDelta)';
}
