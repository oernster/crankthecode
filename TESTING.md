# Testing

How the Crank The Code site is tested: running the checks, reading what they
say, what the gate holds, what CI runs and how a new test or guard is written.
For what holds the code together see [ARCHITECTURE.md](ARCHITECTURE.md); for
setting up the environment the checks run in see
[DEVELOPMENT.md](DEVELOPMENT.md).

## Running the checks

All commands are PowerShell, from the repository root:

```powershell
.\venv\Scripts\python.exe -m black --check .
.\venv\Scripts\python.exe -m flake8 .
.\venv\Scripts\python.exe -m ruff check .
.\venv\Scripts\python.exe -m app.assets.build_static
.\venv\Scripts\python.exe -m pytest
```

That is the gate, in the order CI runs it. `pytest.ini` carries the coverage
options and the floor, so a bare `pytest` enforces them without `--cov`.

**Build the static output before the tests.** A few tests assert on
fingerprinted asset URLs, which only exist once
`python -m app.assets.build_static` has written `static_dist/`. That directory
is gitignored build output, so a fresh clone or a cleared tree has none.

**Run from the repository root.** The application finds its content through
the relative path `posts`, so a run started anywhere else finds no posts.

**A full run takes about fifteen seconds.** Measured on 2026-10-02: 204 tests
passed in 16 seconds on Windows.

**Read the exit code, never the text.** The run prints the coverage table
(fully covered files are skipped from it) then one summary line. A search of
the output for a result word is still not safe, since coverage rows are named
after modules. `$LASTEXITCODE` of 0 means every test passed and the floor
held.

## What the gate holds

- **Coverage.** 100% of `app/`, measured by line AND branch (`branch = True`
  in `.coveragerc`, `--cov-fail-under=100` in `pytest.ini`). Four lines in
  `app/` carry `# pragma: no cover`, in `assets/staticfiles.py` and three
  view models. `main.py` at the root is a deployment shim outside `app/`, so
  it is not measured.
- **Style.** black, flake8 and ruff, run as separate steps rather than as
  tests: a formatting or lint regression passes `pytest` untouched, so run all
  of them. flake8 is configured in `.flake8` and ruff in `pyproject.toml`. The
  two are deliberately kept in agreement on line length, rule families, ignores
  and exclusions: if they disagree, neither can be trusted and every run
  becomes a negotiation. Ruff keeps `E402` live because flake8 does not report
  it here and it is the rule that catches `from __future__ import annotations`
  placed above a module docstring, which silently turns the docstring into a
  bare expression.
- **Structure.** The two guards below.

## Continuous integration

`.github/workflows/checks.yml` runs on every push to `main`, on every pull
request and on demand. It installs both requirements files, runs black, flake8
and ruff, builds the fingerprinted static assets and then runs pytest. The
asset build is not optional: the suite reaches for `static_dist/` and a deploy
produces one, so skipping it would test a state that never ships.

On a push to `main` the same workflow then builds the static site and deploys
it to GitHub Pages; it does so only after those checks pass. `tests/test_build_site.py`
holds the build's path rules, proves its link check by planting a broken link
and runs the real build in a child process. The deploy itself ends by asking
the live site for a fixed set of URLs, each of which must answer 200.

CI runs Python 3.13 with every dependency pinned to the local venv's versions,
so a change green locally should be green there. If it is not, check first
whether the venv has drifted from the pins in the two requirements files.

## Where the tests live

All 38 files sit flat in `tests/`. They fall into three kinds:

| Kind | What it tests | Against |
|---|---|---|
| pages, feeds, redirects, middleware | the HTML routes, the RSS and MMSP feeds, SEO, caching and the canonical redirect | FastAPI's `TestClient` over the application in-process, reading the real `posts/` |
| use cases and helpers | listing and fetching posts, read times, filtering, the view models | `InMemoryPostsRepository` from `tests/fakes.py`; values built in the test |
| the filesystem repository and static delivery | reading markdown and serving assets | real files in a temporary folder and the built `static_dist/` |

Nothing reaches the network: `TestClient` calls the application directly.

## Writing a test

- **No mocking library.** A port is stood in for by a hand-written fake;
  `tests/fakes.py` holds `InMemoryPostsRepository`. Environment and attributes
  are redirected with pytest's own `monkeypatch`.
- **A page.** Build a `TestClient` over the application and request the path;
  `tests/test_html_pages.py` is the nearest example.
- **A post the real content does not have.** Hand the use case an
  `InMemoryPostsRepository` of the posts the test needs rather than adding a
  markdown file to `posts/`.

## Guards

A structural test checks the source tree rather than behaviour, so a rule holds
for code nobody has written yet.

| Guard | Holds |
|---|---|
| `test_architecture_boundaries.py` | the domain imports only the standard library; use cases import only the domain and the ports; ports depend on no adapter, HTTP or asset code; the scan reaches every layer it claims to cover |
| `test_module_size_limits.py` | the 400 line cap and the danger band below it, over the application and the tests alike |

**A guard is not trusted until it has been seen to fail.** A new guard is
proved by planting the violation it exists to catch and reading the failure,
then restoring the tree in a `finally` block so an interrupted proof cannot
leave the plant behind. A test written for a defect is run before the fix,
where it has to fail for the reason named, not merely fail.

---

See also [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md) and
[DEVELOPMENT.md](DEVELOPMENT.md).
