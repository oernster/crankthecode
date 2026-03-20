---
blurb: Local narration for ebooks and documents
date: 2026-03-17 17:30
type: project
role: flagship
image: /static/images/narratex.png
one_liner: A local desktop application that converts books and documents into spoken audio using modern TTS engines.
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

[NarrateX](https://github.com/oernster/NarrateX) is a local desktop narration engine for turning books and documents into spoken audio.

---

NarrateX is built around a simple idea. Narration should be reliable, predictable and easy to follow over long sessions.

The system focuses on stable playback, clear state boundaries and a consistent narration flow. The goal is not just to generate audio but to behave correctly while doing so.

### Architecture

The codebase enforces a clear separation of concerns across the system.

Unit tests go beyond coverage. They encode structural expectations and constrain future changes. The system is designed to resist accidental degradation over time.

*The architecture is part of the product, not just its implementation.*

### UI and Interaction

The interface is designed to remain clear and consistent without adding noise.

Controls are grouped deliberately. Button sizes are consistent across the interface. Disabled states in dark mode remain visible with defined borders.

Playback controls are explicit.
The play and pause control is a single larger toggle.
The stop control is visually distinct.

Navigation feedback is continuous.
The vertical navigation indicator reflects live progress through the text.
Highlighted text is synchronised with audio during playback.

*Subtle visual adjustments improve cohesion and reduce friction during long sessions.*

### Navigation and State

Chapter and section detection supports automatic bookmark generation.

Bookmarks follow a consistent format and are easy to scan during navigation.

The system maintains a strict separation between navigation state and playback state to preserve deterministic behaviour.

---

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
Turn any ebook into natural narration directly on your own machine.
</div>

---

## Problem → Solution → Impact

**Problem:**
Large digital libraries are easy to collect yet difficult to consume when reading time is limited.

**Solution:**
NarrateX converts books and documents into natural spoken narration using modern text to speech engines that run locally.

**Impact:**
Your library becomes something you can listen to anywhere. Books are no longer tied to a screen.

---

## Overview

NarrateX is a desktop application designed to transform written material into spoken narration.

Reading should not require sitting in front of a page. A book should follow you during a walk a commute or quiet work.

The application loads an ebook or document then parses the text into structured segments. These segments are processed through a local text to speech engine which produces audio in real time.

Narration begins almost immediately because synthesis and playback run together in a streaming pipeline. This avoids delays that occur when an entire book must be generated before playback begins.

*Everything runs locally which means the workflow is fast predictable and private.*

---

## NarrateX at a Glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Features</h3>
  <ul>
    <li>Local text to speech narration</li>
    <li>Streaming audio playback</li>
    <li>Selectable voice profiles</li>
    <li>Playback speed control</li>
    <li>Persistent volume control</li>
    <li>Bookmarking with automatic resume</li>
    <li>Chapter navigation with visual tree indicator</li>
    <li>Automatic text chunking for stable narration</li>
    <li>Automatic section and chapter bookmark generation</li>
    <li>Audio synchronised text highlighting</li>
    <li>Support for EPUB PDF and plain text</li>
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

## How It Works

NarrateX processes text through a structured pipeline designed for long form narration.

A book is first loaded and parsed into normalised text.
The text is divided into manageable speech chunks.
Each chunk is synthesised into audio and streamed directly to the playback device.

Chunk based narration keeps the system responsive even for very large books. Audio generation continues ahead of playback which keeps narration smooth.

*Voice profiles can be swapped depending on preference. Some voices suit fiction while others work better for technical writing.*

---

## Playback Control

NarrateX provides fine control over how narration is delivered without altering the underlying text or audio synthesis.

### Playback Speed

Playback speed can be adjusted without changing the TTS output.

Speed is applied during playback rather than synthesis which keeps the audio cache stable and avoids regenerating speech.

*This preserves deterministic behaviour in the narration pipeline.*

### Volume Control

Volume can be adjusted in real time using a simple slider interface.

The control includes a visual indicator that reflects mute low and normal volume states.

*Volume settings persist between runs.*

### UI Locking During Playback

During active narration certain configuration controls are temporarily locked.

This prevents inconsistent playback states and keeps the system predictable.

*Playback controls and volume adjustment remain available.*

---

## Navigation

Long form listening requires the same flexibility readers expect from modern ebook software.

NarrateX implements two complementary navigation systems.

### Bookmarks

Users can create multiple numbered bookmarks during narration.

A hidden resume position is automatically stored when playback stops pauses or the application exits.

Bookmarks include both manual pins and automatically generated section markers.

*Playback resumes from the last listening position.*

### Chapter Navigation

NarrateX detects chapter headings from the book text and builds a navigation index.

Navigation controls allow jumping between chapters instantly.

A vertical tree style indicator provides a structural overview of the book and updates as narration progresses.

*The goal is a calm reference rather than a full table of contents.*

---

## Architecture

The project follows a layered architecture separating interface application services domain logic and infrastructure.

The interface is built using PySide6.
Application services orchestrate playback and navigation.
Domain logic manages chunking chapter detection and bookmark state.

Infrastructure adapters connect to TTS engines audio streaming and ebook parsing tools.

*This structure keeps the narration pipeline predictable and allows components to evolve independently.*

---

## Why Build This

Many people maintain large ebook libraries that are rarely used.

Time is usually the limiting factor.

Audio allows books to accompany everyday activity. Walking, commuting, cooking, or quiet work become opportunities to continue reading.

Commercial audiobook platforms depend on catalog availability, licensing and subscriptions.

NarrateX takes a different approach.

Your books remain yours.

*The software gives them a voice.*

---

## Development Notes

NarrateX is built with a focus on structural integrity rather than feature accumulation.

The system prioritises predictable behaviour clear state boundaries and long term maintainability.

Testing acts as a structural constraint rather than a safety net. The system is designed to resist regression by construction.

UI changes are applied carefully to improve clarity without adding noise. Small improvements compound during long listening sessions.

*The goal remains consistent. A focused narration tool that treats structure as a first class concern.*

---

NarrateX is an exploration of what happens when personal libraries become audible.

Books already contain voices.

*Software helps them speak.*
