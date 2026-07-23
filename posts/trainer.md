---
blurb: Travel tracker
date: 2026-01-19 07:05
type: project
extra_images:
- /static/images/trainer2.png
- /static/images/trainer3.png
- /static/images/trainer4.png
image: /static/images/trainer.png
one_liner: A personal dashboard that brings together travel, weather and other daily-use
  data in one place.
social_image: /static/images/trainer.png
tags:
- cat:Desktop Apps
- train
- train times
- astronomy
- weather
- routing
- travel
- python
thumb_image: /static/images/trainer-icon.png
title: Trainer
---

[Trainer](https://ernster.dev/Trainer/) is a desktop dashboard for train times with weather integration and astronomical events.

[Releases](https://github.com/oernster/Trainer/releases/)

## Problem → System → Outcome

**Problem.**  
Regular travelers (e.g., consultants/trainers) often have messy or inconsistent travel logging.

A common pattern appears in travel tools. They optimise for finding a route, not for staying aligned with a real journey as it unfolds.

**System.**  
Trainer Travel Tracker provides a clean interface and backend for routing travel events, timestamps and offers weather to plan.

**Outcome.** Journeys stayed consistent across planning and real travel: times, stops, weather and context were visible without bouncing between sites or losing state.

---

## Rationale

I wanted a train scheduling app that let me look up times without the frustrating ads you see on sites like [thetrainline.com](https://www.thetrainline.com).  
Then I wanted to know if I needed an umbrella or coat ~ so I added weather support.  
Finally, I tossed in astronomy visuals (moon phase, ISS tracking, etc.) for flair and personal interest ~ I have a degree in physics, after all.

---

## Challenges Along the Way

- Curating every train stop and route (excluding Northern Ireland) was a massive task.
- Finding reliable astronomy sources was harder than expected.
- Weather APIs and moon phase integrations added UI complexity ~ but I pushed through until it felt right.

---

## What it does

A modern **PySide6 desktop app** combining real-time departures with platforms, delays and calling points, route planning with interchanges, destination weather via Open-Meteo with no API key and an astronomy view with moon phases and a seven-day outlook, in one dark Material interface with a light mode a keystroke away. The full feature catalogue lives on the product site: [ernster.dev/Trainer](https://ernster.dev/Trainer/).

---

<p align="center"><em>Simple. Efficient. Informative. Built to travel smart.</em></p>
