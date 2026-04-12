---
title: Command Deck
blurb: An operational control surface
date: 2026-04-12 20:00
type: project
emoji: 🟢
social_image: /static/images/CommandDeck.png
one_liner: A local-first command surface for structuring work as operational state rather than task-list clutter.
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
A local-first operational control surface for issuing intent, tracking execution and recording what actually happened.

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/static/images/CommandDeck.png" alt="Command Deck screenshot" style="max-width:100%; border-radius:12px;" />
</div>

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
  Not a task manager. A control surface for operational state.
</div>

---

## Problem → Solution → Impact

**Problem:** Most task tools collapse intent, activity and completion into the same flat list. That makes it harder to see what is actually in motion, what is blocked and where time is being spent.

**Solution:** Command Deck treats work as operational state. Commands sit inside five categories - Design, Build, Review, Maintain and Recover - and move through a simple execution model: Not Started, In Progress, Blocked or Complete.

**Impact:** The result is a clearer surface for focused execution. You can see what is active, track category-level sessions and preserve a history of outcomes without turning the system into planning theatre.

---

## Overview

Command Deck is an operational system built around execution rather than planning.

Work is organised into five persistent categories:

- Design
- Build
- Review
- Maintain
- Recover

Each command represents intent.  
Each category can host active work.  
Only one category is active at a time.  
Sessions track focused operational time and outcomes record what really happened.

That makes Command Deck useful for people who want to manage motion, not just maintain lists.

---

## Why it is different

Most tools ask you to maintain tasks.

Command Deck asks a different set of questions:

- What am I doing?
- What is in motion?
- What actually happened?

That shift matters. It makes the interface feel less like administration and more like a live operational board.

---

## Command Deck at a Glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Core ideas</h3>
  <ul>
    <li>Five operational categories</li>
    <li>Commands as active units of execution</li>
    <li>Simple state model</li>
    <li>Category-level session tracking</li>
    <li>Outcome history for completed work</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technical stack</h3>
  <ul>
    <li>FastAPI backend</li>
    <li>React + Vite frontend</li>
    <li>SQLite persistence</li>
    <li>Local-first runtime</li>
    <li>Windows packaging and installer support</li>
  </ul>
</div>

</div>

---

## Architecture

Command Deck is intentionally minimal.

It uses a FastAPI backend, a React frontend and SQLite for persistence. The project is designed to run locally, with a development split between backend and frontend and also supports a packaged Windows runtime with installer flow for desktop use.

That keeps the system lightweight, direct and aligned with the idea of a personal operational surface rather than a cloud platform.

---

## Closing note

Command Deck is one of those projects where the interface reflects a deeper belief: work is not just a list of tasks. It is a changing operational state with intent, friction, flow and recovery all visible on the surface.

That is the space this project is trying to serve.