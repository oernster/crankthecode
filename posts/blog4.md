---
title: "WP Bots and RSS Weirdness Blog Update"
date: "2026-01-21 02:20"
tags: ["blog", "update", "rss", "feed", "botnet", "html", "utf8", "encoding"]
one_liner: "Fixed RSS encoding and ignored WordPress sniffers. As one does."
---

# 🤖 WordPress Bots and Encoding Gremlins

## 1. 🕵️ WordPress Probe Bots, Please Go Touch Grass

Apparently my tiny, static blog has joined the elite club of websites now blessed with **nonstop probing from WordPress scanner bots**. That’s cute.

Let’s set the record straight:

> This is not a WordPress site. It doesn’t even smell like one.  
> I don’t use PHP. I handcraft HTML like a person who wants total control and carpal tunnel syndrome.

So if you’re a bot looking for:
- `/wp-login.php`
- `/xmlrpc.php`
- `/wp-admin`

You’ll get exactly what you deserve: a cold, empty 404 and a logged timestamp for my own amusement.

---

## 2. 🧵 RSS Feed Now Less Glitchy, More Readable

Noticed a rogue encoding issue in the RSS feed. Some characters were doing their best impression of glitchy emoji soup - and failing.

The issue? Classic UTF-8 vs misencoded entity tango. Fixed now. The feed’s valid, clean and no longer cursed.

> If you saw strange symbols in your RSS reader: no, you weren’t losing your mind. It was me. Sorry.

---

## 🧼 Summary of Fixes

- Cleaned up RSS encoding so your reader stops crying
- Ignored WordPress bot traffic because blocking them would bring me less joy
- Confirmed that my logging system continues to be overkill for a personal blog

---

If you're here expecting CMS drama or cross-site scripting horror stories… you’re going to be deeply disappointed.  
But if you're here for Python projects, FastAPI abuse, or spicy opinions on build systems, you’re in exactly the right place.

Next update coming soon, assuming I don’t go on a one-man crusade against comment spammers. (Again.)
