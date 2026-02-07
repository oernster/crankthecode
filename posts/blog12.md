---
date: 2026-01-28 15:30
emoji: "\U0001F9F1"
one_liner: Before making code cleaner make sure it can stop cancel and shut down correctly
  every single time.
tags:
- cat:Blog
- stellody
- refactor
- architecture
- tdd
title: 'Refactoring Without Regret: Locking Down Lifecycle First'
---

# Stellody: Why Lifecycle Comes First

A major refactor of Stellody is now underway with one non negotiable rule: behaviour must remain identical. Same UX. Same timing. Same threading model. Same ETA behaviour.

This is a refactor for clarity and maintainability not a redesign.

Once that constraint was in place one truth surfaced almost immediately. If lifecycle and shutdown semantics are not rock solid everything else is built on sand.

Before touching ETA logic progress aggregation or orchestration structure lifecycle behaviour had to be locked down first.

---

## 🔁 The Strict Behavioural Boundary

Both Step 1 and Step 2 workflows are now treated as strict contracts rather than best effort flows.

The following guarantees must hold before any structural change is allowed:

- Cancellation works at any point during execution.
- Multiple stop calls are idempotent and safe.
- No progress or ETA updates are emitted after stop.
- Threads and workers shut down cleanly and deterministically.
- UI state always settles into a consistent final state.

If any of these change the refactor has failed.

---

## 🧪 Why Tests Must Start Here

Lifecycle bugs are the worst kind of bugs.

They are timing sensitive, difficult to reproduce and responsible for the kind of flaky behaviour that makes every other change look suspicious. They poison confidence and make later refactors unnecessarily risky.

By characterising teardown cancellation and shutdown behaviour first, everything that follows becomes simpler. ETA refactors become mechanical. Progress aggregation becomes predictable. Tests stop flapping.

*-This is boring work but it is the difference between a refactor that looks good and one that survives real use.*

---

## 🧭 Architecture by Pressure Not Ideology

I did not introduce a heavy application layer or abstract everything upfront. Instead the approach was pragmatic and pressure driven.

- Existing module boundaries were kept where possible.
- Pure orchestration logic was extracted only when tests demanded it.
- Qt is treated as an adapter not a decision maker.
- Testability drives structure rather than diagrams.

*-This keeps risk low while still allowing the architecture to improve organically.*

---

## ✅ The Refactor Order That Actually Works

The sequence that emerged was straightforward and repeatable:

1. Characterise and lock lifecycle teardown and idempotency.
2. Refactor GUI worker orchestration under those guarantees.
3. Refactor progress and ETA aggregation safely.
4. Leave discovery logic and integrations untouched until orchestration is clean.

*-It is not glamorous but it is correct.*

---

## 🏁 Closing Thought

Clean code is worthless if it cannot stop cleanly.

By starting with lifecycle guarantees I can refactor aggressively later without fear. Everything else builds on this foundation.

*-Refactors should reduce anxiety not create it.*

---

This post builds on the architecture and ETA work described in the previous blog post.