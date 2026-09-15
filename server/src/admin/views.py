from argon2 import PasswordHasher
from sqladmin import ModelView
from sqladmin.filters import BooleanFilter
from sqladmin.filters import ForeignKeyFilter

from src.models.admin import Admin
from src.models.app_settings import AppSettings
from src.models.prize import Prize
from src.models.spin import Spin
from src.models.user import User


class PrizeView(ModelView, model=Prize):
    name = "Prize"
    name_plural = "Prizes"
    icon = "fa-solid fa-gift"

    column_list = [
        Prize.id,
        Prize.name,
        Prize.is_active,
        Prize.quantity,
    ]
    column_searchable_list = [Prize.name]
    column_sortable_list = [
        Prize.id,
        Prize.name,
        Prize.is_active,
        Prize.quantity,
    ]
    column_filters = [BooleanFilter(Prize.is_active)]
    form_columns = [
        Prize.name,
        Prize.is_active,
        Prize.quantity,
    ]


class TelegramUserView(ModelView, model=User):
    name = "Telegram User"
    name_plural = "Telegram Users"
    icon = "fa-solid fa-users"
    can_create = False
    can_edit = False

    column_list = [
        User.id,
        User.telegram_id,
        User.username,
    ]
    column_searchable_list = [
        User.username,
    ]
    column_sortable_list = [
        User.id,
        User.telegram_id,
        User.username,
    ]


class SpinView(ModelView, model=Spin):
    name = "Spin"
    name_plural = "Spins"
    icon = "fa-solid fa-rotate"
    can_create = False
    can_edit = False
    can_delete = True

    column_list = [
        Spin.id,
        Spin.user,
        Spin.prize,
    ]
    column_sortable_list = [
        Spin.id,
        Spin.user_id,
        Spin.prize_id,
    ]
    column_filters = [
        ForeignKeyFilter(Spin.prize_id, Prize.name, Prize),
    ]


class AdminUserView(ModelView, model=Admin):
    name = "Admin"
    name_plural = "Admins"
    icon = "fa-solid fa-user-shield"

    column_list = [
        Admin.id,
        Admin.username,
        Admin.is_active,
    ]
    column_searchable_list = [Admin.username]
    column_sortable_list = [
        Admin.id,
        Admin.username,
        Admin.is_active,
    ]
    column_filters = [BooleanFilter(Admin.is_active)]
    form_columns = [
        Admin.username,
        Admin.password_hash,
        Admin.is_active,
    ]
    form_args = {
        "password_hash": {
            "label": "Password or Argon2 hash",
            "description": "Plain text is hashed before saving.",
        },
    }

    async def on_model_change(self, data, model, is_created, request) -> None:
        password_value = data.get("password_hash")
        if not password_value:
            return

        if str(password_value).startswith("$argon2"):
            return

        data["password_hash"] = PasswordHasher().hash(str(password_value))


class AppSettingsView(ModelView, model=AppSettings):
    name = "App Settings"
    name_plural = "App Settings"
    icon = "fa-solid fa-gear"

    column_list = [
        AppSettings.id,
        AppSettings.greeting_message,
        AppSettings.post_spin_message,
    ]
    column_sortable_list = [
        AppSettings.id,
    ]
    form_columns = [
        AppSettings.greeting_message,
        AppSettings.post_spin_message,
    ]
    form_widget_args = {
        "greeting_message": {
            "rows": 6,
        },
        "post_spin_message": {
            "rows": 6,
        },
    }
    form_args = {
        "greeting_message": {
            "label": "Greeting message",
            "description": "Optional. Bot uses local config fallback when empty.",
        },
        "post_spin_message": {
            "label": "Post-spin message",
            "description": "Optional. Sent as a second Telegram message after prize notification.",
        },
    }
