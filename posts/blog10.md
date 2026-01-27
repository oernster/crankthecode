---
title: "🎧 Rate Limits, Retry Logic and Reality Checks"
date: "2026-01-27 20:30"
tags: ["blog", "stellody", "ratelimit", "spotify", "backoff", "engineering"]
one_liner: "Rate limits strike mid-run - retry logic, async persistence and filesystem stalls all collide in a war for reliability."
---

## The Elephant in the Room - Rate Limiting

It finally happened. I left Stellody running overnight - a clean long-form run over my 5,000 track FLAC library to generate a perfect genre and sub-genre playlist set.  
Woke up to a Spotify 429 rate limit wall. The process had ground to a halt around 45 minutes in - just long enough to give me false hope.

> A smarter retry mechanism is in the works - because sleeping through a 2-3h run only to wake up to a 429 wall is not the dream.

---

## Conservative Retry Policies

Two changes were made quickly:

- Revised the global rate limiter to back off more aggressively under high load
- Introduced a deferred retry path that prevents constant re-hits during throttle windows

These changes were subtle - Stellody must still feel fast but also invisible to Spotify’s rate enforcement.

---

## It Wasn't Just the API...

Logs hinted at something more subtle: **file system stalls** in the `JsonTtlCache` mechanism.

When the app tries to persist intermediate caching data, it was doing so inside a lock - meaning if disk writes stall even briefly, **everything stalls**.

Two improvements were made:

- Introduced async save logic to offload file IO operations without blocking main logic
- Reworked the internal snapshot/save sequence to take the cache copy **before** trying to hit disk

---

## Testing a Real Workload

This isn't about toy datasets. Stellody is now being battle tested with the full FLAC library:

- 5,000+ tracks
- Dozens of genres and sub-genres
- Playlist pool size thresholds in place to prevent tiny, useless output

Runs are being monitored across a 3-5h cycle to verify stability, rate behaviour and filesystem resilience.

---

## Interim Website Warning

The Stellody homepage now reads:

> TURNS OUT IT’S RATE LIMITED (READ SPOTIFY HATES ME!) WHICH STOPS THE APP RUNNING – WILL PROVIDE A NEW RELEASE SOON…

Blunt but honest.

---

## Summary

- Spotify API rate limits are real and unpredictable
- Backoff handling has been overhauled
- Filesystem stalls have been resolved with async logic
- Long-form runs are being tested before the next tagged release

Next release: **v5.1.1**, once the 5,000 track tests pass.

🎧 Onwards
