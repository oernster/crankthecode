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

The board above is the built-in matrixed enterprise, 6,000 people across 1,076 teams, drilled into a single runtime group: the 45.652 score and every listed move belong to that section, not the summit. The group's lead is contested, drawn violet; the repair this frame wants first is already priced: resolving that ownership to a single claimant rates good at around plus 6 section points, while every delegation on offer rates bad and the realignments sit neutral. Beside the moves, seven signals flag the handoff queue age, the 50% rework rate and the centre's escalation load.

The board shows exactly what the model produced and nothing it did not.

## Problem → System → Outcome

**Problem.** Structural decisions are made on intuition and authority, then paid for slowly. By the time a reorganisation is visibly failing, the boundaries have hardened, the informal network has rebuilt around them and the cost of unwinding it is measured in careers. There is no cheap place to be wrong.

**System.** Fulcrum represents teams, domains, dependencies with propagation delays, authority placement and incentive skew, then scores the structure deterministically and enumerates every legal move with its valuation. There is no randomness in the scoring. Two people with the same model get the same number.

**Outcome.** A structure argument becomes an examinable model: point at the board, read the score, play the move and watch the number change before anyone touches an org chart.

*This is where you find the structural problem before it becomes political.*

## Deterministic or it is worthless

A tool that scores organisations has exactly one job it cannot fail at: giving the same answer twice.

Every score is a pure function of the model. Change the model and the number moves; leave it alone and it does not. This is the whole point. The moment a structural score depends on who ran it or when, it becomes another opinion wearing a number; the field already has enough of those.

The rule holds under parallelism too. On a large organisation the guide plans across every processor core, so an enterprise of thousands plans in seconds; the parallel build matches the single-core one to the last digit. Speed was not allowed to move the number.

*Reproducibility is not a feature here. It is the reason the thing is allowed to exist.*

## Model the organisation you actually have

Real organisations are not clean trees, so the model refuses to pretend they are.

![Fulcrum's organisation editor holding the matrixed enterprise: the tree rolls up 1,076 teams and 6,000 people, with the dependency list and the authority claims table beneath it](/static/images/model-org.png)

*The editor holding the enterprise itself: the tree, dependencies and claims, 1,076 teams and 6,000 people.*

Units nest to any depth with teams as the leaves, every row rolls up its teams and people and dependencies link any two items with their delay in turns. Beyond that, the editor carries an authority claims table: matrix management, dual reporting and plain contested ownership, each claim naming who else believes they hold the decision. In the screenshot it is the programme office's standing claims on other units' leads, the matrix disease made explicit, one row per claim. Contested authority is priced, not ignored. The moves that touch it are priced too: resolve the claim, downgrade it or impose a matrix overlay across the organisation, which the model treats as a standing blunder in the same class as an approval layer. The whole model autosaves and round-trips as JSON; even at a thousand teams the editor opens in a fraction of a second.

*If two people both think they own a decision, the score already knows.*

## The numbers betray intuition

The fastest way to understand Fulcrum is to watch it disagree with a confident prediction.

Scale exposes structure. Model the same archetypes at increasing size and the typical organisation collapses from 75.6 to 14.8 while a well-designed one degrades gently from 98.7 to 66.4. Both decline, because the constraints are real and no design abolishes them. Only one of them falls off a cliff. Scale did not amplify the structure. It exposed it.

Moves are asymmetric. On the enterprise archetype the single available approval-layer move scores minus 9.40, while the best good move on the same board is worth plus 6.85. One blunder outweighs the best repair. This is not rhetoric about "process debt"; it is the model pricing a bad move at more damage than the best good move is worth improvement.

*There is no argument to win. The board settled it.*

## The guide plans every level at once

Ask the guide for a way out and it does not hand you one move. It plans the whole organisation.

![Fulcrum's guide: a tree of composing leaf lines on the left, the selected division's move-by-move plan on the right, the whole organisation climbing 16.255 to 60.096](/static/images/play-guide1.png)

*The guide on the enterprise: playing every composing leaf line takes the whole organisation from 16.255 to 60.096.*

Every level of the organisation gets its own line, priced in org points so the numbers compose honestly. Aggregate rows are views, not extra value to double count: the division on the right climbs 43.747 to 98.340 on its own scale, yet the guide labels that the view from its altitude, because its gains overlap the leaf repairs beneath it and only leaf lines count toward the headline. Three lines that would cost the whole organisation are flagged and kept out of the total, so the climb the tree advertises is one the organisation would actually make. Tick one box and the guide is allowed to grow the organisation too, adding owners beside overloaded executives or splitting a lead's team where the model prices the gap.

*No single move fixes an organisation. The guide never claims one will.*

## Structural value lives at the leaves

The most counter-intuitive result is where the value hides.

In a generated organisation of over 1,700 teams, the best whole-organisation move is worth plus 0.024. The same generator's median best local move, played at a single leaf, is worth plus 9.7 in its own frame, roughly four hundred times as much. Repairing leaf by leaf takes the global score from 0.2 to 49.3 in four rounds.

The summit cannot see the moves that matter. That is not a failure of vision; it is geometry. Which is exactly why authority has to sit where the small repairs are visible. It is also exactly the kind of claim that reads as opinion in prose and as arithmetic on the board.

The guide makes the geometry visible. Select a single leaf line and it opens in its own frame:

![A single leaf line opened in the guide: Search group 2 is worth plus 0.070 org points to the whole organisation and runs 49.141 to 79.104 on its own scale](/static/images/play-guide2.png)

*One leaf line: plus 0.070 org points in the organisation's frame, 49.141 to 79.104 in its own.*

In the organisation's frame this line is worth a fraction of a point. On its own scale it is a thirty-point climb: twelve moves that begin by resolving the programme office's standing claim on the group's lead and finish, with growth allowed, by splitting the lead's team. Both numbers are true at once. That is the whole leaf-value result in a single screenshot: barely visible from the summit, decisive where it lands.

## The session is a record

A structural argument is only settled if you can show your working afterwards.

Fulcrum keeps the whole line: every move survives a restart, undo walks back across runs and the centre of the board is a live move record that replays the position move by move, before and after pictures with each move's targets ringed so the two can never read identical. Beside the score sits a golden provenance button, because every number should account for itself: it opens the working that produced the figure on screen.

The plan exports straight to your Downloads as a standalone HTML report with a re-importable JSON sibling, so the analysis can leave the machine without losing the model. Every exported move that acted inside one unit carries two verdicts: its effect on the whole organisation and its effect within that unit's own frame, so a repair that is good where it lives never vanishes into whole-org neutrality.

Here is [a sample exported plan](/static/html/fulcrum-presentation.html) from the enterprise above: before and after maps, every recommendation grouped by the lead who holds the authority to play it, an approval-layer blunder sitting in the middle of the line priced at what it cost and the same resolve that reads neutral at the summit reading good inside its own group, 45.652 to 51.480.

*The report is not a summary. It is the whole line, priced move by move at both scales.*

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

It runs entirely on your machine. Generate a level, open a built-in example (a healthy small agency up to the matrixed enterprise above), model your own organisation or import one as JSON, then ask the guide for a move-by-move line to a stronger score. No account, no server, no telemetry.

*The first edition of the theory asked to be believed. This is part of what asks it to be rerun.*
