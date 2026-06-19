from __future__ import annotations  # not needed if python >=3.14

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )  # primary_key=True makes it autoincrement
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )  # decouple the db from the file structures. Separates data from presentation.

    # forward reference
    # TODO: to support anonymize strategy on user delete, remove cascade and make Post.user_id nullable with ondelete="SET NULL"
    posts: Mapped[list[Post]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )  # 1:many relation, allows us to do users.posts to get all posts

    @property
    def image_path(self) -> str:
        # Not a DB column — computed at runtime so Pydantic can serialize it via from_attributes=True
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    author: Mapped[User] = relationship(
        back_populates="posts"
    )  # Many to 1, back populates, allows to do post.author
