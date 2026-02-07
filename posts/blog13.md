---
title: "The Illusion of Engineering"
date: "2026-01-28 18:00"
tags: ["blog", "ai", "development", "engineering", "quality"]
one_liner: "AI can generate code but it cannot replace software engineering."
emoji: "✨"
---

# AI Tools Bad Code and the Case for Review

AI assisted development has lowered the barrier to entry dramatically. It is now possible for someone with minimal engineering background to generate entire codebases from prompts alone. That accessibility can be empowering and genuinely useful.

It has also created a growing problem. Large volumes of poorly engineered code are being released under the banner of innovation simply because they run.

Prompt only development often bypasses the fundamentals that experienced engineers rely on. Architectural thinking lifecycle awareness and long term maintainability are replaced with surface level functionality. The output works in isolation but it is not good code.

---

## 🧨 Functional Does Not Mean Maintainable

Many AI generated projects share the same structural weaknesses.

There is little or no separation of concerns. Files grow to unreasonable size. Architectural layering is absent or inconsistent. Design patterns are misapplied or ignored entirely. Core principles such as SOLID are violated without hesitation.

In Python this is often paired with no adherence to PEP8 and no use of basic tooling such as `flake8` or `black`. Code is dumped into public repositories complete with emojis and prompt fragments in comments then promoted aggressively on social media.

Meanwhile carefully engineered projects built with attention to structure testing and long term evolution receive little attention simply because they lack a marketing channel or a loud following.

---

## 👀 Code Is for Humans

Code is a communication medium for humans first and machines second. Anyone publishing a project should understand that the codebase itself is documentation for future contributors, maintainers and your future self.

Treating AI as a justification to ignore readability entirely is dangerous. The assumption that future tools will magically refactor unreadable code ignores the reality that comprehension still matters today.

If no human can read your code with confidence it is not fit for collaboration, review or evolution.

---

## 🧠 Engineering Still Matters

Responsible engineers do not accept AI output blindly. They review it refactor it and ensure it aligns with real world constraints team conventions and project goals. AI is a tool not a substitute for judgement.

Good engineering still involves applying design patterns, deliberately structuring code according to language idioms, writing modular understandable components and prioritising clarity over cleverness.

You would not publish a book without proofreading. Publishing AI generated code without review deserves the same criticism.

---

## 🧪 The Pseudoscience Trap

Some AI driven projects go further by wrapping weak engineering in dense mathematical or philosophical language. Advanced terminology can create the illusion of rigour while masking the absence of sound structure testing or peer review.

Occasionally the author genuinely understands the theory. That alone does not redeem poor execution. Expertise in one domain does not excuse neglect in another.

Complexity should earn its place through necessity not intimidation.

---

## ⚙️ Use AI but Use It Well

AI tools are not the enemy. Used properly they offer real productivity gains. Agents, copilots and language models can accelerate development and reduce boilerplate.

What separates responsible use from cargo cult programming is review.

You verify the logic. You refactor where needed. You ensure the result fits the language the team and the platform.

In short, you still do the work of an engineer.

---

## 🏁 Final Words

We are in a new era but the fundamentals remain unchanged.

- Just because something runs does not mean it is good  
- Just because AI helped produce it does not mean it should ship  
- Just because it gained stars does not mean it is useful  

If you publish a repository; AI generated or otherwise, you are responsible for the quality of what you release. Code should be written with the assumption that humans will read it.

If they cannot that is not clever.

*-Code is a conversation. Do not let AI do all the talking.*
