from datetime import date

class Transaction:
    def __init__(self, id: str, account_id: str, date: date, amount: float, type: str, category: str, note: str = ""):
        self.id = id
        self.account_id = account_id
        self.date = date
        self.amount = float(amount)
        self.type = type
        self.category = category
        self.note = note

    def to_dict(self):
        return {
            "id": self.id,
            "account_id": self.account_id,
            "date": self.date.isoformat() if hasattr(self.date, "isoformat") else str(self.date),
            "amount": self.amount,
            "type": self.type,
            "category": self.category,
            "note": self.note
        }
