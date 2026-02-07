---
blurb: Travel tracker
date: 2026-01-19 07:05
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

I developed: [Trainer](https://github.com/oernster/Trainer).

Train Times with Weather Integration & Astronomical Events  
[Releases](https://github.com/oernster/Trainer/releases/)

## Problem → Solution → Impact

**Problem:**  
Regular travelers (e.g., consultants/trainers) often have messy or inconsistent travel logging.

**Solution:**  
Trainer Travel Tracker provides a clean interface and backend for routing travel events, timestamps and offers weather to plan.

**Impact:**  
Simplifies trip management and streamlines journey tracking. Also supports astronomy data for fun!

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

## Overview

A modern **PySide6 desktop app** combining train, weather and astronomy info in a modular, performant and elegant interface.  
It adheres to **SOLID principles**, modern design patterns and is plugin-friendly.

---

## Key Features

| Train Information                         | Weather Integration                        |
|-------------------------------------------|---------------------------------------------|
| Real-time departures (16-hour window)     | Live conditions and 7-day forecast         |
| Platform data, delays, operator info      | Automatic geolocation via Open-Meteo      |
| Smart route filtering & interchanges      | Weather warnings, auto-refresh            |
| Service details with calling points       | No API key required                        |

| Astronomy Features                        | User Interface                             |
|-------------------------------------------|---------------------------------------------|
| APOD & ISS real-time tracking             | Clean, responsive layout                   |
| Moon phases & space event calendar        | Light/Dark mode toggle (Ctrl+T)            |
| Object visibility, educational links      | Custom widgets and keyboard shortcuts      |

---

## Technical Highlights

| Code Quality                              | Performance                                 |
|-------------------------------------------|---------------------------------------------|
| SOLID architecture                        | Lazy loading & intelligent caching         |
| Factory, Strategy, Observer, Manager patterns | Optimised memory & widget pooling     |
| Strong separation of concerns             | Responsive layout with graceful fallback    |

| Testing & Maintainability                 | Development Notes                           |
|-------------------------------------------|---------------------------------------------|
| Modular design with plugin support        | Error recovery with graceful fallback       |
| Unit/integration tests with docs          | Dependency injection and clean layering     |

---

## API Integration

| Services                                  | Features                                     |
|-------------------------------------------|----------------------------------------------|
| Open-Meteo                                | Backoff + rate limiting                     |
| NASA APIs: APOD, ISS, NeoWs, EPIC         | Multi-level caching                         |
|                                           | Request batching & secure key handling      |

---

<p align="center"><em>Simple. Efficient. Informative. Built to travel smart.</em></p>