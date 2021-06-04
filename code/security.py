from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.utils.decor import deprecated_function


# setup to encrypt passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Sicherheit:
    def verify_pwd(plain_pwd, hashed_pwd):
        return pwd_context.verify(plain_pwd, hashed_pwd)

    def get_pwd(pwd: str):
        return pwd_context.hash(pwd)
