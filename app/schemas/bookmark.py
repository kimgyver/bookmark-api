from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class BookmarkCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    url: HttpUrl
    tags: str = Field(default="", max_length=200)


class BookmarkUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    url: Optional[HttpUrl] = None
    tags: Optional[str] = Field(default=None, max_length=200)


class BookmarkOut(BaseModel):
    id: int
    title: str
    url: str
    tags: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
