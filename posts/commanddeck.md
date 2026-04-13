---
title: Command Deck
blurb: A session-driven operational board
date: 2026-04-13 20:00
type: project
thumb_image: /static/images/CommandDeck-icon.png
social_image: /static/images/CommandDeck.png
one_liner: A local-first operational board for moving work through live stages with task-bound focus sessions, outcomes and snapshots.
tags:
- cat:Desktop Apps
- operations
- productivity
- command surface
- fastapi
- react
- sqlite
- windows
- local-first
- python
---

[Command Deck](https://github.com/oernster/CommandDeck)  
A local-first operational board for moving work through clear stages, running one focused session at a time and recording what actually happened.

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/static/images/CommandDeck.png" alt="Command Deck screenshot" style="max-width:100%; border-radius:12px;" />
</div>

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
  Not a task manager. A live board for operational state.
</div>

---

## Problem → Solution → Impact

**Problem:** Most task tools flatten work into lists. They blur intent, execution and history together, which makes it harder to see what is active, what is blocked and where focused time is actually going.

**Solution:** Command Deck uses a fixed four-stage board and a session-driven model. Work items move through Design, Build, Review and Complete. Sessions are tied to specific tasks, outcomes record what happened and snapshots preserve board state.

**Impact:** The result is a clearer operational surface. You can see the current board, run one active focus session, keep lightweight execution history and save meaningful states without turning the system into planning theatre.

---

## Overview

Command Deck is built around execution rather than list maintenance.

The system uses **four fixed workflow stages**:

- Design
- Build
- Review
- Complete

Those stage identities remain stable internally, while the **display labels can be renamed per board**.

In the UI, work items are presented as **Tasks**. Internally, the backend and database still refer to them as **Commands**.

Each task carries a simple status model:

- Not Started
- In Progress
- Blocked
- Complete

The board is intentionally single-screen and single-board.  
Only one session can be active at a time.  
Starting a session requires selecting a task.  
Outcomes attach historical notes to tasks.  
Snapshots let you save and reload named board states.

That makes Command Deck useful for people who want to manage operational motion, not just curate lists.

---

## Why it is different

Most tools ask you to maintain tasks.

Command Deck asks a different set of questions:

- What am I doing right now?
- What is in motion on the board?
- What actually happened?

That shift matters. It makes the interface feel less like administration and more like a control surface for real work.

---

## Command Deck at a Glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Core ideas</h3>
  <ul>
    <li>Four fixed workflow stages</li>
    <li>Renameable stage labels per board</li>
    <li>Tasks as active units of execution</li>
    <li>One active task-bound session at a time</li>
    <li>Outcomes for execution history</li>
    <li>Named snapshots for saved board state</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technical stack</h3>
  <ul>
    <li>FastAPI backend</li>
    <li>React + Vite frontend</li>
    <li>SQLite persistence</li>
    <li>Local-first runtime</li>
    <li>Windows tray launcher</li>
    <li>Packaged Windows runtime and installer</li>
  </ul>
</div>

</div>

---

## Interface

Command Deck is presented as a single board with four stage columns.

Global controls live in the top bar:

- **Start** - enters selection mode so you can choose a task to begin
- **Add** - creates a task in the focused or active stage
- **Stop** - stops the active session

The board supports persisted drag-and-drop ordering within and across stages.

The main interaction model stays deliberately small:

- board view for live work
- create-task modal
- command detail drawer for editing and outcomes
- session timer derived from the active session
- snapshot actions for saving, loading and renaming saved states

---

## Sessions, outcomes and snapshots

Command Deck tracks time at the **task level**, not the category level.

A session stores the selected task and the task's stage at the moment the session begins. Only one session can remain active at once, which keeps the tool aligned with focused work rather than parallel activity theatre.

Outcomes provide a lightweight historical trace by attaching notes directly to tasks.

Snapshots add an extra layer of memory on top of the live board. You can save the current state, reload it later and rename saved snapshots. The implementation also deduplicates structurally identical snapshots so the system stays lightweight.

---

## Architecture

Command Deck is intentionally minimal.

The backend is a FastAPI application with a clean API → Services → Repositories → SQLite flow. The frontend is a single-screen React application built with Vite. When a production build exists, the backend can serve the frontend from the same address.

The project is local-first by design:

- SQLite persists the board locally
- source development keeps backend and frontend separate
- packaged Windows builds run as a desktop-style local runtime
- the Windows release includes a tray flow, a packaged `CommandDeck.exe` runtime and a GUI installer

That keeps the system lightweight, direct and aligned with the idea of a personal operational surface rather than a cloud platform.

---

## Closing note

Command Deck is built around a simple belief: work is not best represented as an ever-growing list. It is better understood as changing operational state across focus, execution, review and completion.

This project is an attempt to give that state a clearer surface - local, direct and grounded in what is actually happening.