---
title: "Escaping the Cursed Realm of GoDaddy Hosting"
date: "2026-01-31"
tags: ["blog", "stellody", "fastapi", "migration", "selfhosted"]
one_liner: "Nothing screams 'freedom' like deleting the last line of PHP from your life."
emoji: "🧹"
---

# Stellody: Escaping the Cursed Realm of GoDaddy Hosting

I’ve finally exorcised the last remaining traces of GoDaddy’s brittle legacy PHP hosting. The Stellody website now runs entirely on a clean self-authored FastAPI codebase - templated, tested and deployed with something resembling dignity.

This wasn’t just a tech upgrade - it was a moral victory. No more hand-editing `.php` files in a web FTP panel like it’s 2003. No more dodgy includes. No more “contact form” that randomly fails on Thursdays.

Now the backend is proper Python, the HTML is rendered intentionally not incidentally, and the forms actually deliver mail like they mean it. I don’t pay for a “cPanel experience” that feels like navigating Excel over dial-up.

I made something better. For once the stack doesn't fight me back.

## 📬 Contact Form: Modern Email Without the Drama

In the old setup sending a contact form email was like asking a haunted toaster to fax a sticky note.

Now it’s handled by [Resend](https://resend.com/) - a clean email API that just works. No SMTP servers to misconfigure. No mysteriously vanishing messages. No “sent from phpmailer@yourdomain.com” nonsense.

The form sends clean HTML email, with reply-to set properly, and the recipient address safely hidden behind a config variable. Just one POST request and it shows up like magic.

---

This is what building with tools you actually like feels like  
It’s not just cleaner - it’s calmer.
