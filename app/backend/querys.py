from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from app.backend.db import session
from app.models import User, Wallet, Transaction
from app.schemas import CreateUser
from app.services.passwords_generator import PasswordHash


class AsyncORM:

    @staticmethod
    async def get_all_users() -> List[User]:
        async with session() as db:
            users = await db.execute(select(User))
            return users.unique().scalars().all()

    @staticmethod
    async def get_user_by_id(user_id: int = None) -> User:
        async with session() as db:
            user = await db.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return user

    @staticmethod
    def check_user_exists(func):
        async def wrapper(user_id, *args, **kwargs):
            if not isinstance(user_id, int):
                raise ValueError("user_id must be an integer")
            await AsyncORM.get_user_by_id(user_id=user_id)
            result = await func(user_id, *args, **kwargs)
            return result

        return wrapper

    @staticmethod
    @check_user_exists
    async def get_or_create_wallet(user_id: int, wallet_id: int) -> Wallet:
        async with session() as db:
            wallet: Wallet | None = await db.scalar(
                select(Wallet).where(Wallet.id == wallet_id).where(Wallet.user_id == user_id))
            if wallet is None:
                try:
                    wallet = await db.execute(insert(Wallet).values(id=wallet_id, user_id=user_id))
                    await db.commit()
                except IntegrityError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This wallet belongs to another user')
            return wallet

    @staticmethod
    @check_user_exists
    async def save_transaction(user_id: int, wallet_id: int, amount: float):
        async with session() as db:
            await db.execute(insert(Transaction).values(user_id=user_id, wallet_id=wallet_id, amount=amount))
            await db.execute(update(Wallet).where(Wallet.id == wallet_id).values(balance=Wallet.balance + amount))
            await db.commit()

    @staticmethod
    @check_user_exists
    async def get_user_wallets(user_id: int) -> List[Wallet]:
        async with session() as db:
            user = await db.scalar(select(User).where(User.id == user_id))
            return user.wallets

    @staticmethod
    @check_user_exists
    async def get_user_transactions(user_id: int) -> List[Transaction]:
        async with session() as db:
            user = await db.scalar(select(User).where(User.id == user_id))
            return user.transactions

    @staticmethod
    async def get_user_by_auth(email: str, password: str) -> User | None:
        async with session() as db:
            user = await db.scalar(
                select(User).where(User.email == email))
            if user and PasswordHash.check_password(password, user.password):
                return user

    @staticmethod
    async def create_user(user: CreateUser):
        async with session() as db:
            await db.execute(insert(User).values(email=user.email,
                                                 first_name=user.first_name,
                                                 surname=user.surname,
                                                 password=PasswordHash.get_password_hash(
                                                     user.password.get_secret_value()),
                                                 is_admin=user.is_admin))
            await db.commit()

    @staticmethod
    @check_user_exists
    async def update_user(user_id: int, user: CreateUser):
        async with session() as db:
            await db.execute(update(User).where(User.id == user_id).values(email=user.email,
                                                                           first_name=user.first_name,
                                                                           surname=user.surname,
                                                                           password=PasswordHash.get_password_hash(
                                                                               user.password.get_secret_value()),
                                                                           is_admin=user.is_admin))
            await db.commit()

    @staticmethod
    @check_user_exists
    async def delete_user(user_id: int):
        async with session() as db:
            await db.execute(delete(User).where(User.id == user_id))
            await db.commit()
