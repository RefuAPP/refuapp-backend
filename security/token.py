from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError

from configuration.auth import SecretKeyToken, Algorithm
from configuration.config import Configuration
from schemas.auth import TokenData

SECRET_KEY = Configuration.get(SecretKeyToken)
ALGORITHM = Configuration.get(Algorithm)


def get_token(data: TokenData, expires: timedelta) -> str:
    encode = dict(data)
    expires = datetime.utcnow() + expires  # type: ignore
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_data_for(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        identifier: Optional[str] = payload.get('id')
        scopes: Optional[list[str]] = payload.get('scopes')
        if identifier is None or scopes is None:
            return None
        return TokenData(id=identifier, scopes=scopes)
    except JWTError:
        return None
