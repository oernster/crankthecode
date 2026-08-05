# Crank The Code

The publishing system behind [www.crankthecode.com](https://www.crankthecode.com), a long-form writing site about decision systems, authority design and structural integrity in engineering organisations.

This repository is the site itself: a FastAPI application that renders markdown posts server-side, plus the static asset pipeline that fingerprints and serves its CSS, JavaScript and images. There is no CMS and no database. The content is markdown files in `posts/` and the structure is expressed in tags.

---

## Why it exists

Most engineering writing stops at tools, frameworks and surface patterns. That misses the real problem: software organisations fail structurally, because decisions are unclear, authority is diffused and systems accrete without ownership.

The writing models those structures directly. The implementation applies the same principles it argues for: clear boundaries, explicit structure and minimal hidden behaviour.

---

## Who it is for

* Readers of the site, who need nothing from this repository
* Anyone who wants to see a small server-rendered site built without a CMS abstraction layer
* Its author, as the deployment source of record

## Who it is not for

* Anyone looking for a reusable blog engine or a static site generator. The routing, the taxonomy and the navigation are specific to this site and are not parameterised for reuse.
* Anyone looking for a downloadable application. This is a continuously deployed web service with no release artefact and no version to install.
* Contributors adding content. The posts are one author's body of writing.

---

## What it does

* Serves markdown posts with YAML frontmatter, the filename becoming the URL slug
* Groups posts into two parallel hub ecosystems, Decision Architecture (Structures) and Decision Architecture Patterns, driven entirely by `cat:` and `layer:` tags
* Splits the post listing into Writing, Projects and Archive views with category and layer filtering
* Renders a Books catalogue page from a single in-repo catalogue definition
* Emits SEO surfaces server-side: canonical URLs, meta descriptions, JSON-LD, an RSS feed, an MMSP feed, a sitemap and robots.txt
* Redirects to a canonical host and scheme, then applies a content-type-aware cache policy at the ASGI level
* Fingerprints static assets at build time and serves them immutable for a year, falling back to the plain sources when no build output is present
* Permanently redirects `/portfolio` to ernster.dev, where the portfolio now lives

---

## Stack

| Concern | Choice |
|---|---|
| Language | Python 3.13 locally, 3.11 in CI |
| Web framework | FastAPI on Starlette |
| Server | Uvicorn |
| Templating | Jinja2, server-rendered |
| Content | Markdown files with YAML frontmatter, via `python-frontmatter` and `markdown` |
| Storage | The filesystem. No database. |
| Tests | pytest with a 100% coverage gate in `pytest.ini` |
| Lint and format | black, flake8 and ruff, all three enforced in CI |
| Hosting | Render, configured by `render.yaml` |

---

## Install and run

PowerShell, from the repo root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
python -m uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000. No environment variables are needed locally and no services have to be running.

## Test

```powershell
.\venv\Scripts\python.exe -m pytest
```

`pytest.ini` carries `--cov-fail-under=100`, so a bare run is the whole gate. Trust the exit code rather than the output text: the coverage table prints last and there is no `N passed` summary line.

## Build

Only the static asset pipeline has a build step; only production needs it:

```powershell
python -m app.assets.build_static
```

That writes fingerprinted copies of everything in `static/` to `static_dist/` along with a manifest mapping logical paths to fingerprinted ones. Render runs it as its build command before starting the app. Locally the app serves `static/` directly unless `CTC_USE_STATIC_DIST` is set.

---

## Documentation

* [ARCHITECTURE.md](ARCHITECTURE.md): the invariants, the tests that hold them, the layering and the request flows
* [DEVELOPMENT-README.md](DEVELOPMENT-README.md): local run, tests, environment variables and the asset pipeline
* [TECH_DEBT.md](TECH_DEBT.md): what is still open, what is deliberately left and what only looks like debt

---

## Licence

MIT. See [LICENSE](LICENSE).
