// lib/services/audit_logger.dart

import 'dart:convert';
import 'package:uuid/uuid.dart';

import 'models/audit_log.dart';
import 'models/inventory_item.dart';
import 'audit_log_repository.dart';

class AuditLogger {
  final AuditLogRepository _repo;
  final Uuid _uuid;

  AuditLogger(this._repo) : _uuid = const Uuid();

  void logItemCreated(InventoryItem item, {String? userId}) {
    _log(
      action: AuditAction.created,
      entityType: 'InventoryItem',
      entityId: item.id,
      userId: userId,
      beforeSnapshot: null,
      afterSnapshot: jsonEncode(item.toJson()),
    );
  }

  void logItemUpdated(
    InventoryItem before,
    InventoryItem after, {
    String? userId,
    String? notes,
  }) {
    _log(
      action: AuditAction.updated,
      entityType: 'InventoryItem',
      entityId: after.id,
      userId: userId,
      beforeSnapshot: jsonEncode(before.toJson()),
      afterSnapshot: jsonEncode(after.toJson()),
      notes: notes,
    );
  }

  void logItemDeleted(InventoryItem item, {String? userId}) {
    _log(
      action: AuditAction.deleted,
      entityType: 'InventoryItem',
      entityId: item.id,
      userId: userId,
      beforeSnapshot: jsonEncode(item.toJson()),
      afterSnapshot: null,
    );
  }

  void logStockIn(
    InventoryItem before,
    InventoryItem after, {
    String? userId,
    String? notes,
  }) {
    _log(
      action: AuditAction.stockIn,
      entityType: 'InventoryItem',
      entityId: after.id,
      userId: userId,
      beforeSnapshot: jsonEncode(before.toJson()),
      afterSnapshot: jsonEncode(after.toJson()),
      notes: notes,
    );
  }

  void logStockOut(
    InventoryItem before,
    InventoryItem after, {
    String? userId,
    String? notes,
  }) {
    _log(
      action: AuditAction.stockOut,
      entityType: 'InventoryItem',
      entityId: after.id,
      userId: userId,
      beforeSnapshot: jsonEncode(before.toJson()),
      afterSnapshot: jsonEncode(after.toJson()),
      notes: notes,
    );
  }

  void logAdjustment(
    InventoryItem before,
    InventoryItem after, {
    String? userId,
    String? notes,
  }) {
    _log(
      action: AuditAction.adjustment,
      entityType: 'InventoryItem',
      entityId: after.id,
      userId: userId,
      beforeSnapshot: jsonEncode(before.toJson()),
      afterSnapshot: jsonEncode(after.toJson()),
      notes: notes,
    );
  }

  void _log({
    required AuditAction action,
    required String entityType,
    required String entityId,
    String? userId,
    String? beforeSnapshot,
    String? afterSnapshot,
    String? notes,
  }) {
    final log = AuditLog(
      id: _uuid.v4(),
      timestamp: DateTime.now(),
      action: action,
      entityType: entityType,
      entityId: entityId,
      userId: userId,
      beforeSnapshot: beforeSnapshot,
      afterSnapshot: afterSnapshot,
      notes: notes,
    );
    _repo.save(log);
  }
}
