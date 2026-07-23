---
blurb: A calm, local-first desktop email, calendar and contacts client
date: 2026-07-16 09:00
type: project
role: project
emoji: 🕊️
image: /static/images/pigeonpost.png
one_liner: A calm, local-first desktop email, calendar and contacts client built as a predictable alternative to Thunderbird.
social_image: /static/images/pigeonpost.png
tags:
- cat:Desktop Apps
- go
- wails
- react
- typescript
- email
- imap
- calendar
- contacts
- sqlite
thumb_image: /static/images/pigeonpost-icon.png
title: PigeonPost

---

[PigeonPost](https://pigeonpost.ink/) is a desktop email, calendar and contacts client for Windows, macOS and Linux.

Most email clients answer to an engagement model: they want attention, they push, they bundle, they change under you.

PigeonPost was built to a different brief:

*Email as a calm, predictable, local tool.*

Your mail stays with your provider. The client reads it, caches it and gets out of the way.

---

## Problem → System → Outcome

**Problem.** Desktop email is dominated by clients that are either webmail in a wrapper, engagement platforms in disguise or venerable but increasingly unpredictable. Switching costs feel high even though the mail itself already lives on the server.

**System.** A local-first client with a Go core and a React front end: IMAP, POP3 and SMTP through explicit protocol libraries, summaries and bodies cached to local SQLite for offline reading, credentials in the OS keychain and one clean-architecture boundary between the mail engine and the UI.

**Outcome.** A fast, native, predictable client for mail, calendar and contacts that never locks you in: the server remains the source of truth and the local cache is disposable.

---

## Why it exists

Thunderbird earned two decades of trust and then became harder to predict. Webmail earned convenience and then spent it on engagement.

The gap is a client that is:

* native and fast
* local-first, reading cleanly offline
* respectful of the protocols underneath
* uninterested in your attention

PigeonPost is that client. It connects to any IMAP or POP3 mailbox, with presets for Gmail, iCloud, Yahoo, Zoho, Fastmail and StartMail via app passwords and Microsoft accounts (Outlook.com, Hotmail, Microsoft 365) via OAuth with the refresh token kept in the OS keychain.

It is deliberately not for webmail-only users and it declines the one-click Google sign-in, because that scope carries a paid annual assessment; personal Gmail connects with an app password instead.

---

## What it does

The everyday surface is a full mail, calendar and contacts client: offline reading from a local cache, sandboxed HTML rendering, operator-grammar search, colour tags synced as IMAP keywords, undo send, send later, snooze, a month/week/day calendar with iTIP/iMIP invites and a vCard contacts book. The feature catalogue lives on the product site: [pigeonpost.ink/features](https://pigeonpost.ink/features.html).

---

## Local first, trust explicit

The design invariant is that PigeonPost never becomes a middleman.

* No PigeonPost account exists.
* Mail stays with your provider; the local cache is a convenience, not a hostage.
* Passwords live in the OS keychain, never the database.
* The HTML sandbox makes no remote requests without consent.
* External links open in your own browser.

*A client you can predict is a client you can trust.*

---

## Architecture

PigeonPost is the Go lineage of the same clean-architecture discipline as the Python desktop apps:

* Wails v2 shell (Go + system WebView)
* Go 1.23+ backend
* React 18 + TypeScript front end
* emersion go-imap, go-smtp and go-message
* modernc.org/sqlite (pure Go) with FTS5
* OS keychain via go-keyring

The domain never touches the UI; the UI never touches a socket. The boundary is enforced by structural tests, with the Go suite and the Vitest front-end suite gating every change.

Windows, macOS (Apple Silicon) and Linux each ship a native installer: a themed Windows setup, a DMG and a Flatpak.

---

## What this taught me

A mail client is mostly a trust exercise.

The protocols are old and well understood. The hard part is refusing the temptations layered on top of them: accounts you do not need, telemetry you never asked for, notifications tuned for engagement rather than information.

Every significant design decision in PigeonPost is a refusal of that kind, made structural: no middleman account, no unsandboxed rendering, no credential in a database, no push where a poll respects the reader more.

*Calm is not a feature you add. It is the set of features you decline.*
