from typing import List, Optional
from datetime import datetime
from models.transaction import Transaction, TransactionType
from repositories.database import InMemoryDatabase


class TransactionRepository:
    def __init__(self, db: InMemoryDatabase):
        self._db = db

    def get_all(self) -> List[Transaction]:
        return self._db.transactions

    def get_by_item_id(self, item_id: str) -> List[Transaction]:
        return self._db.get_transactions_for_item(item_id)

    def get_by_type(self, type: TransactionType) -> List[Transaction]:
        return [t for t in self._db.transactions if t.type == type]

    def get_by_date_range(self, from_date: datetime, to_date: datetime) -> List[Transaction]:
        return [
            t for t in self._db.transactions
            if from_date < t.timestamp < to_date
        ]

    def save(self, transaction: Transaction) -> None:
        self._db.insert_transaction(transaction)