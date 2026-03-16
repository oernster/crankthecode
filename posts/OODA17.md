---
title: Decision facade
one_liner: Complex organisational decision structures can be simplified through a single visible interface.
date: 2026-03-16 20:40
emoji: 🏛️
tags:
- cat:decision-architecture-patterns
- layer:decision-interfaces
- decision-architecture
- organisational-design
- system-dynamics
---

Large organisations frequently expose too many decision interfaces.

Teams cannot determine where authority resides. Questions propagate across multiple departments before reaching a decision boundary.

The system becomes cognitively expensive to navigate.

A **Decision Facade** simplifies the interface.

Instead of exposing every internal decision surface the organisation presents a single entry point for a class of decisions.

Behind the facade the internal structure may remain complex.

Externally the system appears simple.

The facade absorbs complexity so that decision objects enter the organisation through predictable interfaces.

*This reduces coordination cost without removing internal structure.*