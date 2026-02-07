---
title: "Sitemaps, Side-by-Sides and Satisfying Polish"
date: "2026-01-24 15:20"
tags: ["blog", "update", "seo", "layout", "refactor", "tooling"]
one_liner: "Post-launch refinements including sitemap setup, layout alignment and enhanced polish across tooling and templates."
emoji: "🧹"
---

# Another productive pass over the site focused on polish semantics and visibility.

This update was about tightening loose ends rather than introducing anything new. The site was already functional and coherent but a number of small inconsistencies had accumulated across layout tooling and metadata. None of these were urgent on their own but together they were starting to show.

This pass focused on reducing friction improving clarity and making the site easier to reason about for both users and search engines.

---

## 🗺 Sitemap & Robots.txt

| Improvement      | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| Sitemap          | Finalised and submitted via Google Search Console                            |
| Format           | Clean XML with no styling clutter                                            |
| Robots.txt       | Guides crawlers and prevents unwanted indexing (e.g. /static/)              |
| Crawl readiness  | Pages now have canonical and structured metadata consistently                |

Search indexing is now in a good place with clean previews predictable URLs and no accidental crawl paths.

---

## 🧼 UI Fixes & Cleanups

| Fix or Polish                              | Outcome                                                   |
|-------------------------------------------|-----------------------------------------------------------|
| UK British spellings                       | Revised all text throughout the site to UK British        |
| EDColonisationAsst                        | Fully converted to UK British and repository renamed      |
| Moon icon restored                        | Light and dark mode toggle now displays correctly         |
| Read time flash removed                   | “Calculating…” no longer appears on load                  |
| Base.html crash resolved                  | Meta tags now safe even on non-post pages                 |
| About page layout refined                 | Skill lists spaced and aligned for readability             |
| Post images corrected                    | Dual image bug fixed for Stellody and EDColonisationAsst  |
| Duplicate entries removed                | 3D Printer Launcher now appears only once                 |

Typography alignment and responsiveness continue to improve incrementally. Nothing dramatic just fewer rough edges.

---

## 🧰 Tooling Layout Refinement

Tools such as **Trainer**, **AudioDeck**, **AxisDB** and others received structural layout improvements:

| Before                      | After                                   |
|-----------------------------|------------------------------------------|
| Long vertical feature lists | Split into side by side columns           |
| Inconsistent headers        | Normalised under H2 hierarchy             |
| Poor visual alignment       | Icons tags and summaries aligned          |

Tables are easier to scan features are clearer and supporting metadata no longer competes for attention.

---

## 🏷 SEO & Semantic Enhancements

| Change                                         | Benefit                                   |
|-----------------------------------------------|--------------------------------------------|
| Canonical URLs default to `request.url`        | Prevents indexing confusion                |
| Added `<h2>` to homepage sections              | Improves screen reader parsing and SEO     |
| Meta descriptions no longer crash              | Safer templating across base.html           |
| Meta tags more consistent                      | More predictable snippet generation        |

Search engines now receive consistent signals and users benefit from cleaner previews when sharing links.

---

## 🧪 Miscellaneous Updates

| Area            | Update                                                      |
|-----------------|-------------------------------------------------------------|
| requirements.txt| Unpinned versions for improved portability                  |
| Tests           | Coverage held at 100 percent                                |
| Timeline        | Icon placement fixed                                        |
| Posts           | Subtitles and blurbs ensured across tooling entries          |

---

## Summary

- UI polish  
- Layout consistency  
- Tooling presentation  
- Crawl readiness  
- Metadata and accessibility  

*-CrankTheCode now ships with a calmer layout smarter metadata and a more structured experience for humans and machines alike.*

Onwards but elegantly.
