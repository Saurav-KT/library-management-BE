from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.utils.response import success_response, SuccessResponse, error_response
from app.schemas.auth_schema import Login, TokenResponse
from app.service.auth_service import LoginService
from jose import jwt, JWTError
from app.settings.config import SECRET_KEY, ALGORITHM
from app.utils.security import create_access_token, create_refresh_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=SuccessResponse)
async def login(login_data: Login, session: AsyncSession = Depends(get_db)):
        service = LoginService(session)
        result= await service.login(login_data)
        return success_response("Authenticated successfully", data=result,
                                status_code=status.HTTP_200_OK)


@router.post("/refresh")
async def create_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")

        # Create new access token
        new_access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            email=None
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")