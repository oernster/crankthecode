---
title: "Escaping the Cursed Realm of GoDaddy Hosting"
date: "2026-01-31 10:00"
tags: ["blog", "stellody", "fastapi", "migration", "selfhosted", "seo"]
one_liner: "Nothing screams 'freedom' like deleting the last line of PHP from your life."
emoji: "🧹"
---

# Stellody: Escaping the Cursed Realm of GoDaddy Hosting

I’ve finally exorcised the last remaining traces of GoDaddy’s brittle legacy PHP hosting. The Stellody website now runs entirely on a clean self-authored FastAPI codebase. It is templated tested and deployed with something resembling dignity.

This wasn’t just a tech upgrade. It was a moral victory.

No more hand-editing `.php` files in a web FTP panel like it’s 2003. No more cursed includes. No more contact forms that randomly fail on Thursdays for spiritual reasons.

Now the backend is proper Python. HTML is rendered intentionally not incidentally. Forms actually deliver mail like they understand their job.

I no longer pay for a cPanel experience that feels like navigating Excel over dial-up.

For once the stack doesn’t fight me back.

---

## 📬 Contact Form: Modern Email Without the Drama

In the old setup sending a contact form email was like asking a haunted toaster to fax a sticky note.

Now it’s handled by Resend. It is a modern email API that simply works. No SMTP servers to misconfigure. No mysteriously vanishing messages. No phpmailer shame.

The form submits clean HTML email sets Reply-To correctly and keeps the recipient address hidden behind environment variables. One request and the message actually arrives.

The contact page is indexable and included in the sitemap because legitimate businesses should probably be reachable.

---

## 🛒 Add to Cart Add to Sanity

To support license sales I added a deliberately boring cart system.

Users can select a Standard or Pro license add it to their cart and review it before checkout. That’s it. No JavaScript frameworks having emotional episodes. No third-party widgets trying to be clever.

It uses server-side sessions allows one license at a time and behaves predictably. Fast minimal and adult.

---

## 💳 Checkout with PayPal Clean and Contained

Checkout uses PayPal’s hosted payment buttons tied directly to the selected license.

There’s no PayPal email exposed on the site no client-side state hacks and no mystery redirects. The checkout route is intentionally marked noindex nofollow keeping transactional pages out of search results where they don’t belong.

It’s a real endpoint not a decorative placeholder and it’s ready for expansion without leaking into SEO territory.

---

## 📦 Downloads Without Deployment Pain

Installer binaries no longer live in the application repository. They are published separately as versioned release artifacts and served directly from GitHub Releases.

The website exposes stable download URLs which redirect users to the appropriate release asset. This keeps downloads reliable while ensuring the application never touches large binaries during deploy or runtime.

Render builds are now deterministic. Git LFS is no longer part of the deployment story. This was not a workaround. It was a correction.

---

## 🔍 SEO That Is Intentional Not Performative

With the new architecture in place it finally made sense to do SEO properly instead of duct-taping it on afterward.

Canonical URLs are enforced under the primary domain to avoid duplicate indexing. Pages use sensible meta titles and descriptions with a focused update to the homepage to better reflect real search intent.

Open Graph and Twitter metadata are applied consistently with a default preview image that actually explains the product. A real sitemap exists and only includes crawl-worthy pages. Robots rules block transactional routes and those same routes emit noindex nofollow at the page level.

Importantly this was done incrementally. Existing pages were not rewritten for the sake of it. Structure was improved where needed mainly through clearer headings and better signals for search engines.

Search engines now see the site the same way users do. Intentional structured and not trying to outsmart anyone.

---

This is what building with tools you actually like feels like.

Not louder  
Not trendier  
Just calmer

*- And yes deleting the last PHP file still felt incredible.*
