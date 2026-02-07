---
date: 2026-01-21 02:20
emoji: "\U0001F916"
one_liner: Fixed RSS encoding and ignored WordPress sniffers. As one does.
tags:
- cat:Blog
- update
- rss
- feed
- botnet
- html
- utf8
- encoding
title: WP Bots and RSS Weirdness Blog Update
---

# WordPress Bots and Encoding Gremlins

## 1. 🕵️ WordPress Probe Bots, Please Go Touch Grass

At some point my small static blog joined the exclusive club of sites that attract constant probing from WordPress scanner bots. Apparently size and relevance are optional.

Let us be clear:

> This is not a WordPress site. It does not even smell like one.  
> I do not use PHP. I handcraft HTML like someone who enjoys control and mild repetitive strain injury.

If you are a bot looking for:
- `/wp-login.php`
- `/xmlrpc.php`
- `/wp-admin`

You will receive exactly what you deserve: a clean 404 and a logged timestamp saved purely for my own amusement.

No blocks were added. Watching them fail quietly is more satisfying.

---

## 2. 🧵 RSS Feed Now Less Glitchy, More Readable

I noticed an encoding issue in the RSS feed where certain characters were rendering as what can only be described as confused emoji soup.

The cause was a classic UTF-8 versus misencoded entity problem. This has now been corrected. The feed validates cleanly renders correctly and is no longer cursed.

> If you saw strange symbols in your RSS reader no you were not losing your mind. That one was on me.

---

## 🧼 Summary of Fixes

- Cleaned up RSS encoding so feeds render correctly across readers
- Ignored WordPress bot traffic because blocking it would bring me less joy
- Confirmed once again that my logging setup remains excessive for a personal blog

---

If you arrived expecting CMS drama or cross site scripting horror stories you are going to be disappointed.

*-If you are here for Python projects FastAPI misuse or strong opinions on build systems you are exactly where you should be.*

Next update coming soon assuming I do not go on another solo campaign against comment spammers. Again.