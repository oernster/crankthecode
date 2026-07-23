---
blurb: A Go binary that fixes your PowerShell typos before they execute
date: 2026-02-08 01:00
type: project
role: project
emoji: ⌨️
image: /static/images/commandfixer.svg
one_liner: A lightweight PSReadLine hook that corrects common command-line typos at the moment you press Enter, with your approval.
tags:
- cat:Tools & Libraries
- go
- powershell
- cli
- windows
- developer-tools
thumb_image: /static/images/commandfixer.svg
title: CommandFixer

---

[CommandFixer](https://ernster.dev/CommandFixer/) is a small Go binary that corrects common typing mistakes in PowerShell before the command executes.

Type `git sattus`, press Enter and CommandFixer offers `git status` instead. Approve it and the corrected command runs.

```text
PS> git sattus
CommandFixer: did you mean: git status [Y/n]
On branch main ...
```

The source lives at [CommandFixer](https://github.com/oernster/CommandFixer).

---

## Problem → System → Outcome

**Problem.** Command-line muscle memory produces the same small typos hundreds of times: `git sattus`, `docker pss`, transposed letters in commands typed dozens of times a day. Each one costs a failed run, a re-type and a broken train of thought.

**System.** A PSReadLine hook that intercepts Enter, hands the buffer to a fast Go binary, fuzzy-matches it against a built-in database of popular CLI tools and Windows commands and asks for confirmation when a correction changes the command. No keyboard hooks, no background service.

**Outcome.** The typo tax disappears. Corrections happen at the exact moment of failure, cost one keypress to accept and are logged so the rule set can grow from real behaviour.

---

## How it works

CommandFixer hooks into PSReadLine, which is built into both PowerShell 7 and Windows PowerShell 5. When you press Enter:

1. PSReadLine captures the current buffer.
2. The hook calls `commandfixer suggest <your-command>`.
3. CommandFixer fuzzy-matches the buffer against its built-in command database and prints the corrected form.
4. If the command changed, PowerShell prompts for confirmation.
5. The corrected command executes.

The binary runs in milliseconds. There is no system-wide keyboard hook and no persistent service; the tool exists only for the instant between Enter and execution.

The first version asked you to list every typo as a hand-written rule. Version 2 ships the dictionary instead: a built-in database of popular CLI tools and their valid subcommands (git, docker, kubectl, npm, cargo and many more) plus the standard Windows command set, fuzzy-matched within a configurable threshold. Known PowerShell aliases are recognised exactly, so they are never "corrected".

---

## Deliberate boundaries

The design is defined as much by refusals as by features:

* **Consent per correction.** A changed command never runs silently; the confirmation prompt is the contract.
* **A known command set, not a guess.** Suggestions only ever come from a database of real commands within a similarity threshold, so the tool never invents intent.
* **Uninstall keeps your data.** Removing the tool removes the hook and the binary; the config and the corrections log stay yours unless you ask for them to go.
* **Small surface.** A handful of CLI verbs (`suggest`, `correct`, `install`, `uninstall`, `stats`, `version`) and nothing else.

A JSONL log records every correction and `commandfixer stats` shows what it has fixed: exactly the feedback loop that shows the typo tax being repaid.

---

## At a glance

A single native Go binary hooking both PowerShell 7 and Windows PowerShell 5 per-user with no admin rights: typos corrected at the Enter keypress from a built-in command database, every changed command confirmed before it runs, with correction stats, a JSONL log and a clean uninstall. The full rundown lives on the product site: [ernster.dev/CommandFixer](https://ernster.dev/CommandFixer/).

---

## What this taught me

The best tools live at the moment of failure.

A spelling corrector that runs after the error message has already scrolled past is documentation. One that runs in the gap between Enter and execution is infrastructure.

The other lesson is restraint. The dangerous upgrade path (learning rules automatically, correcting silently, guessing intent) leads to a tool you no longer trust at a prompt that can delete things. Fuzzy matching earned its place in version 2 only because it stays inside a known command set and behind a confirmation.

*A tool that asks first gets to stay installed.*
