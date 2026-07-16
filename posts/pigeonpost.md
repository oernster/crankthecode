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

## Core behaviour

**Mail.** Folders and summaries cache to local SQLite and read offline; bodies fetch on open and stay cached. HTML renders in a sandboxed frame that keeps the sender's design while running no scripts and making no remote requests; remote images stay blocked until you load them. In the dark theme a light-designed message is inverted to read comfortably while photos keep their true colour.

**Compose.** Rich text, reply and forward, attachments, reusable templates, per-account signatures and server drafts. In-progress writing autosaves locally. Undo send holds each message for a configurable few seconds. Send later schedules delivery; offline sends queue in a per-account outbox and deliver on the next sync.

**Organise.** Instant offline search with operators (from:, to:, has:attachment, dates), colour tags that sync across devices as IMAP keywords, on-arrival rules, snooze, an optional threaded view and an optional unified inbox that merges every account into one list. Undo and redo unwind the mail actions. Folders create, rename, delete and reorganise by drag.

**Calendar.** Month, week and day views, recurring events with per-event time zones, ICS import and export that round-trips with Outlook and Thunderbird, meeting invites over iTIP/iMIP and early two-way CalDAV sync.

**Contacts.** An address book with vCard and CSV import and export, round-tripping with Outlook and Thunderbird.

**Notifications.** Each IMAP account is watched by a persistent IDLE connection with a poll backstop. New mail raises a native notification; the first sync of an account is silent.

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

## PigeonPost at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>IMAP, POP3 and SMTP accounts</li>
    <li>Provider presets plus manual setup</li>
    <li>Microsoft OAuth sign-in</li>
    <li>Offline reading from a local cache</li>
    <li>Sandboxed HTML rendering</li>
    <li>Operator-grammar offline search</li>
    <li>Colour tags synced as IMAP keywords</li>
    <li>Undo send, send later, snooze</li>
    <li>Unified inbox and threading</li>
    <li>Calendar with ICS and iTIP/iMIP</li>
    <li>Early two-way CalDAV sync</li>
    <li>Contacts with vCard and CSV</li>
    <li>Full keyboard control</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technology</h3>
  <ul>
    <li>Go 1.23+ core</li>
    <li>Wails v2 shell</li>
    <li>React 18 + TypeScript front end</li>
    <li>emersion mail suite</li>
    <li>SQLite (pure Go) with FTS5</li>
    <li>OS keychain credentials</li>
    <li>Windows, macOS and Linux installers</li>
    <li>GPL-3.0, open source</li>
  </ul>
</div>

</div>

---

## What this taught me

A mail client is mostly a trust exercise.

The protocols are old and well understood. The hard part is refusing the temptations layered on top of them: accounts you do not need, telemetry you never asked for, notifications tuned for engagement rather than information.

Every significant design decision in PigeonPost is a refusal of that kind, made structural: no middleman account, no unsandboxed rendering, no credential in a database, no push where a poll respects the reader more.

*Calm is not a feature you add. It is the set of features you decline.*
