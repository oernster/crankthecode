from __future__ import annotations

"""Portfolio route.

The portfolio now lives on ernster.dev (the hub for all project sites).
This route exists only to preserve inbound links: it permanently
redirects the old on-site portfolio page to the hub.
"""

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

PORTFOLIO_HUB_URL = "https://ernster.dev"

router = APIRouter()


@router.get("/portfolio", include_in_schema=False)
async def portfolio_redirect() -> RedirectResponse:
    return RedirectResponse(
        url=PORTFOLIO_HUB_URL,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
