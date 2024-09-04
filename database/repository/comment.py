from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database.models.comment import Comment


def add_comment(user_id: int, book_id: int, comment_text: str, db: Session):
    comment = Comment(user_id=user_id, book_id=book_id, comment_text=comment_text)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comment_by_user_and_book(user_id: int, book_id: int, db: Session):
    comment = db.query(Comment).filter(Comment.user_id == user_id, Comment.book_id == book_id).first()
    return comment


def upsert_comment(user_id: int, book_id: int, comment_text: str, db: Session):

    try:
        existing_comment = db.query(Comment).filter(Comment.user_id == user_id, Comment.book_id == book_id).first()

        if existing_comment:
            existing_comment.comment_text = comment_text
        else:
            new_comment = Comment(
                user_id=user_id,
                book_id=book_id,
                comment_text=comment_text
            )
            db.add(new_comment)

        db.commit()

        db.refresh(existing_comment or new_comment)

        return existing_comment or new_comment
    except SQLAlchemyError as e:
        db.rollback()
        raise e
