// lib/services/transaction_service.dart

import 'package:uuid/uuid.dart';
import 'models/inventory_item.dart';
import 'models/transaction.dart';
import 'inventory_repository.dart';
import 'transaction_repository.dart';
import 'audit_logger.dart';

class TransactionException implements Exception {
  final String message;
  TransactionException(this.message);

  @override
  String toString() => 'TransactionException: $message';
}

class TransactionResult {
  final bool success;
  final String? error;
  final Transaction? transaction;
  final InventoryItem? updatedItem;

  const TransactionResult.ok({
    required this.transaction,
    required this.updatedItem,
  })  : success = true,
        error = null;

  const TransactionResult.fail(this.error)
      : success = false,
        transaction = null,
        updatedItem = null;
}

class TransactionService {
  final InventoryRepository _inventoryRepo;
  final TransactionRepository _transactionRepo;
  final AuditLogger _auditLogger;
  final Uuid _uuid;

  TransactionService({
    required InventoryRepository inventoryRepo,
    required TransactionRepository transactionRepo,
    required AuditLogger auditLogger,
  })  : _inventoryRepo = inventoryRepo,
        _transactionRepo = transactionRepo,
        _auditLogger = auditLogger,
        _uuid = const Uuid();

  // ── Stock In ──────────────────────────────────────────────────────
  TransactionResult stockIn({
    required String itemId,
    required int quantity,
    String? referenceId,
    String? performedBy,
    String? notes,
  }) {
    if (quantity <= 0) {
      return const TransactionResult.fail('Quantity must be greater than zero.');
    }

    final item = _inventoryRepo.findById(itemId);
    if (item == null) {
      return TransactionResult.fail('Item not found: $itemId');
    }

    final updatedItem = item.copyWith(
      quantity: item.quantity + quantity,
      lastUpdated: DateTime.now(),
    );

      final tx = Transaction(
        id: _uuid.v4(),
        timestamp: DateTime.now(),
        type: TransactionType.stockIn,
      itemId: item.id,
      itemSku: item.sku,
      quantityDelta: quantity,
      quantityBefore: item.quantity,
      quantityAfter: updatedItem.quantity,
      unitCost: item.unitCost,
      referenceId: referenceId,
      performedBy: performedBy,
      notes: notes,
    );

    // Atomic: save both item + transaction + audit log
    _inventoryRepo.save(updatedItem);
    _transactionRepo.save(tx);
    _auditLogger.logStockIn(item, updatedItem, userId: performedBy, notes: notes);

    return TransactionResult.ok(transaction: tx, updatedItem: updatedItem);
  }

  // ── Stock Out ─────────────────────────────────────────────────────
  TransactionResult stockOut({
    required String itemId,
    required int quantity,
    String? referenceId,
    String? performedBy,
    String? notes,
  }) {
    if (quantity <= 0) {
      return const TransactionResult.fail('Quantity must be greater than zero.');
    }

    final item = _inventoryRepo.findById(itemId);
    if (item == null) {
      return TransactionResult.fail('Item not found: $itemId');
    }

    if (item.quantity < quantity) {
      return TransactionResult.fail(
        'Insufficient stock. Available: ${item.quantity}, Requested: $quantity',
      );
    }

    final updatedItem = item.copyWith(
      quantity: item.quantity - quantity,
      lastUpdated: DateTime.now(),
    );

    final tx = Transaction(
      id: _uuid.v4(),
      timestamp: DateTime.now(),
      type: TransactionType.stockOut,
      itemId: item.id,
      itemSku: item.sku,
      quantityDelta: -quantity,
      quantityBefore: item.quantity,
      quantityAfter: updatedItem.quantity,
      unitCost: item.unitCost,
      referenceId: referenceId,
      performedBy: performedBy,
      notes: notes,
    );

    _inventoryRepo.save(updatedItem);
    _transactionRepo.save(tx);
    _auditLogger.logStockOut(item, updatedItem, userId: performedBy, notes: notes);

    return TransactionResult.ok(transaction: tx, updatedItem: updatedItem);
  }

  // ── Manual Adjustment ─────────────────────────────────────────────
  TransactionResult adjust({
    required String itemId,
    required int newQuantity,
    String? performedBy,
    String? notes,
  }) {
    if (newQuantity < 0) {
      return const TransactionResult.fail('Quantity cannot be negative.');
    }

    final item = _inventoryRepo.findById(itemId);
    if (item == null) {
      return TransactionResult.fail('Item not found: $itemId');
    }

    final delta = newQuantity - item.quantity;
    final updatedItem = item.copyWith(
      quantity: newQuantity,
      lastUpdated: DateTime.now(),
    );

    final tx = Transaction(
      id: _uuid.v4(),
      timestamp: DateTime.now(),
      type: TransactionType.adjustment,
      itemId: item.id,
      itemSku: item.sku,
      quantityDelta: delta,
      quantityBefore: item.quantity,
      quantityAfter: newQuantity,
      unitCost: item.unitCost,
      performedBy: performedBy,
      notes: notes ?? 'Manual adjustment',
    );

    _inventoryRepo.save(updatedItem);
    _transactionRepo.save(tx);
    _auditLogger.logAdjustment(item, updatedItem, userId: performedBy, notes: notes);

    return TransactionResult.ok(transaction: tx, updatedItem: updatedItem);
  }
}
