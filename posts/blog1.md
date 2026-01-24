---
title: "Site SEO & Search Updates"
date: "2026-01-18 10:55"
tags: ["python", "fastapi", "seo", "blog", "crankthecode", "html"]
one_liner: "Blog formally released but this time updated with SEO optimisation!"
blurb: "Blog update with SEO"
---
# This blog is now a *THING!* However, it needed SEO optimisation

## This iteration involved implementing SEO optimisation.
It wasn't too hard actually.
Main implementation updates to the code were as follows...

## SEO details

Changes were required but I wanted to avoid altering its visual appearance. These improvements focus on metadata, structured content and search engine visibility.

---

## 1. Meta Titles & Descriptions

**Goal:** Add unique meta `<title>` and `<meta name="description">` tags to each page.

**Implementation:**
Extract `title` and `excerpt` from post frontmatter:

```html
<title>{{ post.title }} | CrankTheCode</title>
<meta name="description" content="{{ post.excerpt }}">
```

---

## 2. Heading Structure

**Goal:** Use semantic HTML headings (H1–H3) to organise content.

**Implementation:**
Ensure each post template includes:

```html
<h1>{{ post.title }}</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>
```

---

## 3. Keyword Optimisation

**Goal:** Embed targeted keywords in content naturally, especially in headings and intros.

**Implementation:**
Use relevant phrases (e.g., "FastAPI markdown blog") in:

* Titles
* First paragraph
* Header tags
* Meta description

---

## 4. XML Sitemap

**Goal:** Help search engines index all content.

**Implementation:**
Create `/sitemap.xml` dynamically from post data:

```xml
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
  {% for post in posts %}
  <url>
    <loc>https://www.crankthecode.com/{{ post.slug }}/</loc>
    <lastmod>{{ post.date }}</lastmod>
  </url>
  {% endfor %}
</urlset>
```

---

## 5. Structured Data (Schema Markup)

**Goal:** Enable enhanced search features using JSON-LD.

**Implementation:**
Insert this in `<head>` of each blog post:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ post.title }}",
  "datePublished": "{{ post.date }}",
  "author": { "@type": "Person", "name": "{{ post.author }}" }
}
</script>
```

---

## 6. URL Structure

**Goal:** Ensure clean, descriptive URLs.

**Implementation:**
Slug generation should use post title keywords (e.g., `/fastapi-seo-guide/`), avoiding IDs or symbols.

---

## 7. Internal Linking

**Goal:** Improve site crawlability and user time-on-site.

**Implementation:**
Add relevant inline links to other posts within content:

```md
See also: [My post on FastAPI Markdown](/fastapi-markdown-guide/)
```

---

## 8. Image Alt Tags

**Goal:** Boost image indexing and accessibility.

**Implementation:**
Update image markdown to:

```md
![FastAPI sitemap example](image.png)
```

---

## 9. Content Strategy

**Goal:** Encourage steady SEO growth with regular, high-quality posts.

**Implementation:**

* Publish evergreen technical tutorials
* Use consistent post structure and keyword planning

---

## Final Checklist

* [x] Meta title & description tags
* [x] Structured H1–H3 usage
* [x] Keyword-integrated content
* [x] Sitemap generation
* [x] JSON-LD structured data
* [x] Clean URL slugs
* [x] Internal links
* [x] Alt attributes on images
* [x] Long-term content planning

---

No visual modifications required.


