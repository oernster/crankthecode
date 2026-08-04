# Crank the Code: Technical Debt

A standing reference to the site's outstanding technical debt. It records what is still open, weighs whether each item is worth doing and gives the rationale. Every item is a behaviour-preserving internal concern: nothing here proposes changing the published content, the URLs or the rendered output. Scope is the whole repository (the FastAPI application in `app/`, the templates, the static-asset pipeline and the deployment configuration) read against `ARCHITECTURE.md` and the test suite.

---

## 1. A production diagnostic is still wired into the shipped path

`app/assets/manifest.py` prints on every process start, unconditionally:

```
print(f"USE_STATIC_DIST: {use_dist} (raw={raw_flag!r})")
```

The comment beside it explains why ("It directly answers: is the env flag applied at runtime?") and the file goes further: `CTC_FORCE_STATIC_DIST_MANIFEST` is documented in its own source as "a temporary diagnostic escape hatch to prove that the manifest+templates wiring works even when the env flag is not applied correctly in production".

Both were debugging aids for a specific deployment problem. The problem is presumably solved; the aids shipped. What is left is an env var that can silently force fingerprinted URLs the mounted `/static` cannot serve, plus five `print` calls in a web application that has no other use of `print`. The proportionate fix is to delete the force-load escape hatch and route the remaining diagnostics through the logger at debug level, so Render's log stream carries them only when asked.

This is first in the file because it is the only item here that is visible from outside the repository.

## 2. Two use cases reach past their own ports into the asset layer

`app/usecases/get_post.py` and `app/usecases/list_posts.py` both do:

```python
from app.assets.manifest import get_asset_manifest
```

Everything else in `app/usecases` depends on `app.domain` and `app.ports` only, which is exactly right. `app.assets.manifest` is the opposite of a port: it reads environment variables, touches the filesystem, holds an `lru_cache` and prints. Two use cases therefore cannot be exercised without the asset pipeline's ambient state, and the ports/adapters shape the rest of the package maintains is broken in precisely two places.

The fix is small: declare an `AssetUrls` port beside `MarkdownRenderer` and `PostsRepository`, have the composition root inject the manifest-backed adapter and let the use cases keep depending on the interface. That is one new file and two import changes.

## 3. Nothing enforces the architecture

`ARCHITECTURE.md` is candid about this: "The test suite doubles as architecture enforcement by locking in outward behaviour (routing, SEO, caching and deterministic HTML output)." Behavioural tests are valuable and this suite has a lot of them, but they cannot see item 2, and they will not see the next one either.

`app/domain` is currently pure (stdlib only, verified) and the ports/adapters split is otherwise intact. That state is unguarded. Three source-scan assertions would hold it:

- `app/domain/*` imports nothing outside the standard library.
- `app/usecases/*` imports only `app.domain` and `app.ports`.
- `app/ports/*` imports nothing from `app.adapters`, `app.http` or `app.assets`.

The third one is what would have caught item 2 the day it was written.

## 4. Four files are over the 400-line module cap and nothing measures them

| File | Lines |
|---|---|
| `tests/test_coverage_boost.py` | 695 |
| `tests/test_html_pages.py` | 526 |
| `app/http/routers/posts.py` | 518 |
| `app/http/routers/topics.py` | 468 |
| `static/search.js` | 459 |

There is no size guardrail in the suite, so none of these is reported anywhere. The two routers are the ones that matter: `posts.py` at 518 lines carries route handling, view-model assembly and rendering decisions together, and it is the file most likely to be edited when a post gains a new capability. Splitting each router's view-model assembly out (the `app/http/view_models/` package already exists and already holds `posts.py`) takes both under the cap without inventing structure.

`tests/test_coverage_boost.py` deserves a separate note: it is 695 lines named after the gate rather than after any behaviour, which is what a file becomes when tests are written to move a percentage rather than to pin a rule. Its contents are worth redistributing into the behaviour-named test modules beside it.

## 5. Two broad exception handlers with no stated reason

`app/http/view_models/context.py:76` and `app/http/view_models/posts.py:61` each catch bare `except Exception` with no `# noqa` and no comment. Both are on view-model assembly paths, so the effect is that a malformed post silently renders as something else rather than failing.

That may well be the intent for a content site where one bad frontmatter block should not take down a page. The debt is that the intent is not written down, so neither handler can be reviewed and neither can be narrowed with confidence. Give each one a comment naming what it is degrading and why, then narrow it to the exception type that actually occurs.

## 6. `ARCHITECTURE.md` documents an EPUB book builder that is not in this repository

`ARCHITECTURE.md` carries a full "Book builder (Decision Architecture EPUB)" section describing `book/build_decision_architecture_book.py`, `book/build_da_patterns_book.py`, `book/book_builder/orchestrator.py`, `book/book_builder/repository.py`, `book/book_builder/paths.py` and `book/book_builder/pandoc_epub.py`, each as a clickable source link.

None of it exists. `book/` is not tracked and is not on disk; every link in that section resolves to nothing. The builder is no longer part of this project, so this is documentation describing a subsystem that left.

Delete the section, and delete the builder wherever any trace of it remains. The markdown posts under `posts/` that it consumed stay exactly where they are; only the builder and its documentation go. This is the cheapest item in the file and the one most likely to mislead: an architecture document that describes absent code teaches a reader to distrust the parts that are accurate.

---

## Looks like debt, not worth touching

- The 130 markdown files in `posts/`. That is the content, not the codebase.
- `app/usecases/snippets/axisdb.py`, a code snippet held as a Python module so it can be rendered into a post. It looks like a category error and it is the correct answer: the snippet is under the same lint and the same tests as everything else, so it cannot rot into something that does not run.
- The `app/services/blog_service.py` layer sitting alongside `app/usecases/`. Two names for related things, but each has distinct content and merging them is churn.
- The relaxation from strict clean architecture to "light ports/adapters" that `ARCHITECTURE.md` announces up front. That is the documented web variation and it is the right call for a server-rendered site.
- `pytest.ini` pointing the cache at `.pytest_cache_writable` with a comment about a non-writable directory. Ugly, load-bearing and harmless.

## Not debt (do not "fix" these)

These look like candidates but are correct as they stand; changing them would regress or add cost for nothing.

- **The absence of a `VERSION` file.** Settled decision: this repository does not want one. It is a continuously-deployed website with no released artefact and no user-facing surface that asks for a version, so the portfolio's single-source-of-truth rule does not apply here. Do not add one and do not raise it again.
- **The 100% branch-coverage gate living in `pytest.ini` `addopts`.** A bare `pytest` enforces it with no flags to remember. This is the pattern the rest of the portfolio should copy, not a thing to loosen.
- **The asset-fingerprinting pipeline and the `static/` versus `static_dist/` split.** Two directories for the same assets looks redundant; one is the source and one is the built, hashed output, and the `CTC_USE_STATIC_DIST` switch is what lets the site run from source locally. Item 1 is about the diagnostics bolted onto this, not about the pipeline.
- **The pure `app/domain` package with no framework imports.** Verified pure today. Item 3 exists to keep it that way, not because anything is currently wrong with it.
- **The canonical-host and https redirect middleware in `app/main.py`.** Deployment policy expressed as code, driven by environment. Correct placement.
- **The many small router modules** (`api`, `books`, `html`, `mmsp`, `pages`, `portfolio`, `rss`, `sitemap`). One router per concern plus an aggregator is the intended shape. Item 4 concerns only the two that outgrew it.
