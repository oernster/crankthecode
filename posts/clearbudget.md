---
blurb: A local solvency model for personal cashflow, bills and credit card pressure
date: 2026-06-14 15:17
type: project
role: project
image: /static/images/clearbudget.png
one_liner: A private desktop budget planner that models monthly solvency, bill timing and credit card pressure before problems arrive.
social_image: /static/images/clearbudget.png
tags:
- cat:Desktop Apps
- python
- budgeting
- finance
- cashflow
- pyside6
- sqlite
thumb_image: /static/images/clearbudget-icon.png
title: Clear Budget

---

[ClearBudget](https://ernster.dev/ClearBudget/) is a private desktop budget planner built around a question rather than a ledger.

Most budgeting software is retrospective. It answers *where did the money go?* ClearBudget answers a forward question instead: *will the month survive?*

Not in aggregate. Not once every payment has landed. Day by day, bill by bill, card by card.

---

## Problem → System → Outcome

**Problem.** Budgeting tools are retrospective: they tell you where the money went, long after a healthy monthly total has hidden a structurally unsafe month, one where income lands late, bills cluster early and an affordable month-end payment is impossible on the day it falls.

**System.** A local-first desktop model that projects the balance forward day by day, bill by bill and card by card: credit cards as pressure systems, per-month overrides, isolated multi-user state, the projection logic in a pure domain on a four-layer architecture.

**Outcome.** You see the tightest day of the month and any mid-month overdraft dip before it arrives, up to six months out, early enough to act. I open it to decide whether my own month holds.

---

## Why it exists

A monthly total can look safe while the month itself is structurally unsafe.

Income arrives late. Bills cluster early. A card stays under its limit while its trajectory points the wrong way. A payment is affordable at month end and impossible on the day it actually lands.

ClearBudget models the operational shape of a month instead of treating money as a flat number. The result is not a prettier ledger.

*It is a local decision system for personal solvency.*

---

## The decision-architecture lens

I write about decision architecture: the idea that organisations behave according to how decisions are structured, constrained and allowed to interact. Software is the same problem at a smaller scale. A codebase is a frozen record of past decisions; a personal budget is a live one.

So I built ClearBudget the way I think. Each feature is a decision made explicit and given somewhere to resolve:

- a per-month **skip** or **override** is the decision *"this obligation does not apply this month"*, made first-class instead of held in your head
- a **paid** flag is *"this money has already left"*, so a settled bill stops distorting what is still due
- a **read-only viewer package** is an authority boundary: full visibility, no edit rights, enforced on every screen rather than one
- the **solvency panel** is the termination point, where scattered obligations resolve into a single answer

*Once state is explicit, the decisions on top of it become smaller.*

---

## What it does

The solvency panel projects the balance forward and flags the tightest moment in the month; credit cards model as pressure systems with live pro-rated balances; per-month overrides, skips and paid or received flags absorb real-world irregularity; multiple users get isolated per-user databases behind a bcrypt sign-in; everything is local-first across Windows, macOS and Linux. The feature catalogue lives on the product site: [ernster.dev/ClearBudget](https://ernster.dev/ClearBudget/).

---

## I use it every day

This is dogfood, in the full sense of the expression. ClearBudget is not a portfolio piece I built and walked away from; it is the application I open to decide whether my own month holds together. The failure modes it models are ones I have hit. The features exist because I needed them, not because they demonstrated well. A solvency tool that produces false confidence is worse than none at all, and the surest way I know to keep one honest is to depend on it myself.

---

## What it taught me

A tool becomes useful when it models the real decision boundary.

A monthly total hides timing risk. A transaction list arrives too late. A category breakdown does not expose pressure. A balance without a projection hides its own trajectory.

The useful model is the one that surfaces the failure mode early enough to act on it. That is why ClearBudget tracks solvency rather than accounting. It is not trying to describe money perfectly; it is trying to answer the only operational question that matters in the moment:

*What breaks next, and when?*

---

The value is not that ClearBudget stores financial data.

*The value is that it turns scattered obligation into an explicit operational model, the kind you can actually make a decision against.*
