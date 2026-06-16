---
blurb: A local-first Elite Dangerous session debrief, traced to the journal itself
date: 2026-06-16 16:40
type: project
role: project
image: /static/images/o7debrief.png
one_liner: A Windows tray app that turns your Elite Dangerous Player Journal into a shareable session debrief, with every figure traced to a real journal entry.
social_image: /static/images/o7debrief.png
tags:
- cat:Gaming
- elite dangerous
- space sim
- session report
- journal
- pyside6
- python
- local-first
thumb_image: /static/images/o7debrief-icon.png
title: o7 Debrief

---

[o7 Debrief](https://oernster.github.io/o7Debrief/) turns the most honest record Elite Dangerous keeps, your Player Journal, into a debrief you can actually read.

The game writes down everything you do and then says almost nothing about it. A session ends and the achievement evaporates: the jumps, the scans, the bounties, the long climb of a rank, all logged and none of it summarised. o7 Debrief reads that log and hands the session back to you as a single, verifiable account.

Not a leaderboard. Not an estimate. What actually happened, traced line by line to the journal that recorded it.

---

## Problem → System → Outcome

**Problem.** Elite Dangerous keeps a meticulous Player Journal and then leaves it there. An evening of exploration, combat, trade, mining, missions and exobiology is scattered across thousands of raw events, so the thing you just spent hours doing has no summary you can read, keep or share.

**System.** A local-first Windows app that lives in the system tray, reads the journal the game already writes and reduces a session into one self-contained debrief: every credit, jump and scan resolved to the real event behind it, rendered as a report you can open in any browser or paste into Discord.

**Outcome.** When you close the game you get a clean account of the session you just flew, accurate enough to trust and tidy enough to share. I built it to see what my own commander actually did out there.

---

## Why it exists

A journal is not a report.

The game records faithfully and presents nothing, so the work disappears into a log file: real, complete and unreadable. You finish a three-hour exploration run and the only evidence is ten thousand lines of JSON.

o7 Debrief models a session the way you remember it, by what you were doing, instead of the way the game stores it, as a flat stream of events. The result is not a tidier log.

*It is a faithful account of a session, made from the one source that cannot flatter you: the journal itself.*

---

## The decision-architecture lens

I write about decision architecture: the idea that a system behaves according to how its decisions are structured, where they resolve and what authority stands behind them. A debrief is a small version of the same problem. Every figure in it is a claim; every claim needs a source.

So I built o7 Debrief around provenance rather than presentation:

- **nothing is estimated, inferred or padded.** Every number traces back to a real journal entry, so no figure enters the report without authority behind it
- the **debrief is the termination point**: a session's scattered events resolve into one account, the single place the question *"what did this amount to?"* is answered
- the **live tray watcher and the cold one-shot** are two paths to the same reducer, so a debrief written as you shut down and one written long after the fact are the same answer, not two
- **honest rank reporting** admits what the source cannot yet know: tier-ups show at once, the fractional percentages settle on the next launch, because the journal only records that progress at startup

*A report you can trust is one where every claim can be traced back to where it came from.*

---

## What it does

**A debrief, two ways.** Report your last session or your whole history to date. Leave it running in the tray and it writes the debrief for you when you close the game. Or run it cold, after the fact, when you never had it open at all. Both paths drive the same underlying use case, so the answer never depends on how you asked.

**Real numbers only.** Every credit, jump and scan maps to a real entry in your journal. Exploration, combat, trade, mining, missions and exobiology each get their own panel, with a session log you can tab through by activity and your rank progress across the run. The figures are verifiable because they are not computed from a model; they are read from what happened.

**A report worth keeping or sharing.** Each debrief is one self-contained file that opens in any browser, with a plain-text version ready to paste onto Discord or Reddit. The header names your commander, your ship type and your ship's name from the same session, so the report is unmistakably yours.

**Your back catalogue, browsable.** Recent debriefs lists everything you have produced, newest first; it pages through the lot, so a long history of sessions never gets in the way of the latest one.

**Local-first, no exceptions.** The journal never leaves your machine. No cloud, no account, no telemetry and no administrator rights to install. Your commander's record is yours; the app only reads it and hands you back a summary.

---

## I built it for my own commander

This is a tool I wanted to exist. o7 Debrief is not a tech demo I shipped and forgot; it is the thing I open to see what a session actually came to. The activities it tracks are the ones I fly. The honesty constraint, nothing estimated, inferred or padded, is there because a debrief that flatters you is worth less than no debrief at all. The surest way to keep a summary honest is to want it to be true about your own sessions.

---

## What it taught me

A summary is only as trustworthy as its provenance.

It would have been easy to make the report richer by estimating: filling gaps, inferring intent, rounding a number into a tidier story. Every one of those would have made the debrief prettier and less true. The discipline that made it useful was the opposite one: refuse to show any figure that cannot be traced back to the journal.

That is the whole design in a sentence. o7 Debrief is not trying to impress you with what you did; it is trying to tell you the truth about it, which turns out to be the more impressive thing:

*What did this session actually amount to? And can I prove it?*

---

## o7 Debrief at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Last-session and full-history debriefs</li>
    <li>Automatic debrief on game shutdown</li>
    <li>Cold, after-the-fact generation</li>
    <li>Every figure traced to a real journal entry</li>
    <li>Exploration, combat, trade, mining, missions, exobiology and more</li>
    <li>Tabbed per-activity session log</li>
    <li>Rank progress across the session</li>
    <li>Self-contained HTML report plus Markdown</li>
    <li>Commander and ship named in the header</li>
    <li>Browsable, paged recent-debrief history</li>
    <li>Local-first: no cloud, account or telemetry</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Built with</h3>
  <ul>
    <li>Python 3.13</li>
    <li>PySide6 system-tray app</li>
    <li>Local Player Journal, read-only</li>
    <li>HTML and Markdown reports</li>
    <li>Windows 10 and 11</li>
    <li>Dark theme; open source</li>
  </ul>
</div>

</div>

---

The value is not that o7 Debrief reads your journal.

*The value is that it turns a faithful but unreadable log into an account you can trust, keep and share, with every figure tracing back to where it came from.*
