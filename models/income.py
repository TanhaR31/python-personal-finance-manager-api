from datetime import date

class Income:
    def __init__(self, id: str, account_id: str, date: date, amount: float, source: str = ""):
        self.id = id
        self.account_id = account_id
        self.date = date
        self.amount = float(amount)
        self.source = source

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "date": self.date.isoformat() if hasattr(self.date, "isoformat") else str(self.date),
            "amount": self.amount,
            "source": self.source
        }
