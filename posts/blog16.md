---
date: 2026-02-06 18:00
emoji: "\U0001F6E1️"
one_liner: Quiet changes were made so nothing exciting ever happens again and that
  is the goal.
tags:
- cat:Blog
- stellody
- fastapi
- contact
- dnssec
- security
title: Stellody Is Now Quietly Harder to Break
---

# How Stellody Learned to Stop Worrying and Ignore the Internet

Most of the recent work on Stellody is the sort you only notice when it fails. Which is precisely why it exists.

The contact form has been rebuilt properly from the ground up. Not cosmetically. Structurally. The result is a service that behaves like an adult system rather than a polite suggestion to spammers that someone might be listening.

Cloudflare now sits in front of the site doing exactly what it is good at. Absorbing nonsense at the edge so the application does not have to. Turnstile is enabled and invisible. Real users see a clean success state. Automated traffic sees a locked door and is quietly ignored. No puzzles. No traffic lights. No performative friction.

On the backend every submission is treated with suspicion by default. Honeypot fields catch the lazier attempts. Minimum submit times filter out scripts pretending to type. Inputs are normalised, capped and stripped of anything that looks like it wants to escape into an email header.

If delivery fails the user is still told everything is fine. Advertising your mail infrastructure problems rarely improves security; or trust.

Rate limiting exists but stays dormant unless required. Cloudflare handles the blunt force. The application handles edge cases. Defence in depth without theatrics, or dashboards begging to be admired.

DNS is now fully delegated to Cloudflare with DNSSEC enabled. Responses are signed end to end and tampering becomes someone else’s problem. It required a few screens a small amount of patience and zero heroics.

None of this is flashy. There are no badges to collect and no metrics worth tweeting.

There are simply fewer ways for things to fail and fewer reasons to wake up to surprise email.

The best outcome is that nobody ever notices any of this again.

*-Which would be ideal.*