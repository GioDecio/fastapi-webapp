from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles

# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from config import settings
from database import engine, get_db
from exception_handlers import register_exception_handlers

# Starlette's HTTPException is imported to register a custom error handler that catches ALL HTTP errors,
# including those raised internally by Starlette (e.g. 404 for missing routes).
# FastAPI's HTTPException alone wouldn't catch those.
from routers import posts, templating, users


# live span
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup

    yield

    # Shutdown
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Serve files from the "static" folder at the /static URL path, so templates can reference them via url_for('static', path=...)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")


# API routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])

# Template routers — return HTML via Jinja2
app.include_router(templating.router, prefix="", tags=["templating"])


# Create Home route that responds to get requests at the root url
# Stacking decorators
## home
@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    count_result = await db.execute(select(func.count()).select_from(models.Post))
    total = count_result.scalar() or 0

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.date_posted.desc())
        .limit(settings.posts_per_home_page),
    )
    posts = result.scalars().all()

    has_more = len(posts) < total

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "posts": posts,
            "title": "Home",
            "limit": settings.posts_per_home_page,
            "has_more": has_more,
        },
    )


# Register HTTP and validation error handlers (defined in exception_handlers.py)
register_exception_handlers(app)
