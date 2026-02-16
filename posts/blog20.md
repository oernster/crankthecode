---
title: Trainer Upgrades - Engineering the Second Iteration
one_liner: Revisiting the Trainer app through a different lens
date: 2026-02-16 13:00
emoji: 🚆
tags:
  - cat:blog
  - python
  - desktop-app
  - testing
  - refactoring
  - solid
  - architecture
  - tdd
---
# Trainer 5.0.3 – Architecture Locked In

[Trainer 5.0.3 is now live](https://github.com/oernster/Trainer/releases/tag/v5.0.3). macOS dmg. Windows build. Flatpak. All working.

This release was not about features. It was about structure.

The application now has a single composition root. No service locators. No hidden factories. No singleton accessors hiding in module scope. All dependencies are wired explicitly in bootstrap and injected downward. Architecture is enforced through tests rather than remembered through convention.

*The system now behaves the way it is designed rather than the way it happens to run.*

# From Working Code to Engineered System

At the start of this effort the application worked. It calculated routes. It generated trains. It rendered astronomy. It fetched weather. It passed tests.

That was not enough.

The core domain is now isolated under models and interfaces only. Services live in their own layer. Managers orchestrate without constructing. UI consumes but does not compose. Architecture rules are enforced with AST-based tests so that forbidden imports and hidden instantiation fail the build immediately.

Bootstrap is the only place allowed to assemble the object graph. Composition helpers are permitted but only when called by bootstrap. Nothing else constructs concrete services. There is exactly one object graph.

*Coherence is not claimed. It is verified.*

# 100 Percent Coverage With Intent

Unit test coverage moved from roughly fifty percent to one hundred percent across the core. Not as a vanity metric. As a structural guarantee.

Branch coverage is included. Architectural rules are executable tests. Module level instantiation is banned in protected layers. Service locator patterns are disallowed. These are not comments in a document. They are constraints in code.

Tests do not just confirm behaviour. They defend boundaries.

*Coverage is now a property of structure not a report number.*

# Refactor Without Feature Noise

Along the way several practical issues were resolved.

Moon phase indicators were corrected using a hybrid local and API approach so that astronomical state aligns with the real world rather than drifting visually. Duplicated astronomy links were removed and replaced with per day buttons with unique emojis. Light mode was corrected so train times are readable rather than white on white. JSON loading and network graph construction were hardened and modularised.

None of that is glamorous. All of it matters.

*Polish without structure is decoration. Structure with polish is product.*

# The Flatpak Lesson

Cross platform builds exposed what local development hides. macOS dmg surfaced timing assumptions. Windows revealed path differences. Linux and Flatpak exposed sandbox constraints and event loop timing.

The splash screen occasionally hanging under Flatpak was not a packaging problem. It was a startup sequencing problem. Bootstrap was doing too much synchronously. The fix was not conditional platform logic. The fix was architectural discipline.

Startup now composes. It does not block. Heavy work is deferred. Shutdown is clean. Async sessions close deterministically.

*If it runs reliably inside a sandbox it runs reliably anywhere.*

# Why This Matters

There is a difference between code that works and a system that is shaped.

Trainer 5.0.3 is shaped.

There is one composition root. There is enforced layering. There are no hidden construction paths. There are no accidental singletons. The domain is pure. Services are explicit. UI is a delivery mechanism not a control surface.

The architecture is now harder to violate than to follow.

*That is when software starts to scale beyond the person who wrote it.*

# What Next

Feature work resumes from here. Nuitka builds are stable across platforms. The foundation is locked. Any future expansion sits on deterministic boundaries.

Version 5.0.3 is not the most visible release. It is the most important one so far.

*Engineering is the discipline of making future change cheaper than present convenience.*
