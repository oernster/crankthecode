---
date: 2026-05-27 10:00
type: project
emoji: 👁️
one_liner: A lightweight desktop utility that tracks focused applications to understand attention, interruption and workflow behaviour.
blurb: Focus tracking utility
tags:
- cat:Tools
- golang
- productivity
- desktop
- tracking
- automation
- analytics
title: Focus Reader
image: /static/images/focus-reader.png
social_image: /static/images/focus-reader.png

---

# Understanding Attention Through Focus Tracking

Most productivity tooling focuses on tasks, timers or behavioural dashboards.

Focus Reader started from a much smaller idea:

> What can you learn just by tracking which application currently has focus?

The project monitors focused desktop applications and records how attention moves between them over time.

That sounds trivial until you realise how much workflow behaviour becomes visible from focus transitions alone.

Applications reveal interruption patterns.
Context switching frequency.
Deep work duration.
Attention fragmentation.
Workflow habits.

*The system operates passively in the background with minimal overhead and without requiring manual interaction.*

## Problem → Solution → Impact

**Problem**  
Most productivity tracking systems depend on manual input, intrusive monitoring or heavyweight behavioural analysis. The result is usually friction, inaccurate data or tools that become exhausting to maintain.

**Solution**  
Focus Reader monitors the currently focused application and records focus duration and transition behaviour locally. The system focuses on lightweight passive observation rather than complex activity analysis.

The project intentionally limits scope to focus state tracking rather than attempting to analyse user content or behaviour deeply.

**Impact**  
Patterns around interruption, sustained concentration and workflow fragmentation became visible without requiring active effort from the user.

Simple focus visibility produced surprisingly useful insight into how attention actually behaves during day-to-day computer usage.

*Attention drift becomes much easier to understand once it is visible.*

## Lightweight by design

The project intentionally avoids unnecessary complexity.

There are no cloud services.
No invasive monitoring.
No behavioural scoring systems.
No engagement loops.

The application simply tracks focus state changes and stores the resulting activity data locally.

That simplicity was deliberate.

*The interesting part of the project was exploring how much behavioural understanding could emerge from something as structurally small as application focus tracking.*

## A small tool shaped by workflow reality

Real workflows are fragmented constantly.

People context switch between terminals, browsers, IDEs, documentation, messaging platforms and debugging tools dozens or hundreds of times per day. Most of this behaviour remains invisible until it is measured directly.

Focus Reader exists to make that movement visible without becoming intrusive itself.

The goal was not to build a productivity platform.

The goal was to quietly observe attention movement with as little friction as possible.

*Sometimes the smallest signals reveal the most about how systems actually behave.*