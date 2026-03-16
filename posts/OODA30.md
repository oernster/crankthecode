---
title: Decision semaphore
one_liner: Concurrency control is required when multiple actors attempt to resolve the same decision simultaneously.
date: 2026-03-17 03:10
emoji: 🚦
tags:
- cat:decision-architecture-patterns
- layer:system-dynamics
- decision-architecture
- coordination
---

Multiple actors sometimes attempt to resolve the same decision simultaneously.

The result is duplication, conflict or contradictory outcomes.

A **Decision Semaphore** coordinates access to a decision object.

Only one actor resolves the decision while others wait or observe.

This prevents competing resolutions and preserves consistency across the system.

*Concurrency problems exist in organisations just as they do in software.*