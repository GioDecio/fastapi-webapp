from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# Starlette's HTTPException is imported to register a custom error handler that catches ALL HTTP errors,
# including those raised internally by Starlette (e.g. 404 for missing routes).
# FastAPI's HTTPException alone wouldn't catch those.
from starlette.exceptions import HTTPException as StarletteHTTPException
from schema import PostCreate, PostResponse

app = FastAPI()

# Serve files from the "static" folder at the /static URL path, so templates can reference them via url_for('static', path=...)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Giovanni De Cillis",
        "title": "FastAPI is awesome",
        "content": "My first ever web app",
        "date_posted": datetime.now().strftime("%d %B %Y"),
    },
    {
        "id": 2,
        "author": "Giovanni De Cillis",
        "title": "Python is still here",
        "content": "My first ever web app in python",
        "date_posted": datetime.now().strftime("%B %d %Y"),
    },
]


# Create Home route that responds to get requests at the root url
# Stacking decorators
@app.get("/", include_in_schema=False, name="home") #include_in_schema=False ensures you keep them out of docs
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts":posts, "title":"Giovanni' project"})


@app.get("/api/posts",response_model=list[PostResponse])
def get_posts():
    return posts


## Create Post
@app.post(
    "/api/posts",
    response_model=PostResponse, 
    status_code=status.HTTP_201_CREATED, #restful best practice when creating a new resource
)
def create_post(post: PostCreate): # Automatically parses json body, validates schema and return error before the function is run
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": datetime.now().strftime("%d %B %Y"), 
    }
    posts.append(new_post)
    return new_post


# Single api endpoint for posts
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(request: Request, post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# Single api endpoint for browser post
@app.get("/posts/{post_id}", include_in_schema= False, name="post_page")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"]
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": title}
            )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
