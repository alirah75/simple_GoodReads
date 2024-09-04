from pydantic import BaseModel


class CommentCreate(BaseModel):
    comment_text: str
