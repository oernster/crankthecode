# Crank the Code: Technical Debt

A standing reference to the site's outstanding technical debt. It records what is still open, weighs whether each item is worth doing and gives the rationale. Every item is a behaviour-preserving internal concern: nothing here proposes changing the published content, the URLs or the rendered output. Scope is the whole repository (the FastAPI application in `app/`, the templates, the static-asset pipeline and the deployment configuration) read against `ARCHITECTURE.md` and the test suite.

---

## 1. Four files are over the 400-line module cap and nothing measures them

| File | Lines |
|---|---|
| `tests/test_coverage_boost.py` | 617 |
| `tests/test_html_pages.py` | 558 |
| `app/http/routers/posts.py` | 556 |
| `static/search.js` | 459 |

There is no size guardrail in the suite, so none of these is reported anywhere. The router is the one that matters: `posts.py` carries route handling, view-model assembly and rendering decisions together; it is the file most likely to be edited when a post gains a new capability. Splitting its view-model assembly out (the `app/http/view_models/` package already exists and already holds `posts.py`) takes it under the cap without inventing structure.

`tests/test_coverage_boost.py` deserves a separate note: it is named after the gate rather than after any behaviour, which is what a file becomes when tests are written to move a percentage rather than to pin a rule. Its contents are worth redistributing into the behaviour-named test modules beside it.

## 2. Two broad exception handlers with no stated reason

`load_about_html()` in `app/http/view_models/context.py` and `estimate_read_time_from_template()` in `app/http/view_models/posts.py` each catch a bare `except Exception` with no `# noqa` and no comment. Both are on view-model assembly paths, so the effect is that a malformed post silently renders as something else rather than failing.

That may well be the intent for a content site where one bad frontmatter block should not take down a page. The debt is that the intent is not written down, so neither handler can be reviewed and neither can be narrowed with confidence. Give each one a comment naming what it is degrading and why, then narrow it to the exception type that actually occurs.

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
- **The many small router modules** (`api`, `books`, `html`, `mmsp`, `pages`, `portfolio`, `rss`, `sitemap`). One router per concern plus an aggregator is the intended shape. Item 1 concerns only `posts.py`, the single router that outgrew it.
