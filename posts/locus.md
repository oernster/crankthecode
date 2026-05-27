---
title: Locus
blurb: A local-first focus and operational awareness surface for Windows
date: 2026-05-27 20:00
type: project
social_image: /static/images/locus.png
image: /static/images/locus.png
one_liner: A background focus tracking and operational board system combining execution flow, deep work tracking and lightweight task state management.
tags:
- cat:Desktop Apps
- golang
- productivity
- focus-tracking
- operational-state
- windows
- local-first
- sqlite
- tray-app
- deep-work
---

[Locus](https://github.com/oernster/locus)  
A local-first operational focus system that combines live task flow, focus history and background session tracking into a single lightweight Windows runtime. 

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/static/images/Locus.png" alt="Locus screenshot" style="max-width:100%; border-radius:12px;" />
</div>

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
  Not a productivity dashboard. A live surface for operational focus and execution state.
</div>

---

## Problem → Solution → Impact

**Problem:** Most productivity tools either become passive task graveyards or noisy analytics systems. Focus tracking, operational state and execution flow are usually fragmented across timers, kanban tools and browser reports.

**Solution:** Locus combines lightweight operational flow management with background focus tracking. The system runs as a persistent local Windows service, tracks real application usage, records deep work sessions and provides a fixed operational board for moving active work through execution stages.

**Impact:** The result is a calmer operational surface that reflects what is actually happening. You can see where time went, what is actively moving and what meaningful focused work occurred without turning the system into administrative overhead.

---

## Overview

Locus is the convergence of two ideas:

- operational task flow
- real focus visibility

The application combines concepts from earlier projects including CommandDeck and focus-reader into a single integrated runtime.

The board uses **four fixed workflow stages**:

- Plan
- Execute
- Check
- Done

Tasks move across those stages while the background runtime independently tracks application focus history and deep work sessions.

Unlike traditional kanban tools, the board is intentionally minimal and operational rather than managerial.

The upper section of the interface focuses on:

- application usage history
- deep work duration
- focus session visibility
- current operational state

The lower section acts as a lightweight execution board where tasks can move through live operational stages.

Only one active focus session can exist at once.

That constraint is deliberate.

*Locus is designed around focused execution rather than simulated parallelism.*

---

## Why it is different

Most productivity systems ask users to maintain structure manually.

Locus instead tries to expose operational reality:

- What actually received attention?
- What consumed focused time?
- What is currently active?
- What moved forward?
- What remained idle?

That changes the feel of the system.

The board becomes less like project administration and more like a lightweight operational console for real work.

*The focus history also matters because it grounds the system in observed activity instead of intention alone.*

---

## Locus at a Glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Core ideas</h3>
  <ul>
    <li>Fixed operational workflow stages</li>
    <li>Integrated background focus tracking</li>
    <li>Single active focus session model</li>
    <li>Deep work duration tracking</li>
    <li>Application usage visibility</li>
    <li>Snapshot-based operational memory</li>
    <li>Local-first persistent runtime</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technical stack</h3>
  <ul>
    <li>Golang backend/runtime</li>
    <li>Windows background service model</li>
    <li>SQLite persistence</li>
    <li>System tray integration</li>
    <li>Desktop operational interface</li>
    <li>Packaged Windows installer/runtime</li>
    <li>Local-first architecture</li>
  </ul>
</div>

</div>

---

## Interface

Locus is intentionally presented as a single operational surface.

The top section focuses on live focus visibility:

- application usage history
- deep work totals
- active session visibility
- lightweight operational metrics

The bottom section presents the execution board:

- Plan
- Execute
- Check
- Done

Tasks can be moved between stages through drag-and-drop interaction.

Global controls remain intentionally small:

- **Start** - begins a focused session
- **Add** - creates a new task
- **Snapshots** - stores or reloads operational board states

The interface is designed to remain calm and low-noise.

There are no large reporting surfaces, dashboards or KPI-style management layers.

*The emphasis stays on live operational clarity.*

---

## Focus tracking and deep work

Locus continuously tracks application focus activity in the background while running locally on Windows.

That creates a lightweight historical record of:

- active applications
- focused work duration
- session timing
- operational activity patterns

Deep work time is calculated independently from idle duration, allowing the system to distinguish meaningful active engagement from passive machine time.

This is important because most time tracking systems measure presence rather than attention.

Locus attempts to measure operational focus more honestly.

The runtime is designed to stay lightweight and persistent:

- runs quietly in the Windows tray
- maintains local persistence
- survives across sessions
- keeps operational history local to the machine

---

## Snapshots and operational memory

Locus includes snapshot support for preserving named board states.

Snapshots allow the operational surface to function more like a working state machine than a disposable task list.

That means you can:

- preserve meaningful execution states
- restore previous board configurations
- maintain lightweight operational continuity
- avoid rebuilding working context repeatedly

The snapshot model complements the focus history system by preserving both:

- what the board looked like
- what operational activity occurred

---

## Architecture

Locus is intentionally local-first and runtime-focused.

The system is written in Go and designed to operate as a lightweight persistent Windows background runtime rather than a cloud platform.

The architecture focuses on:

- low operational overhead
- local persistence
- simple deployment
- background execution
- responsive desktop interaction

The runtime integrates:

- focus tracking
- operational state management
- task flow
- snapshot persistence
- tray lifecycle management

SQLite persistence keeps the system self-contained and portable.

The result is a lightweight operational environment that behaves more like a personal execution surface than a SaaS productivity platform.

---

## Relationship to earlier projects

Locus effectively combines ideas from two earlier systems:

- CommandDeck
- focus-reader

CommandDeck provided the operational board and execution flow concepts.

focus-reader provided focus visibility and activity tracking ideas.

Locus merges both into a single runtime with a more coherent operational model.

That integration matters because operational state and actual focus history are tightly connected in practice.

Most systems separate them.

*Locus treats them as part of the same execution surface.*

---

## Closing note

Locus is built around a simple idea:

focus is operational state.

Work is not just tasks on a board and it is not just passive time tracking. Real execution sits somewhere between the two.

*This project attempts to expose that space directly through a lightweight local runtime that tracks motion, focus and operational flow without turning work into administrative theatre.*