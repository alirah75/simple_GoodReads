from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.base_class import Base


class Comment(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    book_id = Column(Integer, ForeignKey('book.id'), index=True)
    comment_text = Column(Text)

    user = relationship("User", back_populates="comments")
    book = relationship("Book", back_populates="comments")
