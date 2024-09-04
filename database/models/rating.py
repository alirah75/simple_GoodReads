from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.base_class import Base


class Rating(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    book_id = Column(Integer, ForeignKey('book.id'), index=True)
    rate = Column(Integer)

    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")
