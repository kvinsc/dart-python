# 📝 Summary and Explanation

**Summary:**  
The Dart Transaction System is an internal business application for managing inventory, tracking stock movements, and maintaining immutable audit logs. It is built in pure Dart and uses an in-memory database by default, but can be easily switched to a real database like SQLite using Drift.

**Explanation:**  
- The system is organized into models (entities), repositories (data access), services (business logic), and utilities.
- Inventory items can be created, updated, or deleted, and all stock changes are handled through the `TransactionService` to ensure data integrity.
- Every transaction (stock in, stock out, adjustment) is validated and logged, recording before/after quantities and writing an audit log entry.
- Audit logs capture every change, storing full snapshots of entities before and after modifications, and are never deleted.
- The architecture allows for easy swapping of the database layer without changing business logic, supporting future scalability.

# 📦 Dart Transaction System

An internal business transaction system with **inventory tracking** and **audit logs**, built in pure Dart.

## Project Structure

```
lib/
├── models/
│   ├── inventory_item.dart     # InventoryItem entity
│   ├── transaction.dart        # Transaction entity + TransactionType enum
│   └── audit_log.dart          # AuditLog entity + AuditAction enum
├── repositories/
│   ├── database.dart           # In-memory store (swap for drift/SQLite in prod)
│   ├── inventory_repository.dart
│   ├── transaction_repository.dart
│   └── audit_log_repository.dart
├── services/
│   ├── audit_logger.dart       # Captures before/after snapshots on every write
│   ├── inventory_service.dart  # Create, update, delete items
│   └── transaction_service.dart# stockIn, stockOut, adjust — all atomic
├── utils/
│   ├── service_locator.dart    # Dependency injection / wiring
│   └── report.dart             # Console report helpers
└── main.dart                   # Demo / entry point
```

## Getting Started

```bash
# Install dependencies
dart pub get

# Run the demo
dart run lib/main.dart
```


# Transaction System - File Explanations

## Key Features

  Defines the `AuditLog` class and `AuditAction` enum. Represents audit trail entries for actions (created, updated, deleted, stock in/out, adjustment) on entities like inventory items or transactions. Stores before/after snapshots, user info, and notes.

  The `InventoryItem` class models an inventory item with fields for ID, SKU, name, quantity, unit cost, last updated date, and optional description. Includes a `copyWith` method for immutability.

  Contains the `Transaction` class and `TransactionType` enum. Represents inventory transactions (stock in/out, adjustment, transfer) with details like item, quantity change, before/after quantities, cost, references, and notes.


- All quantity changes go through `TransactionService` — never direct writes

  Implements an in-memory database (`InMemoryDatabase`) for storing inventory items, transactions, and audit logs. Provides CRUD operations and query methods for each entity.

  Repository for inventory items. Provides methods to get all items, find by ID/SKU, check for low stock, save, and delete items.

  Repository for transactions. Methods to get all transactions, filter by item or type, date range, and save new transactions.

  Repository for audit logs. Methods to get all logs, filter by entity, action, user, date range, and save new logs.


| `stockOut` | Remove stock (e.g. customer order fulfilled) |

  The `AuditLogger` class logs audit events for inventory actions (create, update, etc.), serializing before/after states and storing them via the audit log repository.

  Business logic for inventory management. Handles item creation, retrieval, low stock checks, and integrates with the audit logger for traceability.

  Handles inventory transactions (stock in/out, adjustments). Validates operations, updates inventory, logs actions, and returns results with error handling.


- Records `quantityBefore` and `quantityAfter`

  Utility class for printing inventory reports and transaction ledgers in a formatted table style for the CLI.

  Simple service locator pattern to provide singleton access to repositories and services throughout the app.


- Every create/update/delete/stock movement writes an `AuditLog`

  The main CLI application. Presents a menu for inventory and transaction operations, handles user input, and calls the appropriate services.

  Example entrypoint for running a sample calculation or test from the main package.





```yaml
dependencies:
  drift: ^2.14.1
  drift_flutter: ^0.1.0
  sqlite3_flutter_libs: ^0.5.0
  uuid: ^4.3.3
```
