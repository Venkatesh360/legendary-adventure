from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas import user_schema
from ..utils import utils
from ..utils.utils import get_db

router = APIRouter()

@router.post("/signup")
def user_signup(user: user_schema.UserSignup, db: Session = Depends(get_db)):
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    existing_username = db.query(User).filter(User.username == user.username).first()
    
    if(existing_email):
        raise HTTPException(status_code=409, detail="Email already exists")
    
    if(existing_username):
        raise HTTPException(status_code=409, detail="Username already exists")
    
    hashed = utils.hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = utils.create_jwt({
        "user_id": new_user.id
        })
    
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def user_login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if db_user is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist" 
        )
        
    is_match = utils.match_password(user.password, db_user.hashed_password) #type: ignore
    
    if not is_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect password"
        )
        
    token = utils.create_jwt({
        "user_id":db_user.id
    })
    
    return {"access_token":token, "token_type": "bearer"}


