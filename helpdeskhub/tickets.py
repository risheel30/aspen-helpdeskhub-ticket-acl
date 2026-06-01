from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

from helpdeskhub.auth import current_user
from helpdeskhub.models import store, Comment

router = APIRouter()


class TicketPatch(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class EscalateBody(BaseModel):
    reason: Optional[str] = None


def _serialize_ticket(t):
    return {
        "id": t.id,
        "org_id": t.org_id,
        "customer_id": t.customer_id,
        "assigned_agent_id": t.assigned_agent_id,
        "subject": t.subject,
        "body": t.body,
        "status": t.status,
        "priority": t.priority,
    }


def _serialize_comment(c):
    return {
        "id": c.id,
        "ticket_id": c.ticket_id,
        "author_id": c.author_id,
        "visibility": c.visibility,
        "body": c.body,
    }


def _serialize_attachment(a):
    return {
        "id": a.id,
        "ticket_id": a.ticket_id,
        "filename": a.filename,
        "content": a.content,
    }


@router.get("/tickets/search")
def search_tickets(q: str = Query(default=""), user=Depends(current_user)):
    results = []
    for t in store.tickets.values():
        if q.lower() in t.subject.lower() or q.lower() in t.body.lower():
            results.append(_serialize_ticket(t))
    return {"results": results}


@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str, user=Depends(current_user)):
    t = store.tickets.get(ticket_id)
    if t is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return _serialize_ticket(t)


@router.get("/tickets/{ticket_id}/comments")
def list_comments(ticket_id: str, user=Depends(current_user)):
    t = store.tickets.get(ticket_id)
    if t is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    rows = [_serialize_comment(c) for c in store.comments if c.ticket_id == ticket_id]
    return {"comments": rows}


@router.get("/tickets/{ticket_id}/attachments")
def list_attachments(ticket_id: str, user=Depends(current_user)):
    t = store.tickets.get(ticket_id)
    if t is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    rows = [_serialize_attachment(a) for a in store.attachments if a.ticket_id == ticket_id]
    return {"attachments": rows}


@router.patch("/tickets/{ticket_id}")
def patch_ticket(ticket_id: str, patch: TicketPatch, user=Depends(current_user)):
    t = store.tickets.get(ticket_id)
    if t is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    if patch.subject is not None:
        t.subject = patch.subject
    if patch.body is not None:
        t.body = patch.body
    if patch.status is not None:
        t.status = patch.status
    if patch.priority is not None:
        t.priority = patch.priority
    return _serialize_ticket(t)


@router.post("/tickets/{ticket_id}/escalate")
def escalate(ticket_id: str, body: EscalateBody, user=Depends(current_user)):
    t = store.tickets.get(ticket_id)
    if t is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    t.priority = "urgent"
    return _serialize_ticket(t)
