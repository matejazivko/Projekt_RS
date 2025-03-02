from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    username: str
    password: str
    email: str

class House(BaseModel):
    name: str
    description: str

class Comment(BaseModel):
    username: str
    house_name: str
    content: str

users = []
houses = []
comments = []

@app.get("/")
def read_root():
    return {"message": "Dobrodošli na aplikaciju Kuće za odmor"}

@app.post("/register")
def register_user (user: User):
    users.append(user)
    return {"message": f"Korisnik {user.username} uspješno registriran"}

@app.post("/add_house")
def add_house(house: House):
    houses.append(house)
    return {"message": f"Kuća za odmor {house.name} je uspješno dodana"}

@app.get("/houses", response_model=List[House])
def get_houses():
    return houses

@app.post("/comment")
def add_comment(comment: Comment):
    comments.append(comment)
    return {"message": f"Dodan komentar za kuću {comment.house_name} od korisnika {comment.username}"}

class ContactMessage(BaseModel):
    username: str
    houses_name: str
    message: str

@app.post("/contact_owner")
def contact_owner(contact_message: ContactMessage):
    return {"message": f"Poruka za kuću {contact_message.house_name} uspješno poslana"}