import threading

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sqldaogenerator.logger.logger import log

default_name = 'default'
transaction_managers = {}


class TransactionManager:
    name: str
    session_maker: sessionmaker
    transaction_thread = threading.local()

    def __new__(cls, name: str, datasource):
        instance = super(TransactionManager, cls).__new__(cls)
        if not hasattr(instance, 'session_maker'):
            instance.name = name
            instance.session_maker = sessionmaker(bind=datasource.engine)
        register_transaction_manager(name, instance)
        return instance

    def __enter__(self):
        session = self.session_maker()
        self.transaction_thread.session = session
        self.transaction_thread.is_exists = True
        return session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transaction_thread.session.close()
        self.transaction_thread.is_exists = False

    def is_exists(self):
        return hasattr(self.transaction_thread, 'is_exists') \
            and self.transaction_thread.is_exists

    def get_transaction(self) -> Session:
        if self.is_exists():
            return self.transaction_thread.session
        else:
            raise LookupError('No existing transaction.')

    def new_transaction(self):
        return self.session_maker()


def register_transaction_manager(name: str, transaction_manager: TransactionManager):
    transaction_managers.update({name: transaction_manager})


def transactional(auto_commit=True, name=default_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if transaction_managers[name].is_exists():
                if auto_commit:
                    log.info(f"{func.__module__}.{func.__name__} "
                             f"participating in an existing transaction[{name}].")
                result = func(*args, **kwargs)
            else:
                if auto_commit:
                    log.info(f"{func.__module__}.{func.__name__} creating a new transaction[{name}].")
                with transaction_managers[name] as session:
                    result = func(*args, **kwargs)
                    if auto_commit:
                        session.commit()
            return result

        return wrapper

    return decorator
