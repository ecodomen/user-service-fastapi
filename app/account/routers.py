from fastapi import APIRouter
from app.account.config import fa_users, auth_backend
from app.account.schemas import UserRead, UserCreate, UserUpdate


router = APIRouter()

router.include_router(
    fa_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

router.include_router(
    fa_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fa_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fa_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fa_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
