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

## Dev / TDD

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
black .
flake8
pre-commit install
```
