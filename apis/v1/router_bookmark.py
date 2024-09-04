from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from database.repository.comment import get_comment_by_user_and_book
from database.repository.rating import get_rating_by_user_and_book
from database.session import get_db
from database.repository.bookmark import add_bookmark, delete_bookmark
from database.models.book import Book
from database.models.user import User
from core.security import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/bookmarks/{book_id}", status_code=status.HTTP_200_OK)
def bookmark_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    existing_rating = get_rating_by_user_and_book(user_id=current_user.id, book_id=book_id, db=db)
    existing_comment = get_comment_by_user_and_book(user_id=current_user.id, book_id=book_id, db=db)

    if existing_rating or existing_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot bookmark a book with existing rating or comment")

    bookmark = add_bookmark(book_id=book_id, user_id=current_user.id, db=db)
    if not bookmark:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bookmark already exists")
    return {"msg": "Book bookmarked successfully"}


@router.delete("/bookmarks/{book_id}", status_code=status.HTTP_200_OK)
def unbookmark_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    removed = delete_bookmark(book_id=book_id, user_id=current_user.id, db=db)
    if not removed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bookmark does not exist")
    return {"msg": "Book unbookmarked successfully"}
