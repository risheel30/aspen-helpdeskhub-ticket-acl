from fastapi import FastAPI

from helpdeskhub.tickets import router as tickets_router
from helpdeskhub.users import router as users_router
from helpdeskhub.seed import reset_and_seed


def create_app() -> FastAPI:
    app = FastAPI(title="helpdeskhub")
    app.include_router(tickets_router)
    app.include_router(users_router)
    reset_and_seed()
    return app


app = create_app()
