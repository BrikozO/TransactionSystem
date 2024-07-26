from typing import Annotated

from fastapi import APIRouter, Depends

from app.backend.querys import AsyncORM
from app.schemas import TransactionScheme
from app.services.routers_logic import check_signature

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/")
async def new_transaction(transaction: Annotated[TransactionScheme, Depends(check_signature)]):
    await AsyncORM.get_or_create_wallet(transaction.user_id, transaction.account_id)
    await AsyncORM.save_transaction(transaction.user_id, transaction.account_id, transaction.amount)
    return transaction
