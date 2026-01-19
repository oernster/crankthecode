---
title: "AxisDB"
date: "2026-01-19 05:38"
tags: ["python", "database", "db", "multidimensional", "json", "PyPi"]
blurb: "JSON database"

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/AxisDB.png
---
I developed: [AxisDB](https://github.com/oernster/AxisDB).
What is it? AxisDB is a tiny embedded document database for Python, designed for simple, reliable storage of JSON documents addressed by N-dimensional coordinate keys.
I've deployed it on PyPi.
This was a fun project idea I had and I decided to turn into a real thing.

# AxisDB

**AxisDB** is a tiny embedded document database for Python, designed for simple, reliable storage of JSON documents addressed by **N-dimensional coordinate keys**.

It is library-first, requires no server, and stores all data in a single JSON file with atomic, crash-safe commits.

> **See also:**  
> [USE_CASES.md](https://github.com/oernster/AxisDB/blob/main/USE_CASES.md) — a concise overview of practical applications and patterns enabled by this multidimensional JSON storage model.

---

## Key properties

- Library-first design (usable without any server)
- Single-file JSON storage
- Atomic, crash-safe commits via temp-file replace
- Safe multi-process access (single writer, multiple readers) via file locks
- Minimal but useful query + indexing support (correctness-first)

---

## Features

- Embedded JSON document database
- N-dimensional coordinate keys
- Atomic commit and recovery
- Key listing (`list`) and multidimensional slicing (`slice`)
- Basic querying (`find`) with optional persisted field indexes
- Optional FastAPI wrapper with Swagger (`/docs`) and ReDoc (`/redoc`)
