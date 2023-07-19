import pathlib
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# app create
app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent
print(BASE_DIR)
templates = Jinja2Templates(directory=[
    BASE_DIR / "templates",
])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    posts = [
        {"id":1, "title":"fastapi.blog title 1", "body":"Learn fastapi with fastapi.blog team 1"},
        {"id":2, "title":"fastapi.blog title 2", "body":"Learn fastapi with fastapi.blog team 2"},
        {"id":3, "title":"fastapi.blog title 3", "body":"Learn fastapi with fastapi.blog team 3"},
    ]
    context = {
        "request": request,
        "posts": posts,
        "title": "Home Page"
    }
    response = templates.TemplateResponse("index.html", context)
    return response
