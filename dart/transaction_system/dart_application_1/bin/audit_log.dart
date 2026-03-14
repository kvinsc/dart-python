// lib/models/audit_log.dart

enum AuditAction {
  created,
  updated,
  deleted,
  stockIn,
  stockOut,
  adjustment,
}

class AuditLog {
  final String id;
  final DateTime timestamp;
  final AuditAction action;
  final String entityType;   // e.g. 'InventoryItem', 'Transaction'
  final String entityId;
  final String? userId;
  final String? beforeSnapshot; // JSON string of entity before change
  final String? afterSnapshot;  // JSON string of entity after change
  final String? notes;

  const AuditLog({
    required this.id,
    required this.timestamp,
    required this.action,
    required this.entityType,
    required this.entityId,
    this.userId,
    this.beforeSnapshot,
    this.afterSnapshot,
    this.notes,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'timestamp': timestamp.toIso8601String(),
        'action': action.name,
        'entity_type': entityType,
        'entity_id': entityId,
        'user_id': userId,
        'before_snapshot': beforeSnapshot,
        'after_snapshot': afterSnapshot,
        'notes': notes,
      };

  factory AuditLog.fromJson(Map<String, dynamic> json) => AuditLog(
        id: json['id'] as String,
        timestamp: DateTime.parse(json['timestamp'] as String),
        action: AuditAction.values.byName(json['action'] as String),
        entityType: json['entity_type'] as String,
        entityId: json['entity_id'] as String,
        userId: json['user_id'] as String?,
        beforeSnapshot: json['before_snapshot'] as String?,
        afterSnapshot: json['after_snapshot'] as String?,
        notes: json['notes'] as String?,
      );

  @override
  String toString() =>
      'AuditLog(id: $id, action: ${action.name}, entity: $entityType[$entityId])';
}
