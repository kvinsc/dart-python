// lib/repositories/transaction_repository.dart

import 'models/transaction.dart';
import 'database.dart';

class TransactionRepository {
  final InMemoryDatabase _db;

  TransactionRepository(this._db);

  List<Transaction> getAll() => _db.transactions;

  List<Transaction> getByItemId(String itemId) =>
      _db.getTransactionsForItem(itemId);

  List<Transaction> getByType(TransactionType type) =>
      _db.transactions.where((t) => t.type == type).toList();

  List<Transaction> getByDateRange(DateTime from, DateTime to) =>
      _db.transactions
          .where((t) =>
              t.timestamp.isAfter(from) && t.timestamp.isBefore(to))
          .toList();

  void save(Transaction transaction) => _db.insertTransaction(transaction);
}
