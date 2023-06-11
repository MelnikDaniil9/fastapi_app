from fastapi import FastAPI
from src.auth.auth import auth_backend
from src.api.schemas import UserRead, UserCreate
from src.api.router import router as router_operation, fastapi_users

app = FastAPI(title="CRUD")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
