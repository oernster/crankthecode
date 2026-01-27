---
title: "Refactors & Focus Fights for Stellody 4.1.3"
date: "2026-01-25 18:30"
tags: ["blog", "stellody", "deployment", "flatpak", "refactor", "qt", "release"]
one_liner: "After a heroic refactor/full triple-platform release, Stellody 4.1.3 is live with improved UI, cleaner code and a lot less screaming."
---
# [Stellody v4.1.3](https://www.stellody.com) ~ featuring a major refactor, licensing fixes and improved UI across all supported platforms.

---

## 🔄 Codebase Refactoring & Cleanliness

| Change                                  | Outcome                                                               |
|----------------------------------------|-----------------------------------------------------------------------|
| Enforced ≤ 400 lines per Python file   | Improved maintainability and modularity                              |
| Removed stray/unnecessary files        | Cleaner repo footprint                                               |
| Updated Architecture docs              | Documentation now matches post-refactor structure                    |
| Reorganised UI code                    | Easier to trace focus/tab logic without spelunking through chaos     |

This was a large, sweeping cleanup ~ months of architectural debt finally reconciled.

> I complied with SOLID, OO design patterns, linted my soul with Black and followed TDD to the gates of hell; only to find my app broken and my hope fading.

---

## 🎛 UI and Interaction Improvements

| Feature                                       | Result                                                               |
|----------------------------------------------|----------------------------------------------------------------------|
| Tab ordering and focus behaviour redesigned  | Reliable keyboard navigation across dialogs and menus               |
| Tabbing respects light/dark toggle order      | Horizontal traversal fixed                                           |
| Theme switching no longer breaks tab memory  | Focus correctly restored after theme changes                        |
| “Show console output” toggle button added    | Quieter startup unless explicitly enabled                           |
| “Stop active progress” toggle button added   | Avoids the need to shutdown the app to stop a run                   |
| Improved font scaling                        | Better text legibility on Options dialog                            |

> Qt made the button blink, as if to say 'I thought about helping you' and then walked away.

> The Tab Order Vanishes When I Change My Theme.  Like Qt’s Internal State Is Being Purged by a Witch.

---

## 📦 Installer & Platform Build Updates

| Platform | Change                                                                 |
|----------|------------------------------------------------------------------------|
| Windows  | Installer GUI updated; correct naming and version tagging             |
| macOS    | DMG installer rebuilt with new launcher script and Nuitka output      |
| Linux    | Flatpak manifest corrected to include license files (now accessible)  |

All builds tested, validated and deployed cleanly.

> “Qt finally stopped gaslighting me and started listening. It only took a dozen hacks, five hours and me yelling at my monitor like a feral raccoon.”

---

## 📜 Licensing and Compliance

| Update                              | Description                                                                 |
|-------------------------------------|-----------------------------------------------------------------------------|
| LGPL license files                  | Now included and accessible in Flatpak builds                               |
| Removed committed binaries          | Cleaned up repository bloat from older build approach                        |
| Versioning standardised             | Tags and installer names now follow a consistent, predictable pattern       |

> I included the license file and Flatpak accepted it.  However, it buried the file in a place my app would never see again!

---

## 🧪 Testing, QA and Regression Coverage

| Area                | Status                                             |
|---------------------|----------------------------------------------------|
| Unit Tests          | Coverage at ~60% (PySide6 limitations acknowledged) |
| Manual UI Testing   | Completed across all platforms                      |
| Debug logging       | Silenced post-launch after verification             |

> I silenced the debug logs I'd created; not because I didn’t love them but because the chaos had passed… for now.

---

## 🧱 Git Commit Summary Since v4.0.0

| Area                     | Summary                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| Console Output Toggle    | UI option added to enable or disable console output during app usage.   |
| Stop Run Toggle          | UI option added to stop an active run with confirmation dialog.         |
| Visual Polish            | Adjustments to spinner rendering and font sizes for better readability. |
| Tabbing & Focus Logic    | Tabbing order refined across the UI, especially for dialog buttons.     |
| Codebase Refactor        | Major restructuring for maintainability; redundant files removed.       |
| Architecture Docs        | Updated to reflect the current structure and design philosophy.         |
| Build Cleanup            | Removed unnecessary binaries from the repository.                       |
| Licensing Compliance     | License files now included and accessible in Flatpak deployments.       |
| Versioning Consistency   | All installer outputs and tags now follow a standardised format.        |

---

## Summary

- Major refactor complete  
- UI is stable and focus/tab-aware  
- Builds deploy cleanly on Windows, macOS and Linux  
- Licensing is packaged and compliant  
- Live at [stellody.com](https://www.stellody.com)  

Stellody v4.1.3 marks the most stable and maintainable release to date.  
Everything hurts a little less now.

🛠 Onwards ~ but this time with working tab order.
