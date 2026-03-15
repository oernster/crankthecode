---
blurb: Local AI narration for ebooks and documents
date: 2026-03-15 01:30
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

- Now with custom Windows installer.
- Playback speed control, bookmarking and chapter navigation.
- Persistent volume control with real time adjustment.

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

Recent releases introduced several major usability improvements including playback speed control bookmarking chapter navigation and persistent volume management.

These features were implemented while maintaining strict separation between synthesis playback and navigation logic so the system remains deterministic and easy to evolve.

The goal is not to produce a feature heavy media player but a focused narration tool that makes personal libraries easier to experience.

---

NarrateX is an exploration of what happens when personal libraries become audible.

Books already contain voices.  
*Software simply helps them speak.*