import bcrypt
import jwt
from datetime import datetime, timedelta
import dotenv
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from ..database.config import session
from sqlalchemy.orm import Session
from ..models.user import User


dotenv.load_dotenv()
oauth_schema = OAuth2PasswordBearer(tokenUrl="api/user/login")

def get_db():
    db = session()
    try:
        yield db
        
    finally:
        db.close()
        
def fifteen_days_from_now():
    return datetime.utcnow() + timedelta(days=15)


def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")    
        
    return db_user
    
        
def get_token_data(token: str = Depends(oauth_schema)) -> dict:
    try:
        print(token)
        SECRET_KEY = os.getenv("JWT_SECRET")
        ALGORITHM = str(os.getenv("ALOGRITHM"))
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
                
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token get_token_data",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return payload
        

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode()

def match_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def create_jwt(data: dict, expires_in: int = 7):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=expires_in)
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=os.getenv("ALOGRITHM"))
    
    return token

def decode_jwt(token: str) -> dict:
    try:
        ALGORITHM = str(os.getenv("ALOGRITHM"))
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        