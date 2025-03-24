from fastapi import APIRouter, HTTPException
from app.models import UserRegister, UserLogin
from pydantic import BaseModel
from app.database import users_table 
from app.database import dynamodb
import boto3
import logging
import bcrypt
import traceback

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name="eu-west-1")


class User(BaseModel):
    username: str
    email: str
    password: str
    
router = APIRouter()
@router.post("/register")
def register_user(user:UserRegister):
    try:
        response = users_table.get_item(Key={"username": user.username})
        if "Item" in response:
            raise HTTPException(status_code=400, detail="Korisnik već postoji")
    
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
       
        
        users_table.put_item(Item={
            "username": user.username,
            "email": user.email,
            "password": hashed_password.decode("utf-8")
            
        })
      
        return {"message": f"Korisnik {user.username} uspješno registriran"}

    except Exception as e:
         logger.exception(f"Greška pri registraciji korisnika: {user.username}")
    error_message = f"Greška na serveru: {str(e)}"  
    raise HTTPException(status_code=500, detail=error_message)


@router.post("/login")
def login(user: UserLogin):
    try:
        
        response = users_table.get_item(Key={"username": user.username})
        if "Item" not in response:
            raise HTTPException (status_code=404, detail="Pogrešno korisničko ime")
    
        stored_user = response["Item"]
        logging.debug(f"Pronađen korisnik: {stored_user}")
        
        if not bcrypt.checkpw(user.password.encode ("utf-8"), stored_user["password"].encode("utf-8")):
            logging.error(f"Pogrešna lozinka za korisnika {user.username}")
            raise HTTPException(status_code=400, detail="Pogrešna lozinka")
        
        return {"message": f"Dobrodošli {user.username}!"}

    except Exception as e:
        logging.exception(f"Greška pri prijavi korisnika: {user.username}")
        logging.error(f"Stack Trace: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Greška na serveru")