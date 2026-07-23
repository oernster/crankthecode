--- 
title: Locus
blurb: Project memory for Claude Code
date: 2026-01-19 06:50
type: project
social_image: /static/images/locus.png
image: /static/images/locus.png
thumb_image: /static/images/locus-icon.png
one_liner: A local-first MCP memory and focus tracking layer for Claude Code.
tags:
- cat:Desktop Apps
- golang
- claude
- mcp
- memory
- focus-tracking
- developer-tools
- local-first
- cli
- sqlite
- windows
---

[Locus](https://ernster.dev/locus/) is a local-first memory and operational awareness system for Claude Code workflows and Windows focus tracking.

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
  Persistent project context and operational focus history across long-running development sessions.
</div>

---

## Problem → System → Outcome

**Problem.** AI coding sessions lose project context between runs and most productivity tools fail to capture real operational activity; the reasoning behind past decisions and where the time went both evaporate.

**System.** A local-first Go runtime that captures structured project memory (decisions, conventions, rejected approaches) for Claude Code over MCP, alongside passive Windows focus tracking, all inspectable and developer-controlled.

**Outcome.** Project context and operational history persist across long-running sessions, owned by the developer and the project rather than the model, so work resumes without re-explaining itself.

---

## Overview

Locus combines two ideas:

- persistent project memory
- operational focus tracking

The system captures and resurfaces high-level project context across Claude Code sessions while also tracking real operational activity on Windows over time.

Instead of storing full transcripts, Locus records structured concepts such as:

- architectural decisions
- implementation summaries
- project conventions
- rejected approaches
- workflow notes
- operational context

Alongside that, the runtime continuously tracks focus activity including:

- active applications
- focus duration
- session timing
- operational patterns
- historical activity trends

The goal is simple:

*Important project context and operational state should not disappear between sessions.*

---

## Claude Code integration

Locus integrates directly with Claude Code through MCP.

This allows Claude workflows to:

- search project memory
- review previous decisions
- inspect earlier implementation context
- recover workflow history
- continue long-running work more easily

Locus does not modify the model.

*It provides a persistent local context layer that developers can review and reuse across sessions.*

---

## Focus tracking

Locus also operates as a persistent Windows focus tracking runtime.

The system records operational activity across:

- sessions
- days
- weeks
- longer-running workflows

This creates a lightweight historical operational surface showing:

- what received attention
- how long focus lasted
- what applications were active
- how work patterns changed over time

The focus system is intentionally passive and local-first.

*It is designed to expose operational reality rather than create productivity theatre.*

---

## Memory model

Locus focuses on structured contextual recall rather than transcript persistence.

Captured memory remains:

- local-first
- inspectable
- reviewable
- searchable
- developer-controlled

*The emphasis is on preserving useful project concepts and operational continuity rather than simulating persistent agent memory.*

---

## Diagnostics

Locus is designed to be diagnosable rather than opaque.

The system exposes tooling for:

- memory status
- project scanning
- import visibility
- recall inspection
- focus history inspection
- diagnostic workflows

*Developers can see what has been captured, what is available and how the system is behaving over time.*

---

## What it is

A native Windows tool in a single Go binary: a four-stage task board (Plan, Execute, Check, Done) beside OS-level focus tracking into local SQLite, with Claude Code activity flowing onto the board live. The full capability rundown lives on the product site: [ernster.dev/locus](https://ernster.dev/locus/).

---

## Why it is different

Most AI coding workflows lose context between sessions and most productivity tools fail to capture real operational activity.

Locus combines both:

- persistent project memory
- long-term operational focus tracking

The result is a lightweight local system that preserves both project understanding and historical execution state over time.

*The memory belongs to the developer and the project rather than the model itself.*

---

## Relationship to earlier projects

Locus originally evolved from earlier operational tooling projects including CommandDeck and focus-reader.

*The current version combines those operational awareness ideas with persistent memory tooling for Claude Code workflows.*

---

## Closing note

Locus is built around a simple idea:

important project context and operational history should remain accessible across long-running development workflows.

The focus is not transcript persistence or artificial agent memory.

*The focus is preserving useful project-level concepts and operational visibility in a structured local system that developers can inspect, search and reuse over time.*
