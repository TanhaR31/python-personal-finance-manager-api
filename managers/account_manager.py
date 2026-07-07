from storage.db import get_session
from storage.schemas import AccountORM
from models.account import Account

class AccountManager:
    def __init__(self):
        self._session = get_session()

    def create_account(self, account: Account):
        if self._session.get(AccountORM, account.id):
            raise ValueError("Account id already exists")
        orm = AccountORM(id=account.id, name=account.name, currency=account.currency)
        self._session.add(orm)
        self._session.commit()
        return account

    def get_account(self, account_id: str):
        orm = self._session.get(AccountORM, account_id)
        if not orm:
            return None
        return Account(id=orm.id, name=orm.name, currency=orm.currency)

    def list_accounts(self):
        rows = self._session.query(AccountORM).all()
        return [Account(id=r.id, name=r.name, currency=r.currency) for r in rows]

    def update_account(self, account_id: str, **kwargs):
        orm = self._session.get(AccountORM, account_id)
        if not orm:
            raise ValueError("Account not found")
        
        allowed_fields = ['name', 'currency']
        for key in allowed_fields:
            if key in kwargs and kwargs[key] is not None:
                setattr(orm, key, kwargs[key])
        
        self._session.commit()
        return Account(id=orm.id, name=orm.name, currency=orm.currency)

    def delete_account(self, account_id: str):
        orm = self._session.get(AccountORM, account_id)
        if not orm:
            raise ValueError("Account not found")
        
        self._session.delete(orm)
        self._session.commit()
        return True
