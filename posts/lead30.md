---
title: AI does not remove the need for software engineers
one_liner: Code generation accelerates implementation. Architecture still requires expertise.
date: 2026-03-15 06:00
emoji: 🧠
tags:
  - cat:Leadership
  - layer:structural-design
  - ai
  - software-engineering
  - architecture
  - systems
  - decision-making
---

# AI Did Not Remove the Hard Part

AI coding tools have improved dramatically.

Editors can generate large volumes of code quickly. They understand common libraries, recognise patterns and follow instructions with impressive speed.

It is tempting to conclude that software development itself has been automated.

That conclusion misunderstands where the real difficulty lies.

Writing code has never been the hardest part of building software.

*Designing the system always was.*

## The difference between code and structure

Code expresses behaviour.

Architecture decides where behaviour belongs.

Which component owns a decision. Which layer may depend on another. Where construction occurs. What must never happen.

These choices determine whether software remains coherent as it grows.

AI models can generate implementation rapidly.

They do not yet possess durable understanding of a system’s structural intent.

That responsibility still belongs to the engineer guiding the work.

*Structure must exist before generation can safely begin.*

## What actually goes wrong

When people claim AI generated software is unreliable, the real problem is usually something else.

The person driving the tool lacks architectural discipline.

Without an explicit design, prompts produce local solutions. Each response optimises for the immediate instruction. Boundaries drift quietly as new features appear.

The system grows quickly yet its structure becomes increasingly ambiguous.

Nothing is obviously broken.

Everything simply becomes harder to change.

This failure mode predates AI by decades.

AI merely accelerates it.

*Speed amplifies whatever structure already exists.*

## Why expertise still matters

A capable software engineer approaches a problem differently.

Before writing code the engineer decides how the system should be shaped.

Layers are defined. Responsibilities are separated. Dependency direction is constrained. Construction points are limited deliberately.

Once this structure exists AI becomes extremely useful.

The model can generate implementations, scaffolding and tests rapidly inside a design that already protects coherence.

The engineer remains responsible for architecture.

The AI becomes an implementation accelerator.

*Tools are powerful when guided by expertise.*

## The difference in results

Two developers can use the same AI tool and produce completely different outcomes.

One writes prompts until the application appears to work. Architecture emerges accidentally if it emerges at all.

The other defines the system first. AI is used to fill in the implementation details within those boundaries.

The first approach produces working code quickly.

The second produces software that survives change.

The difference is not the tool.

It is the engineer.

*Capability comes from judgement not generation.*

## A practical example

NarrateX, a small open source ebook reader built recently, illustrates this difference clearly.

The application uses modern machine voice synthesis to read books aloud. That functionality could easily have been generated through a sequence of prompts.

Instead the architecture was defined first.

Domain logic exists independently from orchestration. Infrastructure adapters isolate IO. The UI consumes services but does not construct them. Bootstrap remains the only place where the object graph is assembled.

Tests enforce those boundaries continuously.

AI tools were useful during implementation.

The structure existed before the first line was generated.

*Architecture makes generation safe.*

## What AI actually changes

AI has changed the economics of implementation.

Tasks that once required hours of typing can now be produced in seconds. Boilerplate disappears. Test scaffolding appears instantly. Documentation can be generated alongside code.

This acceleration is genuinely valuable.

However it does not eliminate the need for expertise.

If anything it increases the importance of architectural judgement.

When implementation becomes cheap the quality of the design becomes the limiting factor.

*The faster we can build software the more important structure becomes.*

## Closing observation

AI tools are not replacing software engineers.

They are amplifying them.

An experienced engineer with good architectural discipline can produce systems faster than ever before. An inexperienced developer can generate large volumes of fragile code just as quickly.

The technology did not change the nature of software engineering.

It only increased the consequences of getting the structure wrong.

*AI accelerates implementation. Engineers remain responsible for the system.*