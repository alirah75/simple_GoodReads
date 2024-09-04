from sqlalchemy.orm import Session
from database.models.book import Book
from schemas.book import UpdateBook


def retrieve_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()
    return book


def list_books(db: Session):
    books = db.query(Book).all()
    return books


def update_book(id: int, book: UpdateBook, db: Session):
    book_in_db = db.query(Book).filter(Book.id == id).first()
    if not book_in_db:
        return
    book_in_db.name = book.name
    book_in_db.description = book.description
    db.add(book_in_db)
    db.commit()
    return book_in_db


def delete_book(id: int, db: Session):
    book_in_db = db.query(Book).filter(Book.id == id)
    if not book_in_db.first():
        return {"error": f"Could not find book with id {id}"}
    book_in_db.delete()
    db.commit()
    return {"msg": f"deleted book with id {id}"}
