from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class PasswordHash:
    bcrypt_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.bcrypt_context.hash(password)

    @classmethod
    def check_password(cls, password: str, hashed_password: str) -> bool:
        return cls.bcrypt_context.verify(password, hashed_password)
