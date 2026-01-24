---
title: "Sitemaps, Side-by-Sides and Satisfying Polish"
date: "2026-01-24 15:20"
tags: ["blog", "update", "seo", "layout", "refactor", "tooling"]
one_liner: "Post-launch refinements including sitemap setup, layout alignment and enhanced polish across tooling and templates."
---
# Another productive pass over the site ~ focused on polish, semantics and visibility.

## 🗺 Sitemap & Robots.txt

| Improvement              | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Sitemap                  | Finalised & submitted via Google Search Console                            |
| Format                   | Clean XML with no styling clutter                                          |
| Robots.txt               | Guides crawlers and prevents unwanted indexing (e.g. /static/)             |
| Crawl readiness          | Pages now have canonical and structured metadata consistently              |

Search indexing is now in top form with clean previews and discoverable URLs.

---

## 🧼 UI Fixes & Cleanups

| Fix/Polish                                 | Outcome                                                  |
|-------------------------------------------|----------------------------------------------------------|
| 🌙 Moon icon restored                     | Toggle dark/light mode now displays correctly            |
| 🧮 Read time flash removed                | “Calculating…” no longer appears on load                |
| 🧾 Base.html crash resolved               | Safe meta tags even on non-post pages                   |
| 🧊 About page layout refined              | Skill lists spaced and aligned for improved readability |
| 🖼 Post images corrected                  | Dual image bug for Stellody and EDColonizationAsst fixed |
| 🔁 Duplicate entries removed             | 3D Printer Launcher now appears only once               |

Typography, alignment and responsiveness continue to improve incrementally.

---

## 🧰 Tooling Layout Refinement

Tools like **Trainer**, **AudioDeck**, **AxisDB** and others received structural improvements:

| Before                         | After                                |
|--------------------------------|--------------------------------------|
| Long vertical feature lists    | Split into side-by-side columns      |
| Inconsistent section headers   | Normalised under H2 hierarchy        |
| No visual alignment            | Aligned icons, tags and summaries    |

Tables render better, features are easier to skim and metadata is clearer.

---

## 🏷 SEO & Semantic Enhancements

| Change                                | Benefit                            |
|--------------------------------------|------------------------------------|
| Canonical URLs defaulted to safe `request.url` | Prevents indexing confusion |
| Added `<h2>` to homepage sections    | Improves screenreader parsing and SEO |
| Meta descriptions no longer crash    | Safer templating across base.html  |
| `<meta>` tags now more consistent    | Improves snippet generation        |

Search engines now get consistent signals and users benefit from better link previews.

---

## 🧪 Miscellaneous Updates

| Area              | Update                                                     |
|-------------------|------------------------------------------------------------|
| 📦 `requirements.txt` | Unpinned (no versions), more portable                 |
| ✅ Tests           | Coverage held at 100%                                     |
| 🗓 Timeline        | Icon placement fixed                                      |
| 💬 Posts           | Subtitles and blurbs ensured across all tooling entries   |

---

## Summary

- UI Polish  
- Layout consistency  
- Tooling presentation  
- Crawl readiness  
- Metadata and accessibility  

CrankTheCode now ships with smoother layout, smarter metadata and a more structured experience for humans and machines alike.

🛠 Onwards ~ but elegantly.
