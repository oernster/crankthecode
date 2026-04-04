---
title: What extensive experience across organisations teaches you
one_liner: Decades of software work reveal the same structural failure modes again and again
date: 2026-03-15 10:00
emoji: 🧩
tags:
  - cat:Leadership
  - layer:structural-design
  - software-engineering
  - systems
  - architecture
  - experience
  - organisational-design
---

# What Long Experience Eventually Reveals

People often assume that long experience in software engineering means memorising technologies.

New languages, new frameworks, new tools.

Those things matter far less than most people think.

The real lesson comes from watching systems fail repeatedly in similar ways across different companies, industries and teams.

After enough time the pattern becomes difficult to ignore.

*Structure determines behaviour.*

## The same problems appear everywhere

Across nearly three decades of software work I have encountered the same failure modes repeatedly.

Different technology stacks. Different industries. Different company sizes.

The details change.

The structure rarely does.

Responsibilities blur between layers. Architecture exists mostly in conversation. Decisions drift upward because no one clearly owns them. Dependencies accumulate quietly until change becomes dangerous.

None of these problems appear dramatic at first.

The system still runs. Features still ship.

Over time however something subtle begins to happen.

*The cost of changing the system rises steadily.*

## Failure rarely looks like failure

Most systems do not collapse suddenly.

Instead they become slower to change.

New engineers struggle to understand the boundaries of the codebase. Small modifications trigger unexpected behaviour elsewhere. Architectural discussions repeat every few months because previous decisions were never embedded in the structure.

The organisation interprets this as a delivery problem.

The engineers experience it as friction.

The underlying cause is almost always the same.

The system was never shaped deliberately.

*Without structure entropy becomes the default.*

## What experienced engineers eventually learn

After encountering this pattern often enough, the way you approach software begins to change.

The first instinct is no longer to write code.

The first instinct is to design the shape of the system.

Which decisions belong in the domain. Which components orchestrate behaviour. Where infrastructure interacts with the outside world. Where dependencies must stop.

These boundaries determine how the system evolves long after the initial implementation.

Code can always be rewritten.

Architecture determines whether rewriting is feasible.

*The shape of the system matters more than the speed of the first version.*

## Structure reduces future arguments

Good architecture does something subtle.

It prevents certain conversations from happening repeatedly.

When boundaries are explicit engineers know where decisions belong. When dependencies flow predictably modules cannot quietly entangle themselves. When construction happens in one place the system remains understandable.

The codebase therefore carries part of the organisational discipline itself.

This reduces coordination cost inside the team.

Engineers spend less time negotiating where behaviour should live and more time improving the behaviour itself.

*Structure removes ambiguity before it becomes debate.*

## This thinking appears across my work

Readers of this site will recognise a recurring theme.

Decision Architecture explores similar ideas in organisational systems. Authority alignment reduces decision latency. Clear boundaries prevent escalation from becoming routine.

Software systems follow the same principles.

NarrateX, a recent open source project on this site, was designed deliberately using those constraints. Domain logic is isolated. Services orchestrate without constructing dependencies. Infrastructure remains replaceable. Tests enforce the boundaries continuously.

The result is not merely an application that works.

It is a system that resists structural decay.

*Architecture is the practice of deciding where decisions belong.*

## Why this matters now

Modern tools can generate working code quickly.

AI assistants can implement features faster than any previous generation of developers.

This changes the economics of implementation.

It does not change the importance of structure.

If anything it makes architectural judgement more important. When code becomes cheap the quality of the system design becomes the limiting factor.

The faster we can build software the more dangerous poor structure becomes.

*Acceleration without architecture multiplies entropy.*

## Closing observation

Experience in software engineering does not primarily teach technologies.

Technologies change constantly.

What experience teaches is how systems fail.

Once those patterns become familiar the priorities shift. Writing code becomes secondary to shaping the structure within which that code will live.

The goal is no longer simply to produce working software.

The goal is to create systems that remain understandable, adaptable and coherent long after the first version ships.

*Structure is the missing piece that determines whether software improves or slowly collapses under its own weight.*