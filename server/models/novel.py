from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Novel(BaseModel):
    title: str = Field(...)
    description: Optional[str] = Field(None)
    image_url: str = Field(...)
    banner_url: str = Field(...)
    genres: list = Field(...)
    tags: list = Field(None)
    chapter: int = Field(default=0)
    status: str = Field(default="draft")
    year: int = Field(default=datetime.now().year)
    views: int = Field(default=0)
    rating: float = Field(default=0)
    account_id: str = Field(None)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = Field(None)
    updated_by: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "title": "The Beginning After The End",
                "description": "The story is about a young ",
                "image_url": "https://i.imgur.com/1ZQZ1Zl.jpg",
                "banner_url": "https://i.imgur.com/1ZQZ1Zl.jpg",
                "genres": [
                    "Action",
                    "Adventure",
                ],
                "tags": ["action", "adventure", "fantasy"],
                "chapter": 400,
                "status": "draft",
                "year": 2020,
                "views": 0,
                "rating": 4.5,
                "created_at": "2020-08-09T11:32:39.000Z",
                "updated_at": "2020-08-09T11:32:39.000Z",
                "created_by": "xau",
                "updated_by": "xau",
            }
        }


class UpdateNovel(BaseModel):
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    banner_url: Optional[str] = Field(None)
    genres: Optional[list] = Field(None)
    status: Optional[str] = Field(None)
    updated_at: datetime = Field(default_factory=datetime.now)
    updated_by: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "title": "The Beginning After The End",
                "description": "The story is about a young ",
                "image_url": "https://i.imgur.com/1ZQZ1Zl.jpg",
                "banner_url": "https://i.imgur.com/1ZQZ1Zl.jpg",
                "genres": [
                    "Action",
                    "Adventure",
                ],
                "view": 0,
                "rating": 4.5,
                "tags": ["action", "adventure", "fantasy"],
                "chapter": 400,
                "updated_at": "2020-08-09T11:32:39.000Z",
                "updated_by": "xau",
            }
        }
