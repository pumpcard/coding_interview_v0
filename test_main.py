# test_main.py
from fastapi.testclient import TestClient
from main import app, fetch_instance_offerings, store_instance_data, SessionLocal

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_fetch_aws_data():
    response = client.post("/fetch-aws-data/")
    assert response.status_code == 200
    assert response.json() == {"status": "data fetched and stored"}

def test_get_liquidity():
    # Assuming you've fetched data for 'm5.large'
    response = client.get("/liquidity/m5.large")
    assert response.status_code == 200
    assert "instance_type" in response.json()
    assert "liquidity_rank" in response.json()

def test_get_liquidity_not_found():
    response = client.get("/liquidity/nonexistenttype")
    assert response.status_code == 404
