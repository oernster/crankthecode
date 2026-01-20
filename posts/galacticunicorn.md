---
title: "Galactic Unicorn Timer"
date: "2026-01-19 06:45"
tags: ["GalacticUnicorn", "MicroPython"]
blurb: "MicroPython LED"
one_liner: "MicroPython experiments on the Galactic Unicorn LED matrix, exploring visuals and device control."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/galacticunicorn.png
---
[GalacticUnicorn Timer](https://github.com/oernster/galactic-unicorn)

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
