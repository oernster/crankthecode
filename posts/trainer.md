---
title: "Trainer"
date: "2026-01-19 07:05"
tags: ["train", "train times", "astronomy", "weather", "routing", "travel"]
blurb: "Travel tracker"
one_liner: "A personal dashboard that brings together travel, weather, and other daily-use data in one place."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/trainer.png

extra_images:
  - /static/images/trainer2.png
  - /static/images/trainer3.png
  - /static/images/trainer4.png
---
I developed: [Trainer](https://github.com/oernster/Trainer).
Train Times with Weather Integration & Astronomical Events

# Challenges along the way
Creating a curated list of all train stops, train lines, underground variants etc. throughout the UK (excluding Northern Ireland) took a lot of time and perseverance.
Finding suitable astronomical sites to be linked was not as straightforward as I desired.
Weather and moon phasing and UI subtleties turned out to be quite the frustration but I ploughed on through until I got it how I wanted it! 

## Overview
A modern PySide6 desktop application that displays real-time train departure information with integrated weather forecasting and astronomical events. 
Features include a dark theme, automatic refresh, and a clean architecture following SOLID principles and modern design patterns.

## Key Features

### Train Information
- Real-time departures with a 16-hour window
- Platform numbers, delays, cancellations, and operator info
- Route planning with interchange support
- Calling points and full service details
- Smart route filtering
- Automatic refresh with configurable intervals

### Weather Integration
- Real-time conditions with detailed metrics
- Seven-day forecast
- Automatic location detection via Open-Meteo
- Weather alerts and warnings
- No API key required
- Automatic refresh with error handling

### Astronomy Features
- Astronomy Picture of the Day with metadata
- ISS real-time tracking
- Space and astronomical events
- Seven-day astronomy calendar
- Moon phases and celestial object visibility
- Educational resource links

### User Interface
- Clean, responsive design with accessibility support
- Light/Dark theme switching
- Modular manager-based architecture
- Adaptive layout for different screen sizes
- Custom widgets for optimal usability
- Keyboard shortcuts (Ctrl+T for theme, F5 for refresh)

### Technical Excellence
- SOLID object-oriented architecture
- Service-oriented design with clear separation of concerns
- Design patterns including Factory, Observer, Strategy, Manager
- Robust error handling with graceful fallbacks
- Optimized performance via caching and lazy loading
- Extensible architecture for future plugins

## API Integration

### Integrated Services
- Open-Meteo API
- Astronomy APIs:
  - APOD
  - ISS
  - NeoWs
  - EPIC

### API Features
- Rate limiting with backoff
- Multi-level caching and invalidation
- Robust error recovery
- Request batching and connection pooling
- Secure key handling

## Development Features

### Code Quality
- SOLID design
- Design patterns throughout
- Clean architecture separation
- Dependency injection
- Detailed error handling

### Performance
- Lazy loading
- Widget pooling
- Intelligent caching
- Memory-efficient resource management
- Responsive layouts

### Testing & Maintainability
- Modular design
- Unit and integration tests
- Complete documentation with diagrams
- Plugin-ready extensibility
