from datetime import datetime, timedelta
from typing import Optional
import logging

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User

logger = logging.getLogger(__name__)

# Use PBKDF2-SHA256 by default in development to avoid bcrypt's 72-byte
# input limit and potential binary compatibility issues with the `bcrypt`
# C library on some platforms. For production you may switch back to
# bcrypt or argon2 as desired and ensure the required native libs are
# installed.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash.

    Truncate to 72 bytes (UTF-8) to remain compatible with bcrypt-style
    limitations and to ensure consistent behaviour across platforms.
    """
    try:
        pw = plain_password
        if isinstance(pw, str):
            pw_bytes = pw.encode("utf-8")
            if len(pw_bytes) > 72:
                pw = pw_bytes[:72].decode("utf-8", errors="ignore")
        return pwd_context.verify(pw, hashed_password)
    except Exception as e:
        logger.debug("Password verification error: %s", e, exc_info=True)
        return False


def get_password_hash(password: str) -> str:
    """Hash a password, truncating to 72 bytes (UTF-8) when necessary."""
    pw = password
    if isinstance(pw, str):
        pw_bytes = pw.encode("utf-8")
        if len(pw_bytes) > 72:
            pw = pw_bytes[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(pw)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Resolve the current user from a JWT bearer token.

    Raises a standard 401 HTTPException when the token is invalid or the
    user cannot be found. Logs decode errors for easier debugging.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as e:
        logger.debug("JWT decode error: %s", e, exc_info=True)
        raise credentials_exception

    sub = payload.get("sub")
    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        logger.debug("Invalid 'sub' in token payload: %r", sub)
        raise credentials_exception

    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


def create_password_reset_token(email: str) -> str:
    """Create a short-lived JWT for password reset."""
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": email, "type": "reset"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify reset token and return email if valid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except JWTError:
        return None
