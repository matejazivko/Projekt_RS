from fastapi import APIRouter
from app.models import Comment

router = APIRouter()

comments = []

@router.post("/add_comments")
def add_comment(comment: Comment):
    comments.append(comment)
    return {"message": f"Dodan komentar za kuću {comment.house_name} od korisnika {comment.username}"}

@router.get("/comment")
def get_comments():
    return comments