# CrankTheCode 🧠

A personal blog and portfolio site built to share my development work, technical tools, and software experiments — written and designed by me.

> Visit the live site: [crankthecode.com](https://www.crankthecode.com)

---

## About

This project powers the [CrankTheCode](https://www.crankthecode.com) website — a custom-built, Python-based blog and portfolio designed around fast iteration, clean APIs, and full control of layout and metadata.

Posts cover everything from tool development and API engineering to system-level problem solving. The site also showcases larger projects, technical writeups, and other nerdy chaos.

---

## Features

- Markdown-powered blog posts with syntax highlighting and emoji support
- FastAPI backend with cleanly separated domains and adapters
- Full RSS feed (`/rss.xml`) and SEO meta handling (`/sitemap.xml`, `robots.txt`)
- Built with testability and maintainability in mind — not WordPress
- Deployed via [Render](https://render.com), but flexible for self-hosting

---

## Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests (currently 100% coverage)

- pytest -v --cov


