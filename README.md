# Crank The Code

Crank The Code is a long-form technical writing site focused on decision systems, authority design and structural integrity in engineering organisations.

> https://www.crankthecode.com

---

## What this is

This is not a generic dev blog.

The site is a working body of writing around:

* decision systems and decision latency
* authority design and organisational structure
* CTO operating models
* backend architecture and system design
* failure modes in engineering organisations

The goal is to make the invisible structure of software teams and systems explicit and inspectable.

---

## Why this exists

Most engineering writing focuses on tools, frameworks or surface patterns.

That misses the real problem.

Software organisations fail structurally:

* decisions are unclear
* authority is diffused
* systems accrete without ownership

This site exists to model those structures directly.

---

## Content model

Posts are organised deliberately rather than chronologically.

Primary categories:

* Leadership
* Architecture
* Decision Systems
* Organisational Structure

Each post may also include a layer:

* decision-systems
* cto-operating-model
* organisational-structure
* architecture

This allows:

* composable filtering
* structural navigation rather than timeline browsing

---

## The system

The site is a custom-built FastAPI application.

Key characteristics:

* Markdown-driven content with structured frontmatter
* Explicit domain separation (core, services, adapters)
* Deterministic routing and metadata generation
* RSS, sitemap and search-friendly structure
* No CMS abstraction layer

The system is designed for:

* control over structure
* fast iteration
* long-term maintainability

---

## Local development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Running tests

```powershell
.\venv\Scripts\python.exe -m pytest -q --cov
```

---

## Static assets (dev note)

If images appear broken locally:

```powershell
Remove-Item -Recurse -Force static_dist
```

---

## What this repository represents

This is not just a website.

It is:

* a publishing system
* a structured knowledge base
* an applied model of the ideas described in the writing

The implementation reflects the same principles:
clear boundaries, explicit structure and minimal hidden behaviour.
