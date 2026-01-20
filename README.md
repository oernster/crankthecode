# crankthecode
A blog for my development work

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Render deploy compatibility is preserved via the shim [`main.py`](main.py:1), so `uvicorn main:app` still works.

## Structure

- Domain: [`app.domain`](app/domain/__init__.py:1)
- Ports (interfaces): [`app.ports`](app/ports/__init__.py:1)
- Use cases: [`app.usecases`](app/usecases/__init__.py:1)
- Adapters (filesystem, markdown): [`app.adapters`](app/adapters/__init__.py:1)
- HTTP layer (FastAPI routers): [`app.http`](app/http/__init__.py:1)

## API

- `GET /api/posts` – list posts
- `GET /api/posts/{slug}` – post detail

## RSS

- `GET /rss.xml` – RSS 2.0 feed (latest 20 posts)

If you want absolute URLs in feed items to point at your public domain behind a proxy/CDN,
set `SITE_URL` (e.g. `https://crankthecode.com`). If unset, the feed uses the incoming
request base URL.

## SEO

- `GET /sitemap.xml` – XML sitemap (homepage + index pages + all posts)
- `GET /robots.txt` – robots file (allows crawl + points to sitemap)

For canonical URLs (sitemap, `rel=canonical`, OpenGraph, JSON-LD), set `SITE_URL`
(recommended: `https://www.crankthecode.com`). If unset, the app falls back to the
incoming request base URL (and finally `https://www.crankthecode.com`).

Per-post meta description uses frontmatter `blurb` (fallback `one_liner`).

## Dev / TDD

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
pytest -v --cov
black .
flake8
pre-commit install
```
