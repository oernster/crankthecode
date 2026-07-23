--- 
title: Locus
blurb: Task board and focus tracking for Windows
date: 2026-01-19 06:50
type: project
social_image: /static/images/locus.png
image: /static/images/locus.png
thumb_image: /static/images/locus-icon.png
one_liner: A native Windows task board with automatic focus tracking and live Claude Code integration.
tags:
- cat:Desktop Apps
- golang
- claude
- task-board
- focus-tracking
- productivity
- developer-tools
- local-first
- sqlite
- windows
---

[Locus](https://ernster.dev/locus/) is a native Windows productivity tool that merges a four-stage task board with automatic, OS-level focus tracking and live Claude Code integration.

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
  Where intent meets attention.
</div>

---

## Problem → System → Outcome

**Problem.** Task tools record intent: what you planned and what stage it reached. Time trackers record raw clock time: how long some window was open. Neither checks whether the two matched and an AI coding session adds a third stream of activity that evaporates as scrollback.

**System.** A single Go binary putting a four-stage board (Plan, Execute, Check, Done) and Win32-level focus tracking in one window over one local SQLite database, with Claude Code hook scripts routing each meaningful tool call onto the board as it happens.

**Outcome.** The day ends with an honest, automatic record: what was planned, what actually held attention and what the AI session contributed, all local and inspectable.

---

## Why it exists

Productivity tooling splits into two camps that never talk to each other.

Boards know what you meant to do. Trackers know how long windows were open. The question that matters at the end of a day sits between them: did the work you planned get the attention you thought it did?

That gap is where drift lives and manual logging never survives long enough to expose it.

*Locus exists to close the gap automatically.*

---

## The board

Work moves through four fixed stages: Plan, Execute, Check, Done.

Stages have stable internal IDs and renameable labels. Tasks carry a status, are timed at the task level and only one session is active at a time. A named snapshot is saved automatically at session end.

The stages are deliberately fixed. The discipline is the point; only the labels are yours.

---

## Focus tracking

Locus reads foreground focus straight from the Win32 APIs, polling every 500ms into the same SQLite database as the tasks.

The record is designed to be honest rather than flattering:

- idle gaps over five minutes are subtracted, so idle never counts as focus
- system processes are filtered out automatically
- application names come from real PE version info, not a hardcoded mapping
- focus history ranks today, yesterday, this week and this month

*It exposes operational reality rather than creating productivity theatre.*

---

## Claude Code integration

Hook scripts installed by the installer route each meaningful tool call onto the board live, marked with an amber border:

- edits land at Execute, labelled by filename
- test runs land at Check
- a successful command moves its card to Done; a failure stays put, so what stalled stays visible
- trivial commands are filtered out

An AI coding session normally vanishes when the terminal closes. Here it leaves a structured trail on the same board as the work you planned yourself.

---

## What it is

A native Windows tool in a single Go binary: a four-stage task board (Plan, Execute, Check, Done) beside OS-level focus tracking into local SQLite, with Claude Code activity flowing onto the board live. The full capability rundown lives on the product site: [ernster.dev/locus](https://ernster.dev/locus/).

---

## Local first, by construction

Everything stays on the machine: tasks, sessions and focus history in one SQLite file, no telemetry, no cloud, no accounts.

The binary is pure Go with no CGO, installed per-user by one PowerShell script with no administrator rights, auto-starting on login and removable just as cleanly.

*A tool that watches your focus has to be one you can fully inspect and fully remove.*

---

## Relationship to earlier projects

Locus consolidates two earlier tools: CommandDeck's staged session model and focus-reader's background focus monitor.

*The current version is the native Go synthesis of both, with the Claude Code integration layered on top.*

---

## Closing note

Locus is built around a simple idea: intent and attention should be visible in the same place, recorded by the system rather than by willpower.

*The board says what you meant. The tracker says what happened. Locus is the one window where you can see whether they agree.*
