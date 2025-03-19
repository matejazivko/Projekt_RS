from fastapi import APIRouter, HTTPException
from app.models import User
from pydantic import BaseModel
import boto3
import logging

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8001", region_name="eu-west-1")
users_table = dynamodb.Table('users')

class User(BaseModel):
    username: str
    email: str
    password: str
    
@router.post("/register")
def register_user(user:User):
    response = users_table.get_item(Key={"username": user.username})
    if "Item" in response:
        raise HTTPException(status_code=400, detail="Korisnik već postoji")
    
    users_table.put_item(Item={
        "username": user.username,
        "email": user.email,
        "password": user.password
    })
    return {"message": f"Korisnik {user.username} uspješno registriran"}

@router.post("/login")
def login(user: User):
    try:
        logging.debug(f"Pokušaj prijave korisnika: {user.username}")
        response = users_table.get_item(Key={"username": user.username})
        if "Item" not in response:
            logging.debug(f"Korisnik s korisničkim imenom {user.username} nije pronađen")
            raise HTTPException (status_code=400, detail="Pogrešno korisničko ime ili lozinka")
    
        stored_user = response["Item"]
        logging.debug(f"Pronađen korisnik: {stored_user}")
        
        if stored_user["password"] != user.password:
            logging.error(f"Pogrešna lozinka za korisnika {user.username}")
            raise HTTPException(status_code=400, detail="Pogrešna lozinka")
        
        logging.debug(f"USpješna prijava za korisnika {user.username}")
        return {"message": f"Dobrodošao {user.username}!"}

    except Exception as e:
        logging.exception(f"Greška pri prijavi korisnika: {user.username}")
        raise HTTPException(status_code=500, detail=f"Greška na serveru")