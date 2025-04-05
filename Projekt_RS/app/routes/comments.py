from fastapi import APIRouter, HTTPException
from app.models import Comment
from app.database import dynamodb, houses_table
from boto3.dynamodb.conditions import Key


router = APIRouter()

comments_table = dynamodb.Table("comments")

@router.post("/add_comments")
def add_comment(comment: Comment):
    if not comment.username:
        raise HTTPException(status_code=403, detail="Prijavite se kako biste dodali komentar")
    try:
        comments_table.put_item(Item={
            "house_id": comment.house_id,
            "username": comment.username,
            "content": comment.content
        })
        return {"message": f"Dodan komentar za kuću {comment.house_id} od korisnika {comment.username}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Greška prilikom dodavanja komentara: {str(e)}")
    
@router.get("/comments/{house_id}")
def get_comments(house_id: str):
    try:
        response = comments_table.query(KeyConditionExpression=Key('house_id').eq(house_id))
        comments = response.get("Items", [])
        house = houses_table.get_item(Key={"houses_id": house_id}).get("Item")
        house_name = house.get("house_name", "Naziv kuće") if house else "Naziv kuće"
        for comment in comments:
            comment["house_name"] = house_name
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom dohvaćanja komentara: {str(e)}")

@router.put("/update_comment")
def update_comment(house_id: str, new_content: str, username: str):
    if not username:
        raise HTTPException(status_code=403, detail="Prijavite se kako biste ažurirali svoj komentar")
    try:
        comments_table.put_item(Item={
            "house_id": house_id,
            "username": username,
            "content": new_content
        })
        return {"message": "Komentar je uspješno ažuriran"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom ažuriranja komentara: {str(e)}")
    
  
@router.delete("/delete_comment")
def delete_comment(house_id: str, username: str):
    if not username:
        raise HTTPException(status_code=403, detail="Prijavite se kako biste obrisali komentar")
    try:
            comments_table.delete_item(Key={"house_id": house_id, "username": username})
            return {"message": "Komentar uspješno obrisan"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen ili komentar koji želite obrisati niste Vi dodali")