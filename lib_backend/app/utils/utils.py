import os
import bcrypt
import jwt
import dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database.config import SessionLocal
from ..models import user

# Load environment variables from .env file
dotenv.load_dotenv()

# OAuth2 schema for retrieving token from requests
oauth_schema = OAuth2PasswordBearer(tokenUrl=str(os.getenv("TOKEN_URL")))

def get_db():
    """
    Dependency that provides a database session.
    Ensures that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fifteen_days_from_now() -> datetime:
    """
    Returns the current UTC datetime plus 15 days.
    Useful for setting book return deadlines.
    """
    return datetime.utcnow() + timedelta(days=15)

def get_user_by_id(user_id: int, db: Session):
    """
    Retrieves a user object from the database based on the provided user ID.

    Raises:
        HTTPException: If the user is not found.

    Returns:
        user.User: The user instance.
    """
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

def get_token_data(token: str = Depends(oauth_schema)) -> dict:
    """
    Decodes and validates a JWT access token.

    Raises:
        HTTPException: If the token is expired, malformed, or user ID is missing.

    Returns:
        dict: Payload data from the token.
    """
    try:
        SECRET_KEY = os.getenv("JWT_SECRET")
        ALGORITHM = str(os.getenv("ALOGRITHM"))  # Note: should be "ALGORITHM"
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("user_id") is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token, user_id unavailable"
            )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token get_token_data",
            headers={"WWW-Authenticate": "Bearer"},
        )

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): Plaintext password.

    Returns:
        str: Hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()

def match_password(password: str, hashed_password: str) -> bool:
    """
    Verifies whether a plaintext password matches its hashed version.

    Args:
        password (str): Plaintext password.
        hashed_password (str): Hashed password.

    Returns:
        bool: True if matched, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_jwt(data: dict, expires_in: int = 7) -> str:
    """
    Generates a JWT token with an expiration.

    Args:
        data (dict): Payload data to encode into the token.
        expires_in (int): Expiry time in hours. Default is 7 hours.

    Returns:
        str: Encoded JWT token.
    """
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=expires_in)
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=os.getenv("ALOGRITHM"))

def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token and handles validation errors.

    Raises:
        HTTPException: If the token is expired or invalid.

    Returns:
        dict: Decoded payload data.
    """
    try:
        ALGORITHM = str(os.getenv("ALOGRITHM"))
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
