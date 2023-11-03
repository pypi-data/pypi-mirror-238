from sqldaogenerator.common.TransactionManager import TransactionManager


class Database:
    name: str
    transactionManager: TransactionManager

    def __init__(self, name='default'):
        self.transactionManager = TransactionManager(name, self)

    def is_transaction_exists(self):
        return self.transactionManager.is_exists()

    def get_transaction(self):
        return self.transactionManager.get_transaction()

    def new_transaction(self):
        return self.transactionManager.new_transaction()
