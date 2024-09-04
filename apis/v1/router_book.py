from typing import List, Optional

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status

from core.security import get_current_user
from database.repository.bookmark import get_bookmark_by_user_and_book
from database.repository.comment import upsert_comment
from database.repository.rating import upsert_rating
from database.session import get_db
from database.repository.book import retrieve_book, list_books
from schemas.book import BookDetail, BookList
from schemas.comment import CommentCreate
from schemas.rating import RatingCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/books/{id}", response_model=BookDetail)
def get_book(id: int, db: Session = Depends(get_db)):
    book = retrieve_book(id=id, db=db)
    if not book:
        raise HTTPException(detail=f"Book with ID {id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return book


@router.get("/books", response_model=List[BookList])
def get_all_books(db: Session = Depends(get_db), token: Optional[str] = Depends(oauth2_scheme)):
    user_id = get_current_user(token, db).id
    books = list_books(db=db, user_id=user_id)
    results = []

    for book in books:
        book_data = {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "bookmark_count": book.bookmark_count,
            "is_bookmarked": False
        }

        if token:
            user = get_current_user(token=token, db=db)
            bookmark = get_bookmark_by_user_and_book(user_id=user.id, book_id=book.id, db=db)
            book_data["is_bookmarked"] = bool(bookmark)

        results.append(book_data)

    return results


@router.post("/books/{book_id}/rate_and_comment", status_code=status.HTTP_200_OK)
def rate_and_comment_book(book_id: int, rating: RatingCreate = None, comment: CommentCreate = None,
                          db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    book = retrieve_book(id=book_id, db=db)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    if rating:
        upsert_rating(user_id=current_user.id, book_id=book_id, rate=rating.rate, db=db)

    if comment:
        upsert_comment(user_id=current_user.id, book_id=book_id, comment_text=comment.comment_text, db=db)

    return {"message": "Rating and/or comment updated successfully"}
