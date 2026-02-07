---
date: 2026-01-25 18:30
emoji: "\U0001F9BE"
one_liner: After a major refactor and full triple platform release Stellody 4.1.3
  ships with improved UI cleaner code and much less screaming.
tags:
- cat:Blog
- stellody
- deployment
- flatpak
- refactor
- qt
- release
title: Refactors & Focus Fights for Stellody 4.1.3
---

# Stellody v4.1.3 featuring a major refactor licensing fixes and improved UI across all supported platforms.

---

## 🔄 Codebase Refactoring & Cleanliness

| Change                                | Outcome                                                         |
|--------------------------------------|-----------------------------------------------------------------|
| Enforced ≤ 400 lines per Python file | Improved maintainability and modularity                          |
| Removed stray and unnecessary files  | Cleaner repository footprint                                     |
| Updated architecture docs            | Documentation now matches post refactor structure                 |
| Reorganised UI code                  | Focus and tab logic easier to trace without spelunking through chaos |

This was a large sweeping cleanup. Months of architectural debt were finally reconciled.

*-I complied with SOLID and OO design patterns linted my soul with Black and followed TDD to the gates of hell only to find my app broken and my hope fading.*

---

## 🎛 UI and Interaction Improvements

| Feature                                      | Result                                                        |
|---------------------------------------------|---------------------------------------------------------------|
| Tab ordering and focus behaviour redesigned | Reliable keyboard navigation across dialogs and menus          |
| Tabbing respects light and dark toggle order| Horizontal traversal fixed                                    |
| Theme switching no longer breaks tab memory | Focus restored correctly after theme changes                   |
| Show console output toggle added            | Quieter startup unless explicitly enabled                      |
| Stop active progress toggle added           | No need to shut down the app to stop a run                     |
| Improved font scaling                       | Better text legibility on the Options dialog                   |

*-Qt made the button blink as if to say I thought about helping you and then walked away.*

*-The tab order vanishes when I change my theme like Qt’s internal state is being purged by a witch.*

---

## 📦 Installer & Platform Build Updates

| Platform | Change                                                                |
|----------|------------------------------------------------------------------------|
| Windows  | Installer GUI updated with correct naming and version tagging          |
| macOS   | DMG installer rebuilt with a new launcher script and Nuitka output     |
| Linux   | Flatpak manifest corrected to include license files now accessible     |

All builds were tested validated and deployed cleanly.

 *-Qt finally stopped gaslighting me and started listening. It only took a dozen hacks five hours and me yelling at my monitor like a feral raccoon.*

---

## 📜 Licensing and Compliance

| Update                     | Description                                                         |
|----------------------------|---------------------------------------------------------------------|
| LGPL license files         | Included and accessible in Flatpak builds                            |
| Removed committed binaries | Repository bloat cleaned up from the older build approach            |
| Versioning standardised    | Tags and installer names now follow a predictable pattern             |

*-I included the license file and Flatpak accepted it. It then buried the file in a place my app would never see again.*

---

## 🧪 Testing QA and Regression Coverage

| Area              | Status                                                  |
|-------------------|---------------------------------------------------------|
| Unit tests        | Coverage at around 60 percent PySide6 limitations noted |
| Manual UI testing | Completed across all platforms                          |
| Debug logging     | Silenced post launch after verification                 |

*-I silenced the debug logs I had created not because I did not love them but because the chaos had passed for now.*

---

## 🧱 Git Commit Summary Since v4.0.0

| Area                  | Summary                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| Console output toggle | UI option added to enable or disable console output during app usage     |
| Stop run toggle       | UI option added to stop an active run with confirmation dialog           |
| Visual polish         | Spinner rendering and font size adjustments for readability              |
| Tabbing and focus     | Tabbing order refined across the UI especially dialog buttons            |
| Codebase refactor     | Major restructuring for maintainability redundant files removed          |
| Architecture docs     | Updated to reflect current structure and design philosophy               |
| Build cleanup         | Unnecessary binaries removed from the repository                          |
| Licensing compliance  | License files included and accessible in Flatpak deployments              |
| Versioning consistency| Installer outputs and tags standardised                                   |

---

## Summary

- Major refactor complete  
- UI stable and focus aware  
- Builds deploy cleanly on Windows macOS and Linux  
- Licensing packaged and compliant  
- Live at [stellody.com](https://www.stellody.com)  

Stellody v4.1.3 is the most stable and maintainable release to date.  
Everything hurts a little less now.

*-Onwards but this time with working tab order.*