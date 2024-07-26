from fastapi import APIRouter
from app.schemas import AuthorizeUser
from app.services.auth import Authorization

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(user_data: AuthorizeUser | None = None):
    user = await Authorization.authenticate_user(user_data.email, user_data.password.get_secret_value())
    user_data: dict = {'id': user.id,
                       'email': user.email,
                       'first_name': user.first_name,
                       'surname': user.surname,
                       'is_admin': user.is_admin}
    token: str = await Authorization.create_access_token(user_data)
    return {'token': token}
