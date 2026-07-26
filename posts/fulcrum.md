---
date: 2026-02-08 02:00
type: project
emoji: ⚖️
image: /static/images/play-board.png
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
social_image: /static/images/play-board.png
---

[Fulcrum](https://ernster.dev/fulcrum/) is a local, deterministic scoring engine for organisational structure, built on the Decision Architecture model.

# Organisational Theory You Can Run

Organisational theory has a recurring weakness: it cannot be run. Claims arrive in prose, illustrated by anecdote and defended by seniority. A debate about structure becomes a narrative contest in which the most senior voice wins; a reorganisation then gets tested on real people because there is nowhere else to test it first.

Fulcrum exists because that is the wrong place to find out.

It is not a survey tool. It is not a maturity model. It is not a dashboard of feelings. Fulcrum models an organisation the way the books describe one, scores its structural health from 0 to 100 and values every legal move from blunder to great.

If the score offends you, that is useful information.

The board above is a game in progress: 59 people across 8 teams, four moves played, structural health sitting at 38.9 because an approval layer landed earlier in the line. The strongest repairs on offer are already priced and ranked, delegating authority to the gate at plus 23.2 and collapsing the gate entirely at plus 20.8, both classified great.

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

## Model the organisation you actually have

Real organisations are not clean trees, so the model refuses to pretend they are.

![Fulcrum's organisation editor: the authority claims table sits beside the dependency list, with an approval gate feeding Team Alpha on a delay of 3](/static/images/model-org.png)

*The editor: claims and dependencies side by side, 59 people across 8 teams.*

Beyond teams, domains and dependencies with propagation delays, the editor carries an authority claims table: matrix management, dual reporting and plain contested ownership, each claim naming who else believes they hold the decision. Contested authority is priced, not ignored. The moves that touch it are priced too: resolve the claim, downgrade it or impose a matrix overlay across the organisation, which the model treats as a standing blunder in the same class as an approval layer.

*If two people both think they own a decision, the score already knows.*

## The numbers betray intuition

The fastest way to understand Fulcrum is to watch it disagree with a confident prediction.

Scale exposes structure. Model the same archetypes at increasing size and the typical organisation collapses from 75.6 to 14.8 while a well-designed one degrades gently from 98.7 to 66.4. Both decline, because the constraints are real and no design abolishes them. Only one of them falls off a cliff. Scale did not amplify the structure. It exposed it.

Moves are asymmetric. On the enterprise archetype the single available approval-layer move scores minus 9.40, while the best good move on the same board is worth plus 6.85. One blunder outweighs the best repair. This is not rhetoric about "process debt"; it is the model pricing a bad move at more damage than the best good move is worth improvement.

*There is no argument to win. The board settled it.*

## The guide plans every level at once

Ask the guide for a way out and it does not hand you one move. It plans the whole organisation.

![Fulcrum's guide: a tree of composing leaf lines on the left, the selected line's move-by-move plan on the right, headlined 38.9 to 80.1](/static/images/play-guide1.png)

*The guide on the board above: playing every composing leaf line takes 38.9 to 80.1.*

Every leaf of the organisation gets its own line, priced in org points so the numbers compose honestly: teams directly at the top level are worth plus 21.9, teams in one small group plus 4.6; the headline is the sum of what is actually playable rather than a promise. Aggregate rows are views, not extra value to double count. A line that would do net harm is flagged and left out of the total.

*No single move fixes an organisation. The guide never claims one will.*

## Structural value lives at the leaves

The most counter-intuitive result is where the value hides.

In a generated organisation of over 1,700 teams, the best whole-organisation move is worth plus 0.024. The same generator's median best local move, played at a single leaf, is worth plus 9.7 in its own frame, roughly four hundred times as much. Repairing leaf by leaf takes the global score from 0.2 to 49.3 in four rounds.

The summit cannot see the moves that matter. That is not a failure of vision; it is geometry. Which is exactly why authority has to sit where the small repairs are visible. It is also exactly the kind of claim that reads as opinion in prose and as arithmetic on the board.

The guide makes the geometry visible. Select a single leaf line and it opens in its own frame:

![A single leaf line opened in the guide: worth plus 4.6 org points to the whole organisation, it runs 50.3 to 97.6 on its own scale](/static/images/play-guide2.png)

*One leaf line: plus 4.6 org points in the organisation's frame, 50.3 to 97.6 in its own.*

In the organisation's frame this line is worth plus 4.6 points. On its own scale it is a transformation, 50.3 to 97.6, achieved with two moves on one team. Both numbers are true at once. That is the whole leaf-value result in a single screenshot: small from the summit, decisive where it lands.

## The session is a record

A structural argument is only settled if you can show your working afterwards.

Fulcrum keeps the whole line: every move survives a restart, undo walks back across runs and the report separates what was played in earlier runs from what was played in this one. The plan exports straight to your Downloads as a standalone HTML report with a re-importable JSON sibling, so the analysis can leave the machine without losing the model.

Here is [a sample exported plan](/static/html/fulcrum-presentation.html) from the game on the board above: before and after maps, every recommendation grouped by the domain that holds the authority to play it and the approval-layer blunder sitting in the middle of the line, priced at what it cost.

*The report is not a summary. It is the whole line, priced move by move.*

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
