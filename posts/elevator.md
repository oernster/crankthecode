---
title: "Elevator"
date: "2026-01-19 02:30"
tags: ["python", "Django", "React", "control panel"]
blurb: "Elevator control panel"
one_liner: "A web-based elevator control panel built with Django and React."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/elevator.png
---
[Elevator](https://github.com/oernster/elevator)  🛗

I knocked up a simple elevator control panel you can run locally as a website.

## Problem → Solution → Impact

**Problem:** Real-time simulation and control of elevator logic through the browser is rarely intuitive.

**Solution:** This panel offers a live-reactive UI wired to backend logic that simulates elevator behavior.

**Impact:** A flexible demo platform for teaching, prototyping, or gamifying state-driven UI systems.

# Rationale
A fun test of my, at the time, primitive React skillset.

It uses React on the front end with simple HTML buttons that highlight floors/direction etc in colour and Django on the backend.
It supports multiple floor ranges for different lifts and can optimise for the quickest lift based on a request for a floor number.
