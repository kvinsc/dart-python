// lib/repositories/audit_log_repository.dart

import 'models/audit_log.dart';
import 'database.dart';

class AuditLogRepository {
  final InMemoryDatabase _db;

  AuditLogRepository(this._db);

    List<AuditLog> getAll() => _db.auditLogs;

  List<AuditLog> getForEntity(String entityType, String entityId) =>
      _db.getLogsForEntity(entityType, entityId);

  List<AuditLog> getByAction(AuditAction action) =>
      _db.auditLogs.where((l) => l.action == action).toList();

  List<AuditLog> getByUser(String userId) =>
      _db.auditLogs.where((l) => l.userId == userId).toList();

  List<AuditLog> getByDateRange(DateTime from, DateTime to) =>
      _db.auditLogs
          .where((l) =>
              l.timestamp.isAfter(from) && l.timestamp.isBefore(to))
          .toList();

    void save(AuditLog log) => _db.insertAuditLog(log);
}
