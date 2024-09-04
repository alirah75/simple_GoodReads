from typing import List, Optional

from fastapi import APIRouter, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status

from core.security import get_user_id_from_token, get_current_user
from database.repository.comment import add_comment
from database.repository.rating import add_rating
from database.session import get_db
from database.repository.book import retrieve_book, list_books
from schemas.book import BookDetail, BookList
from schemas.rate_and_comment import RateAndCommentRequest

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
    books = list_books(db=db)
    results = []

    for book in books:
        book_data = {
            "id": book.id,
            "name": book.title,
            "description": book.description,
            "created_at": book.created_at,
            "bookmarked_by": len(book.bookmarks),
            "is_bookmarked": False
        }

        if token:
            user = get_current_user(token=token, db=db)
            bookmark = get_bookmark_by_user_and_book(user_id=user.id, book_id=book.id, db=db)
            book_data["is_bookmarked"] = bool(bookmark)

        results.append(book_data)

    return results


@router.post("/books/{id}/rate_comment")
def rate_and_comment_book(id: int, request: RateAndCommentRequest, authorization: Optional[str] = Header(None),
                          db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    token = authorization.split(" ")[1]
    user_id = get_user_id_from_token(token)

    if request.rate is not None:
        if request.rate < 1 or request.rate > 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Rating must be between 1 and 5")
        add_rating(user_id=user_id, book_id=id, rate=request.rate, db=db)

    if request.comment:
        add_comment(user_id=user_id, book_id=id, comment_text=request.comment, db=db)

    return {"msg": "Rating and/or comment submitted successfully"}
