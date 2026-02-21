---
title: Wiring Up Windsurf - Rules, Hooks and a Harness That Thinks
one_liner: How I turned an AI editor into a disciplined engineering partner
date: 2026-02-21 10:30
emoji: 🪁
tags:
  - cat:blog
  - ai
  - windsurf
  - tooling
  - architecture
  - python
  - developer-experience
---

# The problem with AI editors out of the box

Most AI editors are helpful in the same way a very fast intern is helpful.

They write code quickly. They follow instructions. They forget everything the moment the conversation ends.

Windsurf is different in that it exposes enough surface area to actually train it. Rules, workflows, hooks, skills, memories. The question is whether you bother to use them.

*An unconfigured AI editor is just autocomplete with opinions.*

# What Windsurf actually gives you

Windsurf's Cascade agent operates across several layers that compose cleanly when you understand what each one does.

**Rules** fire conditionally based on file globs or model decisions. A rule attached to `*.py` files fires whenever Python is being written. A rule marked `always_on` fires in every session. Rules are how you encode standards that never need repeating.

**Workflows** are slash commands. `/new-project`, `/resume-session`, `/debug-session`. Each one is a structured sequence of steps the agent follows. They replace the ritual of re-explaining your process at the start of every session.

**Hooks** are event-driven automations. After writing a Python file, run `flake8`. After writing a test file, run `pytest`. Before executing a destructive command, block and confirm. Hooks enforce discipline without requiring thought.

**Skills** are reusable capabilities the agent can invoke. Architecture design. Debug investigation. Python implementation. They sit in `.windsurf/rules/agents/skills/` and give the agent a vocabulary for structured work.

*Together these layers turn a chat interface into a disciplined engineering partner.*

# The harness

The configuration lives in a directory of your choice; I call mine ``harness`` - It is not inside any project. It is a standalone repository that gets applied to whichever project is active.

The rules encode Python standards. Type hints everywhere. Early returns over nesting. Functional core with an imperative shell. SOLID applied with intent. The canonical four-layer model is domain, application, infrastructure and interface. Domain never imports infrastructure. Infrastructure is injected.

The workflows encode process. Every session starts by reading `progress.md`, `architecture.md` and `features.json`. Every session ends by updating them. The agent announces what it is resuming from and what it is doing next before writing a single line of code.

The hooks enforce quality automatically. Black and flake8 run on every Python write. Pytest runs on every test file write. Destructive commands are blocked until confirmed.

*The harness is the difference between an agent that helps and an agent that can be trusted.*

# Activating it

Switching between projects is a single paste. A file called `harness-workspace.md` contains one editable line - the active project path - and a prompt block below it. Edit the path, copy the prompt and paste it into Cascade.

The agent reads both directories, loads all rules and skills, checks for `progress.md` and `architecture.md`, runs the baseline test suite and announces its state. If the project is new it initialises it. If it is existing it resumes from the last stopping point.

No configuration per project. No repeated explanations. No lost context.

*The cost of switching projects is one line edit and one paste.*

# What it changes in practice

The agent no longer needs to be told how to write Python. It already knows. It no longer needs to be reminded to run tests. The hooks do it. It no longer needs to be asked to document what it did. The session end protocol writes `progress.md` automatically.

What remains is the actual work.

The agent designs systems before building them. It works one feature at a time. It writes tests before implementation. It fixes root causes rather than patching symptoms. It leaves the codebase clean at the end of every session.

These are not aspirational qualities. They are encoded constraints.

*Good tooling does not make you more disciplined. It makes discipline the path of least resistance.*
