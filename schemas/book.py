from typing import Optional
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


class ShowBook(BaseModel):
    name: str
    description: Optional[str]
    created_at: date

    class Config:
        orm_mode = True


class UpdateBook(CreateBook):
    pass
