"""Reusable JSON-LD entity builders.

No HTTP/routing dependency. Functions accept primitive values (site_url str)
and return plain dicts ready for json.dumps().
"""

from __future__ import annotations

from app.http.seo import absolute_url


def build_person_jsonld(*, site_url: str) -> dict[str, object]:
    """Primary `Person` entity for Oliver Ernster.

    Used on the homepage and About page to strengthen the entity association
    between the person and the domain.
    """

    home = absolute_url(site_url, "/")
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{home}#oliver-ernster",
        "name": "Oliver Ernster",
        "url": home,
        "jobTitle": "Principal Engineer and Decision Architect",
        "description": (
            "Principal engineer and decision architect focused on structural system "
            "design, authority boundaries and backend engineering."
        ),
        "sameAs": [
            "https://github.com/oernster",
        ],
        # Typed Things with URLs signal topical authority to crawlers and
        # AI knowledge graphs. Far stronger than bare strings.
        "knowsAbout": [
            {
                "@type": "Thing",
                "name": "Decision Architecture",
                "url": absolute_url(site_url, "/essays"),
            },
            {"@type": "Thing", "name": "Decision Systems"},
            {"@type": "Thing", "name": "CTO Operating Model"},
            {"@type": "Thing", "name": "Organisational Structure"},
            {"@type": "Thing", "name": "Structural Design"},
            {"@type": "Thing", "name": "Software Architecture"},
            {"@type": "Thing", "name": "Backend Systems Design"},
        ],
    }
