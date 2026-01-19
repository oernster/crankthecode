---
title: "Galactic Unicorn Timer"
date: "2026-01-19 07:15"
tags: ["GalacticUnicorn", "MicroPython"]

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/galacticunicorn.png
---
I played with micropython and a Galactic Unicorn device: [GalacticUnicorn Timer](https://github.com/oernster/galactic-unicorn).
TBH I don't get on with micropython since it's such a limited feature set but it was quite fun to do.

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
