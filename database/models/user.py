from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database.base_class import Base


class User(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(50))
    is_admin = Column(Boolean, default=False)

    bookmarks = relationship("Bookmark", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
