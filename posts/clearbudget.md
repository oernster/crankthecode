---
blurb: A local solvency model for personal cashflow, bills and credit card pressure
date: 2026-05-20 08:30
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
title: ClearBudget

---

[ClearBudget](https://github.com/oernster/ClearBudget/releases) is a private desktop budget planner that models monthly solvency, bill timing and credit card pressure before problems arrive.

---

ClearBudget is not a spending tracker.

It is a solvency model.

Most budgeting tools answer a retrospective question:

*Where did the money go?*

That is useful but it is not the question I needed answered.

The question I needed answered was sharper:

*Will the month survive?*

Not in theory.
Not in aggregate.
Not once all income and bills have conveniently landed.

Day by day.
Bill by bill.
Card by card.
Before the damage happens.

---

## Why this exists

A monthly budget total can look safe while the month itself is structurally unsafe.

Income may arrive late.
Bills may cluster early.
Credit card minimum payments may hide rising balances.
A payment may be affordable at month end but impossible on the day it is due.

That is the gap ClearBudget was built to expose.

The app models the operational shape of a month rather than treating money as a single flat total.

It asks:

* What income is expected?
* Which income is reliable?
* Which bills are active this month?
* Which bills are skipped this month?
* Which payments hit the bank?
* Which payments hit a credit card?
* What happens before the next income date?
* What happens next month?
* What happens if credit card utilisation keeps rising?

The result is not a prettier ledger.

*It is a local decision system for personal solvency.*

---

## Core behaviour

* Month-by-month budget planning
* Income tracking with reliability markers
* Bill tracking with categories and due days
* Per-bill active and skip controls
* One-month bill skips without deleting the underlying template
* Bank and credit card payment methods
* Credit card balances, limits, APRs and due dates
* Minimum payment modelling
* Month-end card balance projection
* Forward solvency projection
* Mid-month overdraft detection
* Archive snapshots for completed months
* Local SQLite persistence
* Database import and export

---

## Problem → system → outcome

**Problem:**
A budget can appear solvent when viewed as a monthly total while still becoming unsafe inside the month because of timing, debt pressure or bill clustering.

**System:**
ClearBudget models income, bills, due days, credit cards, minimum payments and future balances as explicit state. It projects the month forward instead of only recording what has already happened.

**Outcome:**
The user can see whether the month is safe, where the risk sits and which obligations create pressure before the bank account proves it the hard way.

---

## Monthly budget

The monthly budget view is the operational surface.

It shows the selected month, expected income, committed bills and projected balance.

Bills are not treated as anonymous numbers. They have names, amounts, categories, payment methods, due days, active states and skip states.

This matters because the behaviour of a bill depends on more than its value.

A rent payment due on day one is structurally different from a subscription due after income lands.
A bill paid from the bank account has a different cashflow effect from a bill placed on a credit card.
A skipped credit card payment has a different consequence from a skipped discretionary expense.

ClearBudget keeps those differences visible.

*The point is not to store transactions. The point is to preserve the structure of obligation.*

---

## Solvency

The solvency view is the heart of the application.

It answers the question the budget view alone cannot answer:

*Does this month actually hold together?*

It separates headline balance from operational safety.

A month can have enough total income and still contain a temporary overdraft.
A credit card can be under its limit and still be moving in the wrong direction.
A payment can be mathematically affordable and still land on the wrong day.

ClearBudget models those conditions directly.

The solvency panel presents:

* overall safety status
* projected balance
* committed monthly obligations
* remaining bank payments
* remaining card payments
* credit card utilisation
* card interest
* minimum payments
* month-end card balances
* forward risk over the next months

This turns vague financial anxiety into explicit state.

*Once the state is explicit, decisions become smaller.*

---

## Credit cards

Credit cards are not modelled as simple debts.

They are modelled as pressure systems.

Each card has:

* a credit limit
* a current balance
* an APR
* a payment due day
* an optional expiry date
* a minimum payment rule
* an active state

The application tracks utilisation and projects future closing balances.

That distinction matters.

A card balance is not only a number owed.
It is future cashflow.
It is interest.
It is minimum payment drag.
It is available headroom.
It is risk compression.

ClearBudget makes that visible by showing card status, projected balances and colour-coded headroom across a six-month projection.

The goal is not moral judgement.

*The goal is mechanical clarity.*

---

## Archive

The archive exists because a month is a stateful object.

Once a month is complete, it can be preserved as a snapshot.

That snapshot records the income, bills, balance and solvency status for the period.

This gives the application memory without turning it into a bank-feed transaction system.

The archive answers a different question:

*What did this month look like when it was closed?*

That is useful because planning systems need continuity.

*A future month is easier to reason about when past months are not rewritten accidentally.*

---

## Local first

ClearBudget is local software.

The database lives on the machine.
The interface runs as a desktop application.
The model does not depend on a hosted service, a bank integration or a third-party finance platform.

That is deliberate.

Personal financial planning contains sensitive information even when no account numbers are present.

Income timing, rent, benefits, debt levels, family support, creditors and payment pressure are all private.

A cloud budgeting tool may offer convenience but the modelling problem here did not require cloud infrastructure.

It required explicit state, local persistence and predictable behaviour.

*Private data should not leave the machine just because the software wants a dashboard.*

---

## Architecture

ClearBudget is built as a PySide6 desktop application backed by SQLite.

The architecture is intentionally direct.

The application has to manage a small but important domain:

* monthly budget state
* recurring bill templates
* monthly bill skips and overrides
* income records
* credit card state
* projected balances
* archive records
* import and export validation

The complexity is not in scale.

The complexity is in correctness.

A wrong projection is worse than no projection because it creates false confidence.

That means the model has to be careful about how it treats timing, skipped items, credit card payments and future months.

*The hard part is not drawing tables. The hard part is deciding what the tables mean.*

---

## ClearBudget at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Month-by-month budget planning</li>
    <li>Income and bill management</li>
    <li>Reliable income markers</li>
    <li>Bill categories and due days</li>
    <li>Per-month bill skips</li>
    <li>Bank and credit card payment methods</li>
    <li>Solvency status calculation</li>
    <li>Mid-month overdraft detection</li>
    <li>Credit card utilisation tracking</li>
    <li>Credit card interest and minimum payment modelling</li>
    <li>Forward balance projection</li>
    <li>Monthly archive snapshots</li>
    <li>Database import and export</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technology</h3>
  <ul>
    <li>Python 3.11+</li>
    <li>PySide6 desktop interface</li>
    <li>SQLite local database</li>
    <li>Dark theme UI</li>
    <li>Local-first data model</li>
    <li>Open source repository</li>
  </ul>
</div>

</div>

---

## Why not screenshots?

ClearBudget is visual software but the screenshots are not the product.

The product is the model.

Real screenshots expose too much.
Personal finance data is sensitive even when partially redacted.

Dummy screenshots create a different problem.
If the numbers are too clean, they look artificial.
If they are realistic, they invite speculation.

So the public write-up focuses on the structure instead.

That is the more honest representation of the work.

The important thing is not a table of private numbers.

*The important thing is the system that makes those numbers interpretable.*

---

## What this taught me

ClearBudget reinforced a familiar lesson:

A tool becomes useful when it models the real decision boundary.

A normal monthly total hides too much.
A transaction list arrives too late.
A generic category breakdown does not explain timing risk.
A credit card balance without projection does not show pressure.

The useful model is the one that exposes the failure mode early enough to act.

That is why ClearBudget focuses on solvency rather than accounting.

It is not trying to describe money perfectly.

It is trying to answer the operational question:

*What breaks next and when?*

---

## Development notes

ClearBudget is intentionally pragmatic.

It is not a fintech platform.
It is not a bank replacement.
It is not a double-entry accounting system.

It is a personal desktop model for household cashflow pressure.

The design priorities are:

* privacy
* predictability
* clear state
* explicit timing
* useful projection
* low operational friction

The application exists because the problem was concrete.

The month either works or it does not.

*ClearBudget makes that visible before the month decides for you.*

---

ClearBudget is a working example of software built around structural clarity.

The value is not that it stores financial data.

The value is that it turns scattered obligation into an explicit model.

*Once the model exists, the anxiety has somewhere to go.*