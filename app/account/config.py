import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from app.account.models import User
from app.account.manager import get_user_manager
from app.core.config import settings


_bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def _get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=_bearer_transport,
    get_strategy=_get_jwt_strategy,
)

fa_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
