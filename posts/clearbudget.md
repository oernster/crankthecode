---
blurb: A local solvency model for personal cashflow, bills and credit card pressure
date: 2026-06-11 08:30
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

[ClearBudget](https://github.com/oernster/ClearBudget/releases) is a private desktop budget planner focused on solvency rather than expense tracking.

Most budgeting software answers a retrospective question:

*Where did the money go?*

ClearBudget was built to answer a different one:

*Will the month survive?*

Not in aggregate.
Not once all income has landed.
Not after the damage is done.

*Day by day.
Bill by bill.
Card by card.*

---

## Why this exists

A monthly total can look safe while the month itself is structurally unsafe.

Income may arrive late.
Bills may cluster early.
Credit card minimum payments may hide rising balances.
A payment may be affordable at month end but impossible on the day it lands.

That is the gap ClearBudget was built to expose.

The application models the operational shape of a month rather than treating money as a flat number.

It tracks:

* expected income
* bill timing
* skipped obligations
* bank vs credit card payments
* credit card utilisation
* minimum payment pressure
* future balance projection
* mid-month solvency risk

The result is not a prettier ledger.

*It is a local decision system for personal solvency.*

---

## Core behaviour

* Month-by-month budget planning
* Income tracking with reliability markers
* Per-month income overrides, skips and one-off entries
* Bill tracking with categories and due days
* Per-bill active, skip and paid controls
* One-month bill skips without deleting templates
* Bank and credit card payment methods
* Credit card balances, limits, APRs and due dates
* Minimum payment modelling
* Live, pro-rated credit card balance projection
* Forward solvency projection
* Mid-month overdraft dip warnings, with an optional overdraft facility
* Archive snapshots for completed months
* Read-only viewer accounts and viewer packages
* Local SQLite persistence
* Database import and export

---

### Multi-user login system

ClearBudget now supports isolated user accounts with secure authentication.

Features include:

* first-run admin setup wizard
* self-service account creation from the login screen
* per-user encrypted login credentials
* isolated user databases
* password recovery codes
* user switching without restarting
* admin-only user management
* read-only viewer accounts
* secure account deletion, data is always removed with the account

The goal was simple:

*Multiple people should be able to use the application on the same machine without sharing financial state.*

Only the very first account ever created is an admin. Every account created afterwards, whether from the login screen or via user management, is non-admin by default.

---

### Read-only viewer access

Sometimes someone needs visibility without edit rights. A partner. An accountant. A future version of yourself, checking in.

ClearBudget supports read-only viewer accounts:

* an admin can export a snapshot of the budget database as a viewer package
* a viewer imports that package directly from the login screen
* a viewer sees the full Monthly Budget, Solvency and Credit Card views
* every destructive or editing action is disabled and visually marked

*Read-only mode is read-only everywhere, not just on one screen.*

---

### Display currency selection

The application now supports 25 display currencies covering major English-speaking territories.

Currency changes apply immediately across:

* tables
* labels
* solvency panels
* credit card projections
* dialogs
* projections

*The setting is stored per-user inside the local database.*

---

### Desktop workflow improvements

Several usability improvements were added to make the application feel more like a polished desktop tool rather than a prototype:

* Import / Export grouped into its own File menu submenu
* live database reload after import
* automatic table column sizing
* destructive action confirmations
* fresh-start "New Budget" workflow
* "How It Works" help dialog covering pro-rating, balances and archiving
* reworked navigation header with centred month controls
* dark theme contrast and colour rework
* sensible default window size and position

---

## Solvency

The solvency panel is the heart of the application.

It answers the question the budget view alone cannot:

*Does this month actually hold together?*

A month can have enough total income while still containing a temporary overdraft.
A card can remain under its limit while still moving toward failure.
A payment can be affordable overall while landing on the wrong day.

ClearBudget models those conditions directly.

The solvency system tracks:

* projected balances
* committed obligations
* remaining bank payments
* remaining card payments
* utilisation pressure
* minimum payments
* interest drag
* overdraft facility headroom and interest cost
* six-month forward risk

If the projected balance dips below zero at any point in the month, even when the month ends positive, the panel raises a warning:

* amber, with the day it happens and an estimated daily interest cost, when an overdraft facility covers the dip
* red, when there is no facility, or when the dip would exceed the facility limit

This turns vague financial anxiety into explicit state.

*Once the state is explicit, decisions become smaller.*

---

## Credit cards

Credit cards are not treated as static debt numbers.

They are treated as pressure systems.

Each card tracks:

* current balance
* credit limit
* APR
* due day
* minimum payment rules
* projected closing balances
* utilisation trend

That distinction matters because a credit card balance is not only money owed.

It is:

* future interest
* minimum payment drag
* reduced headroom
* compressed future cashflow

The credit card view itself moved from a single wide table to a scrollable list of per-card panels, each showing status, limits, utilisation and this month's activity, with edits handled through one consistent dialog.

*ClearBudget keeps those pressures visible before they become irreversible.*

---

## Local first

ClearBudget is intentionally local software.

The database lives on the machine.
The interface runs as a desktop application.
The model does not depend on bank integrations or hosted infrastructure.

That decision was deliberate.

Personal finance contains highly sensitive behavioural data even when account numbers are absent.

Income timing, debt pressure, payment sequencing and solvency risk are private operational information.

The problem did not require cloud infrastructure.

*It required explicit state and predictable behaviour.*

---

## Architecture

ClearBudget is built with:

* Python 3.11+
* PySide6
* SQLite
* bcrypt password hashing
* local-first persistence

The complexity is not scale.

The complexity is correctness.

A projection system that produces false confidence is worse than no projection at all.

*The application therefore focuses heavily on explicit state transitions, timing correctness and predictable month modelling.*

---

## ClearBudget at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Month-by-month budget planning</li>
    <li>Income and bill management</li>
    <li>Reliable income markers</li>
    <li>Per-month income and bill overrides</li>
    <li>Bill categories, due days and paid tracking</li>
    <li>Per-month bill skips</li>
    <li>Bank and credit card payment methods</li>
    <li>Solvency status calculation</li>
    <li>Mid-month overdraft dip warnings</li>
    <li>Optional overdraft facility modelling</li>
    <li>Credit card utilisation tracking</li>
    <li>Interest and minimum payment modelling</li>
    <li>Live, pro-rated card balance projection</li>
    <li>Forward balance projection</li>
    <li>Archive snapshots</li>
    <li>Database import/export</li>
    <li>Read-only viewer accounts</li>
    <li>Multi-user authentication</li>
    <li>Per-user budget isolation</li>
    <li>Display currency selection</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technology</h3>
  <ul>
    <li>Python 3.11+</li>
    <li>PySide6 desktop interface</li>
    <li>SQLite local database</li>
    <li>bcrypt password hashing</li>
    <li>Dark theme UI</li>
    <li>Local-first architecture</li>
    <li>Open source repository</li>
  </ul>
</div>

</div>

---

## What this taught me

ClearBudget reinforced a familiar engineering lesson:

A tool becomes useful when it models the real decision boundary.

A monthly total hides timing risk.
A transaction list arrives too late.
A category breakdown does not expose pressure.
A credit card balance without projection hides trajectory.

The useful model is the one that exposes the failure mode early enough to act.

That is why ClearBudget focuses on solvency rather than accounting.

It is not trying to describe money perfectly.

It is trying to answer the operational question:

*What breaks next and when?*

---

ClearBudget is a working example of software built around structural clarity.

The value is not that it stores financial data.

*The value is that it turns scattered obligation into an explicit operational model.*