---
title: "Raising Test Coverage Without Breaking Trust"
date: "2026-01-28 19:30"
tags: ["blog", "stellody", "testing", "refactor", "quality"]
one_liner: "Higher coverage only matters if the tests survive refactors and real use."
emoji: "⚖️"
---
## Stellody: Raising Test Coverage Without Breaking Trust

With the major refactor work complete, I turned to improving unit test coverage. Stellody was already sitting at around 57 percent which is perfectly reasonable for a PySide6 application, but there was clear opportunity to improve confidence without chasing an unrealistic number.  This is not an exciting job but it is necessary to maintain good code quality going forward. 
I've made some changes to increase confidence meaningfully in the highest-value, most failure-prone logic while keeping tests stable across refactors.
> Test case coverage is now sitting at an enhanced level of 63%; given that covering PySide6 with unit tests is flaky I feel this is reasonable. 

*- The guiding principle was simple: **coverage is a signal, not a goal**.*

My somewhat controversial take: *- Tests are tools, not talismans. If your suite breaks when the code grows up, you’re worshipping assertions, not quality.*

---

## 🎯 What Was Tested More Heavily

Coverage was increased only where tests add long term value and remain stable over time:

- Core domain logic and models.
- ETA prediction and smoothing logic across realistic scenarios.
- Progress aggregation and lifecycle state transitions.
- Deterministic error handling paths.

*- These areas now have strong coverage because they are logic heavy, observable and unlikely to change shape frequently.*

---

## 🚫 What Was Intentionally Left Alone

Some parts of the system were deliberately not chased for coverage:

- Qt widget rendering and layout.
- Trivial signal wiring already exercised indirectly.
- Timing sensitive or thread interleaving behaviour.
- Glue code where tests would mirror implementation details.

*- Tests that depend on sleeps, real time delays or fragile signal ordering were explicitly avoided.*

---

## 🧭 Testing Philosophy

Every new test answers one question: *will this still be useful after the next refactor*.

- Tests assert behaviour, not structure.
- Tests are deterministic, fast and boring.
- Logic is extracted out of Qt where necessary to make it testable. (Translation: “Qt is a beautiful dumpster fire and I’m tired!”)
- If a test feels brittle or awkward, it is usually a design smell.

*- This approach naturally increases coverage where it matters and leaves the rest alone.*

---

## 🏁 Final words...

Good test suites build confidence, not anxiety.

*- By focusing on durable tests instead of numbers, Stellody now has higher coverage that actually means something and a test suite that can be trusted to stay out of the way as the code continues to evolve.*

Or, more sardonically: *- Well-written tests survive refactors. The rest are just expensive opinions with assertion statements.*