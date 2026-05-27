---

date: 2026-05-26 09:30
type: project
emoji: 🛠️
one_liner: A small command correction tool built to explore Go, terminal ergonomics and the gap between human intent and shell precision.
blurb: Terminal commands fixer
tags:
- cat:Tools
- golang
- terminal
- cli
- developer-tools
- automation
title: Command Fixer

---

# A Small Tool for When Humans Type Faster Than They Think

[Command Fixer](https://github.com/oernster/CommandFixer)

Terminals are precise. Humans are not.

Most command line mistakes are not complicated failures of understanding. They are tiny mismatches between intent and syntax: a forgotten flag, a transposed command, a mistyped binary or a command recalled from memory slightly incorrectly after months away from a tool.

The shell does not care.

Command Fixer exists because the terminal remains structurally hostile to minor human error even when the intended action is obvious.

This was my first serious experimentation with Go. The project started less as an attempt to build a sophisticated shell assistant and more as an excuse to explore Go’s concurrency model, compilation model and approach to building small distributable tooling.

The result became a lightweight command correction utility designed around fast feedback, deterministic behaviour and explicit correction logic rather than opaque AI-style guessing.

If the tool can understand what you meant quickly enough that the interruption disappears, the terminal becomes calmer to use.

*That matters more than novelty.*

## Problem → Solution → Impact

**Problem**
Command line tooling assumes precision under conditions where humans are usually operating from memory, context switching rapidly or working under time pressure. Small mistakes break flow disproportionately. Most shells simply fail and force the user to manually reconstruct intent.

**Solution**
Command Fixer intercepts failed commands, analyses likely intent and proposes corrected alternatives using explicit matching and structured correction logic. The system focuses on lightweight deterministic behaviour rather than heavyweight runtime inference.

The tool is designed to operate fast enough that command correction feels like continuation rather than interruption.

**Impact**
Minor terminal failures stopped becoming cognitive interruptions. Instead of retyping commands repeatedly, the shell became capable of acknowledging probable intent and recovering quickly without introducing unpredictable behaviour.

*This is not about making terminals intelligent. It is about reducing unnecessary friction.*

## Go as a systems language, not a fashion statement

This project existed partly because I wanted to understand Go properly rather than form opinions about it from a distance.

Go’s appeal became obvious very quickly.

Compilation is fast. Distribution is simple. Concurrency primitives are direct. Building small standalone tooling feels operationally lightweight in a way many ecosystems do not. The language encourages shipping utilities instead of endlessly architecting them.

That simplicity comes with tradeoffs. The language can feel intentionally minimal to the point of stubbornness and abstraction patterns require discipline because the language rarely protects you from yourself.

For this category of tool, though, the constraints were useful.

Command Fixer benefits from predictability more than cleverness.

*The tooling experience around Go is arguably more important than the language itself.*

## Deterministic correction over probabilistic theatre

Many modern tooling experiences drift toward opaque inference systems that attempt to appear intelligent while making behaviour harder to reason about.

That was deliberately avoided here.

Command Fixer is intentionally explicit about why a correction was suggested. Matching behaviour is deterministic. Candidate generation is constrained. Corrections are derived from observable command structure rather than probabilistic language modelling.

This matters because shell commands are dangerous precisely when systems become overconfident.

A correction utility should behave conservatively. Predictability builds trust faster than cleverness.

*The terminal is not the place for hallucinated confidence.*

## Fast enough to disappear

Developer tooling succeeds when it stops drawing attention to itself.

The correction pipeline was intentionally kept lightweight so interaction latency stayed low enough that the feedback loop remained conversational rather than disruptive. If the user spends longer waiting for correction logic than retyping the command manually, the tool has already failed.

This shaped most implementation decisions.

The project prioritised:

* Fast startup
* Minimal runtime dependencies
* Simple distribution
* Low overhead correction logic
* Clear correction output
* Predictable execution behaviour

The goal was not feature accumulation.
The goal was preserving flow.

## A tool shaped by terminal reality

Real terminal usage is messy.

People paste commands from outdated documentation. They partially remember flags. They context switch between ecosystems with incompatible conventions. Muscle memory leaks between tools. Aliases drift. Package managers change behaviour between versions.

Most command line environments pretend this is user failure.

It is not.

Humans operate through approximation constantly and good tooling acknowledges that reality instead of punishing it. Command Fixer exists in that gap between human intent and machine strictness.

*Small friction compounds surprisingly aggressively over time.*

## What this project actually taught me about Go

The interesting part was not syntax.

The interesting part was how quickly Go encourages operational thinking. The language and tooling push you toward building complete executable systems early rather than endlessly refining architecture in abstraction.

That changes behaviour.

You start optimising for distribution, startup time, observability and simplicity because the ecosystem makes those concerns feel close instead of theoretical.

For small infrastructure and tooling projects, that mindset is valuable.

Command Fixer became less interesting as a command correction tool and more interesting as an exercise in understanding how language ecosystems shape engineering behaviour.

*Languages influence architecture long before architecture becomes visible.*
