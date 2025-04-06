from pydantic import BaseModel
from typing import List

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class House(BaseModel):
    name: str
    description: str
    images: List[str]

class Comment(BaseModel):
    username: str
    house_id: str
    content: str

class Contact(BaseModel):
    house_name: str
    sender_email: str
    message: str