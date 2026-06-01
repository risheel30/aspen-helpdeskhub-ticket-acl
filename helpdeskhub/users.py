from fastapi import APIRouter, Depends, HTTPException

from helpdeskhub.auth import current_user
from helpdeskhub.models import store

router = APIRouter()


@router.get("/me")
def me(user=Depends(current_user)):
    return {
        "id": user.id,
        "name": user.name,
        "org_id": user.org_id,
        "role": user.role,
    }


@router.get("/orgs/{org_id}")
def get_org(org_id: str, user=Depends(current_user)):
    if user.org_id != org_id:
        raise HTTPException(status_code=403, detail="not your org")
    org = store.orgs.get(org_id)
    if org is None:
        raise HTTPException(status_code=404, detail="org not found")
    return {"id": org.id, "name": org.name}


@router.get("/orgs/{org_id}/members")
def list_members(org_id: str, user=Depends(current_user)):
    if user.org_id != org_id:
        raise HTTPException(status_code=403, detail="not your org")
    rows = [
        {"id": u.id, "name": u.name, "role": u.role}
        for u in store.users.values()
        if u.org_id == org_id
    ]
    return {"members": rows}
