# Crank the Code: Technical Debt

A standing reference to the site's outstanding technical debt. It records what is still open, weighs whether each item is worth doing and gives the rationale. Every item is a behaviour-preserving internal concern: nothing here proposes changing the published content, the URLs or the rendered output. Scope is the whole repository (the FastAPI application in `app/`, the templates, the static-asset pipeline and the deployment configuration) read against `ARCHITECTURE.md` and the test suite.

---

## 1. `static/search.js` is 459 lines and the size rule cannot reach it

Every Python file is now under the 400-line cap and `tests/test_module_size_limits.py` holds both halves of the rule, the cap and the 5% danger band, over `app/`, `tests/` and the repository root. Its scope is Python only, so this one file sits outside it.

Splitting it is not a refactor, it is a pipeline change. `static/search.js` is a single IIFE loaded as a classic deferred script from `templates/base.html`. Breaking it up means ES modules; the asset pipeline cannot serve those: `app/assets/build_static.py` fingerprints each file by content hash but never rewrites anything inside a file, while `AssetManifest.rewrite_html_static_urls` only rewrites `src`/`href` attributes and CSS `url(...)` in rendered HTML. An `import "./search_index.js"` would therefore keep pointing at an unfingerprinted path and 404 once `CTC_USE_STATIC_DIST` is on. There are no JavaScript tests, so that failure would reach production unseen.

**Needs a ruling**, two ways to settle it. Either the pipeline learns to rewrite JS import specifiers (or an import map is emitted beside the manifest) and the file is then split. Or the cap is recorded as Python-only by design and this moves to "Not debt". Splitting the file without doing one of those first would break search in the fingerprinted build.

---

## Looks like debt, not worth touching

- The markdown files in `posts/`. That is the content, not the codebase.
- The `app/services/blog_service.py` layer sitting alongside `app/usecases/`. Two names for related things; each has distinct content and merging them is churn.
- The relaxation from strict clean architecture to "light ports/adapters" that `ARCHITECTURE.md` announces up front. That is the documented web variation and it is the right call for a server-rendered site.
- `pytest.ini` pointing the cache at `.pytest_cache_writable` with a comment about a non-writable directory. Ugly, load-bearing and harmless.

## Not debt (do not "fix" these)

These look like candidates but are correct as they stand; changing them would regress or add cost for nothing.

- **The absence of a `VERSION` file.** Settled decision: this repository does not want one. It is a continuously-deployed website with no released artefact and no user-facing surface that asks for a version, so the portfolio's single-source-of-truth rule does not apply here. Do not add one and do not raise it again.
- **The 100% branch-coverage gate living in `pytest.ini` `addopts`.** A bare `pytest` enforces it with no flags to remember. This is the pattern the rest of the portfolio should copy, not a thing to loosen.
- **flake8 and ruff both running over the same code.** Deliberate duplication; `pyproject.toml` explains it: the two are held to the same line length, rule families, ignores and exclusions so they cannot contradict each other; ruff carries `E402` because flake8 does not report it here. Do not drop either one to save a CI step.
- **The asset-fingerprinting pipeline and the `static/` versus `static_dist/` split.** Two directories for the same assets looks redundant; one is the source and one is the built, hashed output; the `CTC_USE_STATIC_DIST` switch is what lets the site run from source locally.
- **The pure `app/domain` package with no framework imports.** Verified pure, then held that way by the source scan in `tests/test_architecture_boundaries.py` rather than by habit.
- **The canonical-host and https redirect middleware in `app/main.py`.** Deployment policy expressed as code, driven by environment. Correct placement.
- **The many small router modules** (`api`, `books`, `html`, `mmsp`, `pages`, `portfolio`, `rss`, `sitemap`). One router per concern plus an aggregator is the intended shape; every one of them is now under the size cap.
