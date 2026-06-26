from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# project imports (expect these to exist in your project)
from database import get_db
from user_repository import UserRepository

SECRET_KEY = "YOURSECRETKEY"
ALGORITHM = "HS256"


def create_access_token(user_id: int):
    payload = {"sub": str(user_id)}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    payload = decode_access_token(token)
    user_id = int(payload["sub"])

    repository = UserRepository(db)

    user = await repository.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
