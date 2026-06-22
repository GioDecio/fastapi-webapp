from typing import Annotated, Any

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles

# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Starlette's HTTPException is imported to register a custom error handler that catches ALL HTTP errors,
# including those raised internally by Starlette (e.g. 404 for missing routes).
# FastAPI's HTTPException alone wouldn't catch those.
from routers import posts, users, templating
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import models
from database import Base, engine, get_db
from exception_handlers import register_exception_handlers


# live span
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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
async def home(request: Request, db: Annotated[AsyncSession, Depends(get_db)]) -> Any:
    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .order_by(models.Post.date_posted.desc()),
    )
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )


# Register HTTP and validation error handlers (defined in exception_handlers.py)
register_exception_handlers(app)
