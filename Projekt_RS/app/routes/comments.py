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
            "houseId": comment.houseId,
            "username": comment.username,
            "content": comment.content
        })
        return {"message": f"Dodan komentar za kuću {comment.houseId} od korisnika {comment.username}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Greška prilikom dodavanja komentara: {str(e)}")
    
@router.get("/comments/{houseId}")
def get_comments(houseId: str):
    try:
        response = comments_table.query(KeyConditionExpression=Key('house_id').eq(houseId))
        comments = response.get("Items", [])
        house = houses_table.get_item(Key={"houses_id": houseId}).get("Item")
        house_name = house.get("house_name", "Naziv kuće") if house else "Naziv kuće"
        for comment in comments:
            comment["house_name"] = house_name
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom dohvaćanja komentara: {str(e)}")

@router.put("/update_comment")
def update_comment(houseId: str, new_content: str, username: str):
    if not username:
        raise HTTPException(status_code=403, detail="Prijavite se kako biste ažurirali svoj komentar")
    try:
        comments_table.put_item(Item={
            "houseId": houseId,
            "username": username,
            "content": new_content
        })
        return {"message": "Komentar je uspješno ažuriran"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom ažuriranja komentara: {str(e)}")
    
  
@router.delete("/delete_comment")
def delete_comment(houseId: str, username: str):
    if not username:
        raise HTTPException(status_code=403, detail="Prijavite se kako biste obrisali komentar")
    try:
            comments_table.delete_item(Key={"houseId": houseId, "username": username})
            return {"message": "Komentar uspješno obrisan"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Komentar nije pronađen ili komentar koji želite obrisati niste Vi dodali")