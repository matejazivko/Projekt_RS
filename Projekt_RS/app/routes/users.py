from fastapi import APIRouter
from app.models import User

router = APIRouter()

users = []

@router.post("/register")
def register_user(user:User):
    users.append(user)
    return {"message": f"Korisnik {user.username} uspješno registriran"}
