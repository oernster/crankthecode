---
title: "UI Polish, CTAs and the Slow March to Done"
date: "2026-01-24 06:15"
tags: ["blog", "update", "ui", "ux", "accessibility", "css", "dark-mode"]
one_liner: "A tour through UI tweaks, CTA wrangling and why stopping matters more than starting."
---

# UI Polish, CTAs and Knowing When to Stop

This week’s commits look chaotic at first glance. UI tweaks. CTA shuffling. Light/dark mode flips. Words rewritten, then rewritten again. Buttons nudged by a few pixels. Icons muted. Then un-muted. Then muted properly.

From the outside, it probably looks like indecision.

From the inside, it’s the **boring, necessary work of making something feel right**.

---

## 1. ✨ UI Niceties Are Never “Just UI”

Most of the early commits were deceptively small:

- UI layout enhancements
- Hover colouring tweaks
- Image positioning adjustments

None of these change functionality. All of them change *how long someone stays on the page*.

UI work isn’t about visual fireworks. It’s about removing friction you didn’t realise was there until it’s gone.

---

## 2. 📩 CTAs: Visible but Not Shouting

A surprising amount of time went into Call To Action placement:

- Making the CTA always visible
- Moving it
- Moving it back
- Making sure it doesn’t glare unless hovered

The goal was simple:

> Be obvious without being desperate.

If someone wants to work with me, the path should be clear. If they don’t, the site shouldn’t nag them like a newsletter pop-up with abandonment issues.

---

## 3. 🌗 Light/Dark Mode: The Icon Lies (At First)

Light/dark mode support landed properly this week:

- Theme persistence
- OS preference fallback
- Correct tab order
- Icons that represent the *target* state, not the current one

That last bit matters more than people think.

If a button shows a sun, clicking it should take you to light mode, not confirm you’re already there. Tiny detail. Huge usability difference.

Also: fake console output stays dark. Because fake terminals in light mode look like crimes.

---

## 4. ⌨ Accessibility Isn’t a Checkbox

A few quiet but important improvements went in:

- Correct tab order
- Skip-to-content link
- Read-time estimates added consistently

None of this required ARIA acrobatics. Just:

- Proper HTML
- Thinking about keyboards
- Remembering that not everyone uses a mouse

Accessibility is mostly about *not being clever*.

---

## 5. 🧠 Content Rewrites: Let the Images Do the Talking

The Battlestation page got a rewrite with one explicit goal:

> Let the photos carry the weight, not the prose.

The images already show what matters: real hardware, real wear, real decisions. The job of the text was simply to **stop getting in the way**.

That meant:
- Rewriting sections by hand
- Removing explanatory fluff
- Tightening language until it matched what you can already see

No hype. No manufactured excitement. No trying to sell what’s plainly visible.

The same approach carried over to the About page: a legacy section added, polish applied, then anything unnecessary stripped back.

If a sentence doesn’t add context beyond what the images already communicate, it doesn’t belong there.

---

## 6. 🧭 Meta Descriptions and Other “Finish Line” Work

The final commit adds proper meta descriptions to the base and index templates.

This is classic end-game work:
- Nobody notices when it’s done
- Everyone notices when it’s missing

Search engines get a clear summary. Social previews behave. I control the snippet instead of leaving it to chance.

That’s not optimisation. That’s hygiene.

---

## 🧼 The Real Lesson

The most important change this week wasn’t a commit.

It was reverting.

After a lot of tweaking, aligning, centring, un-centring and second-guessing, the homepage went back to its earlier layout ~ because it felt right.

> If improving something keeps making it worse, stop.

That’s not quitting. That’s taste doing its job.

---

CrankTheCode is now in a good place:
- The UI is calm
- The CTAs are clear
- And nothing is trying too hard

Which means it’s time to do the hardest thing in software:

**Leave it alone and build something else.**

Until the next bout of unnecessary polish.
