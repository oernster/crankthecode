---
blurb: Elevator control panel
date: 2026-01-19 02:30
type: project
image: /static/images/elevator.png
one_liner: A web-based elevator control panel built with Django and React.
social_image: /static/images/elevator.png
tags:
- cat:Web Apis
- python
- Django
- React
- control panel
title: Elevator
---

[Elevator](https://github.com/oernster/elevator)  🛗

I knocked up a simple elevator control panel you can run locally as a website.

## Problem → Solution → Impact

**Problem:** Real-time simulation and control of elevator logic through the browser is rarely intuitive.

**Solution:** This panel offers a live-reactive UI wired to backend logic that simulates elevator behavior.

**Impact:** People could prototype and teach state-driven UI behaviour with a system that behaved consistently instead of collapsing into edge-case bugs.

# Rationale
A fun test of my, at the time, primitive React skillset.

It uses React on the front end with simple HTML buttons that highlight floors/direction etc in colour and Django on the backend.
It supports multiple floor ranges for different lifts and can optimise for the quickest lift based on a request for a floor number.
