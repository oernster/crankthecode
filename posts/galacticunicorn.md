---
blurb: MicroPython LED
date: 2026-01-19 06:45
image: /static/images/galacticunicorn.png
one_liner: MicroPython experiments on the Galactic Unicorn LED matrix, exploring visuals
  and device control.
social_image: /static/images/galacticunicorn.png
tags:
- cat:Hardware
- GalacticUnicorn
- MicroPython
title: Galactic Unicorn Timer
---

[GalacticUnicorn Timer](https://github.com/oernster/galactic-unicorn)  🦄

## Problem → Solution → Impact

**Problem:** LED animation projects for MicroPython often lack structured, beginner-friendly examples.

**Solution:** This project showcases MicroPython control of the Galactic Unicorn LED board with reusable patterns.

**Impact:** Provides a fun and approachable starting point for embedded LED development.

# Rationale
I bought a GalacticUnicorn as a fun device to play with and wanted a project to work on rather than simply
play with the supplied apps.  This allowed me to play with micropython.  To be honest I don't really like 
micropython since it's such a limited feature set but it was quite fun to write.

## Overview
Button controls on the Galactic Unicorn itself...

A) Reset and start timer.

B) Stop timer and store current time.

C) If you have pressed (B) it will show the stored time, otherwise it will default to hh:mm:ss::d and show that.

...where hh = hours, mm = minutes, ss = seconds, d = tenths of a second.

Commands available on the console...

'A' through 'C' as above for the GU buttons.

D) Show clock.

R) Reset timer to zero but do not start it.