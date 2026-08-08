"""Selected Essays: the curated essay set and its on-page grouping.

This is editorial structure, not derived taxonomy: the groups and their
order carry the argument of the Decision Architecture thesis, so they are
fixed here rather than computed from tags.
"""

from __future__ import annotations

ESSAY_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "The model",
        (
            "what-is-decision-architecture",
            "model1",
            "lead29",
        ),
    ),
    (
        "Authority and decisions",
        (
            "lead4",
            "lead17",
            "lead21",
            "lead32",
            "lead6",
        ),
    ),
    (
        "Structure in practice",
        (
            "lead2",
            "lead28",
            "lead27",
            "lead30",
        ),
    ),
    (
        "Beyond the firm",
        (
            "governance1",
            "governance2",
        ),
    ),
)

# Crystalline is the method preface linked from the /essays header. It is not
# an essay in the curated set and never appears in the grouped listing.
CRYSTAL_SLUG = "crystal"

ESSAY_SLUGS: frozenset[str] = frozenset(
    slug for _, slugs in ESSAY_GROUPS for slug in slugs
)
