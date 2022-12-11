from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ChapterSchema(BaseModel):
    chapter_number: int = Field(None)
    title: str = Field(...)
    content: str = Field(...)
    novel_id: str = Field(...)
    views: int = Field(default=0)
    source_file_url: str = Field(None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(None)
    updated_by: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "chapter_number": 1,
                "title": "Chapter 1",
                "content": "The story is about a young ",
                "novel_id": "6360e51e6eeec7db8f2a0f10",
                "views": 0,
                "source_file_url": "https://www.google.com",
                "created_at": "2020-08-09T11:32:39.000Z",
                "updated_at": "2020-08-09T11:32:39.000Z",
                "created_by": "xau",
                "updated_by": "xau",
            }
        }


class UpdateChapter(BaseModel):
    title: Optional[str] = Field(None)
    content: Optional[str] = Field(None)
    views: Optional[int] = Field(None)
    source_file_url: Optional[str] = Field(None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "title": "Chapter 1",
                "content": "The story is about a young ",
                "views": 0,
                "source_file_url": "https://www.google.com",
                "updated_at": "2020-08-09T11:32:39.000Z",
                "updated_by": "xau",
            }
        }
