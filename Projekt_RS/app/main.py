from fastapi import FastAPI
from app.routes import users, houses, comments, contacts
app = FastAPI()

app.include_router(users.router)
app.include_router(houses.router)
app.include_router(comments.router)
app.include_router(contacts.router)

@app.get("/")
def home():
    return {"message": "Dobrodošli na API aplikacije Kuće za odmor"}