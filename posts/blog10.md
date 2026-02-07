---
date: 2026-01-27 20:30
emoji: "\U0001F3A7"
one_liner: Rate limits strike mid run as retry logic async persistence and filesystem
  stalls collide in a war for reliability.
tags:
- cat:Blog
- stellody
- ratelimit
- spotify
- backoff
- engineering
title: Rate Limits, Retry Logic and Reality Checks
---

# The Elephant in the Room - Rate Limiting

It finally happened.

I left Stellody running overnight on a long form run across my 5,000 track FLAC library to generate a complete genre and sub genre playlist set. Everything looked healthy. Progress bars moved. Logs behaved.

I woke up to a Spotify 429 rate limit wall.

The run stalled roughly 45 minutes in which is just long enough to give false confidence that everything is fine before reality intervenes.

*-A smarter retry mechanism is in the works because sleeping through a two to three hour run only to wake up to a 429 wall is not the dream.*

---

## Conservative Retry Policies

Two changes were implemented immediately.

The global rate limiter was revised to back off more aggressively under sustained load. At the same time a deferred retry path was introduced to prevent repeated hits during throttle windows.

The balance here matters. Stellody still needs to feel fast but it also needs to stay invisible to Spotify’s enforcement logic.

This is not about winning a race. It is about finishing one.

---

## It Wasn't Just the API

The logs pointed to a second more subtle problem. File system stalls inside the `JsonTtlCache` persistence layer.

Intermediate cache state was being written to disk while holding a lock. If disk IO stalled even briefly the entire pipeline stalled with it.

That was never going to scale.

The fix involved two coordinated changes. Persistence was moved to async logic so disk writes no longer block the main execution path. The snapshot sequence was also reordered so cache state is copied before any attempt is made to touch disk.

The result is a pipeline that can tolerate slow IO without grinding everything else to a halt.

---

## Testing a Real Workload

This work is not being validated against toy datasets.

Stellody is now being exercised against the full library:

- Over 5,000 tracks
- Dozens of genres and sub genres
- Enforced pool size thresholds to prevent tiny unusable playlists

Runs are monitored across three to five hour cycles to verify rate behaviour retry logic and filesystem resilience under sustained load.

If it fails it fails loudly and early rather than politely and too late.

---

## Interim Website Warning

The Stellody homepage now includes a very direct message:

*-TURNS OUT IT’S RATE LIMITED READ SPOTIFY HATES ME WHICH STOPS THE APP RUNNING WILL PROVIDE A NEW RELEASE SOON*

It is not subtle. It is accurate.

---

## Summary

Spotify API rate limits are real unpredictable and unavoidable. Backoff and retry handling has been reworked to respect that reality. Filesystem stalls have been eliminated through async persistence and long form runs are now being validated properly before another tagged release.

*-Next release will be **v5.1.1** once the 5,000 track tests pass cleanly.*

🎧 Onwards