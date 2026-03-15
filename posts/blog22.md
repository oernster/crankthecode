---
title: NarrateX - When software is engineered rather than assembled
one_liner: A local audiobook reader that quietly replaces an entire commercial category
date: 2026-03-15 02:45
emoji: 🔊
tags:
  - cat:blog
  - python
  - desktop-app
  - tts
  - kokoro
  - architecture
  - software-engineering
  - open-source
---

# NarrateX

[NarrateX](https://github.com/oernster/NarrateX) is a desktop application that reads books aloud using modern machine voice synthesis. EPUB, PDF and plain text are supported directly. Kindle formats can be converted automatically through Calibre.

That description is technically correct.

It is also not the interesting part.

The interesting part is that NarrateX exists largely to demonstrate what happens when software is engineered as a system rather than assembled as a collection of features.

Most personal projects optimise for speed of construction. NarrateX was built with a different priority.

*Structure first.*

## The problem with most small software

Many small applications work. They read files. They display windows. They perform their intended function.

Few are designed to survive their own success.

Dependencies are hidden. Lifecycle is implicit. Packaging is an afterthought. Architecture lives mostly in the developer's head.

The software works until the moment it needs to change.

NarrateX was built under a different constraint.

*The system should behave the way it is designed rather than the way it happens to run.*

## Architecture as a first class decision

NarrateX follows a layered architecture deliberately.

Domain logic exists separately from orchestration. Infrastructure adapters handle IO. The user interface consumes services rather than constructing them.

Responsibility is separated across clear boundaries.

The UI does not create services.
The services do not know about the UI.
Infrastructure components are replaceable without rewriting behaviour.

Each layer has a defined role. Each boundary prevents accidental coupling.

This sounds obvious.

It is also surprisingly rare.

*Architecture only matters when it prevents future mistakes.*

## The runtime system

At runtime the application performs several coordinated tasks.

A book is loaded and parsed. Text is chunked into spoken segments. These segments are passed to the Kokoro text to speech engine. Generated audio streams through a background audio pipeline while the interface highlights the active text.

All of this occurs concurrently.

The UI remains responsive. Audio generation can parallelise. Playback is streamed rather than buffered in full.

The result feels simple.

The system underneath is anything but.

*Simple behaviour often hides deliberate structure.*

## Deterministic packaging

Most Python desktop software ships as a zip file or a single executable.

NarrateX instead uses a two stage build process.

The application is first compiled into a PyInstaller bundle. That bundle becomes a deterministic payload containing every file required for runtime execution.

A separate installer executable then embeds that payload together with a manifest that records file sizes and SHA256 hashes.

Files are sorted. Timestamps are normalised. Payloads are reproducible.

This matters for a simple reason.

*Reproducible software is easier to trust than accidental software.*

## Installer lifecycle

The installer itself behaves like a real application rather than a copy script.

Fresh installs stage files before swapping them atomically into place. Upgrades replace existing bundles safely. Repair operations verify file integrity using the manifest and restore corrupted components automatically.

Uninstall removes registry entries, shortcuts and user data cleanly.

Desktop applications should behave like citizens of the operating system.

Surprisingly many do not.

*Software quality includes the way software arrives and leaves.*

## Machine voice without cloud dependency

NarrateX uses the Kokoro speech engine.

Voices are generated locally. No network service is required once models are available. CPU inference is sufficient for smooth playback.

The effect is straightforward.

Any ebook can become an audiobook instantly.

No subscription.

No DRM.

No platform lock in.

This capability existed in early ebook ecosystems before commercial audio platforms decided that listening should be monetised.

NarrateX simply restores that ability.

*Technology rarely disappears. It is usually removed for business reasons.*

## Tests as structural enforcement

Test coverage across the core is complete.

Coverage is not treated as a vanity metric. It exists to protect architecture.

Tests confirm behaviour. Architectural tests enforce boundaries. Forbidden imports and hidden construction paths fail immediately.

The codebase therefore has an unusual property.

Violating the architecture is harder than following it.

*Structure enforced by code survives longer than structure described in documents.*

## A quiet result

The final application is intentionally modest.

A window. A reader. Voice selection. Playback controls. Cover art. Chapter navigation.

It reads books.

Behind that simplicity sits a deliberately engineered system designed to demonstrate something that is easy to forget.

Software quality is rarely about clever algorithms or impressive frameworks.

It is about structure.

*NarrateX exists as a small example of what happens when structure is treated as the primary feature.*