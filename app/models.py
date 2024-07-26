from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(64))
    surname: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(128))

    is_admin: Mapped[bool] = mapped_column(default=False)

    wallets: Mapped[List['Wallet']] = relationship(back_populates='user', lazy='joined')

    transactions: Mapped[List['Transaction']] = relationship(back_populates='user', lazy='joined')

    def get_full_name(self):
        return self.first_name + ' ' + self.surname

    def __repr__(self):
        return f'User: {self.get_full_name()}'


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='wallets')

    transactions: Mapped[List['Transaction']] = relationship(back_populates='wallet')

    def __repr__(self):
        return f'Wallet: {self.id} with balance {self.balance}'


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(default=0.0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    wallet_id: Mapped[int] = mapped_column(ForeignKey('wallets.id'))

    user: Mapped['User'] = relationship(back_populates='transactions')
    wallet: Mapped['Wallet'] = relationship(back_populates='transactions')

    def __repr__(self):
        return f'Transaction: {self.id} with amount - {self.amount}'
