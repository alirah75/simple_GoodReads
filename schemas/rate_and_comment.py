from typing import Optional

from pydantic import BaseModel


class RateAndCommentRequest(BaseModel):
    rate: Optional[int] = None
    comment: Optional[str] = None