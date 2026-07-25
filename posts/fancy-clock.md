---
blurb: Desktop clock with proper alarms
date: 2026-07-25 10:10
type: project
extra_images:
- /static/images/fancy-clock2.png
- /static/images/fancy-clock3.png
image: /static/images/fancy-clock.png
one_liner: A customisable desktop clock with skins, full localisation, animated video
  backgrounds and alarms that behave like a phone's.
social_image: /static/images/fancy-clock.png
tags:
- cat:Desktop Apps
- clock
- alarms
- fancy
- fun
- internationalisation
- skins
- video
- python
thumb_image: /static/images/fancyclock-icon.png
title: Fancy Clock
---

[FancyClock](https://ernster.dev/FancyClock/) is a customisable desktop clock with skins, full localisation, animated video displays and alarms that behave like a phone's.

## Problem → System → Outcome

**Problem.** Default desktop clocks are boring, inflexible and lack meaningful utility; the ones that try to do more usually get the time itself wrong.

**System.** FancyClock is a customisable desktop clock with additional display options, user-adjustable features and a full alarm subsystem that fires on the same NTP-corrected time the clocks display.

**Outcome.** The clock stayed readable and responsive in real use, without UI jank or layout drift during long-running desktop sessions; alarms ring when they should, snooze like a phone's and own up to anything they missed.

# Rationale
I wanted to knock something up quickly to show off to a friend using AI but got diverted into making it fully featured 
when I started turning it into a better product.

## Challenges along the way
This was quite the project but it turned out to be more complex the more I added.  
Then I decided to add video skins - that was a fun challenge but I got there in the end.
The REAL struggle was internationalising the app.  Multiple languages and timezones throughout the world are HARD
to support.  Especially when you want to support regional numbering systems AS WELL!
Then came alarms. Alarms sound simple; they are not. They have to fire on the corrected time the clocks actually
show, survive daylight-saving transitions in both directions (a spring-forward time that does not exist, an
autumn time that exists twice) and still owe you an answer for anything that should have rung while the machine
was asleep or switched off.

[Releases](https://github.com/oernster/FancyClock/releases)

## Alarms, done properly

Weekly repeating or one-off alarms, each with a label, a colour, a sound and its own timezone, so changing the
displayed timezone never silently shifts an alarm. Snooze carries a per-alarm duration, a budget of snoozes per
ring and a dropdown that re-picks the duration on any snooze. A persistent firing window stays up until you act
and a missed-alarms summary covers anything that fired while the app was closed or the machine was asleep;
suspend-and-wake and off-between-runs are deliberately the same code path.

*It will never wake a sleeping machine. It tells you what it missed instead.*

## What it does

A frameless, draggable PySide6 desktop clock in analogue and digital modes with automatic timezone localisation
(region names, numbers and numeral systems translated across 70+ languages, menus and skin names included),
optional NTP accuracy, nine skins from the Starfield default to full-video backgrounds, adjustable window opacity
with keyboard and mouse-wheel shortcuts, phone-grade alarms with bundled sounds and a system tray presence, and a
single-instance guard that brings the running clock to the front instead of launching a second one. Shipped for
Windows, macOS and Linux. The full feature rundown lives on the product site:
[ernster.dev/FancyClock](https://ernster.dev/FancyClock/).
