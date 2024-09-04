from sqlalchemy.orm import Session
from database.models.bookmark import Bookmark


def add_bookmark(user_id: int, book_id: int, db: Session):
    bookmark = Bookmark(user_id=user_id, book_id=book_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def delete_bookmark(user_id: int, book_id: int, db: Session):
    bookmark = db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.book_id == book_id).first()
    if bookmark:
        db.delete(bookmark)
        db.commit()
    return bookmark


def is_bookmarked(user_id: int, book_id: int, db: Session):
    return db.query(Bookmark).filter(Bookmark.user_id == user_id, Bookmark.book_id == book_id).first() is not None
