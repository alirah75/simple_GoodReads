from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database.models.rating import Rating


def add_rating(user_id: int, book_id: int, rate: int, db: Session):
    rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.book_id == book_id).first()
    if rating:
        rating.rate = rate
    else:
        rating = Rating(user_id=user_id, book_id=book_id, rate=rate)
        db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


def get_rating_by_user_and_book(user_id: int, book_id: int, db: Session):

    rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.book_id == book_id).first()
    return rating


def upsert_rating(user_id: int, book_id: int, rate: int, db: Session):
    try:
        existing_rating = db.query(Rating).filter(Rating.user_id == user_id, Rating.book_id == book_id).first()

        if existing_rating:
            existing_rating.rate = rate
        else:
            new_rating = Rating(
                user_id=user_id,
                book_id=book_id,
                rate=rate
            )
            db.add(new_rating)

        db.commit()

        db.refresh(existing_rating or new_rating)

        return existing_rating or new_rating
    except SQLAlchemyError as e:
        db.rollback()
        raise e

