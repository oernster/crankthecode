from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
import os
from pathlib import Path
import frontmatter

app = FastAPI()

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

POSTS_DIR = Path("posts")

def get_all_posts():
    posts = []
    for post_file in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        post = frontmatter.load(post_file)  # parse frontmatter
        slug = post_file.stem
        summary_md = post.content.split("\n\n")[0]  # first paragraph
        summary_html = markdown.markdown(summary_md, extensions=["fenced_code"])
        posts.append({
            "slug": slug,
            "title": post.get("title", slug),
            "date": post.get("date", "Unknown Date"),
            "tags": post.get("tags", []),
            "summary": summary_html
        })
    return posts

def get_post(slug):
    post_path = POSTS_DIR / f"{slug}.md"
    if not post_path.exists():
        return None

    post = frontmatter.load(post_path)  # parse frontmatter
    html_content = markdown.markdown(post.content, extensions=["fenced_code", "codehilite"])
    return {
        "title": post.get("title", slug),
        "date": post.get("date", "Unknown Date"),
        "tags": post.get("tags", []),
        "content": html_content
    }

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    posts = get_all_posts()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.get("/posts/{slug}", response_class=HTMLResponse)
async def read_post(request: Request, slug: str):
    post = get_post(slug)
    if not post:
        return HTMLResponse(content="<h1>404 - Post Not Found</h1>", status_code=404)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
