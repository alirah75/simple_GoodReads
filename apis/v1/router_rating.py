from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.rating import RatingCreate

from database.models.user import User
from database.session import get_db
from database.repository.rating import get_rating_by_user_and_book, upsert_rating
from database.repository.bookmark import delete_bookmark
from core.security import get_current_user

router = APIRouter()


@router.post("/ratings/{book_id}", status_code=status.HTTP_200_OK)
def rate_book(book_id: int, rating: RatingCreate, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    existing_rating = get_rating_by_user_and_book(user_id=current_user.id, book_id=book_id, db=db)

    if existing_rating:
        existing_rating.rate = rating.rate
    else:
        existing_rating = upsert_rating(user_id=current_user.id, book_id=book_id, rating=rating.rate, db=db)

    delete_bookmark(book_id=book_id, user_id=current_user.id, db=db)

    db.commit()
    return {"msg": "Book rating updated successfully"}
