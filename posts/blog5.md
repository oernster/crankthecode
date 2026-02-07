---
title: "UI Polish, CTAs and the Slow March to Done"
date: "2026-01-24 06:15"
tags: ["blog", "update", "ui", "ux", "accessibility", "css", "dark-mode"]
one_liner: "A tour through UI tweaks, CTA wrangling and why stopping matters more than starting."
emoji: "🌗"
---

# UI Polish, CTAs and Knowing When to Stop

This week’s commits look chaotic at first glance. UI tweaks. CTA shuffling. Light and dark mode flips. Words rewritten then rewritten again. Buttons nudged by a few pixels. Icons muted then un-muted then muted properly.

From the outside it probably looks like indecision.

From the inside it is the boring necessary work of making something feel right.

---

## 1. ✨ UI Niceties Are Never “Just UI”

Most of the early commits were deceptively small:

- UI layout enhancements  
- Hover colouring tweaks  
- Image positioning adjustments  

None of these change functionality. All of them change how long someone stays on the page.

UI work is not about visual fireworks. It is about removing friction you did not realise was there until it disappears.

---

## 2. 📩 CTAs: Visible but Not Shouting

A surprising amount of time went into Call To Action placement:

- Making the CTA always visible  
- Moving it  
- Moving it back  
- Ensuring it only draws attention on hover  

The goal was simple:

> Be obvious without being desperate.

If someone wants to work with me the path should be clear. If they do not the site should not nag them like a newsletter pop-up with abandonment issues.

---

## 3. 🌗 Light and Dark Mode: The Icon Lies at First

Light and dark mode support landed properly this week:

- Theme persistence  
- OS preference fallback  
- Correct tab order  
- Icons that represent the target state rather than the current one  

That last detail matters more than people expect.

If a button shows a sun clicking it should take you to light mode not confirm you are already there. Tiny detail. Large usability difference.

Fake console output also stays dark because fake terminals in light mode look like crimes.

---

## 4. ⌨ Accessibility Isn’t a Checkbox

Several quiet but important improvements were made:

- Correct tab order  
- Skip to content link  
- Read time estimates added consistently  

None of this required ARIA acrobatics. Just:

- Proper HTML  
- Thinking about keyboard navigation  
- Remembering that not everyone uses a mouse  

Accessibility is mostly about not being clever.

---

## 5. 🧠 Content Rewrites: Let the Images Do the Talking

The Battlestation page was rewritten with one explicit goal:

> Let the photos carry the weight not the prose.

The images already show what matters. Real hardware. Real wear. Real decisions. The job of the text was simply to stop getting in the way.

That meant:
- Rewriting sections by hand  
- Removing explanatory fluff  
- Tightening language until it matched what was already visible  

No hype. No manufactured excitement. No attempt to sell what is plainly there.

The same approach was applied to the About page. A legacy section was added polish was applied and anything unnecessary was stripped back.

If a sentence does not add context beyond what the images already communicate it does not belong.

---

## 6. 🧭 Meta Descriptions and Other Finish Line Work

The final commit added proper meta descriptions to the base and index templates.

This is classic end game work:
- Nobody notices when it is done  
- Everyone notices when it is missing  

Search engines get a clear summary. Social previews behave. I control the snippet rather than leaving it to chance.

That is not optimisation. That is hygiene.

---

## 🧼 The Real Lesson

The most important change this week was not a commit.

It was reverting.

After a lot of tweaking aligning centre-ing uncentre-ing and second guessing the homepage returned to its earlier layout because it felt right.

> If improving something keeps making it worse stop.

That is not quitting. That is taste doing its job.

---

CrankTheCode is now in a good place:
- The UI is calm  
- The CTAs are clear  
- Nothing is trying too hard  

Which means it is time to do the hardest thing in software:

*-Leave it alone and build something else.*

Until the next bout of unnecessary polish.
