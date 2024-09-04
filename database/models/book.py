from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base_class import Base


class Book(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), unique=True, index=True)
    description = Column(String(600))
    author = Column(String(80))

    bookmarks = relationship("Bookmark", back_populates="book")
    comments = relationship("Comment", back_populates="book")
    ratings = relationship("Rating", back_populates="book")
