from sqladmin import Admin
from fastapi import FastAPI

from src.admin.auth import AdminAuth

from src.admin.views import SpinView
from src.admin.views import PrizeView
from src.admin.views import AppSettingsView
from src.admin.views import AdminUserView
from src.admin.views import TelegramUserView

from src.core.config import settings

from src.core.database import async_engine
from src.core.database import async_session_maker


def setup_admin(app: FastAPI) -> Admin:
    admin = Admin(
        app=app,
        engine=async_engine,
        session_maker=async_session_maker,
        title=settings.ADMIN_TITLE,
        favicon_url="/static/admin/favicon.png",
        authentication_backend=AdminAuth(
            secret_key=settings.ADMIN_SECRET_KEY.get_secret_value()
        ),
    )

    admin.add_view(PrizeView)
    admin.add_view(SpinView)
    admin.add_view(AppSettingsView)
    admin.add_view(AdminUserView)
    admin.add_view(TelegramUserView)

    return admin
