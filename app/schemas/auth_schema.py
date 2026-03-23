from pydantic import BaseModel

class Login(BaseModel):
    user_id: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    email: str | None
    token_type: str = "bearer"

