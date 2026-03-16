---
title: Decision cache
one_liner: Repeated decisions should be cached so the organisation does not resolve the same question repeatedly.
date: 2026-03-17 00:30
emoji: 🗂️
tags:
- cat:decision-architecture-patterns
- layer:decision-primitives
- decision-architecture
- organisational-design
---

Some decisions recur frequently.

Teams repeatedly escalate the same questions because the system forgets previous resolutions.

A **Decision Cache** stores resolved decision outcomes for reuse.

Future decisions with the same constraints can reuse the cached answer.

This prevents the organisation from rediscovering the same resolution repeatedly.

*Caches accelerate decision systems by converting past resolution into reusable knowledge.*