# Here is agreed what is exposed in the api

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    image_file: str | None
    image_path: str


class UserPrivate(UserPublic):
    email: EmailStr


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)


class Token(BaseModel):
    access_token: str
    token_type: str


class PostBase(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=100)
    content: Optional[str] = Field(min_length=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostResponse(PostBase):
    model_config = ConfigDict(
        from_attributes=True
    )  # from_attributes=True allow dot notation
    # The fields below are from system not provided by the client
    id: int
    # TODO: make user_id and author optional (int | None, UserResponse | None) when anonymize delete strategy is implemented
    user_id: int
    date_posted: datetime  # This will be serialised to standard ISO 8601 format
    author: UserPublic  # This gets nested json
