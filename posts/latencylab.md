---
date: 2026-02-07 16:30
emoji: ⏱️
one_liner: A small tool was built so arguments about performance could finally be
  settled by something impolite called reality.
tags:
- cat:Tools
- latency
- simulation
- python
- engineering
title: LatencyLab Or How I Learned to Stop Guessing and Start Modelling
---

# A Small Tool for Uncomfortable Performance Truths
[LatencyLab on github](https://github.com/oernster/latencylab)

Latency discussions are usually confident. They are also usually wrong.

Most systems do not feel slow because a function is slow. They feel slow because work queues politely wait their turn, because progress updates crowd out the thing the user actually wanted, or because someone decided that showing effort was more important than finishing.

This is difficult to reason about by inspection. It is even harder to reason about while reading code that has opinions about threads, signals, callbacks and optimism.

So I stopped trying.

LatencyLab exists because I wanted a way to describe what happens between a user click and something visible changing on screen without lying to myself about why it felt bad.

I have more plans for this project but they are still in the design phase.  I'll likely report such on in the blog section of my crankthecode site.

*-Not faster. Not optimised. Explained.*

## The Problem With Measuring Things That Haven’t Happened Yet

Profilers are excellent. They are also useless at design time.

By the time you are profiling you have already made several irreversible decisions, about concurrency, about feedback, about how much work the UI thread is expected to absorb while smiling politely.

LatencyLab deliberately does not attach to running code. It does not trace anything live. It does not measure reality.

Instead it models intent.

You describe tasks, you describe queues, you describe when events happen and when they do not. You assign durations that feel roughly honest and distributions that admit long tails because reality always has one.

Then you run the model ten thousand times and ask a rude question.

*-Why did the user wait.*

## A Single Click Is More Than It Looks

The initial model was deliberately small. One click in Stellody. Music Discovery. Playlist Generation.

The user clicks a button. That much is obvious.

What follows is not.

Labels update. An ETA text shifts optimistically. Emojis spin with enthusiasm. Logs scroll if the user has asked to see them. Meanwhile background work happens somewhere else and progress signals are fired with the best intentions.

All of that is UI work. All of it competes for a single thread. None of it is free.

LatencyLab models that with one task. One brutally honest task called update_progress_feedback.

That is enough.

*-The point is not how pretty the progress is. The point is that it happens often and sometimes at the wrong time.*

## Delays Are Not Bugs They Are Decisions

One of the first things LatencyLab learned to make visible was delay.

Not slowness. Delay.

Debounce windows. Backoff timers. Artificial pacing introduced so things feel smoother while quietly extending the critical path.

In LatencyLab delays are explicit. They appear as synthetic nodes in traces. They show up in the critical path when they dominate. They are no longer hiding inside timestamps pretending to be inevitable.

*-This is uncomfortable and that is the idea.*

## Versioning Without Regret

The second uncomfortable thing was schema migration.

Models change. Interpretations change. People forget what they meant six months ago.

So the model schema version is explicit and separate from the application version. The tool version can move. The meaning of the model does not drift silently.

Legacy behaviour is frozen and kept as an oracle. Not because it is elegant but because confidence matters more than tidiness.

*-Git history is not an oracle. Executable tests are.*

## Determinism Is Not Optional

Randomness is useful. Undisciplined randomness is not.

Every run in LatencyLab is seeded. Legacy behaviour remains reproducible. Migration tests use fixed durations so equality can be asserted without arguments about probability distributions and vibes.

When the numbers change it is because something meaningful changed and not because entropy felt like it.

*-This is not clever. It is calm.*

## The Outcome Nobody Notices

After modelling the Music Discovery flow something boring happened.

The dominant delays were not where intuition said they would be. UI progress updates were crowding the queue. The final render was waiting politely behind enthusiasm.

Reducing the frequency of feedback shortened the critical path without speeding up any background work.

Nothing became faster. Everything felt faster.

*-Which is the correct outcome.*

## Why This Exists At All

LatencyLab is not a performance tool. It is a thinking tool.

It exists to answer questions before they become commits and to make latency arguments dull because the graph already settled it.

If it does its job properly nobody will argue about why something feels slow again.

*-Which is what I'm after.*