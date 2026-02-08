---
date: 2026-02-09 10:10
emoji: 🧱
one_liner: The decisions that lock in latency long before there is anything to measure.
tags:
- cat:Blog
- architecture
- latency
- performance
- engineering
- systems
title: The architectural mistakes you make before the first profiler runs
social_image: /static/images/latencylab.png
---
# Where latency really gets decided

Profilers are good tools. They explain where time went in a running system and they are invaluable when code already exists. The problem is not what profilers do. The problem is when they arrive.

By the time a system can be profiled, most of the decisions that shape perceived latency are already fixed. Concurrency models are chosen. Feedback paths are wired. Queues exist where they exist. Coordination costs are now part of the architecture rather than variables to explore.

At that point profiling can optimise but it cannot fundamentally change how the system behaves.

*This post is about the mistakes that happen earlier.*

## Mistake one: assuming background work is invisible

Background work feels harmless because it is framed as off the critical path. It runs elsewhere. It is asynchronous. It is not blocking the user, at least not intentionally.

In practice, background work still competes for shared resources. Threads are shared. Queues are shared. Locks are shared. UI updates triggered by background completion still need to run somewhere.

Background work is only invisible if it never blocks progress.

When background tasks emit progress events, trigger callbacks or contend for execution slots, they quietly enter the critical path. The user does not care that the work was labelled background. They only experience the delay.

*Profilers can show that background tasks are running. They rarely make it obvious that those tasks are extending perceived latency through coordination and contention.*

## Mistake two: treating progress feedback as free

Progress indicators are almost always added with good intent. They reassure users. They make systems feel alive. They buy patience.

They are also a common source of unexamined cost.

Each progress update requires scheduling, rendering and coordination with the UI thread. Delays added to make updates feel smooth add up. Multiple progress sources compound. What looks like responsiveness often extends the time to the one result the user actually wanted.

This is not an argument against progress feedback. It is an argument against treating it as free.

*Profilers can show the cost of rendering a progress update. They do not show how repeated updates stretch the critical path through coordination overhead.*

## Mistake three: equating parallelism with speed

Parallelism is attractive because it feels like progress. More threads. More workers. More things happening at once.

Parallelism also increases coordination cost.

As parallel work increases, so does queueing variance. Partial completion becomes common. Systems wait for the slowest participant. More time is spent reconciling work than doing it.

Parallelism without a coordination strategy is a latency amplifier.

*Profilers can show that CPUs are busy. They cannot easily show that the structure of parallel work is what made the system feel slow.*

## Mistake four: deferring structure to later

“We will profile it later” is often a sincere statement. It is also a way of postponing uncomfortable design decisions.

Later measurement happens in a different environment. Code exists. Deadlines exist. Stakeholders exist. Architectural change becomes expensive and politically constrained.

At that stage teams optimise locally. Hot functions are tuned. Caches are added. The structure that causes latency remains because changing it is too disruptive.

*Profilers are then asked to solve problems they were never designed to solve.*

## Why profiling cannot save you here

Profilers excel at local optimisation. They are precise. They are concrete. They answer the question of where time went.

The mistakes described above are global. They are about coordination, sequencing and structure. By the time profiling begins, the critical paths have already formed.

*At that point coordination costs are no longer hypotheses. They are features of the system.*

## What to do instead

The alternative is not to stop profiling. It is to move some of the thinking earlier.

Make coordination explicit before code exists. Name feedback paths. Consider contention as a first class concern. Model how work interacts, not just how long it runs.

Tools like [LatencyLab](https://www.crankthecode.com/posts/latencylab) exist to make this possible but the deeper point is cultural rather than technical.

Latency problems are rarely caused by a single slow function. They are caused by decisions made long before there is anything to measure.

*By the time the profiler runs, the most important mistakes have already been made.*
