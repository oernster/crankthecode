---
blurb: Correspondence chess over your own email, with no network code at all
date: 2026-07-16 11:00
type: project
role: project
emoji: ♟️
image: /static/images/postal-gambit.png
one_liner: A local-first desktop app that keeps your chess games, enforces the rules and turns each move into a ready-to-send email in whatever mail client you already use.
social_image: /static/images/postal-gambit.png
tags:
- cat:Gaming
- python
- pyside6
- chess
- email
- correspondence
- local-first
thumb_image: /static/images/postal-gambit-icon.png
title: Postal Gambit

---

[Postal Gambit](https://ernster.dev/postal-gambit/) is correspondence chess over your own email.

It is a local-first desktop app that keeps your games, enforces the rules and turns each move into a ready-to-send email in whatever mail client you already use.

The defining property is a refusal:

*It never touches the network. Not once. Not ever.*

---

## Problem → System → Outcome

**Problem.** Slow, thoughtful chess with a friend used to work over postcards. Online platforms replaced the ritual with ratings, clocks, engines and accounts, and the quiet version of the game went with them.

**System.** A PySide6 desktop app with python-chess quarantined behind a port: it manages any number of games, enforces every rule including all draw rules and exports each move as a pre-filled email draft or clipboard text carrying a readable preamble, an ASCII board and a delimited PGN block that holds the entire game state.

**Outcome.** Postal chess with modern rigour: moves travel through your own mail client, the opponent needs nothing more than the ability to reply and every game survives in a local file you own.

---

## Why it exists

Correspondence chess is not a worse version of online chess. It is a different game: days per move, one deliberate decision at a time, played against a person rather than a rating pool.

What killed it was friction, not preference. Keeping the board state straight across letters, catching an illegal move, remembering whose turn it is across five games: that is exactly the bookkeeping software is for.

Postal Gambit does the bookkeeping and refuses to do anything else. The transport is your mail client. The opponent's client can be anything.

*The app is the scorekeeper, never the middleman.*

---

## The wire format

Every outbound move is an email built to be read by a human first and a parser second:

* a readable preamble stating the move
* an ASCII board so the position is visible in any client
* a delimited PGN block carrying the entire game state

Because the whole game travels with every message, the format is versioned and self-contained: nothing depends on both players' apps staying in sync. Importing the opponent's reply means pasting the email text or a `.pgn` file; a plain-text reply like `Nf6` imports fine, so the opponent does not even need the app.

Divergence between the imported game and the local record is detected and reported, never silently resolved.

Every outbound email also carries an https link that works in any mail client: a static page bounces it to the installed app with the move prefilled, routed to the running instance when there is one. One click and the move is in.

Invitations, draw offers, draw acceptance and resignation travel over the same format. A game arriving as an invitation is created with the opponent's reply address taken from the message itself, so nothing needs typing.

---

## No machines, structurally

Two design refusals define the app:

**No network code.** There is no in-app sending and there never will be. Export is `mailto:` or the clipboard; import is paste or a file. The app cannot leak, phone home or fail on someone else's server because the capability does not exist.

**No engine.** Postal Gambit ships no analysis, deliberately. Correspondence chess died once already from machines; this is the version where your opponent is a person and the app holds the door against anything else.

The rules engine itself, python-chess, is quarantined behind a port in the architecture, so the domain owns the game and the dependency stays replaceable.

---

## Core behaviour

* Any number of ongoing games: whose move, full history, archive
* Full rules enforcement including all draw rules
* Move export as a pre-filled email draft or clipboard text
* Import by pasted email text, plain-text move or `.pgn` file
* One-click import via the https bounce link
* Invitations, draw offers, acceptance and resignation over the wire format
* Bulk actions across multi-selected games, each with eligibility filtering and confirmation
* A move history panel, with game names carrying the same short id as the email subject
* A full keyboard focus ring everywhere including dialogs
* Dark and light themes, persisted between runs
* One JSON file per game, local, atomic writes

---

## Postal Gambit at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Multiple concurrent games</li>
    <li>Full rules and draw-rule enforcement</li>
    <li>Email draft and clipboard export</li>
    <li>Paste, plain-text and PGN import</li>
    <li>One-click move import link</li>
    <li>Divergence detection, never silent</li>
    <li>Invitations, draws and resignations</li>
    <li>Bulk actions with confirmation</li>
    <li>Full keyboard navigation</li>
    <li>Dark and light themes</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technology</h3>
  <ul>
    <li>Python 3.13, PySide6 widgets</li>
    <li>python-chess behind a port</li>
    <li>One JSON file per game, atomic writes</li>
    <li>No network code at all</li>
    <li>195 tests, 100% coverage outside the UI</li>
    <li>Nuitka installer, Flatpak, DMG</li>
    <li>GPL-3.0, open source</li>
  </ul>
</div>

</div>

---

## What this taught me

Constraints are features when they are structural.

"Local-first" is usually a caching strategy. Here it is absolute: the absence of network code is the product's strongest promise and it cannot be broken by a bug, a toggle or a future feature, because the capability was never built.

The wire format taught the same lesson from the other side. Carrying the entire game in every message looks redundant until you remember the medium: email is unordered, lossy and occasionally read by a human on a phone. A self-contained message survives all of that.

*The strongest guarantees are the ones the code cannot violate.*
