from pydantic import BaseModel
from typing import Optional

class BookRequest(BaseModel):
    user_id: int
    title: str
    author: str

class AddBook(BaseModel):
    title: str
    author: str
    count: int