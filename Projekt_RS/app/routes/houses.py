from fastapi import APIRouter
from app.models import House

router = APIRouter()

houses = []

@router.post("/add")
def add_house(house: House):
    houses.append(house)
    return {"message": f"Kuća {house.name} je dodana u aplikaciju"}

@router.get("/houses")
def get_houses():
    return houses