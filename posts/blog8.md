---
title: "👹 Stellody v5.0.0 – Playlist Purgatory, Parallel Processing & Progress Bar Penance"
date: "2026-01-27 00:00"
tags: ["blog", "stellody", "release", "playlist", "refactor", "bugfix", "music", "qt", "multithreading"]
one_liner: "v5.0.0 brings actual working playlists, thread-safe speed-ups and a UI that doesn’t break from being clicked too hard."
---
# **Stellody v5.0.0** is live and critically, now generates real, functional playlists again.

Yes, the UI was beautiful before. The codebase, refactored. The installers, pristine.  
But the playlists? The actual core purpose of the app?  
Broken. Absolutely borked.

---

## 👺 The Playlist Crisis (Resolved)

Somewhere deep in the v4.0.0+ evolution, the playlist track pool logic degraded into oblivion. The app began shuffling artists into tiny subgenre pools, filtering out too many matches and producing *either* no playlists *or* large genre-dump lists like “Pop”, “Rock”, “Pop #2”, “Pop #3”... until *nothing* made sense.

That’s been fixed. Now:

- Pools are sized more accurately.
- Track generation ensures minimum viable playlist lengths.
- Sub-genre fallbacks use smarter heuristics.
- Playlist naming follows consistent, ordered logic (starting at `#1`, not `#4`).
- “Pop #10” no longer appears before “Pop #2”.

This work included multiple regression tests, a rebaseline back to v3.0.0, cherry-picking stable commits forward, deleting broken tags and replaying history into the main branch.

> I didn't just fix bugs. I rewrote history so the bugs never existed in the first place.

---

## 🧵 Threading, Speed and Global Sanity

To keep things fast but safe:

- Worker threads now run in parallel (using Python’s `ThreadPoolExecutor`),  
- A **global rate limiter** prevents hammering the Spotify or MusicBrainz APIs.
- UI remains responsive throughout discovery and generation.

This means faster startup, quicker playlist generationand no accidental bans.

> The speed boost is nice. The screaming in my logs is gone. My soul is... slightly cleaner.

---

## 🔄 UI Behaviour Fixes

Plenty of small, vital updates:

| Fix | Outcome |
|-----|---------|
| Maximise disabled | The maximise button now does nothing (because it made everything worse). |
| Console toggle sync | Console button now actually reflects the internal state between sessions. |
| Stop button | Pressing stop no longer kills the app; it just, well, stops. |
| Title text styling | The Stellody title and 🎵 emoji now render in proper colours (mauve/dark mode, purple/light). |
| Genre Focus dialog | Now in two columns, scrolls if too tall and fits on 13” laptops properly. |

> One bug made the stop button act like “self-destruct.” Another forgot what it did five seconds ago. Fixed.

---

## 🧹 Logging & Console Output

- MusicBrainz and Spotify hash identifiers are now scrubbed from visible logs.
- Request IDs, UUIDs and other low-level gibberish removed unless you’re debugging.
- Logging is tighter, clearer and won’t expose anything weird if console output is toggled on.

> Nobody needs to see “REQID: 93819AD9-BORK-420”. Least of all... me.

---

## Summary

- ✅ Real playlists again  
- ✅ UI is fast and no longer self-destructs  
- ✅ Better threading with safe limits  
- ✅ Logging won’t blind you  
- ✅ Version 5.0.0 - live and tagged  

Stellody is finally back on its feet. It not only looks the part but now actually *does the job it was built for*.  
More playlists, better structure and a UI that can take a punch.

[Check it out at stellody.com](https://www.stellody.com)

---

> This was one of those releases that looked like a minor patch from the outside - but inside? A total exorcism.

