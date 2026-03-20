from jose import jwt
from datetime import datetime, timedelta,UTC
from app.settings.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRATION_TIME_MINUTES

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
def hash_password(pwd)-> str:
    return ph.hash(pwd)

def verify_password(pwd_hash: str, pwd: str)->bool:
    try:
        ph.verify(pwd_hash, pwd)
        return True
    except VerifyMismatchError:
        return False

def create_access_token(email)-> str:
    # now + token lifespan
    expiration_time = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload={
        "sub": email,
        "exp": expiration_time,
        "type": "access"
    }
    token= jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def create_refresh_token(email) -> str:
    expiration_time = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time,
        "type": "refresh"
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

