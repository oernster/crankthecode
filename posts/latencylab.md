---
date: 2026-02-07 16:30
emoji: ⏱️
image: /static/images/latencylab.png
one_liner: A small tool was built so arguments about performance could finally be settled by something impolite called reality.
tags:
- cat:Tools
- latency
- simulation
- python
- engineering
title: LatencyLab
social_image: /static/images/latencylab.png
---

# A Small Tool for Uncomfortable Performance Truths

## Problem → Solution → Impact

**Problem:**  
Latency discussions are dominated by intuition, confidence and post-hoc profiling. By the time real systems can be measured, critical decisions about concurrency, feedback, sequencing and delay have already been made and are difficult to reason about without invasive instrumentation or significant rewrites. Profilers explain *what happened* in a running system but rarely clarify *why the user waited*.

**Solution:**  
LatencyLab provides a deterministic simulation engine for modelling latency at design time. Instead of attaching to running production code, it executes explicit models of tasks, events, queues, delays and resource contention using reproducible randomness and well-defined scheduling semantics. By running these models many times it produces concrete metrics such as critical paths, queue wait, UI timing and percentiles. This makes sources of delay visible and attributable.

A lightweight client UI sits alongside the engine, allowing models to be executed, inspected and compared interactively without turning the tool into an IDE or dashboard framework.

**Impact:**  
LatencyLab turns performance arguments into inspectable artifacts. It exposes counter-intuitive bottlenecks, often in coordination, feedback or queueing rather than raw execution, makes delay a first-class concept and enables informed design decisions before implementation. Systems do not necessarily become faster but they feel faster for reasons that can be explained, repeated and defended.

*The UI is intentionally literal. It shows what ran, how often it ran and where time accumulated. Percentiles are separated for UI events and overall makespan because they answer different questions. Critical paths are presented as concrete sequences rather than diagrams because naming work matters more than visual polish. If something dominates the output it is because it dominated the model, not because the interface is trying to be helpful.*

## Rationale

LatencyLab exists because reasoning about latency after the fact is too late.

I wanted a way to explore how systems *behave* under load before they exist in code without relying on optimistic timelines, hand-waved concurrency or “we’ll profile it later.” Traditional profiling is indispensable once software is real but it is silent during the phase where the most damaging latency decisions are made.

This tool forces explicitness. Tasks, events, queues, delays and feedback paths must be named. Randomness is seeded. Models are versioned. Legacy behaviour is preserved as an executable oracle. When numbers change it is because the model changed, not because the measurement drifted.

The goal is not optimisation. It is understanding.  
If LatencyLab does its job, performance discussions become calm, graphs replace confidence and arguments about why something *felt* slow quietly disappear.

[LatencyLab on GitHub](https://github.com/oernster/latencylab)

Latency discussions are usually confident. They are also usually wrong.

Most systems do not feel slow because a function is slow. They feel slow because work queues politely wait their turn, because progress updates crowd out the thing the user actually wanted or because someone decided that showing effort was more important than finishing.

This is difficult to reason about by inspection. It is even harder to reason about while reading code that has opinions about threads, signals, callbacks and optimism.

So I stopped trying.

LatencyLab exists because I wanted a way to describe what happens between a user click and something visible changing on screen without lying to myself about why it felt bad.

## The Problem With Measuring Things That Haven’t Happened Yet

Profilers are excellent. They are also useless at design time.

By the time you are profiling you have already made several irreversible decisions about concurrency, about feedback and about how much work the UI thread is expected to absorb while smiling politely.

LatencyLab deliberately does not attach to running production code. It does not trace live systems or observe wall-clock behaviour. Instead it executes explicit models and measures their consequences.

You describe tasks. You describe queues. You describe when events happen and when they do not. You assign durations that feel roughly honest and distributions that admit long tails because reality always has one.

Then you run the model thousands of times and ask a rude question.

*Why did the user wait.*

## A Single Click Is More Than It Looks

The initial model was deliberately small. One click. One flow. One outcome.

The user clicks a button. That much is obvious.

What follows is not.

Labels update. An ETA shifts optimistically. Emojis spin with enthusiasm. Logs scroll if the user has asked to see them. Meanwhile background work happens elsewhere and progress signals are fired with the best intentions.

All of that is UI work. All of it competes for a single thread. None of it is free.

LatencyLab models that explicitly, sometimes with a single brutally honest task. That is often enough.

*The point is not how pretty the progress is. The point is that it happens often and sometimes at the wrong time.*

## The Client UI Is Part of the System

The client UI exists because text output alone was not enough to reason about timing, ordering and consequence.

Building it was not straightforward.

Layout became a constraint early on. Making trace output readable without collapsing into a scrolling wall of noise required constant adjustment. Button placement mattered more than expected because execution ordering, resets and repeated runs are the primary interaction loop.

Dark and light mode support turned out to be less cosmetic than anticipated. Colour choices that worked for traces failed for controls. Contrast that looked fine in isolation broke down once focus states and hover states were layered on top.

Accessibility was not optional. Keyboard navigation exposed brittle assumptions about tab order and focus management. Fixing those issues forced the UI structure to become simpler and more honest about what could be interacted with and when.

Saving results to disk became necessary once runs stopped being disposable and started being compared. The ability to persist a suite of run logs changed how the tool was used, shifting it from experimentation to comparison. Once results could be saved, they could be revisited and argued about without rerunning everything.

None of this was accidental. The UI is deliberately small but it is not incidental. It participates in the same discipline as the engine: explicit state, predictable behaviour and no hidden work.

## Delays Are Not Bugs They Are Decisions

One of the first things LatencyLab made visible was delay.

Not slowness. Delay.

Debounce windows. Backoff timers. Artificial pacing introduced so things feel smoother while quietly extending the critical path.

In LatencyLab delays are explicit. They appear as synthetic nodes in traces. They show up in the critical path when they dominate. They are no longer hiding inside timestamps pretending to be inevitable.

I suspect most systems hide similar delays even if the details differ.

*This is uncomfortable and that is the idea.*

## Versioning Without Regret

As the models grew so did the cost of changing their meaning.

Early iterations moved quickly: an initial executable skeleton followed by a minimal working model and then a conscious stripping away of speculative architecture in favour of something smaller and executable. Once behaviour existed it was treated as a constraint, not a suggestion.

From there the tool evolved in phases. A second execution path was introduced, schema evolution became explicit and compatibility stopped being an accident. Legacy behaviour was frozen deliberately, not because it was elegant but because confidence matters more than tidiness.

Model versions describe meaning. Application versions describe tooling. Those concerns do not drift silently into each other.

*Git history is not an oracle. Executable tests are.*

## Determinism Is Not Optional

Randomness is useful. Undisciplined randomness is not.

Every run in LatencyLab is seeded. Behaviour remains reproducible across versions. Migration tests assert equivalence where it matters and expose differences where they are intentional.

The code is written so this property is enforced rather than hoped for.

*As is the code.*
