enum AuditAction { created, updated, deleted, stockIn, stockOut, adjustment }

class AuditLog {
  final String id;
  final DateTime timestamp;
  final AuditAction action;
  final String entityType;
  final String entityId;
  final String? userId;
  final String? beforeSnapshot;
  final String? afterSnapshot;
  final String? notes;

  AuditLog({
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
        'entityType': entityType,
        'entityId': entityId,
        'userId': userId,
        'beforeSnapshot': beforeSnapshot,
        'afterSnapshot': afterSnapshot,
        'notes': notes,
      };

  factory AuditLog.fromJson(Map<String, dynamic> json) => AuditLog(
        id: json['id'],
        timestamp: DateTime.parse(json['timestamp']),
        action: AuditAction.values.byName(json['action']),
        entityType: json['entityType'],
        entityId: json['entityId'],
        userId: json['userId'],
        beforeSnapshot: json['beforeSnapshot'],
        afterSnapshot: json['afterSnapshot'],
        notes: json['notes'],
      );
}
