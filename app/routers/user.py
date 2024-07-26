from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.routers_logic import get_current_user_info, get_current_user_wallets, get_current_user_transactions

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_me(user_data: Annotated[dict, Depends(get_current_user_info)]):
    return user_data


@router.get('/wallets')
async def get_my_wallets(wallets_data: Annotated[dict, Depends(get_current_user_wallets)]):
    return wallets_data


@router.get('/transactions')
async def get_my_transactions(transactions: Annotated[dict, Depends(get_current_user_transactions)]):
    return transactions
