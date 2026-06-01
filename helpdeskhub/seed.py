from helpdeskhub.models import Org, User, Ticket, Comment, Attachment, store


def reset_and_seed():
    store.orgs.clear()
    store.users.clear()
    store.tickets.clear()
    store.comments.clear()
    store.attachments.clear()
    store.next_id = 1

    store.orgs["acme"] = Org(id="acme", name="Acme Corp")
    store.orgs["globex"] = Org(id="globex", name="Globex Inc")

    store.users["risheel"] = User(id="risheel", name="Risheel", org_id="acme", role="customer")
    store.users["vaibhav"] = User(id="vaibhav", name="Vaibhav", org_id="acme", role="customer")
    store.users["akhil"] = User(id="akhil", name="Akhil", org_id="acme", role="agent")
    store.users["manthan"] = User(id="manthan", name="Manthan", org_id="globex", role="customer")
    store.users["diya"] = User(id="diya", name="Diya", org_id="globex", role="agent")
    store.users["priya"] = User(id="priya", name="Priya", org_id="acme", role="admin")

    store.tickets["tk-acme-1"] = Ticket(
        id="tk-acme-1",
        org_id="acme",
        customer_id="risheel",
        assigned_agent_id="akhil",
        subject="Login is broken",
        body="I cannot sign in to the app since this morning.",
        status="open",
        priority="high",
    )
    store.tickets["tk-acme-2"] = Ticket(
        id="tk-acme-2",
        org_id="acme",
        customer_id="vaibhav",
        assigned_agent_id="akhil",
        subject="Billing question",
        body="Why was I charged twice this month?",
        status="pending",
        priority="normal",
    )
    store.tickets["tk-globex-1"] = Ticket(
        id="tk-globex-1",
        org_id="globex",
        customer_id="manthan",
        assigned_agent_id="diya",
        subject="Export not working",
        body="My CSV export keeps failing with a 500 error.",
        status="open",
        priority="high",
    )

    store.comments.append(
        Comment(
            id=store.new_id("cm"),
            ticket_id="tk-acme-1",
            author_id="akhil",
            visibility="public",
            body="Thanks for reaching out, we are looking into it.",
        )
    )
    store.comments.append(
        Comment(
            id=store.new_id("cm"),
            ticket_id="tk-acme-1",
            author_id="akhil",
            visibility="internal",
            body="Customer mentioned login fails after the morning browser update. Will check auth-service logs for the token expiry trace.",
        )
    )
    store.comments.append(
        Comment(
            id=store.new_id("cm"),
            ticket_id="tk-globex-1",
            author_id="diya",
            visibility="internal",
            body="Globex export pipeline is hitting rate limit on the storage backend. Need to bump the per-tenant quota.",
        )
    )

    store.attachments.append(
        Attachment(
            id=store.new_id("att"),
            ticket_id="tk-acme-1",
            filename="login-error.png",
            content="<binary login error screenshot>",
        )
    )
    store.attachments.append(
        Attachment(
            id=store.new_id("att"),
            ticket_id="tk-globex-1",
            filename="export-failure.log",
            content="Globex storage backend returned a quota error trace with internal endpoint URLs and a sensitive request id from the pipeline.",
        )
    )
