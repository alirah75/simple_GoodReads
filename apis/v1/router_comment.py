# router_comment.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.comment import CommentCreate

from database.models.user import User
from database.session import get_db
from database.repository.comment import get_comment_by_user_and_book, upsert_comment
from database.repository.bookmark import delete_bookmark
from core.security import get_current_user

router = APIRouter()


@router.post("/comments/{book_id}", status_code=status.HTTP_200_OK)
def comment_on_book(book_id: int, comment: CommentCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    existing_comment = get_comment_by_user_and_book(user_id=current_user.id, book_id=book_id, db=db)

    if existing_comment:
        existing_comment.comment_text = comment.comment_text
    else:
        existing_comment = upsert_comment(user_id=current_user.id, book_id=book_id, comment_text=comment.comment_text,
                                          db=db)

    delete_bookmark(book_id=book_id, user_id=current_user.id, db=db)

    db.commit()
    return {"msg": "Book comment updated successfully"}
