# aspen-helpdeskhub-ticket-acl

FastAPI helpdesk substrate for the Aspen `aspen__helpdeskhub_ticket_acl_001` test-authoring task.

The substrate intentionally contains cross-org and role-bypass bugs in the ticket read/mutation surface. The agent reads `helpdeskhub/` and writes a pytest suite that catches them while keeping legitimate customer and agent access working.

## Layout

- `helpdeskhub/models.py` — Org, User, Ticket, Comment, Attachment
- `helpdeskhub/tickets.py` — ticket read, comments, attachments, patch, escalate, search
- `helpdeskhub/users.py` — me, org info, members listing
- `helpdeskhub/seed.py` — seeded orgs, users, tickets, comments, attachments
- `helpdeskhub/auth.py` — bearer token plumbing
- `tests/test_smoke.py` — legitimate flow smoke tests

## Local

```
pip install -r requirements.txt
pytest -q
```
