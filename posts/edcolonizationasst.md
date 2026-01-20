---
title: "Elite Dangerous Colonization Assistant"
date: "2026-01-19 04:40"
tags: ["elite", "frontier", "dangerous", "colonization", "trailblazer", "gaming", "game", "python"]
blurb: "Elite helper"
one_liner: "A helper tool for Elite Dangerous colonisation planning and Trailblazer workflow."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/edcolonizationasst.png
thumb_image: /static/images/edcolonizationasst-icon.png

extra_images:
  - /static/images/EDColonizationAsst2.png
---
[EDColonizationAsst](https://github.com/oernster/EDColonizationAsst)

## Problem → Solution → Impact

**Problem:** Complex games like Elite: Dangerous overwhelm players with disorganized data.

**Solution:** EDColonizationAsst captures and organizes in-game colonization data for easy reference and planning.

**Impact:** Enhances user experience by reducing decision fatigue and helping players track long-term objectives.

# Rationale
I play the game Elite Dangerous a lot and have a full HOTAS and rudder pedals and GameGlass setup for it on a tablet.
I wanted the ability to manage a shopping list of goods and commodities for when you're building out new space stations and orbital sites
on a second tablet (I run Samsung Galaxy A9+ tablets).

[Releases](https://github.com/oernster/EDColonizationAsst/releases)

# Challenges along the way
Making it function correctly by reading game journal data was a bit of a hassle.  However, once I understood the structure of the data
and how it updates the journal files became a little easier to work with.
UI challenges on the website were a little funky for me since I'm more of a backend dev rather than a front end UI designer.
However, I actually feel that the UI came out rather nicely.
The UI is fully tested in a web browser, both on a PC and a tablet. 

# Supported features:
- Add heartbeat to keep awake and make tablet only.
- Settings | Display/Power keep awake (recommended for tablets).
- Better carrier data reporting.
- Boot on launch into system tray option on install/repair.
- Fleet carrier manifest support.
- Light / dark mode theme in Windows standalone installer.
- Light / dark mode theme in UI.
- Auto refresh of UI on journal file updates.
- Major refactoring operation of codebase, using Object Oriented design, design patterns, SOLID principles.
- PEP8 compliance.
- Unit test case coverage increased.
- Multiple instances of the UI prevented by using Mutex / singleton logic.
- All documentation updated.
- Reorganisation of files to reduce file lengths.
- Linux support with easy to run shell scripts

# Tested on Windows 11 pro, Ubuntu Questing Quokka.
# Linux run scripts provided for: (Note: non Debian scripts are untested)
- Arch
- Debian
- Fedora
- RHEL
- Void
