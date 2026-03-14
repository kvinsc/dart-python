from repositories.database import InMemoryDatabase
from repositories.inventory_repository import InventoryRepository
from repositories.transaction_repository import TransactionRepository
from repositories.audit_log_repository import AuditLogRepository
from services.audit_logger import AuditLogger
from services.inventory_service import InventoryService
from services.transaction_service import TransactionService


class ServiceLocator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Initialize database and repositories
        self.db = InMemoryDatabase()
        self.inventory_repo = InventoryRepository(self.db)
        self.transaction_repo = TransactionRepository(self.db)
        self.audit_log_repo = AuditLogRepository(self.db)

        # Initialize services
        self.audit_logger = AuditLogger(self.audit_log_repo)
        self.inventory_service = InventoryService(
            repo=self.inventory_repo,
            audit_logger=self.audit_logger,
        )
        self.transaction_service = TransactionService(
            inventory_repo=self.inventory_repo,
            transaction_repo=self.transaction_repo,
            audit_logger=self.audit_logger,
        )