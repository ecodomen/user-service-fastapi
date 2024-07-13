import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.jwt import SecretType, generate_jwt
from fastapi_users.db import SQLAlchemyUserDatabase
from asyncer import asyncify
from app.account.email import (
    generate_new_account_email,
    send_email,
    generate_reset_password_email,
)
from app.account.database import get_user_db
from app.account.models import User
from app.account.schemas import UserCreate, UserRead
from app.core.config import settings


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    def __init__(
        self,
        reset_password_token_secret: SecretType,
        verification_token_secret: SecretType,
        **kwargs,
    ):
        self.reset_password_token_secret = reset_password_token_secret
        self.verification_token_secret = verification_token_secret

        super().__init__(**kwargs)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        email_data = generate_new_account_email(user.email, token)
        await asyncify(send_email)(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.content,
        )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        email_data = generate_reset_password_email(user.email, token)
        await asyncify(send_email)(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.content,
        )

    async def create(  # type: ignore
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Request | None = None,
    ):
        user = await super().create(user_create, safe, request)  # type: ignore
        return UserRead(id=user.id, email=user.email)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(
        reset_password_token_secret=settings.SECRET_KEY,
        verification_token_secret=settings.SECRET_KEY,
        user_db=user_db,
    )
