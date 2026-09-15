from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error
from sqlalchemy import select
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.core.database import async_session_maker
from src.models.admin import Admin


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username", ""))
        password = str(form.get("password", ""))

        async with async_session_maker() as session:
            admin = await session.scalar(
                select(Admin).where(
                    Admin.username == username,
                    Admin.is_active.is_(True),
                )
            )

        if admin is None:
            return False

        password_hasher = PasswordHasher()
        try:
            password_is_valid = password_hasher.verify(
                admin.password_hash,
                password
            )
        except Argon2Error:
            return False

        if not password_is_valid:
            return False

        request.session.update(
            {
                "admin_id": admin.id,
                "admin_username": admin.username,
            }
        )
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        admin_id = request.session.get("admin_id")
        if admin_id is None:
            return False

        async with async_session_maker() as session:
            admin = await session.get(Admin, admin_id)

        return admin is not None and admin.is_active
