from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Org:
    id: str
    name: str


@dataclass
class User:
    id: str
    name: str
    org_id: str
    role: str  # "customer", "agent", "admin"


@dataclass
class Ticket:
    id: str
    org_id: str
    customer_id: str
    assigned_agent_id: Optional[str]
    subject: str
    body: str
    status: str  # "open", "pending", "resolved", "closed"
    priority: str  # "low", "normal", "high", "urgent"


@dataclass
class Comment:
    id: str
    ticket_id: str
    author_id: str
    visibility: str  # "public" (visible to customer) or "internal" (agents only)
    body: str


@dataclass
class Attachment:
    id: str
    ticket_id: str
    filename: str
    content: str


@dataclass
class Store:
    orgs: dict = field(default_factory=dict)
    users: dict = field(default_factory=dict)
    tickets: dict = field(default_factory=dict)
    comments: list = field(default_factory=list)
    attachments: list = field(default_factory=list)
    next_id: int = 1

    def new_id(self, prefix: str) -> str:
        x = self.next_id
        self.next_id += 1
        return f"{prefix}-{x:04d}"


store = Store()
