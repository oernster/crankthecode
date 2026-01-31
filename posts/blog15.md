---
title: "Escaping the Cursed Realm of GoDaddy Hosting"
date: "2026-01-31"
tags: ["blog", "stellody", "fastapi", "migration", "selfhosted", "seo"]
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

## 🛒 Add to Cart, Add to Sanity

To support license sales, I added a simple cart system. Users can now select either a Standard or Pro license, add it to their cart, and review their purchase before checkout. It’s all done using server-side session storage with no client-side JS frameworks getting in the way.

This addition keeps things snappy, minimal and non-annoying. Adding to cart feels immediate and clear, and the total is neatly calculated. It looks and works like a real store.

No third-party cart plugins. No Shopify integration disasters. Just FastAPI, sessions and a bit of templating.

## 💳 Checkout with PayPal - Fully Integrated

Once in the cart, the user is shown a hosted PayPal checkout button tied to the selected license. Only one license can be purchased at a time - adding a new one replaces the current selection.

No PayPal email is shown on the site. Everything is session-based and configured via environment variables. Clean, minimal and safe.

A dedicated `/checkout` route now renders a clear post-payment summary page once payment completes - not a placeholder, but a working endpoint ready for expansion.

## 🔍 SEO That Doesn’t Suck

With the new architecture in place, it finally made sense to add proper SEO polish:

- Canonical URLs based on `https://stellody.com` (no `www`) to avoid duplicate indexing.
- Robots meta tags like `noindex,nofollow` applied to `/cart` and `/checkout` to keep transactional pages out of search.
- Open Graph and Twitter card support including fallback `og:image` previews and handle metadata (`@stellody`).
- Dynamically generated sitemap containing only crawlable, high-value pages.
- Proper robots.txt allowing public routes while excluding sensitive ones.
- Descriptive meta titles and fallback descriptions across all HTML pages.
- No outdated or spammy `meta keywords` tags in sight.

These upgrades make the site more visible, more indexable, and more professional to both search engines and humans.

---

This is what building with tools you actually like feels like. It's not just cleaner - it's calmer.