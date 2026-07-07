from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from storage.db import Base

class AccountORM(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    transactions = relationship("TransactionORM", back_populates="account", cascade="all, delete-orphan")
    incomes = relationship("IncomeORM", back_populates="account", cascade="all, delete-orphan")

class TransactionORM(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    note = Column(String, default="")

    account = relationship("AccountORM", back_populates="transactions")

class IncomeORM(Base):
    __tablename__ = "income"
    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    source = Column(String, default="")

    account = relationship("AccountORM", back_populates="incomes")
