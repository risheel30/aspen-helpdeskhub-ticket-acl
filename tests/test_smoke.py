import pytest
from fastapi.testclient import TestClient

from helpdeskhub.main import create_app
from helpdeskhub.seed import reset_and_seed


@pytest.fixture
def client():
    reset_and_seed()
    app = create_app()
    return TestClient(app)


def _auth(name: str):
    return {"Authorization": f"Bearer tok-{name}"}


def test_smoke_me_returns_caller(client):
    r = client.get("/me", headers=_auth("risheel"))
    assert r.status_code == 200
    assert r.json()["id"] == "risheel"


def test_smoke_customer_can_read_own_ticket(client):
    r = client.get("/tickets/tk-acme-1", headers=_auth("risheel"))
    assert r.status_code == 200
    assert r.json()["id"] == "tk-acme-1"


def test_smoke_customer_sees_public_comment(client):
    r = client.get("/tickets/tk-acme-1/comments", headers=_auth("risheel"))
    assert r.status_code == 200
    bodies = [c["body"] for c in r.json()["comments"]]
    assert any("Thanks for reaching out" in b for b in bodies)


def test_smoke_no_auth_returns_401(client):
    r = client.get("/tickets/tk-acme-1")
    assert r.status_code == 401


def test_smoke_org_endpoint_scoped(client):
    r = client.get("/orgs/acme", headers=_auth("risheel"))
    assert r.status_code == 200
    r2 = client.get("/orgs/globex", headers=_auth("risheel"))
    assert r2.status_code == 403
