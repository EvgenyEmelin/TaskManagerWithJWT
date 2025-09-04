from passlib.context import CryptContext
from sqlalchemy.util import deprecated
from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError
from config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Optional

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

def hash_password(password:str) -> str:
    """
    Принимает обычный пароль, возвращает его безопасный bcrypt-хеш для сохранения в базе данных.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введённый пароль сохранённому хешу.
    Возвращает True, если пароли совпадают.
    """
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Генерирует JWT токен с данными из data.
    В payload добавляется время истечения срока (exp).
    Возвращает JWT в виде строки.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Декодирует и проверяет JWT токен.
    Если токен валидный, возвращает payload (данные токена).
    Если нет — возвращает None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        return None
