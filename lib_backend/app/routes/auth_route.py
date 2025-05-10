from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas import user_schema
from ..utils import utils
from ..utils.utils import get_db

router = APIRouter()

@router.post("/signup")
def user_signup(user: user_schema.UserSignup, db: Session = Depends(get_db)):
    """
    Handle user signup. This endpoint registers a new user, checks for existing email
    or username, hashes the password, and returns an access token.

    Args:
        user: The user signup data containing username, email, and password.
        db: The database session dependency.
    
    Raises:
        HTTPException: If the email or username already exists in the database.

    Returns:
        A dictionary containing the access token and token type (bearer).
    """
    # Check if the email or username already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    existing_username = db.query(User).filter(User.username == user.username).first()
    
    # Raise HTTP exception if email or username exists
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    if existing_username:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    # Hash the password before saving it in the database
    hashed = utils.hash_password(user.password)
    
    # Create the new user object
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
    )
    
    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create JWT token for the new user
    token = utils.create_jwt({"user_id": new_user.id})
    
    # Return the access token and token type
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def user_login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    """
    Handle user login. This endpoint checks if the user exists, compares the hashed
    password with the provided password, and returns an access token if successful.

    Args:
        user: The login data containing email and password.
        db: The database session dependency.

    Raises:
        HTTPException: If the user doesn't exist or if the password is incorrect.

    Returns:
        A dictionary containing the access token and token type (bearer).
    """
    # Query the user by email
    db_user = db.query(User).filter(User.email == user.email).first()
    
    # If user does not exist, raise a 404 error
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )
        
    # Compare the provided password with the stored hashed password
    is_match = utils.match_password(user.password, db_user.hashed_password)  # type: ignore
    
    # If password doesn't match, raise a 401 error
    if not is_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
        
    # Create JWT token for the user
    token = utils.create_jwt({"user_id": db_user.id})
    
    # Return the access token and token type
    return {"access_token": token, "token_type": "bearer"}
