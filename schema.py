from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=100)
    content: Optional[str] = Field(min_lenght=1)
    author: Optional[str] = Field(min_length=1, max_length=50)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    model_config = ConfigDict(
        from_attributes=True
    )  # from_attributes=True allow dot notation
    # The fields below are from system not provided by the client
    id: int
    date_posted:str

