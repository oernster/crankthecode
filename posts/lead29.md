---
title: Decision Architecture in code
one_liner: When ideas about structure move from essays into working systems
date: 2026-03-15 04:30
emoji: 🎙️
tags:
  - cat:Leadership
  - layer:architecture
  - decision-architecture
  - systems
  - software-design
  - authority
  - structure
---

# From Idea to System

Over the past year this site has explored a single recurring theme.

Structure determines outcomes.

Several essays examined the concept from an organisational perspective. Decision latency, authority alignment and structural failure modes were discussed in abstract terms.

Eventually those ideas were consolidated into the *Decision Architecture* ebook.

Theory is useful.

Implementation is more interesting.

Recently those same principles were applied in a different domain.

*Software.*

## The original premise

Decision Architecture begins with a simple observation.

Organisations rarely fail because individuals lack skill. They fail because the system cannot decide clearly or early enough.

Authority becomes ambiguous. Responsibility fragments. Decisions escalate unnecessarily. Coordination cost rises.

Delivery slows long before anyone understands why.

The failure appears human.

The cause is structural.

*Systems behave according to their decision surfaces.*

## Software suffers the same problem

Codebases experience remarkably similar failure modes.

Responsibilities blur. Modules reach across boundaries. Construction happens in unexpected places. Hidden dependencies accumulate.

The system continues to run yet its behaviour becomes increasingly fragile.

Small changes trigger large side effects. Refactors stall. Engineers avoid touching unfamiliar areas.

Again the failure appears human.

The cause is structural.

*Software systems also have decision architecture.*

## The experiment

NarrateX (narratex.co.uk) was built partly as a practical exercise.

The goal was not simply to create an ebook reader with speech synthesis. The goal was to construct the system in a way that reflects the same structural principles discussed in these essays.

Authority boundaries were defined explicitly.

Domain logic was isolated. Services orchestrate behaviour without constructing dependencies. Infrastructure handles IO. The user interface consumes services but does not assemble them.

Bootstrap is the only place where the object graph is composed.

Each layer has authority over a specific class of decision.

Each layer refuses the rest.

*Decision surfaces exist in code just as they do in organisations.*

## Authority boundaries in software

In a well structured system certain decisions belong to specific layers.

The domain decides rules. Services decide orchestration. Infrastructure decides implementation details. The UI decides presentation.

None of these layers should quietly absorb the responsibilities of another.

When boundaries hold, the system behaves predictably. When they collapse, complexity multiplies.

This dynamic is identical to organisational systems.

Teams function well when authority aligns with responsibility. They degrade when decisions must escalate unnecessarily or occur in the wrong place.

*Architecture is simply decision allocation expressed in code.*

## Structural enforcement

The most important property of this approach is enforcement.

Architecture that exists only in diagrams eventually drifts. Code written under pressure will take the shortest available path.

NarrateX therefore enforces structure through tests.

Hidden instantiation is disallowed in protected layers. Dependency construction is restricted to bootstrap. Architectural violations fail immediately during testing.

The system therefore protects its own design.

*Constraints are the only reliable guardians of architecture.*

## A useful symmetry

The same principles appear in two very different environments.

Organisations require clear authority boundaries so that decisions occur near information. Software systems require clear module boundaries so that behaviour remains predictable.

Both degrade when responsibility becomes ambiguous.

Both benefit from explicit structure.

Both accumulate coordination cost when boundaries collapse.

This symmetry is not accidental.

Software systems are themselves organisational artefacts.

*They reflect the way their creators think about structure.*

## Why this matters

Ideas about decision architecture can easily remain theoretical.

NarrateX demonstrates that the same thinking can shape real systems.

The result is not merely a functioning application. It is a small example of structural design applied deliberately.

Concept becomes essay.

Essay becomes book.

Book becomes working software.

*Ideas are most convincing when they survive contact with implementation.*

## Closing observation

Decision Architecture is often discussed in terms of organisations and leadership.

Its underlying principle is simpler.

Structure determines behaviour.

That principle applies equally to teams, institutions and code.

*NarrateX exists as a quiet illustration of that idea in action.*