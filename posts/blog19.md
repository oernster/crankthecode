---
date: 2026-02-15 15:00
emoji: 🎛️
one_liner: The simulator was not the constraint. The surface was.
tags:
- cat:blog
- architecture
- modelling
- systems
- product-design
title: When the interface becomes the bottleneck
---

# Authoring ergonomics is the real constraint

The simulator was never the problem.

LatencyLab’s core was stable, deterministic and versioned. The execution engines were separated cleanly from the UI. Validation was strict. The architecture was explicit about boundaries.

What was failing was not execution.

It was expression.

The recent revamp changed only the UI. No simulation logic was altered. No schema rules were relaxed. No core modules were touched.

This was deliberate.

The constraint was not correctness. It was ergonomics.

*Users were translating intent into structure by hand.*

## Structure versus intent

The schema is organised around contexts, events, tasks and wiring.

That structure is correct. It is testable. It is deterministic.

However users do not think in those primitives first.

They think in:

- user action
- flow
- responsibility
- coordination
- what blocks what

When the surface forces users to think in schema terms before intent is clear, friction appears.

The friction does not show up in performance metrics.

*It shows up in hesitation.*

## A UI only intervention

The updated `ARCHITECTURE.md` makes the boundary explicit. Core remains stdlib only. UI owns composition. Validation remains authoritative.

This separation allowed a bold change.

The UI was redesigned without touching the engine.

Tasks became cards instead of grids. Wiring was clarified. Events were derived rather than authored manually. Ordering rules were made deterministic and visible.

Nothing about simulation changed.

Everything about authoring did.

*The composer now exposes intent. The core continues to enforce structure.*

## What changed in practice

Before the revamp users were editing JSON or navigating dense tables. The surface reflected schema first and flow second.

After the revamp the surface reflects flow first and schema second.

The result is subtle but material.

Users can construct a scenario without thinking about how it will be serialised. They can see ordering. They can see wiring. They can reason about behaviour without reading raw structure.

The exported JSON remains deterministic and sorted.

*The mental load has moved.*

## The hidden cost of poor authoring surfaces

When modelling tools are hard to author in, two things happen.

Users simplify models to reduce friction.

Or they avoid modelling entirely.

Neither outcome is visible in logs.

The system continues to run correctly. Tests continue to pass. Performance remains stable.

What degrades is willingness to explore.

*If authoring is awkward, modelling becomes rare.*

## The architectural lesson

There is a temptation to refine engines endlessly.

Optimise execution. Improve validation. Add features.

Sometimes the engine is not the constraint.

Sometimes the surface is.

A clean architecture makes this easier to see. When the UI can be rebuilt without touching core logic, it becomes obvious where the friction truly lives.

This revamp was not a rewrite.

It was a recognition.

*The real issue was authoring models ergonomically, not simulation.*
