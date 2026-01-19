---
title: "Elevator"
date: "2026-01-19 04:30"
tags: ["python", "Django", "React", "control panel"]
blurb: "Elevator control panel"
one_liner: "A web-based elevator control panel built with Django and React."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/elevator.png
---
I knocked up a simple elevator control panel you can run locally as a website: [Elevator](https://github.com/oernster/elevator).

It uses React on the front end with simple HTML buttons that highlight floors/direction etc in colour and Django on the backend.
It supports multiple floor ranges for different lifts and can optimise for the quickest lift based on a request for a floor number.
