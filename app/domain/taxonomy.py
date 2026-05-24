from __future__ import annotations

"""Domain taxonomy: canonical layer and category constants.

No HTTP dependency. Safe to import from any layer of the stack.
"""

# Portfolio/systems categories (used to classify posts as "projects" vs "writing").
PROJECT_CATEGORY_LABELS: frozenset[str] = frozenset({
    "desktop apps",
    "tools",
    "gaming",
    "hardware",
    "web apis",
    "data / ml",
})

# Archive view: explicit category sort buckets.
# Bucket 0 = portfolio/project categories (alpha within bucket).
# Bucket 1 = Decision Architecture (Leadership).
# Bucket 2 = Decision Architecture Patterns.
# Bucket 3 = Governance.
# Bucket 4 = Blog and any other writing categories (alpha within bucket).
# Bucket 5 = uncategorised ("Other") — always last.
ARCHIVE_CAT_BUCKETS: dict[str, int] = {
    "desktop apps": 0,
    "data / ml": 0,
    "gaming": 0,
    "hardware": 0,
    "tools": 0,
    "web apis": 0,
    "leadership": 1,
    "decision-architecture-patterns": 2,
    "governance": 3,
    "blog": 4,
}

# Writing view: explicit category sort buckets.
# Bucket 0 = Decision Architecture (Leadership).
# Bucket 1 = Decision Architecture Patterns.
# Bucket 2 = Governance.
# Bucket 3 = Blog.
# Bucket 4 = anything else (alpha within bucket).
# Bucket 5 = uncategorised ("Other") — always last.
WRITING_CAT_BUCKETS: dict[str, int] = {
    "leadership": 0,
    "decision-architecture-patterns": 1,
    "governance": 2,
    "blog": 3,
}

# Decision Architecture Patterns
PATTERNS_CAT_TAG: str = "cat:decision-architecture-patterns"

PATTERNS_LAYER_ORDER: list[str] = [
    "decision-primitives",
    "decision-interfaces",
    "authority-models",
    "system-dynamics",
    "pattern-catalogue",
]

PATTERNS_LAYER_LABELS: dict[str, str] = {
    # IMPORTANT: keys are canonical slugs referenced by frontmatter/routing.
    # Only change the human-readable labels.
    "decision-primitives": "Decision Objects",
    "decision-interfaces": "Decision Interfaces",
    "authority-models": "Authority Patterns",
    "system-dynamics": "Behaviour Patterns",
    "pattern-catalogue": "System Patterns",
}

PATTERNS_LAYER_EMOJIS: dict[str, str] = {
    "decision-primitives": "🧠",
    "decision-interfaces": "🪟",
    "authority-models": "🧬",
    "system-dynamics": "🧩",
    "pattern-catalogue": "🧭",
}

# Decision Architecture (structures) layer pill UI (for /topics/<layer> pages).
STRUCTURES_LAYER_ORDER: list[str] = [
    "decision-systems",
    "cto-operating-model",
    "organisational-structure",
    "structural-design",
    "architecture",
]

STRUCTURES_LAYER_EMOJIS: dict[str, str] = {
    "decision-systems": "⚙️",
    "cto-operating-model": "🎛️",
    "organisational-structure": "🏛️",
    "structural-design": "🧱",
    "architecture": "🏗️",
}
