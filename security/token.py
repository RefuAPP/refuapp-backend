from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError

from configuration.auth import SecretKeyToken, Algorithm
from configuration.config import Configuration
from models.users import Users

SECRET_KEY = Configuration.get(SecretKeyToken)
ALGORITHM = Configuration.get(Algorithm)


def get_token(user: Users, expires: timedelta) -> str:
    encode = {'sub': user.phone_number, 'id': user.id}
    expires = datetime.utcnow() + expires  # type: ignore
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_id_for(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get('id')
        return user_id
    except JWTError:
        return None
