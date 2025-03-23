from fastapi import APIRouter
from app.models import Contact

router = APIRouter()

@router.post("/send")
def contact_owner(contact_message: Contact):
    return {"message": f"Poruka za kuću {contact_message.house_name} uspješno poslana"}