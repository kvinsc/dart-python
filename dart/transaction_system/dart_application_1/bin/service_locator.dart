// lib/utils/service_locator.dart

import 'database.dart';
import 'inventory_repository.dart';
import 'transaction_repository.dart';
import 'audit_log_repository.dart';
import 'audit_logger.dart';
import 'inventory_service.dart';
import 'transaction_service.dart';

/// Simple service locator. Replace with get_it package for larger apps.
class ServiceLocator {
  static ServiceLocator? _instance;
  static ServiceLocator get instance => _instance ??= ServiceLocator._init();

  late final InMemoryDatabase db;
  late final InventoryRepository inventoryRepo;
  late final TransactionRepository transactionRepo;
  late final AuditLogRepository auditLogRepo;
  late final AuditLogger auditLogger;
  late final InventoryService inventoryService;
  late final TransactionService transactionService;

  ServiceLocator._init() {
    db = InMemoryDatabase();
    inventoryRepo = InventoryRepository(db);
    transactionRepo = TransactionRepository(db);
    auditLogRepo = AuditLogRepository(db);
    auditLogger = AuditLogger(auditLogRepo);
    inventoryService = InventoryService(
      repo: inventoryRepo,
      auditLogger: auditLogger,
    );
    transactionService = TransactionService(
      inventoryRepo: inventoryRepo,
      transactionRepo: transactionRepo,
      auditLogger: auditLogger,
    );
  }
}
