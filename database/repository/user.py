from sqlalchemy.orm import Session

from schemas.user import UserCreate
from database.models.user import User
from core.hashing import Hasher


def create_new_user(user: UserCreate, db: Session):
    user = User(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
