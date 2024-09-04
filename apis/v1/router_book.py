from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException, status

from database.session import get_db
from database.repository.book import retrieve_book, list_books, update_book
from schemas.book import ShowBook, UpdateBook

router = APIRouter()


@router.get("/books/{id}", response_model=ShowBook)
def get_book(id: int, db: Session= Depends(get_db)):
    book = retrieve_book(id=id, db=db)
    if not book:
        raise HTTPException(detail=f"Book with ID {id} does not exist.", status_code=status.HTTP_404_NOT_FOUND)
    return book


@router.get("/books", response_model=List[ShowBook])
def get_all_book(db: Session = Depends(get_db)):
    books = list_books(db=db)
    return books

