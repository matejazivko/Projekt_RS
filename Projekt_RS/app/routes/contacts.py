from fastapi import APIRouter, HTTPException
from app.models import Contact
from app.database import dynamodb
import uuid

router = APIRouter()
contacts_table=dynamodb.Table("contacts")

@router.post("/send")
def contact_owner(contact_message: Contact):
    try:
        contacts_table.put_item(Item={
            "house_name": contact_message.house_name,
            "sender_email": contact_message.sender_email,
            "message": contact_message.message
        })
        return {"message": f"Poruka za kuću {contact_message.house_name} uspješno poslana"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Došlo je do greške prilikom slanja poruke")