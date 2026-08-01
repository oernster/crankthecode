# Development guide

How to run, test and work on the Crank The Code site locally. For what the site is, see [README.md](README.md); for how it is structured, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Prerequisites

* Python 3.13 (the checked-in `venv/` was built with it)
* No database, no external services: the site is a FastAPI application whose content is markdown files in `posts/`

## Run the site

All commands are PowerShell, from the repo root.

```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. The `--reload` flag restarts the server when Python files change; markdown content and templates are read per request, so editing a post only needs a browser refresh.

If the venv does not exist yet:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
```

`main.py` at the root is a compatibility shim for deployment (`uvicorn main:app` also works); the real application lives in `app/main.py`.

## Static assets in development

In development no environment variables are needed. With `CTC_USE_STATIC_DIST` unset, the app serves `static/` directly, so a change to `static/styles.css` or an image shows on the next refresh.

Production builds fingerprinted copies into `static_dist/` instead (see Deployment below). If images or styles look broken locally, a stale local `static_dist/` is the usual cause:

```powershell
Remove-Item -Recurse -Force static_dist
```

## Tests

The suite enforces 100% coverage (`pytest.ini` carries `--cov-fail-under=100`), so a bare run is the whole gate:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Trust the exit code, not the output text: the coverage table prints last and there is no `N passed` summary line. `$LASTEXITCODE` of 0 means every test passed and the coverage gate held.

Formatting and lint checks:

```powershell
.\venv\Scripts\python.exe -m black --check .
.\venv\Scripts\python.exe -m flake8
.\venv\Scripts\python.exe -m ruff check .
```

## Content

* Posts are markdown files in `posts/` with YAML frontmatter (title, date, type, tags, images, one_liner). The filename becomes the URL slug: `posts/fulcrum.md` serves at `/posts/fulcrum`.
* Raw HTML inside a post passes through the renderer, so a post can reuse site CSS classes where markdown is not enough.
* Image paths in posts are absolute under `/static/`, for example `/static/images/play-board.png`.

## Environment variables

None are required locally. The ones the app reads:

| Variable | Default | Purpose |
|---|---|---|
| `CTC_USE_STATIC_DIST` | unset | Serve fingerprinted assets from `static_dist/` instead of `static/` (production) |
| `CTC_STATIC_DIST_DIR` | `static_dist` | Where the fingerprinted assets live |
| `CTC_STATIC_MANIFEST_PATH` | `static_dist/manifest.json` | Manifest mapping logical asset paths to fingerprinted ones |
| `CTC_CANONICAL_HOST` | `www.crankthecode.com` | Host the canonical-redirect middleware normalises to |

## Deployment

The site deploys to Render from [render.yaml](render.yaml): the build installs `requirements.txt` and runs `python -m app.assets.build_static` to produce `static_dist/`, then starts `uvicorn main:app` with the static-dist variables set. Nothing needs doing locally for a deploy beyond pushing to the repository.
