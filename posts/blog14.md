---
title: "Raising Test Coverage Without Breaking Trust"
date: "2026-01-28 19:30"
tags: ["blog", "stellody", "testing", "refactor", "quality"]
one_liner: "Higher coverage only matters if the tests survive refactors and real use."
emoji: "⚖️"
---

# Stellody: Raising Test Coverage Without Breaking Trust

With the major refactor work complete I turned to improving unit test coverage. Stellody was already sitting at around 57 percent which is perfectly reasonable for a PySide6 application but there was clear opportunity to increase confidence without chasing a meaningless number.

This is not exciting work but it is necessary if the codebase is going to continue evolving without fear. The focus was not on coverage for its own sake but on strengthening tests around logic that is both critical and stable over time.

Test case coverage is now sitting at around 63 percent. Given the realities of testing PySide6 this is a level I am comfortable defending.

*-The guiding principle was simple: coverage is a signal not a goal.*

My slightly controversial take:

*-Tests are tools not talismans. If your suite breaks when the code grows up you are worshipping assertions not quality.*

---

## 🎯 What Was Tested More Heavily

Coverage was increased selectively in areas where tests add long term value and are unlikely to become brittle.

Core domain logic and models were expanded to cover edge cases and failure modes. ETA prediction and smoothing logic was exercised across realistic scenarios rather than synthetic happy paths. Progress aggregation and lifecycle state transitions now have stronger guarantees and deterministic error handling paths are covered explicitly.

*-These areas now have strong coverage because they are logic heavy observable and unlikely to change shape frequently.*

---

## 🚫 What Was Intentionally Left Alone

Some parts of the system were deliberately not chased for coverage.

Qt widget rendering and layout logic were left alone along with trivial signal wiring that had been already exercised indirectly through integration paths. Timing sensitive behaviour and thread interleaving logic was also avoided along with glue code where tests would simply mirror implementation details.

*-Tests that depend on sleeps real time delays or fragile signal ordering were explicitly avoided.*

---

## 🧭 Testing Philosophy

Every new test answers a single question: will this still be useful after the next refactor.

Tests assert behaviour not structure. They are deterministic fast and intentionally boring. Where necessary logic is extracted out of Qt to make it testable which is another way of saying that Qt remains a beautiful dumpster fire and I am tired.

If a test feels awkward, brittle, or over specified it is usually exposing a design smell rather than a testing gap.

*-This approach naturally increases coverage where it matters and leaves the rest alone.*

---

## 🏁 Final Words

Good test suites build confidence not anxiety.

By focusing on durable tests instead of chasing numbers, Stellody now has higher coverage that actually means something and a test suite that can be trusted to stay out of the way as the code continues to evolve.

Or more sardonically:

*-Well written tests survive refactors. The rest are just expensive opinions with assertion statements.*
