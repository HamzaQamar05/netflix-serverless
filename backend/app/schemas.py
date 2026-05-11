from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    genre: str = Field(..., min_length=1, max_length=80)
    description: str = Field(..., min_length=1)
    release_year: int = Field(..., ge=1888, le=2100)
    rating: float = Field(0, ge=0, le=10)
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieOut(MovieBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WatchEventCreate(BaseModel):
    movie_id: int
    user_id: str = Field(..., min_length=1, max_length=80)
    seconds_watched: int = Field(0, ge=0)


class WatchEventOut(WatchEventCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HealthOut(BaseModel):
    status: str
    database: str
    redis: str
