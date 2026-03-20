from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.schemas.auth_schema import Login, TokenResponse
from app.models.staff import Staff
from app.utils.security import verify_password
from app.core.exception import UnauthorizedException
from app.utils.security import create_access_token, create_refresh_token
class LoginService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, login_data: Login) -> TokenResponse:
            # Fetch user from DB
            result = await self.session.execute(
                select(Staff).where(Staff.email == login_data.user_id)
            )
            user = result.scalars().first()

            if not user:
                raise UnauthorizedException("Invalid user ID or password")

            # Verify password
            is_valid = verify_password(user.password_hash, login_data.password)

            if  not is_valid:
                raise UnauthorizedException("Invalid user ID or password")

            access_token = create_access_token(email=user.email)
            refresh_token= create_refresh_token(email=user.email)
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
            )

