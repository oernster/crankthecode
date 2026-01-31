---
title: "The Illusion of Engineering"
date: "2026-01-28 18:00"
tags: ["blog", "ai", "development", "engineering", "quality"]
one_liner: "AI can generate code. It can’t replace software engineering."
emoji: "✨"
---
# AI Tools, Bad Code and the Case for Review

The rise of AI-assisted development has empowered many newcomers to generate code from prompts alone without deep software engineering knowledge. This ease of creation can be inspiring, although it introduces a growing issue: massive amounts of poorly engineered code are being pushed to the world under the false banner of innovation.

These prompt-only developers often lack understanding of the software development lifecycle, architecture and principles that experienced engineers rely on. They submit vague or technically shallow prompts, receive functional output and mistake that for good code. It works, sure - although it isn’t good.

---

## 🧨 Functional Doesn’t Mean Maintainable

These AI-generated codebases can be riddled with design flaws:

- No separation of concerns  
- Monolithic, oversized files  
- No architectural layering or file organisation  
- No use (or misuse) of design patterns  
- Violation of fundamental principles like SOLID

In Python, this usually comes with zero adherence to PEP8 or any linting or formatting standards like `flake8` or `black`. Code is dumped into GitHub repositories - often full of emojis and copy-pasted prompts in comments - then loudly promoted on social media where hype outpaces quality by a wide margin.

These projects often gain hundreds or thousands of stars while skilled engineers who invest time into building robust, clean and maintainable codebases remain in the shadows without a marketing channel, Twitter following or LinkedIn soapbox.

---

## 👀 Code Is for Humans

Let’s be clear: code is a communication tool for humans even if it’s ultimately read by machines. Any developer who uploads a project to GitHub should understand this. Your README isn't just a billboard - your *codebase* is documentation for future contributors, maintainers or even your future self.

Yet some people treat AI as an excuse to abandon readability altogether. The reasoning goes something like: “I don’t care what it looks like - AI can just refactor it later.” This approach assumes future AI tools will clean up all the mess and that human understanding is now optional.

This is not only shortsighted - it is reckless. We are nowhere near the point where AI can fully replace human comprehension and code review. If no one can read your code today, it is not fit for collaboration or evolution.

---

## 🧠 Engineering Still Matters

A good engineer does not blindly accept AI output. They review it, refactor it and ensure it aligns with real-world constraints, team conventions and project goals. They use AI as a tool - not a crutch.

Good software design still includes:

- Applying design patterns appropriately (and avoiding anti-patterns)  
- Ensuring code structure matches the idioms of the language  
- Writing clean, modular code that others can understand  
- Prioritising readability, not just cleverness

You wouldn’t publish a book without proofreading. You shouldn’t publish AI-generated code without the same care.

---

## 🧪 The Pseudoscience Trap

Some AI-driven projects go even further off the rails by layering in advanced mathematical jargon - Tensor algebra, postgrad-level math and philosophical theory - all of which sounds smart but adds 
little to the actual functionality or maintainability of the code. The result is pseudo-scientific projects dressed up in complex terminology to avoid scrutiny.  Likely not peer reviewed and well cited 
like a good scientific paper should be either.

Sometimes the authors genuinely understand the math. That doesn’t make the *code* any better. Intelligence in one domain does not excuse a lack of care in engineering execution.

---

## ⚙️ Use AI but Use It Well

Let’s be fair: I sometimes use AI tools myself; I find they are good for productivity gains. Agents, LLMs and code copilots are useful. You need to understand the landscape; which tools work well, 
what their limitations are and how to curate the output you receive.

What separates responsible use from cargo cult programming is review.

- You check the logic  
- You refactor when needed  
- You ensure everything aligns with best practices for the language, the team and the platform

In short: *you still do the job of a software developer*.

---

## 🏁 Final Words…

We are living in a fascinating new era although we are still bound by some old truths:

- Just because something runs does not mean it is good  
- Just because AI helped you build it does not mean it should go live  
- Just because it got stars on github does not mean it is useful

If you are creating a GitHub repository - AI-generated or not - your code should be written with the assumption that humans will read it. If they can’t, that is not clever. That is failure.

*- Code is a conversation. Don’t let the AI do all the talking.*
