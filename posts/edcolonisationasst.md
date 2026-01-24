---
title: "EDColonisation Assistant"
date: "2026-01-24 18:35"
tags:
  - "elite dangerous"
  - "dashboard"
  - "space sim"
  - "colonisation"
  - "in-game tool"
  - "python"
blurb: "In-game tool for Elite Dangerous"
one_liner: "A browser-based in-game tool for colonisation tracking and planning in Elite Dangerous."
# NOTE: Deployed environments are typically case-sensitive.
# The actual asset filename is `EDColonisationAsst.png`.
image: /static/images/EDColonisationAsst.png
social_image: /static/images/EDColonisationAsst.png
thumb_image: /static/images/edcolonisationasst-icon.png
---

[EDColonisation Assistant](https://github.com/oernster/EDColonisationAsst) 🛰  

## Problem → Solution → Impact

**Problem:** Coordinating colonisation efforts and managing fleet carriers in *Elite Dangerous* lacks a centralised, structured tool ~ especially during station build-outs.

**Solution:** A browser-based cockpit tool that tracks infrastructure requirements, build-out progress, system / station 'shopping lists' and real-time carrier inventory.

**Impact:** Enables commanders to efficiently manage space station construction, resource logistics, and fleet carrier assets ~ streamlining both solo and group colonisation efforts.

---

## Key Features

| Category              | Capabilities                                                                 |
|-----------------------|------------------------------------------------------------------------------|
| **System Tracking**   | - Record system visits<br>- Log planetary base landings<br>                             |
| **Browser UI**        | - Lightweight HUD<br>- Browser-based display<br>- Tablet-friendly layout     |
| **Data Sync**         | - Reads system data from in game journal data<br>- Syncs JSON records        |
| **Mission Planning**  | - Prioritises targets<br>- Filter by criteria<br>                            |

---

## Requirements

- Any modern browser  
- External screen/tablet recommended for cockpit integration  
- *Elite Dangerous* PC/linux edition with Horizons+Odyssey/Trailblazer DLC (Note: Untested on macOS) 

## Usage

1. Go to [Releases](https://github.com/oernster/EDColonisationAsst/releases)  
2. Install the executable
3. Open the page localhost:8000/app in your browser (or your IP if on your wifi network from a tablet)
4. Use keyboard/mouse or touchscreen controls to navigate  
5. Optionally mount to a cockpit tablet for immersion

---

## Ideal For

- Space exploration nerds  
- Individual commanders or groups of players (Note: NOT squadrons) contributing toward colonisation goals  
- Long-range missions needing minimal-distraction tools

---

> “There’s something satisfying about flipping to a local HUD and seeing your shopping list for a station/system construction operation go green on reaching full delivery of a commodity. This is the kind of immersion that even the game itself didn’t build in.”

## Screenshots

![ED Colonisation Assistant Carrier UI](/static/images/EDColonisationAsst2.png)
