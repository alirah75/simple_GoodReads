from pydantic import BaseModel


class RatingCreate(BaseModel):
    rate: int
