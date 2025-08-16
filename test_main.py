from fastapi.testclient import TestClient
from main import app, history  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# TODO Add more tests
def setup_function():
    # Clear history before each test
    history.clear()
    # Add some dummy calculations
    history.append({"expr": "1+1", "result": 2})
    history.append({"expr": "2+2", "result": 4})
    history.append({"expr": "3+3", "result": 6})


def test_history_no_limit():
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_history_limit_small():
    response = client.get("/history?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # Last two expressions should be present
    assert data[0]["expr"] == "2+2"
    assert data[1]["expr"] == "3+3"


def test_history_limit_zero():
    response = client.get("/history?limit=0")
    assert response.status_code == 200
    data = response.json()
    # limit=0 should return all history
    assert len(data) == 3


def test_history_limit_large():
    response = client.get("/history?limit=100000")
    assert response.status_code == 200
    data = response.json()
    # Even with huge limit, should only return available records
    assert len(data) == 3


def test_history_delete_clears_history():
    # Add something to history
    client.post("/calculate", params={"expr": "10*2"})

    # Clear the history
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True

    # Now history should be empty
    r2 = client.get("/history")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2 == []
