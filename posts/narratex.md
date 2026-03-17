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

[NarrateX](https://github.com/oernster/NarrateX/releases) is a local desktop narration engine for turning books and documents into spoken audio.

---

## Version 2.0.0

This release introduces a structural overhaul of the system along with a set of focused usability improvements.

### Architecture

The codebase has been refactored to remove accumulated technical debt and enforce a clearer separation of concerns across the system.

Unit tests now go beyond coverage. They actively constrain future changes by encoding structural expectations into the test suite. The goal is simple. The system should resist accidental degradation over time.

*The architecture is now part of the product, not just its implementation.*

### UI and Interaction

The interface has been refined to improve clarity and consistency without adding noise.

Controls are grouped more deliberately. Button sizes are consistent across the interface. Disabled states in dark mode are clearly visible with defined borders.

Playback controls have been made more explicit.  
The play and pause control is now a single larger toggle.  
The stop control is visually distinct.

Navigation feedback has been improved.  
The vertical navigation indicator now reflects live progress through the text.  
Highlighted text is synchronised with audio during playback.

*Subtle visual adjustments have been applied across the interface to improve overall cohesion and reduce friction during long sessions.*

### Navigation and State

Chapter and section detection has been extended to support automatic bookmark generation.

Bookmarks now follow a consistent visual format and are easier to scan during navigation.

*The system continues to maintain a clear separation between navigation state and playback state to preserve deterministic behaviour.*

---

<div style="text-align:center; font-size:1.2em; margin: 1em 0;">
Turn any ebook into natural narration directly on your own machine.
</div>

---

## Problem → Solution → Impact

**Problem:**  
Large digital libraries are easy to collect yet surprisingly difficult to consume when reading time is limited.

**Solution:**  
NarrateX converts books and documents into natural spoken narration using modern text to speech engines that run locally.

**Impact:**  
Your library becomes something you can listen to anywhere. Books are no longer tied to a screen.

---

## Overview

NarrateX is a desktop application designed to transform written material into spoken narration.

The idea is straightforward. Reading should not require sitting in front of a page. A book should be able to follow you during a walk, a commute or quiet work.

The application loads an ebook or document then parses the text into structured segments. These segments are processed through a local text to speech engine which produces audio in real time.

Narration begins almost immediately because synthesis and playback run together in a streaming pipeline. This avoids the long delays that often occur when an entire book must be generated before playback begins.

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
The text is then divided into manageable speech chunks.  
Each chunk is synthesised into audio and streamed directly to the playback device.

Chunk based narration has an important benefit. The system can stay responsive even when processing very large books. Audio generation continues ahead of playback which keeps narration smooth.

*Voice profiles can be swapped depending on preference. Some voices work well for fiction while others suit technical writing.*

---

## Playback Control

NarrateX provides fine control over how narration is delivered without altering the underlying text or audio synthesis.

### Playback Speed

Playback speed can be adjusted between slower and faster narration rates without changing the TTS output itself.

Speed is applied during playback rather than synthesis which keeps the audio cache stable and avoids regenerating speech for different speeds.

*This allows smooth adjustment while maintaining deterministic behaviour in the narration pipeline.*

### Volume Control

Volume can be adjusted in real time during playback using a simple slider interface.

The control includes a visual indicator that reflects mute low and normal volume states.

*Volume settings are persisted between runs so the application starts with the previously selected level.*

### UI Locking During Playback

While narration is actively playing the interface temporarily locks certain configuration controls such as voice selection and playback speed.

This avoids inconsistent playback states and keeps the narration pipeline deterministic.

*Playback controls and volume adjustment remain available.*

---

## Navigation

Long form listening requires the same navigation flexibility readers expect from modern ebook software.

*NarrateX implements two complementary navigation systems.*

### Bookmarks

Users can create multiple numbered bookmarks during narration.

A separate hidden resume position is automatically stored when playback stops pauses or the application exits.

Bookmarks include both manual pins and automatically generated section markers to support different navigation styles.

*When playback resumes the system automatically continues from the last listening position.*

### Chapter Navigation

NarrateX detects chapter headings directly from the book text and builds a navigation index.

Navigation controls allow jumping to the previous or next chapter instantly.

A visual chapter indicator appears alongside the reading pane as a vertical tree style guide.  
This acts as a structural overview of the book and updates dynamically as narration progresses.

*The goal is not to replicate a full table of contents but to provide a calm visual reference for long form listening.*

---

## Architecture

The project follows a layered architecture separating interface application services domain logic and infrastructure.

The desktop interface is built using PySide6.  
Application services orchestrate narration playback and navigation.  
Domain logic manages chunking chapter detection and bookmark state.

Infrastructure adapters connect the system to TTS engines audio streaming libraries and ebook parsing tools.

*This structure keeps the narration pipeline predictable and allows components such as TTS engines or audio streaming backends to evolve independently.*

---

## Why Build This

Many people maintain large personal ebook libraries. Those collections often contain hundreds or thousands of titles that rarely get opened.

Time is usually the limiting factor rather than interest.

Audio solves that constraint by letting a book accompany everyday activity. Walking, commuting, cooking, or working quietly all become opportunities to continue reading.

Commercial audiobook platforms provide a partial answer however they depend on catalog availability, licensing and subscription models.

NarrateX takes the opposite approach.

Your books remain yours.  
*The software simply gives them a voice.*

---

## Development Notes

Version 2.0.0 represents a shift from feature accumulation to structural integrity.

The system has been refactored to reduce internal complexity while strengthening guarantees around behaviour and evolution.

Testing now acts as a structural constraint rather than a safety net. The system is designed to resist regression by construction.

UI improvements were applied carefully to improve clarity without introducing visual noise. Most changes are subtle yet compound over time during long listening sessions.

The goal remains consistent. A focused narration tool that treats structure as a first class concern.

---

NarrateX is an exploration of what happens when personal libraries become audible.

Books already contain voices.  
*Software simply helps them speak.*