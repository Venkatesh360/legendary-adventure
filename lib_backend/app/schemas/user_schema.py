from pydantic import BaseModel
from datetime import datetime
from typing import List


class UserData(BaseModel):
    """
    Schema representing minimal user identification.

    Attributes:
        user_id (int): Unique ID of the user.
    """
    user_id: int


class UserSignup(BaseModel):
    """
    Schema used for user registration.

    Attributes:
        username (str): Desired username of the user.
        email (str): Email address of the user.
        password (str): Password for the account.
    """
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """
    Schema used for user login.

    Attributes:
        email (str): Registered email address of the user.
        password (str): Corresponding password for authentication.
    """
    email: str
    password: str


class UserOut(BaseModel):
    """
    Schema for outputting user information.

    Attributes:
        username (str): Username of the user.
        email (str): Email of the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp of the last update.
        is_admin (bool): Indicates if the user has admin privileges.
    """
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    is_admin: bool

    class Config:
        orm_mode = True  # Allows compatibility with ORM models


class UserOutResponse(BaseModel):
    """
    Schema representing a list of users in the response.

    Attributes:
        users (List[UserOut]): List of user records.
    """
    users: List[UserOut]
