---
title: "Stellody Is Now Quietly Harder to Break"
date: "2026-02-36 18:00"
tags: ["blog", "stellody", "fastapi", "contact", "dnssec"]
one_liner: "Quiet changes were made so nothing exciting ever happens again and that is the goal."
emoji: "🛡️"
---
# How Stellody Learned to Stop Worrying and Ignore the Internet 

Most of the recent work on Stellody is the sort you never notice unless it goes wrong. Which is exactly the point.

The contact form was rebuilt properly from the ground up. Not cosmetically. Structurally. The result is a form that behaves like an adult service instead of a polite suggestion to spammers.

Cloudflare now sits in front of the site doing what it does best which is absorbing nonsense at the edge so the application does not have to. Turnstile is in place and working invisibly. Real users see a simple success state. Bots see a locked door and are politely ignored. No puzzles. No traffic lights. No humiliation rituals.

On the backend every submission is treated with suspicion. Honeypot fields catch the lazier attempts. Minimum submit times filter out scripts pretending to type. Inputs are normalised capped and stripped of anything that looks like it wants to become an email header. If delivery fails the user is still told everything is fine because advertising your mail infrastructure problems is rarely a good idea.

Rate limiting exists but stays asleep unless needed. Cloudflare handles the blunt force and the app handles the edge cases. Defence in depth without the theatrics.

DNS is now correctly delegated to Cloudflare with DNSSEC enabled. That means responses are signed end to end and tampering becomes someone else’s problem. It took a few screens and a small amount of patience. It was worth it.

Nothing here is flashy. There are no dashboards being admired. No badges being collected. Just fewer ways for things to fail and fewer reasons to wake up to surprise email.

The best outcome is that nobody notices any of this ever again.

*-Which would be ideal.*
