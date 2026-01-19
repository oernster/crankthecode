---
title: "Elite Dangerous Colonization Assistant"
date: "2026-01-19 04:40"
tags: ["elite", "frontier", "dangerous", "colonization", "trailblazer", "gaming"]
---
I play the game Elite Dangerous a lot and have a full HOTAS and rudder pedals and GameGlass setup for it on a tablet.
I wanted the ability to manage a shopping list of goods and commodities for when you're building out new space stations and orbital sites etc..
So I wrote: [EDColonizationAsst code](https://github.com/oernster/EDColonizationAsst).

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

![EDColonizationAsst cover](/static/images/EDColonizationAsst.png)