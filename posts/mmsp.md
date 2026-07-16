---
blurb: A community specification for multimedia feed subscription beyond RSS and Atom
date: 2026-07-16 08:30
type: project
role: project
emoji: 📡
image: /static/images/mmsp-icon.png
one_liner: An open, JSON-based subscription protocol designed as a semantic superset of RSS 2.0 and Atom, with calm consumption as a wire-level guarantee.
social_image: /static/images/mmsp-icon.png
tags:
- cat:Tools
- protocol
- specification
- feeds
- rss
- atom
- json-schema
- open-standards
thumb_image: /static/images/mmsp-icon.png
title: MMSP

---

[MMSP](https://oernster.github.io/MMSP-Spec/), the MultiMedia Subscription Protocol, is an open community specification for subscribing to multimedia content feeds.

RSS answered a question the early web needed answered:

*How do I follow a site's articles without visiting it?*

MMSP answers the question the current web actually poses:

*How do I follow a publisher whose output is video, audio, articles, images, releases, events and things that do not exist yet, without surrendering my attention to a platform?*

The specification and its source live at [MMSP-Spec](https://github.com/oernster/MMSP-Spec).

---

## Problem → System → Outcome

**Problem.** Modern publishing spans a dozen content forms across disconnected platforms. RSS 2.0 and Atom model one of them well. Everything else is bolted on through namespace extensions, platform APIs or not at all, and every push-based alternative monetises attention.

**System.** A JSON-based, pull-only protocol defined as a semantic superset of RSS 2.0 and Atom: twelve first-class item types, formal JSON Schemas, a defined normalization from existing feeds, discovery via `/.well-known/mmsp.json` and a conformance suite targeting every normative statement in the spec.

**Outcome.** A published specification with a working reference client (Meridian), a live production feed (this site) and machine-verifiable conformance, offered as a foundation other publishers and clients can adopt.

---

## What the protocol guarantees

MMSP is designed around calm consumption and makes it enforceable at the wire level rather than aspirational:

* **Pull-only.** There is no server-push mechanism. Subscribers consume feeds when they choose to, not when publishers demand attention.
* **A minimum poll interval.** Clients respect a 300 second floor; a compliant client cannot hammer a publisher or refresh compulsively.
* **HTTPS everywhere.** All URLs in the protocol are HTTPS.
* **One honest User-Agent.** Clients identify as `MMSP/1.0`.

Presentation behaviour such as notifications is out of scope for the base protocol; clients that want to commit further can conform to the optional Calm Consumption Profile.

---

## A semantic superset, not a replacement

MMSP does not ask the feed ecosystem to move. It defines how existing feeds map into it:

| Source type | Acquires from |
|---|---|
| `mfeed` | Native MMSP manifest |
| `rss` | Any RSS 2.0 feed |
| `atom` | Any Atom 1.0 feed |
| `podcast` | RSS with podcast namespace extensions |
| `platform` | Platform-specific adapter |

Twelve first-class item types carry the multimedia model: video, audio, article, image, short, document, gallery, event, release, newsletter, course and livestream.

The format is JSON with the MIME type `application/mmsp+json`. Feeds and items are formally described by JSON Schemas, so a publisher can validate output mechanically instead of eyeballing an XML sample.

---

## Discovery

Finding a publisher's feed should not require finding a feed URL.

MMSP defines discovery through a well-known endpoint:

```text
/.well-known/mmsp.json
```

or an HTML `<link rel="alternate">`. A client given only a domain can find everything the publisher exposes.

This site practices what the spec preaches: crankthecode.com serves its own live MMSP manifest at that endpoint.

---

## Specification discipline

The project is run like a standards effort, not a README:

* a versioned specification document (`draft-mmsp-00`) written with RFC-style normative language
* JSON Schema 2020-12 definitions for feeds and items
* worked examples alongside the schemas
* a conformance test suite whose coverage target is 100 percent of normative spec statements

The `draft-NN` versioning borrows IETF Internet-Draft naming as a familiar convention. MMSP is an independent community specification; it has not been submitted to the IETF and an IETF track is a possible future path rather than a current status.

The specification is licensed Apache-2.0.

---

## The reference client

A protocol without an implementation is an opinion.

[Meridian](/posts/meridian) is the reference client: a local-first desktop reader that consumes RSS, Atom and MMSP through one model and proves the normalization rules against real feeds.

The pairing is deliberate. The spec keeps the client honest; the client keeps the spec real.

---

## MMSP at a glance

<div style="display: flex; flex-wrap: wrap; gap: 2rem; justify-content: center; align-items: flex-start; margin-top: 1rem;">

<div style="flex: 1; min-width: 250px;">
  <h3>Protocol</h3>
  <ul>
    <li>JSON format, application/mmsp+json</li>
    <li>Semantic superset of RSS 2.0 and Atom</li>
    <li>Twelve first-class item types</li>
    <li>Pull-only, no push, no notifications</li>
    <li>300 second minimum poll interval</li>
    <li>HTTPS-only URLs</li>
    <li>Well-known endpoint discovery</li>
    <li>Optional Calm Consumption Profile</li>
  </ul>
</div>

<div style="flex: 1; min-width: 250px;">
  <h3>Artefacts</h3>
  <ul>
    <li>Versioned specification document</li>
    <li>JSON Schema 2020-12 definitions</li>
    <li>Worked feed and item examples</li>
    <li>Conformance test suite</li>
    <li>Reference client (Meridian)</li>
    <li>Live production feed on this site</li>
    <li>Apache-2.0 licence</li>
  </ul>
</div>

</div>

---

## What this taught me

Writing software teaches you what a system does. Writing a specification teaches you what you actually believe.

Every MUST in the document is a design decision defended in public. Every SHOULD is an admission that context matters. The conformance suite is the difference between a specification and an essay.

The deepest lesson is the calm constraint. It would have been easy to leave politeness to client authors as a cultural norm. Making it a wire-level property (pull-only, minimum interval) turns a hope into a guarantee.

*Protocols outlive platforms. That is the entire bet.*
