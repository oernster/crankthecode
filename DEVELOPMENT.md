# Development guide

How to run, test and work on the Crank The Code site locally. For what the site is, see [README.md](README.md); for how it is structured and what holds it together, see [ARCHITECTURE.md](ARCHITECTURE.md); for running and writing the tests, see [TESTING.md](TESTING.md).

## Prerequisites

* Python 3.13, locally and in CI. Black and ruff still target 3.11, so avoid syntax newer than that.
* Dependencies are pinned in `requirements.txt` and `requirements-dev.txt` to the versions in the local venv. To upgrade one, install it in the venv, run the gate, then move its pin to match; CI installs exactly the pins.
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

`main.py` at the root is a compatibility shim (`uvicorn main:app` also works); the real application lives in `app/main.py`.

## Static assets in development

In development no environment variables are needed. With `CTC_USE_STATIC_DIST` unset, the app serves `static/` directly, so a change to `static/styles.css` or an image shows on the next refresh.

Production builds fingerprinted copies into `static_dist/` instead (see Deployment below). If images or styles look broken locally, a stale local `static_dist/` is the usual cause:

```powershell
Remove-Item -Recurse -Force static_dist
```

`static_dist/` is gitignored build output, so a fresh clone does not have one. The app no longer refuses to start in that state: if the configured static directory is missing it falls back to `static/` and serves the unfingerprinted sources.

## Tests, lint and CI

The gate, its order, what CI runs and how to read a result are in [TESTING.md](TESTING.md).

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

The site is static files on GitHub Pages at `www.crankthecode.com`. A push to `main` runs `.github/workflows/checks.yml`; once its checks pass, it:

1. runs `python build_site.py`, which builds `static_dist/` with `CTC_USE_STATIC_DIST` on, renders every page into `site/` and fails on any internal link that lands on nothing;
2. publishes `site/` to Pages;
3. asks the live site for a fixed set of URLs, each of which must answer 200 directly.

Nothing needs doing locally for a deploy beyond pushing to the repository. To see what will ship, build and serve it:

```powershell
python build_site.py --serve
```

The repository's Pages source must be set to GitHub Actions, with `www.crankthecode.com` as its custom domain. The build writes the same name into `site/CNAME`, taken from the site URL the app already uses.

There is no release artefact and no version to cut. The deployed site is whatever is on `main`.

---

See also [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md) and
[TESTING.md](TESTING.md).
