from pydantic import BaseModel, conint


class RatingCreate(BaseModel):
    rate: conint(ge=1, le=5)
