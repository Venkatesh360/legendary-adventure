from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserData(BaseModel):
    user_id: int
    
class UserSignup(BaseModel):
    username: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str
    
class UserOut(BaseModel):
    username: str
    email: str
    cluster_key: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
class UserOutResponse(BaseModel):
    users: List[UserOut]