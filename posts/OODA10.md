---
title: Decision adapter
one_liner: Organisations often require translation layers when decisions move between incompatible domains.
date: 2026-03-16 23:00
emoji: 🔌
tags:
- cat:decision-architecture-patterns
- layer:decision-interfaces
- decision-architecture
- organisational-design
---

Different parts of an organisation often reason about problems differently.

Engineering frames decisions in terms of systems and risk.  
Finance frames decisions in terms of cost and return.  
Legal frames decisions in terms of liability.

When decisions move between these domains the language of the decision may no longer be compatible.

A **Decision Adapter** translates the decision object so that it can move between domains.

The underlying decision remains the same.

Only the interface representation changes.

*Without adapters decisions stall at organisational boundaries because the receiving domain cannot interpret them correctly.*