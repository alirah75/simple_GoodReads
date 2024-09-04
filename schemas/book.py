from typing import Optional, Dict, List
from pydantic import BaseModel, root_validator
from datetime import date


class CreateBook(BaseModel):
    name: str
    description: str

    @root_validator(pre=True)
    def generate_slug(cls, slug, values):
        name = values.get('title')
        slug = None
        if name:
            slug = name.replace(" ", "-").lower()
        return slug


class RatingDetail(BaseModel):
    user_id: int
    rate: int


class CommentDetail(BaseModel):
    user_id: int
    comment_text: str


class BookDetail(BaseModel):
    name: str
    description: str
    number_of_comments: int
    number_of_ratings: int
    average_rating: float
    rating_distribution: Dict[int, int]
    comments: List[CommentDetail]
    ratings: List[RatingDetail]

    class Config:
        orm_mode = True


class BookList(BaseModel):
    id: int
    name: str
    bookmark_count: int
    is_bookmarked: Optional[bool] = None

    class Config:
        orm_mode = True
