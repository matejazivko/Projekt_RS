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
    house_name: str
    content: str

class Contact(BaseModel):
    username: str
    house_name: str
    message: str