---
title: "Refactoring Without Regret: Locking Down Lifecycle First"
date: "2026-01-28 15:30"
tags: ["blog", "stellody", "refactor", "architecture", "tdd"]
one_liner: "Before you make code cleaner, make sure it can stop, cancel and shut down correctly every single time."
emoji: "🧱"
---
## 🧱 Stellody: Why Lifecycle Comes First

I have performed a major refactor of Stellody with one non-negotiable rule: **all behaviour must remain identical**. Same UX, same timing, same threading, same ETA behaviour. This is a refactor for clarity and maintainability, not a redesign.

With that constraint in place, one truth became obvious very quickly:

If lifecycle and shutdown semantics are not rock solid, everything else is a lie.

Before touching ETA logic, progress aggregation or orchestration structure, I decided to lock down lifecycle behaviour first.

---

## 🔁 The Strict Behavioural Boundary

Both Step 1 and Step 2 workflows are now treated as **strict contracts**, not best-effort flows.

That means the following behaviour must remain identical and fully characterised in tests before refactoring:

* Cancellation works at any point in execution.
* Multiple stop calls are idempotent and safe.
* No progress or ETA updates are emitted after stop.
* Threads and workers shut down cleanly and deterministically.
* UI state always ends in a consistent, settled state.

If any of that changes, the refactor has failed.

---

## 🧪 Why Tests Must Start Here

Lifecycle bugs are the worst kind of bugs:

* They are timing sensitive.
* They are hard to reproduce.
* They cause flaky tests.
* They make every other refactor look broken.

By characterising teardown, cancellation and shutdown behaviour first, every later refactor sits on firm foundations. ETA refactors become straightforward. Progress aggregation becomes predictable. Tests stop flapping.

*- This is boring work, but it is the difference between a refactor that looks good and one that survives real use.*

---

## 🧭 Architecture by Pressure, Not Ideology

I did not introduce a full application layer up front. Instead I took a hybrid approach:

* Keep existing module boundaries where possible.
* Extract pure orchestration logic only when tests demand it.
* Treat Qt as an adapter, not a decision maker.
* Let testability drive structure, not diagrams.

*- This keeps risk low while still allowing the architecture to improve organically.*

---

## ✅ The Refactor Order That Actually Works

The refactor sequence that emerged looks like this:

1. Characterise and lock lifecycle teardown and idempotency.
2. Refactor GUI worker orchestration under those guarantees.
3. Refactor progress and ETA aggregation safely.
4. Leave discovery logic and integrations untouched until orchestration is clean.

*- It is not glamorous but it is correct.*

---

## 🏁 Closing Thought

Clean code is worthless if it cannot stop cleanly.

By starting with lifecycle guarantees, I can refactor aggressively later without fear. Everything else builds on this foundation.

*– Refactors should reduce anxiety, not create it.*

---

*This post builds on the architecture and ETA work described in the previous blog post*
