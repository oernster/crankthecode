# Development guide

How to run, test and work on the Crank The Code site locally. For what the site is, see [README.md](README.md); for how it is structured and what holds it together, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Prerequisites

* Python 3.13 locally (the checked-in `venv/` was built with it). CI runs 3.11; black and ruff both target 3.11, so avoid syntax newer than that.
* Nothing else. No database, no external services: the content is markdown files in `posts/`.

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

The test and lint tooling lives in `requirements-dev.txt`, not `requirements.txt`. Installing only the latter gives you an app that runs and a suite that cannot.

`main.py` at the root is a compatibility shim for deployment (`uvicorn main:app` also works); the real application lives in `app/main.py`.

## Static assets in development

In development no environment variables are needed. With `CTC_USE_STATIC_DIST` unset, the app serves `static/` directly, so a change to `static/styles.css` or an image shows on the next refresh.

Production builds fingerprinted copies into `static_dist/` instead (see Deployment below). If images or styles look broken locally, a stale local `static_dist/` is the usual cause:

```powershell
Remove-Item -Recurse -Force static_dist
```

`static_dist/` is gitignored build output, so a fresh clone does not have one. The app no longer refuses to start in that state: if the configured static directory is missing it falls back to `static/` and serves the unfingerprinted sources.

## Tests

The suite enforces 100% coverage of `app/` (`pytest.ini` carries `--cov-fail-under=100`), so a bare run is the whole gate:

```powershell
.\venv\Scripts\python.exe -m pytest
```

Trust the exit code, not the output text: the coverage table prints last and there is no `N passed` summary line. `$LASTEXITCODE` of 0 means every test passed and the coverage gate held.

A few tests assert on fingerprinted asset URLs, so build the static output first if you have just cleared it:

```powershell
.\venv\Scripts\python.exe -m app.assets.build_static
```

## Formatting and lint

```powershell
.\venv\Scripts\python.exe -m black --check .
.\venv\Scripts\python.exe -m flake8 .
.\venv\Scripts\python.exe -m ruff check .
```

flake8 is configured in `.flake8` and ruff in `pyproject.toml`. The two are deliberately kept in agreement on line length, rule families, ignores and exclusions: if they disagree, neither can be trusted and every run becomes a negotiation. Ruff keeps `E402` live because flake8 does not report it here and it is the rule that catches `from __future__ import annotations` placed above a module docstring, which silently turns the docstring into a bare expression.

## Continuous integration

`.github/workflows/checks.yml` runs on every push to `main`, on every pull request and on demand. It installs both requirements files, runs black, flake8 and ruff, builds the fingerprinted static assets and then runs pytest. The asset build is not optional: the suite reaches for `static_dist/` and a deploy produces one, so skipping it would test a state that never ships.

If a change is green locally and red in CI, check the Python version first: CI is on 3.11.

## Content

* Posts are markdown files in `posts/` with YAML frontmatter (title, date, type, tags, images, one_liner). The filename becomes the URL slug: `posts/fulcrum.md` serves at `/posts/fulcrum`.
* Category and layer come from `cat:` and `layer:` tags. Navigation is derived from those, so adding a post to a hub is a tag edit and not a code change.
* Raw HTML inside a post passes through the renderer, so a post can reuse site CSS classes where markdown is not enough.
* Image paths in posts are absolute under `/static/`, for example `/static/images/play-board.png`.

## Environment variables

None are required locally. The ones the app reads:

| Variable | Default | Purpose |
|---|---|---|
| `CTC_USE_STATIC_DIST` | unset | Serve fingerprinted assets from the build output instead of `static/` (production) |
| `CTC_STATIC_DIST_DIR` | `static_dist` | Which directory that is. It selects the mounted directory as well as the CV lookup. |
| `CTC_STATIC_MANIFEST_PATH` | `static_dist/manifest.json` | Manifest mapping logical asset paths to fingerprinted ones |
| `CTC_CANONICAL_HOST` | `www.crankthecode.com` | Host the canonical-redirect middleware normalises to |

Two further variables, `CTC_ASSET_MANIFEST_DEBUG` and `CTC_FORCE_STATIC_DIST_MANIFEST`, are leftover deployment diagnostics rather than configuration. Do not build on them; see item 1 of [TECH_DEBT.md](TECH_DEBT.md).

## Deployment

The site deploys to Render from [render.yaml](render.yaml): the build installs `requirements.txt` and runs `python -m app.assets.build_static` to produce `static_dist/`, then starts `uvicorn main:app` with the static-dist variables set. Nothing needs doing locally for a deploy beyond pushing to the repository.

There is no release artefact and no version to cut. The deployed site is whatever is on `main`.
