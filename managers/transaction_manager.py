from storage.db import get_session
from storage.schemas import TransactionORM, AccountORM
from models.transaction import Transaction
from datetime import datetime

class TransactionManager:
    def __init__(self):
        self._session = get_session()

    def create_transaction(self, tx: Transaction):
        if not self._session.get(AccountORM, tx.account_id):
            raise ValueError("Account not found")

        if self._session.get(TransactionORM, tx.id):
            raise ValueError("Transaction id already exists")

        orm = TransactionORM(
            id=tx.id,
            account_id=tx.account_id,
            date=tx.date,
            amount=tx.amount,
            type=tx.type,
            category=tx.category,
            note=tx.note
        )
        self._session.add(orm)
        self._session.commit()
        return tx

    def list_transactions(self, date_from=None, date_to=None):
        q = self._session.query(TransactionORM)
        if date_from:
            q = q.filter(TransactionORM.date >= date_from)
        if date_to:
            q = q.filter(TransactionORM.date <= date_to)
        q = q.order_by(TransactionORM.date)
        rows = q.all()
        return [Transaction(id=r.id, account_id=r.account_id, date=r.date, amount=r.amount, type=r.type, category=r.category, note=r.note) for r in rows]

    def get_transaction(self, transaction_id: str):
        orm = self._session.get(TransactionORM, transaction_id)
        if not orm:
            return None
        return Transaction(id=orm.id, account_id=orm.account_id, date=orm.date, amount=orm.amount, type=orm.type, category=orm.category, note=orm.note)

    def update_transaction(self, transaction_id: str, **kwargs):
        orm = self._session.get(TransactionORM, transaction_id)
        if not orm:
            raise ValueError("Transaction not found")
        
        allowed_fields = ['date', 'amount', 'type', 'category', 'note']
        for key in allowed_fields:
            if key in kwargs and kwargs[key] is not None:
                setattr(orm, key, kwargs[key])
        
        self._session.commit()
        return Transaction(id=orm.id, account_id=orm.account_id, date=orm.date, amount=orm.amount, type=orm.type, category=orm.category, note=orm.note)

    def delete_transaction(self, transaction_id: str):
        orm = self._session.get(TransactionORM, transaction_id)
        if not orm:
            raise ValueError("Transaction not found")
        
        self._session.delete(orm)
        self._session.commit()
        return True
