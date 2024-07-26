import hashlib
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError

from app.backend.querys import AsyncORM
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import TransactionScheme
from app.services.auth import Authorization


async def get_current_user(token: Annotated[str, Depends(Authorization.TOKEN_URI)]) -> dict:
    exception: HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail='Could not validate credentials')
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('email')
        if email is None:
            raise exception
    except InvalidTokenError:
        raise exception
    return payload


async def get_current_user_info(current_user_data: Annotated[dict, Depends(get_current_user)]) -> dict:
    user_data: dict = {'id': current_user_data.get('id'),
                       'email': current_user_data.get('email'),
                       'full_name': current_user_data.get('first_name') + ' ' + current_user_data.get('surname')}
    return user_data


async def get_current_user_wallets(current_user_data: Annotated[dict, Depends(get_current_user)]) -> dict:
    user_id: int = current_user_data.get('id')
    wallets_data: dict = {'id': user_id,
                          'wallets': await AsyncORM.get_user_wallets(user_id)}
    return wallets_data


async def get_current_user_transactions(current_user_data: Annotated[dict, Depends(get_current_user)]) -> dict:
    user_id: int = current_user_data.get('id')
    transactions_data: dict = {'id': user_id,
                               'transactions': await AsyncORM.get_user_transactions(user_id)}
    return transactions_data


async def is_current_user_admin(current_user_data: Annotated[dict, Depends(get_current_user)]) -> dict:
    if not current_user_data.get('is_admin'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have permission to perform this action")
    return current_user_data


# WEBHOOK SIGNATURE CHECK
async def check_signature(transaction: TransactionScheme):
    wallet_id: int = transaction.account_id
    amount: str = str(transaction.amount) if int(transaction.amount) != transaction.amount else str(
        int(transaction.amount))
    transaction_uuid: str = transaction.transaction_id
    user_id: int = transaction.user_id
    signature = hashlib.sha256(f'{wallet_id}{amount}{transaction_uuid}{user_id}{SECRET_KEY}'.encode()).hexdigest()
    if transaction.signature != signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Signature does not match')
    return transaction
