from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from database.models.book import Book
from database.models.bookmark import Bookmark
from database.models.comment import Comment
from database.models.rating import Rating
from schemas.book import CommentDetail, RatingDetail, BookDetail, BookList


def retrieve_book(id: int, db: Session):
    book = db.query(Book).filter(Book.id == id).first()

    number_of_comments = db.query(Comment).filter(Comment.book_id == id).count()
    number_of_ratings = db.query(Rating).filter(Rating.book_id == id).count()

    average_rating = db.query(func.avg(Rating.rate)).filter(Rating.book_id == id).scalar() or 0

    rating_distribution = db.query(Rating.rate, func.count(Rating.rate)).filter(Rating.book_id == id).group_by(
        Rating.rate).all()
    rating_distribution = dict(rating_distribution)

    comments = db.query(Comment).filter(Comment.book_id == id).all()
    comment_details = [CommentDetail(user_id=comment.user_id, comment_text=comment.comment_text) for comment in
                       comments]

    ratings = db.query(Rating).filter(Rating.book_id == id).all()
    rating_details = [RatingDetail(user_id=rating.user_id, rate=rating.rate) for rating in ratings]

    return BookDetail(name=book.title, description=book.description, number_of_comments=number_of_comments,
                      number_of_ratings=number_of_ratings, average_rating=average_rating,
                      rating_distribution=rating_distribution, comments=comment_details, ratings=rating_details)


def list_books(db: Session, user_id: Optional[int] = None):
        books = db.query(Book).all()
        book_list = []

        for book in books:
            bookmark_count = db.query(func.count(Bookmark.id)).filter(Bookmark.book_id == book.id).scalar()

            is_bookmarked = None
            if user_id:
                is_bookmarked = db.query(Bookmark).filter(Bookmark.book_id == book.id,
                                                          Bookmark.user_id == user_id).first() is not None

            book_list.append(BookList(id=book.id,
                                      title=book.title,
                                      description=book.description,
                                      bookmark_count=bookmark_count,
                                      is_bookmarked=is_bookmarked))

        return book_list
