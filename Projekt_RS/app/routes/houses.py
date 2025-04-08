import os
import uuid
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, Form, Depends
from app.models import House
from app.database import dynamodb
import boto3
from botocore.exceptions import ClientError

router = APIRouter()

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000", region_name="eu-west-1")
houses_table = dynamodb.Table('houses')
images_table = dynamodb.Table('images')

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

def save_image(image: UploadFile) -> str:
    try:
        file_extension = image.filename.split(".")[-1]
        new_file_name = str(uuid.uuid4()) + "." + file_extension
        file_path = os.path.join(UPLOAD_DIR, new_file_name)

        with open(file_path, "wb") as f:
            f.write(image.file.read())
    
        return file_path
    except Exception as e:
        raise HTTPException (status_code=500, detail=f"Greška prilikom spremanja slike: {str(e)}")


@router.post("/add_houses")
async def add_houses(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = None
):
    houseId = str(uuid.uuid4())
    image_path = save_image(image) if image else None

    try:
        print(f"Spremam kuću {name}")
        houses_table.put_item(
            Item={
                "houseId": houseId,
                "name": name,
                "description": description, 
                "image": image_path
            }
        )
        print(f"Kuća {name}je pohranjena u bazu")
        return {"message": f"Kuća {name} je dodana", "houses_id": houseId, "image_path": image_path}
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
    
@router.post("/add_images")
async def add_images(
    houseId: str = Form(...),
    image: UploadFile = None
):
    if not image:
        raise HTTPException (status_code=400, detail="Slika nije dodana")
    image_id = str(uuid.uuid4())
    image_path = save_image(image) 

    try: 
        print(f"Dodajem sliku kući {houseId}")
        images_table.put_item(
            Item={
                "image_id": image_id,
                "houseId": houseId,
                "path": image_path,
                "description": "Slika interijera"
            }
        )
        return {"message": f"Slika dodana kući {houseId}", "image_path": image_path}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom dodavanja slike: {e.response['Error']['Message']}")
    
def get_images(houseId: str):
    try:
        print(f"Dohvaćanje slika za kuću {houseId}")
        response = images_table.scan(
            FilterExpression = "houseId = :houseId",
            ExpressionAttributeValues = {":houseId": houseId}
        )
        return response.get("Items", [])
    except ClientError as e:
        raise HTTPException (status_code= 500, detail = f"Greška prilikom dohvaćanja slika: {e.response['Error']['Message']}")