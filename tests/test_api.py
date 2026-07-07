import pytest
from app import create_app
from storage.db import init_db, engine, Base
from storage.schemas import AccountORM, TransactionORM, IncomeORM
from sqlalchemy.orm import sessionmaker
import json

@pytest.fixture
def client(tmp_path):
    from config import DB_FILE
    app = create_app()
    app.testing = True
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with app.test_client() as c:
        yield c

def test_create_account_and_income_forecast(client):
    rv = client.post("/accounts", json={"id":"A1","name":"Wallet","currency":"HUF"})
    assert rv.status_code == 201
    rv = client.post("/income", json={"id":"I2025-01","account_id":"A1","date":"2025-01-15","amount":300000,"source":"salary"})
    assert rv.status_code == 201
    rv = client.post("/income", json={"id":"I2025-02","account_id":"A1","date":"2025-02-15","amount":320000,"source":"salary"})
    assert rv.status_code == 201

    rv = client.get("/income")
    data = rv.get_json()
    assert len(data) == 2

    rv = client.get("/stats/income_forecast?n_months=2")
    assert rv.status_code == 200
    body = rv.get_json()
    assert "history" in body and "forecast" in body
    assert len(body["forecast"]) == 2

def test_transactions_summary(client):
    client.post("/accounts", json={"id":"A2","name":"Card","currency":"USD"})
    client.post("/transactions", json={"id":"T1","account_id":"A2","date":"2025-01-05","amount":100,"type":"expense","category":"food"})
    client.post("/transactions", json={"id":"T2","account_id":"A2","date":"2025-01-10","amount":200,"type":"income","category":"bonus"})
    rv = client.get("/stats/summary")
    assert rv.status_code == 200
    body = rv.get_json()
    assert "stats" in body and "by_category" in body
    assert body["stats"]["count"] == 2

def test_account_crud_operations(client):
    
    rv = client.post("/accounts", json={"id":"ACC_CRUD","name":"Test Account","currency":"USD"})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["id"] == "ACC_CRUD"
    assert data["name"] == "Test Account"
    assert data["currency"] == "USD"
    
    rv = client.get("/accounts/ACC_CRUD")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["name"] == "Test Account"
    
    rv = client.get("/accounts")
    assert rv.status_code == 200
    accounts = rv.get_json()
    assert len(accounts) >= 1
    
    rv = client.put("/accounts/ACC_CRUD", json={"name":"Updated Account","currency":"EUR"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["name"] == "Updated Account"
    assert data["currency"] == "EUR"
    
    rv = client.put("/accounts/ACC_CRUD", json={"name":"Final Name"})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["name"] == "Final Name"
    assert data["currency"] == "EUR"
    
    rv = client.delete("/accounts/ACC_CRUD")
    assert rv.status_code == 200
    data = rv.get_json()
    assert "message" in data
    
    rv = client.get("/accounts/ACC_CRUD")
    assert rv.status_code == 404

def test_account_update_not_found(client):
    rv = client.put("/accounts/NONEXISTENT", json={"name":"Test"})
    assert rv.status_code == 404
    data = rv.get_json()
    assert "error" in data

def test_account_delete_not_found(client):
    rv = client.delete("/accounts/NONEXISTENT")
    assert rv.status_code == 404
    data = rv.get_json()
    assert "error" in data

def test_account_cascade_delete(client):
    client.post("/accounts", json={"id":"CASCADE_ACC","name":"Cascade Test","currency":"USD"})
    
    client.post("/income", json={"id":"CASCADE_INC","account_id":"CASCADE_ACC","date":"2025-01-15","amount":1000,"source":"test"})
    client.post("/transactions", json={"id":"CASCADE_TX","account_id":"CASCADE_ACC","date":"2025-01-20","amount":100,"type":"expense","category":"food"})
    
    rv = client.get("/income/CASCADE_INC")
    assert rv.status_code == 200
    
    rv = client.delete("/accounts/CASCADE_ACC")
    assert rv.status_code == 200
    
    rv = client.get("/income/CASCADE_INC")
    assert rv.status_code == 404

def test_income_crud_operations(client):
    
    client.post("/accounts", json={"id":"INC_ACC","name":"Income Test","currency":"USD"})
    
    rv = client.post("/income", json={
        "id":"INC_CRUD",
        "account_id":"INC_ACC",
        "date":"2025-01-15",
        "amount":5000,
        "source":"Salary"
    })
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["id"] == "INC_CRUD"
    assert data["amount"] == 5000
    assert data["source"] == "Salary"
    
    rv = client.get("/income/INC_CRUD")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["amount"] == 5000
    
    rv = client.get("/income")
    assert rv.status_code == 200
    incomes = rv.get_json()
    assert len(incomes) >= 1
    
    rv = client.put("/income/INC_CRUD", json={
        "amount":5500,
        "source":"Salary + Bonus",
        "date":"2025-01-20"
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["amount"] == 5500
    assert data["source"] == "Salary + Bonus"
    assert data["date"] == "2025-01-20"
    
    rv = client.put("/income/INC_CRUD", json={"amount":6000})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["amount"] == 6000
    assert data["source"] == "Salary + Bonus"  # Should remain unchanged
    
    rv = client.delete("/income/INC_CRUD")
    assert rv.status_code == 200
    data = rv.get_json()
    assert "message" in data
    
    rv = client.get("/income/INC_CRUD")
    assert rv.status_code == 404

def test_income_update_not_found(client):
    rv = client.put("/income/NONEXISTENT", json={"amount":1000})
    assert rv.status_code == 404
    data = rv.get_json()
    assert "error" in data

def test_income_delete_not_found(client):
    rv = client.delete("/income/NONEXISTENT")
    assert rv.status_code == 404
    data = rv.get_json()
    assert "error" in data

def test_income_update_validation(client):
    client.post("/accounts", json={"id":"VALID_ACC","name":"Validation Test","currency":"USD"})
    client.post("/income", json={"id":"VALID_INC","account_id":"VALID_ACC","date":"2025-01-15","amount":1000,"source":"test"})
    
    rv = client.put("/income/VALID_INC", json={"amount":-100})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data

def test_account_update_no_fields(client):
    client.post("/accounts", json={"id":"NO_FIELDS","name":"Test","currency":"USD"})
    
    rv = client.put("/accounts/NO_FIELDS", json={})
    assert rv.status_code == 400
    data = rv.get_json()
    assert "error" in data
