---
title: "Stellody v5.0.0 – Playlist Purgatory, Parallel Processing & Progress Bar Penance"
date: "2026-01-27 00:00"
tags: ["blog", "stellody", "release", "playlist", "refactor", "bugfix", "music", "qt", "multithreading"]
one_liner: "v5.0.0 restores real playlists adds thread safe performance gains and ships with a UI that survives heavy clicking."
emoji: "👹"
---

# Stellody v5.0.0 is live and critically now generates real functional playlists again.

The UI was already polished. The codebase had been refactored. The installers were clean and predictable.  
Unfortunately the one thing the application actually exists to do had quietly fallen apart.

Playlists were broken. Completely.

That problem is now fixed properly.

---

## 👺 The Playlist Crisis Resolved

Somewhere during the v4.0.0 evolution the playlist track pool logic degraded beyond recognition. Artist pools shrank too aggressively, sub genres filtered themselves into oblivion and the system began producing either empty playlists, or meaningless genre dumps like “Pop,” “Rock,” “Pop #2,” “Pop #3,” until the output stopped making sense entirely.

The fix required more than patching symptoms. Pool sizing was rebuilt so generation produces viable playlist lengths again. Sub genre fallback logic now applies sensible heuristics rather than panicking. Naming follows a strict ordered sequence starting at `#1` so numbering is predictable and stable.

Under the hood this meant regression testing against v3.0.0 cherry picking known good commits removing broken tags and replaying history forward into main.

*-I did not just fix bugs. I rewrote history so the bugs never existed in the first place.*

---

## 🧵 Threading Speed and Global Sanity

Once playlists were reliable again performance became the next constraint.

Worker threads now run in parallel using Python’s `ThreadPoolExecutor` with a global rate limiter enforcing sane access to Spotify and MusicBrainz. The result is faster startup quicker generation and a UI that remains responsive throughout discovery.

Just as importantly the application no longer flirts with accidental API bans.

*-The speed boost is welcome. The screaming in my logs is gone. My soul is slightly cleaner.*

---

## 🔄 UI Behaviour Fixes

A collection of smaller interaction issues were addressed during this release.

The maximise button was disabled entirely because it consistently made everything worse. The console toggle now correctly reflects internal state across sessions instead of lying. Pressing stop no longer terminates the application but simply stops the active run as intended.

The Stellody title and 🎵 emoji now render correctly in both light and dark modes. The Genre Focus dialog was reworked into a two column layout that scrolls cleanly and fits on smaller laptops without feeling cramped.

*-One bug made the stop button behave like self destruct. Another forgot what it did almost immediately. Both are gone.*

---

## 🧹 Logging and Console Output

Logging was tightened considerably.

MusicBrainz and Spotify hash identifiers are now scrubbed from visible logs. Request IDs UUIDs and other low level noise are hidden unless debugging is explicitly enabled. Console output remains readable useful and safe when toggled on.

*-Nobody needs to see “REQID: 93819AD9-BORK-420”. Least of all me.*

---

## Summary

Stellody v5.0.0 brings the application back to where it should have been all along.  
Playlists are real again. Performance is faster without being reckless. The UI behaves itself even when pushed.

*-This release looked minor from the outside. Internally it was a full exorcism.*

[Check it out at stellody.com](https://www.stellody.com)
