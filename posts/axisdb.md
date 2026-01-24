---
title: "AxisDB"
date: "2026-01-19 12:38"
tags: ["python", "database", "db", "multidimensional", "json", "PyPi"]
blurb: "JSON database"
one_liner: "An embedded Python database that stores JSON documents with atomic commits and multidimensional keys."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/AxisDB.png
social_image: /static/images/axisdb-card.png
---
[AxisDB](https://github.com/oernster/AxisDB)  🗃️

## Problem → Solution → Impact

**Problem:** Small projects often need reliable, lightweight data storage without a full-blown RDBMS.

**Solution:** AxisDB is a Python-native, atomic, multidimensional key-value JSON database with optional RESTful interface.

**Impact:** Provides durable and minimal-effort local storage with modern developer ergonomics. [Install via PyPI](https://pypi.org/project/axisdb)

# Rationale
Because everything else was too normal...

What is it? A lightweight atomic JSON database. Because sometimes SQLite is too much and CSVs make me sad.
AxisDB is a tiny embedded document database for Python, designed for simple, reliable storage of JSON documents addressed by N-dimensional coordinate keys.

I've deployed it on PyPi.
This was a fun project idea I had and I decided to turn into a real thing.
I explored other embedded JSON stores but they didn’t enforce atomic writes in a way I needed here.

## Quick start

Create a quick test script (see the install steps in the terminal above):

<div class="code-block" aria-label="axisdbmain.py example">
  <div class="code-block__header">
    <span class="code-block__label">axisdbmain.py</span>
    <button
      class="code-copy code-copy--icon"
      type="button"
      data-copy-target="axisdbmain"
      aria-label="Copy code"
      title="Copy code"
    >
      <svg class="code-copy__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path
          d="M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
        />
      </svg>
    </button>
  </div>
  <pre class="code-block__body"><code id="axisdbmain">from axisdb import AxisDB

db = AxisDB.create("./mydb.json", dimensions=2)
db.set(("user1", "orders"), {"count": 3})
db.commit()

ro = AxisDB.open("./mydb.json", mode="r")
print(ro.get(("user1", "orders")))
</code></pre>
</div>

Or additionally define a field index:

<div class="code-block" aria-label="Define a field index">
  <div class="code-block__header">
    <span class="code-block__label">Define a field index</span>
    <button
      class="code-copy code-copy--icon"
      type="button"
      data-copy-target="axisdb-index"
      aria-label="Copy code"
      title="Copy code"
    >
      <svg class="code-copy__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path
          d="M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
        />
      </svg>
    </button>
  </div>
  <pre class="code-block__body"><code id="axisdb-index">from axisdb import AxisDB

db = AxisDB.create("./mydb.json", dimensions=2)
db.define_field_index("by_customer_id", ("customer_id",))
</code></pre>
</div>

Or perhaps query with an expression:

<div class="code-block" aria-label="Query example">
  <div class="code-block__header">
    <span class="code-block__label">Query example</span>
    <button
      class="code-copy code-copy--icon"
      type="button"
      data-copy-target="axisdb-query"
      aria-label="Copy code"
      title="Copy code"
    >
      <svg class="code-copy__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path
          d="M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
        />
      </svg>
    </button>
  </div>
  <pre class="code-block__body"><code id="axisdb-query">from axisdb import AxisDB
from axisdb.query.ast import Field

db = AxisDB.open("./mydb.json", mode="r")
rows = db.find(prefix=("orders",), where=Field(("customer_id",), "==", "c2"))
</code></pre>
</div>

<div class="fake-terminal fake-terminal--axisdb-run" aria-label="Run the server">
  <div class="fake-terminal__title">
    <span>bash</span>
    <button
      class="code-copy code-copy--icon"
      type="button"
      data-copy-target="axisdb-run-command"
      aria-label="Copy run command"
      title="Copy run command"
    >
      <svg class="code-copy__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path
          d="M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
        />
      </svg>
    </button>
  </div>
  <pre class="fake-terminal__body"><code><span class="ft-step ft-step--1"><span class="fake-terminal__prompt">user@linux:~$ </span><span class="fake-terminal__typed fake-terminal__typed--run">python -m uvicorn axisdb.server.app:app --reload</span><span class="fake-terminal__cursor-wrap fake-terminal__cursor-wrap--run" aria-hidden="true"><span class="fake-terminal__cursor"></span></span></span>
</code></pre>
  <pre class="visually-hidden"><code id="axisdb-run-command">python -m uvicorn axisdb.server.app:app --reload</code></pre>
</div>

<blockquote class="axisdb-run-note">
  <p>Then the server will start at:</p>
  <div class="axisdb-run-note__url">
    <code id="axisdb-local-url">http://localhost:8000</code>
    <button
      class="code-copy code-copy--icon"
      type="button"
      data-copy-target="axisdb-local-url"
      aria-label="Copy URL"
      title="Copy URL"
    >
      <svg class="code-copy__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path
          d="M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z"
        />
      </svg>
    </button>
  </div>
</blockquote>

# AxisDB

**AxisDB** is a tiny embedded document database for Python, designed for simple, reliable storage of JSON documents addressed by **N-dimensional coordinate keys**.

It is library-first, requires no server and stores all data in a single JSON file with atomic, crash-safe commits.

**See also:**
[USE_CASES.md](https://github.com/oernster/AxisDB/blob/main/USE_CASES.md) - a concise overview of practical applications and patterns enabled by this multidimensional JSON storage model.

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
