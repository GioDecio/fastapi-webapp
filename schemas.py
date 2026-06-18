# Here is agreed what is exposed in the api

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_file: str | None
    image_path: str


class PostBase(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=100)
    content: Optional[str] = Field(min_length=1)


class PostCreate(PostBase):
    user_id: int  # TEMPORARY


class PostResponse(PostBase):
    model_config = ConfigDict(
        from_attributes=True
    )  # from_attributes=True allow dot notation
    # The fields below are from system not provided by the client
    id: int
    user_id: int
    date_posted: datetime  # This will be serialised to standard ISO 8601 format
    author: UserResponse  # This gets nested json
