import argparse
import asyncio
import getpass
from collections.abc import Sequence

from argon2 import PasswordHasher
from sqlalchemy import select

from src.core.database import async_session_maker
from src.models.admin import Admin


async def create_admin(username: str) -> int:
    password = getpass.getpass("Password: ")
    password_repeat = getpass.getpass("Repeat password: ")

    if not password:
        print("Password cannot be empty.")
        return 1

    if password != password_repeat:
        print("Passwords do not match.")
        return 1

    async with async_session_maker() as session:
        existing_admin = await session.scalar(
            select(Admin).where(Admin.username == username)
        )
        if existing_admin is not None:
            print(f"Admin '{username}' already exists.")
            return 1

        admin = Admin(
            username=username,
            password_hash=PasswordHasher().hash(password),
            is_active=True,
        )
        session.add(admin)
        await session.commit()

    print(f"Admin '{username}' created.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m src.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_admin_parser = subparsers.add_parser(
        "create-admin",
        help="Create the first admin user.",
    )
    create_admin_parser.add_argument(
        "--username",
        required=True,
        help="Admin username.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "create-admin":
        return asyncio.run(create_admin(args.username))

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
