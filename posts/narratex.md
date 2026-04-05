---

blurb: Structured local narration for ebooks and documents
date: 2026-04-05 08:30
type: project
role: flagship
image: /static/images/narratex.png
one_liner: A structured desktop reading system that converts books and documents into continuous audio playback.
social_image: /static/images/narratex.png
tags:
- cat:Desktop Apps
- python
- tts
- audiobooks
- ebooks
- pyside6
- calibre
thumb_image: /static/images/narratex-icon.png
title: NarrateX

---

[NarrateX](https://narratex.co.uk/) is a structured desktop reading system that converts books and documents into continuous audio playback.

---

NarrateX treats books as structured systems rather than raw text.

This allows navigation to be correct, playback to be predictable and behaviour to remain consistent across real-world formats.

The system preserves document structure, derives navigation from headings and bookmarks and maintains deterministic playback across sessions.

It has been validated against real Kindle EPUBs, paperback PDFs and multi-book compilation documents.

---

## Core behaviour

* Playback follows document structure rather than file order
* Section navigation is derived from headings and bookmarks
* Non-content sections (e.g. frontmatter, indexes) are excluded from playback
* Navigation loads immediately and processes in the background
* Playback position is deterministic and consistent across sessions

---

## Architecture

The system is designed as a set of cooperating layers with clear boundaries.

Interface, application services, domain logic and infrastructure are separated to preserve predictable behaviour.

Unit tests act as structural constraints rather than simple verification. They encode expected system behaviour and limit unintended change.

*The architecture is part of the product, not just its implementation.*

---

## UI and interaction

The interface is designed to remain stable and consistent over long sessions.

Controls are grouped deliberately. Button sizes are consistent across the interface. Disabled states remain visible in dark mode with defined borders.

Playback controls are explicit:

* A single toggle for play and pause
* A distinct stop control

Navigation feedback is continuous:

* A vertical indicator reflects progress through the text
* Highlighted text is synchronised with audio

*Small visual decisions reduce friction during extended listening.*

---

## Navigation and state

NarrateX maintains a strict separation between navigation state and playback state.

Chapter and section detection supports automatic bookmark generation.

Bookmarks follow a consistent format and are easy to scan.

A hidden resume position is always maintained.

*This ensures that playback remains stable even when navigation changes.*

---

## Problem → system → outcome

**Problem:**
Most reading tools treat documents as linear text streams.
This leads to incorrect navigation, unreliable playback and inconsistent behaviour across formats.

**System:**
NarrateX treats books as structured systems.
Structure is preserved, navigation is derived from it and playback follows it.

**Outcome:**
Navigation becomes reliable.
Playback becomes predictable.
Books behave consistently regardless of source format.

---

## Overview

NarrateX transforms written material into continuous spoken narration using a structured pipeline.

A book is loaded and normalised into structured text.
The text is divided into manageable chunks.
Each chunk is synthesised and streamed directly to the playback device.

Synthesis and playback run concurrently which allows narration to begin immediately.

*Everything runs locally which keeps the system fast, predictable and private.*

---

## NarrateX at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Local text to speech narration</li>
    <li>Streaming audio playback</li>
    <li>Deterministic playback and resume</li>
    <li>Automatic section and chapter detection</li>
    <li>Bookmarking with automatic resume</li>
    <li>Chapter navigation with structural tree view</li>
    <li>Audio synchronised text highlighting</li>
    <li>Playback speed and persistent volume control</li>
    <li>Support for EPUB, PDF and plain text</li>
    <li>Optional Kindle format support via Calibre conversion</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technology</h3>
  <ul>
    <li>Python 3.11</li>
    <li>PySide6 desktop interface</li>
    <li>Local TTS engines</li>
    <li>Sounddevice audio streaming</li>
    <li>Calibre conversion pipeline</li>
  </ul>
</div>

</div>

---

## How it works

NarrateX processes text through a structured narration pipeline.

Text is segmented into chunks that can be synthesised independently.
Audio is generated ahead of playback and streamed continuously.

This keeps the system responsive even for large books.

*Voice profiles can be selected depending on the type of material.*

---

## Playback control

Playback behaviour is controlled without altering underlying synthesis.

### Playback speed

Playback speed is applied at runtime rather than during synthesis.
This avoids regenerating audio and preserves deterministic behaviour.

### Volume control

Volume can be adjusted in real time and persists between sessions.

### UI locking

During active playback certain configuration controls are temporarily locked.
This prevents inconsistent system states.

---

## Navigation

NarrateX provides structured navigation for long-form listening.

### Bookmarks

Manual bookmarks and automatically generated section markers are supported.

A hidden resume position is always maintained and used by default.

### Chapter navigation

Chapter headings are detected and used to build a navigation index.

A vertical tree view provides a structural overview and updates during playback.

---

## Why this exists

Many ebook libraries are large but underused.

Time is the limiting factor.

NarrateX allows books to be consumed during everyday activity without relying on external services or catalog availability.

Your books remain yours.

*The system makes them usable.*

---

## Development notes

NarrateX is built with a focus on structural integrity.

The system prioritises:

* predictable behaviour
* clear state boundaries
* long-term maintainability

Testing enforces structure rather than simply detecting failure.

*Changes are made carefully to preserve system behaviour over time.*

---

NarrateX is a working example of what happens when software is designed around structure first.

Behaviour follows.
*Outcome becomes predictable.*
