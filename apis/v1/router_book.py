from typing import List, Optional

from fastapi import APIRouter, Header
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status

from core.security import get_user_id_from_token
from database.session import get_db
from database.repository.book import retrieve_book, list_books
from schemas.book import BookDetail, BookList

router = APIRouter()


@router.get("/books/{id}", response_model=BookDetail)
def get_book(id: int, db: Session= Depends(get_db)):
    book = retrieve_book(id=id, db=db)
    if not book:
        raise HTTPException(detail=f"Book with ID {id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return book


@router.get("/books", response_model=List[BookList])
def get_all_books(db: Session = Depends(get_db), authorization: Optional[str] = Header(None)):
    user_id = None

    if authorization:
        try:
            token = authorization.split(" ")[1]
            user_id = get_user_id_from_token(token)
        except IndexError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid authorization header format")

    books = list_books(db=db, user_id=user_id)
    return books

