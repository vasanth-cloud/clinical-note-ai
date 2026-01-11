import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_copd_case():
    response = client.post("/extract", json={
        "text": "72yo male COPD SOB sputum SpO2 88% albuterol prednisone duoneb"
    })
    data = response.json()
    assert response.status_code == 200
    assert "albuterol" in str(data["structured_data"]["medications"])
    assert data["confidence_score"] >= 0.75

# Add 20+ more test cases...
