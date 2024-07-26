from typing import Annotated

from fastapi import APIRouter, status, Depends

from app.backend.querys import AsyncORM
from app.schemas import CreateUser
from app.services.routers_logic import is_current_user_admin

router = APIRouter(prefix="/users/admin", tags=["admin"])


async def server_answer(admin_data: Annotated[dict, Depends(is_current_user_admin)]):
    return {'Success': True,
            'action_performed_by': admin_data.get('email')}


@router.get("/")
async def get_all_users(response: Annotated[dict, Depends(server_answer)]):
    response['users'] = await AsyncORM.get_all_users()
    return response


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, response: Annotated[dict, Depends(server_answer)]):
    await AsyncORM.create_user(user)
    return response


@router.put('/update', status_code=status.HTTP_200_OK)
async def update_user(user: CreateUser, user_id: int, response: Annotated[dict, Depends(server_answer)]):
    await AsyncORM.update_user(user_id, user)
    return response


@router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, response: Annotated[dict, Depends(server_answer)]):
    await AsyncORM.delete_user(user_id)
    return response
