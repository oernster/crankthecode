---
title: "Concurrency, Stability and UI Polish for Stellody"
date: "2026-01-28 12:00"
tags: ["blog", "stellody", "performance", "concurrency", "ui"]
one_liner: "Concurrency dialed to 11 - thread-safe caching, UI polish and performance that respects rate limits without dragging its feet."
emoji: "🧵"
---
## ⚙️ Speed & Stability Improvements

* Stellody now maximises available CPU cores across threads and processes.
* Global API limits (Spotify and MusicBrainz) are respected across all concurrency layers.
* Introduced a SQLite-backed coordinator that governs API pacing like a diplomatic bouncer.
* Coordinated token-bucket strategy with penalty windows now prevents bursty API misfires.
* Added a diagnostic profiler that logs token wait, DB locks and retry timing.
* Implemented thread-safe caching and safe shutdown signaling across process boundaries.

*– Because respecting rate limits shouldn’t mean watching paint dry.*

---

## 🧹 Logging, Tuning and Diagnostics

* The console output can now be logged to a rotating file with timestamped filenames.
* Console output logging is user-configurable in the Settings | Options dialog.
* Added 🧹 button to clear console output mid-run (and rotate the log file if enabled).
* Logging continues even when a run is stopped early.
* Rate limit profiling output is logged for post-run analysis.
* Environment variables can now tweak runtime concurrency + retry behaviour for advanced users.

*– Because tuning Stellody should feel like drag racing a racehorse with an API learner’s permit.*

---

## 🧪 Spotify 403(-1) Transport Bug: Eliminated

* Diagnosed a concurrency issue with Spotipy usage across threads.
* Now each thread gets its own Spotify client + session, eliminating shared-state corruption.
* Result: No more malformed 403 errors or weird URL fragments mid-request.
* Step 1 collection is now resilient, clean and achieves higher artist + track resolution.

*– Spotipy now knows how to stay in its lane. Literally.*

---

## 🧵 Thread Safety and Shutdown Behavior

* Shutdown is now responsive even under heavy multiprocessing load.
* No more hangs, orphaned logs or crashy UI flails when aborting a run.
* Signal propagation to all subprocesses now works cleanly on all platforms.
* Thread-safe state updates remove post-run UI weirdness and flickers.

*– Ctrl+C now means “stop nicely” not “summon the crash demon.”*

---

## 🔠 UI Fixes and Enhancements

* Completed a full sweep of UI refinements and beautification across Stellody.
* Standardised button colours to rich violet.
* Added hover state with a teal colour for active visual feedback.
* Broom button 🧹 styling and tab ordering fixed.
* Console output and main button area colours now properly match (no more rogue dark trays).
* Increased font sizes on help/about pages for legibility.
* Fixed disappearing label updates, layout glitches and rogue visual artefacts.
* Removed the pesky intermittent right-side black panel (die in a fire).
* The Options dialog no longer warns users to save settings when no changes were made.
* Added in Phase numbered ETA and Total ETA for progress indication.

*– Death to janky spacing, font clipping and random trays of doom.*

---

## ✅ Final Result

🎉 Victory lap activated! Stellody is handling massive artist payloads like a champ - thousands of tracks, dozens of threads and not a single tray of UI shame in sight.

* End-to-end runs complete without error.
* Recommendations and playlist generation are faster, more stable and more observable.
* Intermittent API failures are now rare and retryable.
* UI is consistent, polished and pleasant.
* Built for Windows, linux and macOS.
* Deployed here [Stellody](https://www.stellody.com)


*– Less chaos. More playlists. Same unrepentant Stellody attitude.*
