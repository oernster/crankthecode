---
date: 2026-01-28 12:00
emoji: "\U0001F9F5"
one_liner: Concurrency dialled up with thread safe caching UI polish and performance
  that respects rate limits without dragging its feet.
tags:
- cat:Blog
- stellody
- performance
- concurrency
- ui
title: Concurrency, Stability and UI Polish for Stellody
---

# Speed & Stability Improvements

This release focused on pushing Stellody harder without letting it tear itself apart.

Concurrency is now scaled aggressively across available CPU cores using a mix of threads and processes while still respecting global API limits imposed by Spotify and MusicBrainz. Rather than relying on best effort backoff a dedicated SQLite backed coordinator now governs API pacing centrally acting as a diplomatic bouncer between the application and external services.

A coordinated token bucket strategy with penalty windows prevents bursty misfires and smooths throughput under load. To make this observable a diagnostic profiler was added that logs token wait times database locks and retry behaviour for post run analysis. Thread safe caching and clean shutdown signalling are now enforced across process boundaries so runs stop when asked and state remains consistent.

*-Because respecting rate limits should not mean watching paint dry.*

---

## 🧹 Logging, Tuning and Diagnostics

Logging was expanded to support deeper inspection without overwhelming the UI.

Console output can now be written to rotating timestamped log files with the behaviour controlled from the Settings Options dialog. Output continues even if a run is stopped early and a dedicated broom button allows console output to be cleared mid run while safely rotating the log file if enabled.

Rate limit profiling output is persisted for later analysis and environment variables can be used to tweak concurrency and retry behaviour for advanced tuning without recompiling anything.

*-Because tuning Stellody should not feel like drag racing a racehorse with an API learner’s permit.*

---

## 🧪 Spotify 403(-1) Transport Bug Eliminated

A long standing intermittent failure was traced to shared Spotipy client state being accessed across threads.

Each worker thread now owns its own Spotify client and session which eliminates shared state corruption and malformed requests. As a result the mysterious 403 errors with broken URLs have disappeared and initial collection phases achieve higher and more reliable artist and track resolution.

*-Spotipy now knows how to stay in its lane. Literally.*

---

## 🧵 Thread Safety and Shutdown Behaviour

Shutdown behaviour was hardened under heavy multiprocessing load.

Signal propagation now reaches all subprocesses reliably on all platforms. Abort requests are handled cleanly without hanging the UI orphaning logs or leaving zombie workers behind. Thread safe state updates also eliminate post run flicker and inconsistent UI states.

*-Ctrl C now means stop nicely not summon the crash demon.*

---

## 🔠 UI Fixes and Enhancements

A full sweep of UI refinement was completed alongside the performance work.

Button colours were standardised to a rich violet with a clear teal hover state for active feedback. The broom button styling and tab ordering were corrected and console output colours now match the main control area without rogue dark panels appearing unexpectedly.

Font sizes were increased on help and about pages for legibility. Disappearing labels layout glitches and intermittent artefacts were fixed and the long standing right side black panel issue was finally removed. The Options dialog no longer warns users to save settings when nothing has changed.

*-Death to janky spacing font clipping and random trays of doom.*

---

## 🧭 Advanced ETA for Progress Indication

Progress indication was rethought entirely.

Rather than resetting at phase boundaries Stellody now provides a forward looking ETA that predicts downstream work early using real artist and track counts. Phase aware weighting ensures that expensive collection phases dominate the estimate rather than fast tail steps.

Smoothing and clamping prevent jitter and late surprises and the ETA logic runs off the UI thread so it remains reusable across workflows. Optional opt in persistence allows safe post release tuning without impacting normal users.

*-Turns out guessing ETAs is easy. Being right takes work.*

---

## ✅ Final Result

Stellody is now handling massive payloads with confidence. Thousands of tracks dozens of threads and sustained runs complete without UI embarrassment or mysterious stalls.

End to end runs finish cleanly. Playlist generation is faster more stable and observable. Intermittent API failures are rare and recoverable. The UI is consistent polished and predictable across Windows Linux and macOS.

Deployed here: [Stellody](https://www.stellody.com)

*-Less chaos. More playlists. Same unrepentant Stellody attitude.*