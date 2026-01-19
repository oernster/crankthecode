"""Compatibility shim.

Deployments may still reference `uvicorn main:app` (see [`render.yaml`](render.yaml:1)).

The real application lives in [`app.main`](app/main.py:1).
"""

from app.main import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
