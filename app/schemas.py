from pydantic import BaseModel, Field, EmailStr, SecretStr


class CreateUser(BaseModel):
    email: EmailStr
    first_name: str
    surname: str
    password: SecretStr
    is_admin: bool = Field(default=False)


class AuthorizeUser(BaseModel):
    email: EmailStr
    password: SecretStr


class TransactionScheme(BaseModel):
    transaction_id: str
    user_id: int
    account_id: int
    amount: float
    signature: str
