---
blurb: A local solvency model for personal cashflow, bills and credit card pressure
date: 2026-06-12 20:00
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

[ClearBudget](https://github.com/oernster/ClearBudget) is a private desktop budget planner built around a question rather than a ledger.

Most budgeting software is retrospective. It answers *where did the money go?* ClearBudget answers a forward question instead: *will the month survive?*

Not in aggregate. Not once every payment has landed. Day by day, bill by bill, card by card.

[Releases](https://github.com/oernster/ClearBudget/releases)

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

**Solvency, day by day.** The solvency panel is the core. It projects the balance forward and flags the tightest moment in the month, not just the month-end figure. If the balance dips below zero at any point it warns: amber, with the day and an estimated daily interest cost, when an overdraft facility (limit and APR) covers the dip; red when there is no facility or the dip would exceed it. Forward risk runs six months out.

**Credit cards as pressure systems.** A card balance is not a static number owed; it is future interest, minimum-payment drag and shrinking headroom. Each card models its limit, APR, due day, minimum payment and utilisation, with a live pro-rated balance that accrues through the month and a projected closing balance for months ahead. Cards display as scannable per-card panels rather than one unreadably wide table.

**Per-month flexibility, bills and income at parity.** Overrides, skips, a "paid" flag for bills and a "received" flag for income, plus one-off *"this month only"* income that never touches your recurring templates. Real months are irregular; the model lets you say so without editing the underlying plan.

**Multiple people, isolated state.** First-run admin setup, self-service account creation, per-user databases, bcrypt-hashed credentials with recovery codes, user switching without a restart, and admin management. Deleting an account always deletes its data with it, so destroyed credentials can never be recreated to reach data left orphaned behind them.

**Local-first, now cross-platform.** The database lives on your machine. No bank integrations, no hosted infrastructure: personal finance is sensitive behavioural data even without account numbers, and this problem never needed the cloud. The same codebase now ships natively on Windows, macOS and Linux, with the identical model on each. Add 25 per-user display currencies, archive snapshots of completed months, and validated database import and export.

**A finished tool, not a prototype.** A built-in "How It Works" guide explains the pro-rating and projection logic in plain English; a consistent dark theme and a unified navigation header colour-code the current month by financial health (green, amber, red); and the layout stays readable from a 13-inch laptop to a 4K display.

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

## ClearBudget at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Day-by-day solvency projection</li>
    <li>Mid-month overdraft dip warnings</li>
    <li>Optional overdraft facility (limit, APR, interest cost)</li>
    <li>Six-month forward risk</li>
    <li>Credit card pressure modelling</li>
    <li>Live, pro-rated card balance projection</li>
    <li>Per-month bill and income overrides, skips, paid/received</li>
    <li>One-off "this month only" income</li>
    <li>Archive snapshots for completed months</li>
    <li>Multi-user accounts with per-user isolation</li>
    <li>Read-only viewer packages</li>
    <li>25 display currencies; database import/export</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Built with</h3>
  <ul>
    <li>Python 3.11+</li>
    <li>PySide6 desktop interface</li>
    <li>SQLite, local-first</li>
    <li>bcrypt authentication</li>
    <li>Windows, macOS and Linux</li>
    <li>Dark theme; open source</li>
  </ul>
</div>

</div>

---

The value is not that ClearBudget stores financial data.

*The value is that it turns scattered obligation into an explicit operational model, the kind you can actually make a decision against.*
