---
blurb: Dev cockpit + 3D printer room.
date: 2026-05-25 12:00
image: /static/images/command-battlestation1.jpg
social_image: /static/images/command-battlestation1.jpg
thumb_image: /static/images/command-battlestation1.jpg
one_liner: The Command Battlestation - daily driver workstation, HOTAS cockpit and 3D printer room.
tags:
- cat:Blog
- battlestation
- setup
- 3D printing
- HOTAS
- elite dangerous
- peripherals
title: The Command Battlestation
---

![Command battlestation photo 1: desk setup with curved primary monitor, three 4K monitors, control decks and HOTAS cockpit](/static/images/command-battlestation1.jpg)

![Command battlestation photo 2](/static/images/command-battlestation2.jpg)

![Command battlestation photo 3](/static/images/command-battlestation3.jpg)

## Welcome to the cockpit where the chaos gets compiled; and occasionally extruded in molten thermoplastic.

This is my daily driver: part developer workstation, part hardware museum. Every cable, macro pad and monitor is exactly where it needs to be; mostly because it's been there so long it's developed squatter's rights.

The 34 inch curved primary monitor runs enough terminals, consoles and dashboards to make NORAD nervous.  
Below it sit three 13.4 inch 4K monitors on professional stands (not OLED; I have a budget), each running its own application: **MediaMonkey** handling audio on the left, Word holding my CV in the middle (as it happens in this photo) and my Discord on the right.  
I didn't plan on becoming a multi-display maximalist... However, here we are.

A **StreamDeck XL** with hand-labelled macros sits front and centre-left, loaded with launch macros for all my websites, driving audio through my [AudioDeck](/posts/audiodeck) tool and muting meetings I regret joining.

On the far left, lit up in RGB, is the larger variant of the [PCPanel](https://www.getpcpanel.com); tactile volume control, because RGB is cheaper than therapy.

On the far right is my Samsung Galaxy Tab A9+ running **GameGlass** for **Elite Dangerous**: my favourite space combat/mining/trading/operations/on-foot-fun/exploration/you-name-it massively multiplayer mega game. Despite its age it is still actively developed and they do a good job of it. The tablet also fronts shards for my [Elite Dangerous Colonisation Assistant](/posts/edcolonisationasst), because space truckers need dashboards too.

And yes, that is a wet flannel on the immediate left. The British Summer heat is completely unbearable and hydro-cooling is not just for the PC.

Audio is handled by the **Focal Bathys** - a HiFi headphone setup that gracefully moonlights between Discord chaos and deep/old school house music.  
Wireless. Ridiculous. Perfect.

Not pictured: a 2025 **MacBook Air** (M4, 16GB RAM, 512GB SSD), perfect for pretending to be normal. Alongside it, a **Framework 13** with a Ryzen AI 7 350, 96GB of DDR5, 2TB of NVMe SSD and the upgraded 2.8K display, which is beautiful. The Framework is a multiboot setup running a custom-configured **rEFInd** and I regularly add and remove Linux distros on it (when Microsoft isn't busy messing up my bootable drives and sectors with Windows updates). It also carries Windows 11 Pro, purely in case a job opportunity ever needs me to bring my own Windows machine; I'd prefer not to, since Windows causes no end of grief for Linux on a regular basis.

---

## Flight Sim / HOTAS Setup

For high-immersion dogfights and questionable docking maneuvers in **Elite Dangerous** (and other flight sims but let's be honest - it's mostly Elite), I run a full HOTAS + pedal setup:

- **VKB Gunfighter IV joystick** with premium base
- **Virpil CM3 throttle** with all the throw and tension tuning a digital pilot could want
- **MFG Crosswind v3 rudder pedals** in graphite, because even my feet deserve nuanced control

Everything is mounted to **MonsterTech hardware**, which is just German for "no wobble, no mercy."  
The entire cockpit snaps into place like it was meant to launch me into low orbit.

---

## Input Devices

Input-wise, the setup is unapologetically niche.  
The mouse is a **FinalMouse Frostlord**: serial number 0222 of only 10,000 ever made, which is quite a nice number to hold. It is very lightweight; it weighs approximately nothing.

The keyboard and numpad are both **Epomaker**. The main board runs white creamy jade thocky switches - quiet, precise and borderline therapeutic to type on. The white numpad (an essential accessory, I feel) runs Wisteria linear switches.

Peripherals and controllers evolve - what matters is the workflow they enable.

---

## 3D Printing Zone

In a separate room lives the **Printer Room**. The current fleet is a curated duo: a highly customised, self-constructed **Voron Trident 350** (electronics, hardware, software, configuration and printed parts, many of them printed on the machine itself) and a **Qidi Q1 Pro**, a reliable workhorse that never seems to fail me despite its cheap price point.  
Each is fed by a meticulously organised filament armory below.  
It's a shrine to heat, motion and calibration agony - but also where entire machines are born, layer by painstaking layer.

I only own two printers currently but I am on my 10th overall and the graveyard tells its own story. My first, a **Biqu B1**, set itself on fire; I no longer trust the Biqu/BigTreeTech brand for anything beyond basic circuit boards. A **Tronxy X5SA 400** was a reliable machine I planned to upgrade into a VzBot, acquiring all the parts (pricey ones too) before deciding to take a different direction: I sold the entire package in favour of the Formbot Voron Trident 350 kit I still run today. A **Prusa MK3S+** bedslinger was a GREAT machine; I printed everything but the kitchen sink on it and though I rarely needed Prusa support, when I did it was very much available and incredibly good. There were Bambus too: an **X1C** with two AMS units and a **P1S** with one, both very good machines right up until just after the one-year guarantee expired. Given I'd been printing almost 24/7 on both, you could say the guarantee was only worth the time you bought it for. When a printer breaks I want to be able to fix it; Bambus are a nightmare to fix and replacement parts cost a lot of money, so I don't really want to go the Bambu route again.

Next, maybe, a colour printer of some variety. I have yet to decide between an AMS-oriented setup (Bambu, for example) or an IDEX variant; perhaps the **Prusa Core One** if it ever ships with an out-of-the-box IDEX colour solution (not the XL, which feels too pricey). My feeling on Prusas is that they are very good machines; unlike Bambus they are maintainable: they almost always offer some kind of upgrade path as they evolve and their 24/7 support is outstanding, with amazing documentation. Bambu simply doesn't compare. Other competitors are arriving on the market: I tried the AnyCubic colour line and didn't get on with it at all (the reliability wasn't there for me) but I've heard good things about the **Snapmaker** series of colour printers.

![Printer room shelf with multiple 3D printers and filament storage](/static/images/3D-printer-setup.png)

### 3D printing caveats...

**No, I do not print guns.  
3D printers like mine use plastics - useful for brackets, enclosures and mechanical parts; entirely unsuitable for anything ballistics-related.  
If improvised weapons are your concern, you are looking in the wrong workshop.  
This is a printer room, not an armoury.**

---

## Final comments

This setup has shipped production APIs, 3D-printed entire machines, debugged firmware over serial and hosted at least one panicked git revert at 2AM.  
It is a monument to function over form; and somehow still standing.

*Yes, I dust it. Occasionally. Don't @ me.*
