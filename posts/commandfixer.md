---
blurb: A Go binary that fixes your PowerShell typos before they execute
date: 2026-02-08 01:00
type: project
role: project
emoji: ⌨️
image: /static/images/commandfixer.svg
one_liner: A lightweight PSReadLine hook that corrects common command-line typos at the moment you press Enter, with your approval.
tags:
- cat:Tools
- go
- powershell
- cli
- windows
- developer-tools
thumb_image: /static/images/commandfixer.svg
title: CommandFixer

---

[CommandFixer](https://oernster.github.io/CommandFixer/) is a small Go binary that corrects common typing mistakes in PowerShell before the command executes.

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

**System.** A PSReadLine hook that intercepts Enter, hands the buffer to a fast Go binary, applies user-defined correction rules from a JSON config and asks for confirmation when a correction changes the command. No keyboard hooks, no background service.

**Outcome.** The typo tax disappears. Corrections happen at the exact moment of failure, cost one keypress to accept and are logged so the rule set can grow from real behaviour.

---

## How it works

CommandFixer hooks into PSReadLine, which is built into both PowerShell 7 and Windows PowerShell 5. When you press Enter:

1. PSReadLine captures the current buffer.
2. The hook calls `commandfixer suggest <your-command>`.
3. CommandFixer loads the rules, applies them and prints the corrected form.
4. If the command changed, PowerShell prompts for confirmation.
5. The corrected command executes.

The binary runs in milliseconds. There is no system-wide keyboard hook and no persistent service; the tool exists only for the instant between Enter and execution.

Corrections are user-defined rules in a JSON config:

```json
{
  "typos": [
    { "from": "git sattus", "to": "git status" },
    { "from": "docker pss", "to": "docker ps" }
  ]
}
```

---

## Deliberate boundaries

The design is defined as much by refusals as by features:

* **Consent per correction.** A changed command never runs silently; the confirmation prompt is the contract.
* **Your rules, not a model.** Corrections come from an explicit config you own, so the tool never surprises you with a guess.
* **Uninstall keeps your data.** Removing the tool removes the hook and the binary; the config and the corrections log stay yours unless you ask for them to go.
* **Small surface.** A handful of CLI verbs (`suggest`, `correct`, `install`, `uninstall`, `stats`, `version`) and nothing else.

A JSONL log records every correction, and `commandfixer stats` shows the count and rule breakdown, which is exactly the feedback loop needed to decide which typos deserve rules.

---

## CommandFixer at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Capabilities</h3>
  <ul>
    <li>Corrects typos at the Enter keypress</li>
    <li>Confirmation before any changed command runs</li>
    <li>User-defined JSON rule set</li>
    <li>PowerShell 7 and Windows PowerShell 5</li>
    <li>Correction stats and JSONL log</li>
    <li>Idempotent installer and clean uninstall</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Technology</h3>
  <ul>
    <li>Go, single native binary</li>
    <li>PSReadLine Enter-key hook</li>
    <li>JSON configuration</li>
    <li>Millisecond execution, no service</li>
    <li>Per-user install, no admin rights</li>
    <li>Open source</li>
  </ul>
</div>

</div>

---

## What this taught me

The best tools live at the moment of failure.

A spelling corrector that runs after the error message has already scrolled past is documentation. One that runs in the gap between Enter and execution is infrastructure.

The other lesson is restraint. The obvious upgrade path (fuzzy matching everything, learning rules automatically, correcting silently) leads to a tool you no longer trust at a prompt that can delete things.

*A tool that asks first gets to stay installed.*
