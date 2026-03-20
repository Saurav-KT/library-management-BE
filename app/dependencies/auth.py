from fastapi import Depends, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer

from app.settings.config import SECRET_KEY, ALGORITHM
from app.db.database import get_db
from app.models.staff import Staff

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
):
    payload = decode_token(token)
    user_id = payload.get("sub")

    result = await session.execute(
        select(Staff).where(Staff.id == int(user_id))
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# Role-based access
def require_role(role: str):
    async def checker(user: Staff = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return checker