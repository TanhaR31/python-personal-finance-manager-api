class Account:
    def __init__(self, id: str, name: str, currency: str):
        self.id = id
        self.name = name
        self.currency = currency

    def to_dict(self):
        return {"id": self.id, "name": self.name, "currency": self.currency}
