from datetime import datetime
import requests
import uuid


def assert_balance(user, expected_balance, date=None):
    url = f'http://localhost:8000/v1/user/{user["id"]}'
    if date:
        url += f"?date={date}"
    balance_resp = requests.get(url)
    assert balance_resp.status_code == 200
    assert balance_resp.json()["balance"] == expected_balance


def assert_current_balance(user, expected_balance):
    url = f'http://localhost:8000/v1/user/balance/{user["id"]}'
    balance_resp = requests.get(url)
    assert balance_resp.status_code == 200
    assert balance_resp.json()["balance"] == expected_balance


def test_api():
    user_resp = requests.post("http://localhost:8000/v1/user", json={"name": "petya"})

    assert user_resp.status_code == 201
    user = user_resp.json()
    assert user["id"] > 0
    assert user["name"] == "petya"

    assert_balance(user, 0.0)

    txn = {
        "uid": str(uuid.uuid4()),
        "type": "DEPOSIT",
        "amount": "100.0",
        "user_id": user["id"],
    }
    txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn)
    assert txn_resp.status_code == 201
    assert_balance(user, 100.0)

    detail_resp = requests.get(f'http://localhost:8000/v1/transaction/{txn["uid"]}')
    assert detail_resp.json()["type"] == "DEPOSIT"
    assert detail_resp.json()["amount"] == 100.0

    txn = {
        "uid": str(uuid.uuid4()),
        "type": "WITHDRAW",
        "amount": "50.0",
        "user_id": user["id"],
    }
    txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn)
    assert txn_resp.status_code == 201
    assert_balance(user, 50.0)

    txn = {
        "uid": str(uuid.uuid4()),
        "type": "WITHDRAW",
        "amount": "60.0",
        "user_id": user["id"],
        "timestamp": datetime.utcnow().isoformat(),  # technical field to make tests possible
    }
    txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn)
    assert txn_resp.status_code == 400  # insufficient funds
    assert_balance(user, 50.0)

    txn = {
        "uid": str(uuid.uuid4()),
        "type": "WITHDRAW",
        "amount": "10.0",
        "user_id": user["id"],
        "timestamp": datetime(
            2023, 2, 5
        ).isoformat(),  # technical field to make tests possible
    }
    txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn)
    assert txn_resp.status_code == 201
    assert_balance(user, 40.0)

    assert_current_balance(user, 40.0)
