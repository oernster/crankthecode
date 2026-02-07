---
title: "Escaping the Cursed Realm of GoDaddy Hosting"
date: "2026-01-31 10:00"
tags: ["blog", "stellody", "fastapi", "migration", "selfhosted", "seo"]
one_liner: "Nothing screams freedom like deleting the last line of PHP from your life."
emoji: "🧹"
---

# Stellody: Escaping the Cursed Realm of GoDaddy Hosting

I have finally exorcised the last remaining traces of GoDaddy’s brittle legacy PHP hosting. The Stellody website now runs entirely on a clean self authored FastAPI codebase. It is templated tested and deployed with something resembling dignity.

This was not just a technical upgrade. It was a moral victory.

No more hand editing `.php` files in a web FTP panel like it is 2003. No more cursed includes. No more contact forms that randomly fail on Thursdays for spiritual reasons.

The backend is now proper Python. HTML is rendered intentionally rather than incidentally. Forms actually deliver mail like they understand their job.

I no longer pay for a cPanel experience that feels like navigating Excel over dial up.

For once the stack does not fight me back.

---

## 📬 Contact Form: Modern Email Without the Drama

Under the old setup sending a contact form email felt like asking a haunted toaster to fax a sticky note.

That entire mess is now handled by Resend. It is a modern email API that simply works. No SMTP servers to misconfigure. No mysteriously vanishing messages. No phpmailer shame.

The form submits clean HTML email sets Reply-To correctly and keeps the recipient address hidden behind environment variables. One request goes out and the message actually arrives.

The contact page is indexable included in the sitemap and behaves like a legitimate point of communication rather than an afterthought.

---

## 🛒 Add to Cart Add to Sanity

To support license sales I added a deliberately boring cart system.

Users select a Standard, Upgrade to Pro, or Pro license add it to the cart and review it before checkout. That is the entire feature set. No JavaScript frameworks having emotional episodes. No third party widgets trying to be clever.

Everything is server side. One license at a time. Predictable behaviour. Fast minimal and adult.

---

## 💳 Checkout with PayPal Clean and Contained

Checkout uses PayPal’s hosted payment buttons tied directly to the selected license.

No PayPal email address is exposed. There is no client side state hackery and no mystery redirects. Transactional routes are explicitly marked noindex nofollow keeping them out of search results where they do not belong.

This is a real endpoint not a decorative placeholder and it is ready to expand without polluting the public surface area of the site.

---

## 📦 Downloads Without Deployment Pain

Installer binaries no longer live in the application repository.

They are published separately as versioned release artefacts and served directly from GitHub Releases. The website exposes stable download URLs which redirect users to the appropriate release asset.

This keeps downloads reliable while ensuring the application never touches large binaries during deploy or runtime. Render builds are now deterministic. Git LFS is no longer part of the story.

This was not a workaround. It was a correction.

---

## 🔍 SEO That Is Intentional Not Performative

With the new architecture in place it finally made sense to approach SEO properly rather than duct taping it on afterwards.

Canonical URLs are enforced under the primary domain to avoid duplicate indexing. Pages use sensible meta titles and descriptions with a focused update to the homepage that reflects actual search intent.

Open Graph and Twitter metadata are applied consistently with a default preview image that explains the product instead of gesturing vaguely at it. A real sitemap exists and includes only crawl worthy pages. Robots rules block transactional routes and those same routes emit noindex nofollow at the page level.

Crucially this was done incrementally. Existing pages were not rewritten for the sake of it. Structure was improved where needed mainly through clearer headings and more honest signals for search engines.

Search engines now see the site the same way users do: Intentional, structured and not trying to outsmart anyone.

---

This is what building with tools you actually like feels like.

> Not louder  
> Not trendier  
> Just calmer

*-And yes deleting the last PHP file still felt incredible.*
