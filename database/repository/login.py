from sqlalchemy.orm import Session
from database.models.user import User


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
