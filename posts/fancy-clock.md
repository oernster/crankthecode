---
title: "Fancy Clock"
date: "2026-01-19 02:35"
tags: ["clock", "fancy", "fun", "internationalization", "skins", "video"]
blurb: "Desktop clock"
one_liner: "A customisable desktop clock featuring skins, localisation, and animated/video backgrounds."
# Primary (cover) image used by the site header.
# This will NOT be duplicated in the post body (the renderer strips a matching standalone image).
image: /static/images/fancy-clock.png

extra_images:
  - /static/images/fancy-clock2.jpg
  - /static/images/fancy-clock3.jpg
---
I wrote a FancyClock app for fun: [FancyClock](https://github.com/oernster/FancyClock).

# Challenges along the way
This was quite the project since I wanted to knock something up quickly to show off to a friend
but it turned out to be more complex as I added more features.  Then I decided to add video skins - that was 
a fun challenge but I got there in the end.
The REAL struggle was internationalizing the app.  Multiple languages and timezones throughout the world are HARD
to support.  Especially when you want to support regional numbering systems AS WELL! 

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

![Fancy Clock 2](/static/images/fancy-clock2.png)

![Fancy Clock 3](/static/images/fancy-clock3.png)
