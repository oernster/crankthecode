---
blurb: Calendar tool
date: 2026-01-19 06:35
type: project
extra_images:
- /static/images/calendifier-ha.png
image: /static/images/calendifier.png
thumb_image: /static/images/calendifier-icon.png
one_liner: A calendar app with full iCalendar (RFC5545) support and deep internationalisation
  across languages and locales.
social_image: /static/images/calendifier.png
tags:
- cat:Desktop Apps
- calendar
- event
- events
- RFC5545
- notes
- internationalisation
- clock
- python
title: Calendifier
---

[Calendifier](https://ernster.dev/Calendifier/) is a desktop calendar with full iCalendar (RFC 5545) support and deep internationalisation.

## Problem → System → Outcome

**Problem.** Implementing RFC-compliant calendars manually is tedious and error-prone.

**System.** Calendifier parses and generates RFC5545 calendar formats for event management.

**Outcome.** Scheduling features stopped drifting out of sync with real dates and edge cases, so shipping calendar-dependent behaviour became predictable.

# Rationale
I wanted a fun project that created a next-gen calendar for both desktop and Home Assistant.
I then wanted to make it fully featured with an NTP synchronised digital/analogue clock, with full and effective 
support for eventing.  Then I fancied adding in some additional features so for extra fun and defiance I wrote in 
functionality for locale specific holidays.  As a final coup de grace, I made it fully internationlised for a large 
number of locales around the world in foreign languages/numbering standards; that, by the way, was freaking HARD! 


# Challenges along the way
A standards-compliant calendar backend. RFC5545? I *hardly* knew her.
The main app was HARD due to internationalisation; this was my first foray into internationalising an app and I did it 
for BOTH a browser AND home assistant dashboard cards.

Another really difficult thing for me was not only identifying holidays for locales which aren't British but making them 
appear correctly on the UI depending on the locale selected.
However, aside from the aforementioned internationalisation support challenges, I really struggled through writing code to support
RFC5545 which is basically the official canonical way to support Eventing in a Calendar application.  I got there in the end though
and I feel the UI is relatively intuitive for this purpose.

[Releases](https://github.com/oernster/Calendifier/releases)

## What it does

**Calendifier** ships in two deployment modes: a cross-platform desktop calendar built with Python and PySide6 plus an optional Home Assistant dashboard of web cards. It carries public holidays and cultural observances for 40 countries shown under their native names, speaks 13+ languages with native number and date formatting, keeps an NTP-synchronised analog clock and handles events with standard RRULE recurrence, notes and import/export locally with no account. The full feature catalogue lives on the product site: [ernster.dev/Calendifier](https://ernster.dev/Calendifier/).
