enum TransactionType { stockIn, stockOut, adjustment }

class Transaction {
  final String id;
  final DateTime timestamp;
  final TransactionType type;
  final String itemId;
  final String itemSku;
  final int quantityDelta;
  final int quantityBefore;
  final int quantityAfter;
  final double unitCost;
  final String? referenceId;
  final String? performedBy;
  final String? notes;

  Transaction({
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

  Map<String, dynamic> toJson() => {
        'id': id,
        'timestamp': timestamp.toIso8601String(),
        'type': type.name,
        'itemId': itemId,
        'itemSku': itemSku,
        'quantityDelta': quantityDelta,
        'quantityBefore': quantityBefore,
        'quantityAfter': quantityAfter,
        'unitCost': unitCost,
        'referenceId': referenceId,
        'performedBy': performedBy,
        'notes': notes,
      };

  factory Transaction.fromJson(Map<String, dynamic> json) => Transaction(
        id: json['id'],
        timestamp: DateTime.parse(json['timestamp']),
        type: TransactionType.values.byName(json['type']),
        itemId: json['itemId'],
        itemSku: json['itemSku'],
        quantityDelta: json['quantityDelta'],
        quantityBefore: json['quantityBefore'],
        quantityAfter: json['quantityAfter'],
        unitCost: (json['unitCost'] as num).toDouble(),
        referenceId: json['referenceId'],
        performedBy: json['performedBy'],
        notes: json['notes'],
      );
}
