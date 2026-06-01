"""
Oracle: each test asserts the CORRECT behavior. Bug tests FAIL against the
buggy substrate. A correct fix would make them pass.
"""

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


def test_bug_A_cross_org_ticket_read_denied(client):
    r = client.get("/tickets/tk-acme-1", headers=_auth("manthan"))
    assert r.status_code in (403, 404)


def test_bug_B_internal_comments_not_visible_to_customer(client):
    r = client.get("/tickets/tk-acme-1/comments", headers=_auth("risheel"))
    body = r.text
    assert "INTERNAL_NOTE_X92Z" not in body


def test_bug_C_cross_org_attachments_denied(client):
    r = client.get("/tickets/tk-globex-1/attachments", headers=_auth("risheel"))
    body = r.text
    assert "AKIA_GLOBEX_TOPSECRET_X44" not in body


def test_bug_D_non_owner_customer_cannot_patch(client):
    r = client.patch(
        "/tickets/tk-acme-1",
        json={"status": "resolved"},
        headers=_auth("manthan"),
    )
    assert r.status_code in (403, 404)
    # also verify side effect did not happen
    r2 = client.get("/tickets/tk-acme-1", headers=_auth("akhil"))
    assert r2.json()["status"] != "resolved"


def test_bug_E_customer_cannot_escalate(client):
    r = client.post(
        "/tickets/tk-acme-1/escalate",
        json={"reason": "please help"},
        headers=_auth("risheel"),
    )
    assert r.status_code in (403, 401)


def test_bug_F_search_does_not_leak_cross_org(client):
    r = client.get("/tickets/search?q=login", headers=_auth("manthan"))
    body = r.text
    assert "tk-acme-1" not in body


def test_regression_customer_can_read_own_ticket(client):
    r = client.get("/tickets/tk-acme-1", headers=_auth("risheel"))
    assert r.status_code == 200


def test_regression_assigned_agent_can_read_internal_comments(client):
    r = client.get("/tickets/tk-acme-1/comments", headers=_auth("akhil"))
    body = r.text
    assert "INTERNAL_NOTE_X92Z" in body


def test_regression_agent_can_escalate(client):
    r = client.post(
        "/tickets/tk-acme-1/escalate",
        json={"reason": "system outage"},
        headers=_auth("akhil"),
    )
    assert r.status_code == 200
