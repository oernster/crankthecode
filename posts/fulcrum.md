---
date: 2026-02-08 02:00
type: project
emoji: ⚖️
image: /static/images/fulcrum-icon.png
thumb_image: /static/images/fulcrum-icon.png
one_liner: The Decision Architecture model made executable, scoring an organisation's structure and valuing every move deterministically.
blurb: Organisational theory you can actually run
tags:
- cat:Decision Architecture Instruments
- decision architecture
- organisational design
- simulation
- python
title: Fulcrum
social_image: /static/images/fulcrum-icon.png
---

[Fulcrum](https://ernster.dev/fulcrum/) is a local, deterministic scoring engine for organisational structure, built on the Decision Architecture model.

# Organisational Theory You Can Run

Organisational theory has a recurring weakness: it cannot be run. Claims arrive in prose, illustrated by anecdote and defended by seniority. A debate about structure becomes a narrative contest in which the most senior voice wins; a reorganisation then gets tested on real people because there is nowhere else to test it first.

Fulcrum exists because that is the wrong place to find out.

It is not a survey tool. It is not a maturity model. It is not a dashboard of feelings. Fulcrum models an organisation the way the books describe one, scores its structural health from 0 to 100 and values every legal move from blunder to great.

If the score offends you, that is useful information.

The board shows exactly what the model produced and nothing it did not.

## Problem → System → Outcome

**Problem.** Structural decisions are made on intuition and authority, then paid for slowly. By the time a reorganisation is visibly failing, the boundaries have hardened, the informal network has rebuilt around them and the cost of unwinding it is measured in careers. There is no cheap place to be wrong.

**System.** Fulcrum represents teams, domains, dependencies with propagation delays, authority placement and incentive skew, then scores the structure deterministically and enumerates every legal move with its valuation. There is no randomness in the scoring. Two people with the same model get the same number.

**Outcome.** A structure argument becomes an examinable model: point at the board, read the score, play the move and watch the number change before anyone touches an org chart.

*This is where you find the structural problem before it becomes political.*

## Deterministic or it is worthless

A tool that scores organisations has exactly one job it cannot fail at: giving the same answer twice.

Every score is a pure function of the model. Change the model and the number moves; leave it alone and it does not. This is the whole point. The moment a structural score depends on who ran it or when, it becomes another opinion wearing a number; the field already has enough of those.

*Reproducibility is not a feature here. It is the reason the thing is allowed to exist.*

## The numbers betray intuition

The fastest way to understand Fulcrum is to watch it disagree with a confident prediction.

Scale exposes structure. Model the same archetypes at increasing size and the typical organisation collapses from 75.6 to 14.8 while a well-designed one degrades gently from 98.7 to 66.4. Both decline, because the constraints are real and no design abolishes them. Only one of them falls off a cliff. Scale did not amplify the structure. It exposed it.

Moves are asymmetric. On the enterprise archetype the single available approval-layer move scores minus 9.40, while the best good move on the same board is worth plus 6.85. One blunder outweighs the best repair. This is not rhetoric about "process debt"; it is the model pricing a bad move at more damage than the best good move is worth improvement.

*There is no argument to win. The board settled it.*

## Structural value lives at the leaves

The most counter-intuitive result is where the value hides.

In a generated organisation of over 1,700 teams, the best whole-organisation move is worth plus 0.024. The same generator's median best local move, played at a single leaf, is worth plus 9.7 in its own frame, roughly four hundred times as much. Repairing leaf by leaf takes the global score from 0.2 to 49.3 in four rounds.

The summit cannot see the moves that matter. That is not a failure of vision; it is geometry. Which is exactly why authority has to sit where the small repairs are visible. It is also exactly the kind of claim that reads as opinion in prose and as arithmetic on the board.

## Falsifiable by design

Fulcrum is built to be proven wrong.

Model a realistic organisation in which adding an approval layer improves its structural health. Model one in which centralising every decision class reduces cycle latency under contention. Either result breaks the framework in a way anyone can inspect and rerun. The evidence standard is not "an organisation once measured this". It is "given a structure with these properties, these consequences follow mechanically, at this magnitude".

*A claim you cannot rerun is not evidence. It is a story with a graph attached.*

## Who this is not for

Fulcrum is not a culture survey and it does not measure morale.

It will not tell you whether people are happy. It does not read sentiment, it does not grade individuals and it does not generate a change-management deck. It scores structure; structure is only the precondition of good decisions, never their substance. A perfectly scored organisation can still pursue the wrong product, swiftly and coherently.

If you want a tool that tells you the reorganisation was a success, this one will decline.

## Built on the series, one of its two instruments

Fulcrum is the Decision Architecture model made executable: one of the two instruments the theory rests on. Its move classifications, blunder through great, come from Decision Architecture: The Move Space; the geometry it scores against is the subject of Relativistic Decision Architecture. Its sibling, [LatencyLab](https://ernster.dev/latencylab/), does the same job for latency: the two exist so the quantitative claims in the books can be rerun rather than believed.

It runs entirely on your machine. Generate a level, model your own organisation or import one as JSON, then ask the guide for a move-by-move line to a stronger score. No account, no server, no telemetry.

*The first edition of the theory asked to be believed. This is part of what asks it to be rerun.*
