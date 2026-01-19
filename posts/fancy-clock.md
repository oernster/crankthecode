---
title: "Fancy Clock"
date: "2026-01-19 02:35"
tags: ["clock", "fancy", "fun", "internationalisation"]
---
I wrote a FancyClock app for fun: [FancyClock](https://github.com/oernster/FancyClock).
This was quite the project since I wanted to knock something up quickly to show off to a friend.
However, it turned out to be more complex as I added more features.

## Current release v1.5.3
- Majorly refactored code to be OO, meet SOLID principles, PEP8 compliant, flake8/black compliant, TDD; all files < 350 lines.
- Created proper flatpak for linux distros; buildable on debian distros such as Ubuntu/Mint or Debian itself.
- Windows support.

### Features: 
- Hour minute and second hands on analogue clock.
- Digital clock including date and day.
- Full internationalization for all time zones throughout the world for natural language support. 
- As part of internationalization, numeral types are supported such as Devanagari/Indic/Bengali/Hindi/Thai/Arabic.
- Ability to search for a city to find your time zone.
- Custom skins with many choices of animated video backgrounds for the analogue clock.

![Fancy Clock cover](/static/images/fancy-clock.png)
