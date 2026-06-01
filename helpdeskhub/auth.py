from fastapi import Header, HTTPException
from helpdeskhub.models import store, User


def current_user(authorization: str = Header(default="")) -> User:
    if not authorization.startswith("Bearer tok-"):
        raise HTTPException(status_code=401, detail="missing bearer token")
    uid = authorization[len("Bearer tok-"):].strip()
    user = store.users.get(uid)
    if user is None:
        raise HTTPException(status_code=401, detail="unknown user")
    return user
