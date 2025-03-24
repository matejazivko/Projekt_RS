import os
import uuid
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, Form
from app.models import House
from app.database import dynamodb
import boto3
from botocore.exceptions import ClientError

router = APIRouter()

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name="eu-west-1")
houses_table = dynamodb.Table('houses')

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

def save_image(image: UploadFile):
    file_extension = image.filename.split(".")[-1]
    new_file_name = str(uuid.uuid4()) + "." + file_extension
    file_path = os.path.join(UPLOAD_DIR, new_file_name)

    with open(file_path, "wb") as f:
        f.write(image.file.read())
    
    return file_path


@router.post("/add_houses")
async def add_houses(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = None
):
    houses_id = str(uuid.uuid4())
    image_path = save_image(image) if image else None

    try:
        houses_table.put_item(
            Item={
                "houses_id": houses_id,
                "name": name,
                "description": description, 
                "image": image_path
            }
        )
        return {"message": f"Kuća {name} je dodana", "houses_id": houses_id, "image_path": image_path}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Greška kod dodavanja kuće: {e.response['Error']['Message']}")
    
@router.get("/houses")
def get_houses():
    try:
        print("Pokušavam dohvatiti kuće iz  Dynamo DB")
        response = houses_table.scan()
        print ("Odgovor baze", response)
        return response.get("Items", [])
    except ClientError as e:
        print(f"Greška kod dohvaćanja kuća: {e}")
        raise HTTPException(status_code=500, detail=f"Greška kod dohvaćanja kuća: {e}" )
    