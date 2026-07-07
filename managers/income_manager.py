from storage.db import get_session
from storage.schemas import IncomeORM, AccountORM
from models.income import Income

class IncomeManager:
    def __init__(self):
        self._session = get_session()

    def create_income(self, inc: Income):
        if not self._session.get(AccountORM, inc.account_id):
            raise ValueError("Account not found")
        if self._session.get(IncomeORM, inc.id):
            raise ValueError("Income id already exists")
        orm = IncomeORM(id=inc.id, account_id=inc.account_id, date=inc.date, amount=inc.amount, source=inc.source)
        self._session.add(orm)
        self._session.commit()
        return inc

    def list_income(self, date_from=None, date_to=None):
        q = self._session.query(IncomeORM)
        if date_from:
            q = q.filter(IncomeORM.date >= date_from)
        if date_to:
            q = q.filter(IncomeORM.date <= date_to)
        q = q.order_by(IncomeORM.date)
        rows = q.all()
        return [Income(id=r.id, account_id=r.account_id, date=r.date, amount=r.amount, source=r.source) for r in rows]

    def get_income(self, income_id: str):
        orm = self._session.get(IncomeORM, income_id)
        if not orm:
            return None
        return Income(id=orm.id, account_id=orm.account_id, date=orm.date, amount=orm.amount, source=orm.source)

    def update_income(self, income_id: str, **kwargs):
        orm = self._session.get(IncomeORM, income_id)
        if not orm:
            raise ValueError("Income not found")
        
        allowed_fields = ['date', 'amount', 'source']
        for key in allowed_fields:
            if key in kwargs and kwargs[key] is not None:
                setattr(orm, key, kwargs[key])
        
        self._session.commit()
        return Income(id=orm.id, account_id=orm.account_id, date=orm.date, amount=orm.amount, source=orm.source)

    def delete_income(self, income_id: str):
        orm = self._session.get(IncomeORM, income_id)
        if not orm:
            raise ValueError("Income not found")
        
        self._session.delete(orm)
        self._session.commit()
        return True
