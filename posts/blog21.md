---
date: 2026-02-08 19:30
emoji: ⌛
one_liner: Slow decisions shape slow systems long before runtime behaviour is discussed.
tags:
- cat:Blog
- performance
- latency
- organisations
- product
- decision-making
title: Decision latency is the performance problem
social_image: /static/images/latencylab.png
---

# Where performance really slows down

When systems feel slow, organisations look for technical causes. When decisions feel slow, organisations call it governance. In practice, these are usually the same problem expressed in different domains.

Products do not just execute code. They execute decisions. What a system does at runtime is the accumulated result of choices made earlier about behaviour, sequencing, approval and responsibility. When those choices take time, the product inherits that latency.

*Performance is rarely lost first in code. It is lost in how long it takes to decide what should happen.*

## Where decision latency comes from

Decision latency does not usually come from incompetence. It comes from structure.

Ownership is unclear. Authority is centralised. Risk is pushed upward. Incentives reward safety over clarity. Questions that affect product behaviour require alignment across multiple groups with different priorities.

Each of these adds time. None of them look like performance problems when viewed in isolation.

*By the time a decision is made, the organisation has already paid a latency cost. That cost does not disappear when the decision is implemented. It becomes embedded in the product.*

## How slow decisions become product behaviour

Products reflect the way decisions flow through an organisation.

When decisions are sequential, products behave sequentially. When approval chains are deep, products exhibit waiting. When responsibility is fragmented, products signal excessively and block on coordination.

These behaviours often look like technical inefficiency. In reality, they are accurate implementations of organisational process.

*A system that waits for five services before responding is often modelling an organisation that requires five approvals before acting.*

## Why this is rarely discussed as performance

Decision latency is uncomfortable to measure. It has no dashboard. It does not fit neatly into a percentile. It is political rather than technical.

It is also easier to optimise code than to change how decisions are made. Code changes feel local. Organisational changes feel risky.

*As a result, organisations focus on what they can measure easily. They profile runtimes. They tune implementations. They optimise what is visible and immediate while leaving the underlying cause untouched.*

### Measurement is not the problem

Measurement itself is not the problem. Easy measurement is.

I was trained as a physicist and in any experimental discipline evidence is only meaningful when interpreted within error bars, timing and context. Numbers collected without an experimental frame give confidence without understanding.

Repeatability matters. Uncertainty matters. Using multiple methods to examine the same phenomenon matters.

Runtime metrics are valuable but only when read as part of a broader experimental approach that includes decision making, product behaviour and organisational structure.

Tools that operate at different points in the lifecycle and tools that approach the same question from different angles, are complementary rather than competitive.

What matters is not that something was measured but that the evidence was interpreted correctly and used to inform decisions rather than justify them.

*This is why performance work so often feels busy and unsatisfying.*

## Governance as an invisible queue

### Concentrated authority slows decisions

Decision latency often increases when control over decisions becomes overly concentrated. Individuals who act as permanent gatekeepers tend to optimise for stability of authority rather than speed or clarity of outcome.

*This is not a moral failing. It is an incentive effect.*

### Pure democracy does not scale

At the same time, fully democratic decision making does not scale well in most organisations. Consensus driven processes can be slow, diffuse responsibility and favour popularity over judgement.

*Organisations that attempt to vote on every consequential decision usually replace decisiveness with delay.*

### Authority must be permeable

Effective organisations sit somewhere between these extremes. Authority exists but it is not impermeable.

*Formal leaders provide direction and accountability, while influence is allowed to flow to those with relevant knowledge and situational understanding. Decisions can be challenged, clarified or bypassed when necessary, without undermining responsibility.*

### Meritocratic influence reduces latency

This balance is difficult to maintain, particularly in smaller organisations but it matters.

*Where meritocratic influence is encouraged and informal leadership is recognised, decisions tend to be made earlier and with greater clarity. Where authority is hoarded or insulated, decision latency grows and products inherit that delay.*

## Why tooling does not help here

Tools can expose runtime latency. They cannot expose decision latency directly.

By the time a tool shows a problem, the decision structure that caused it is already embedded. The product is behaving correctly according to the rules it was given.

This is why better tools often produce better explanations but not better outcomes. Insight arrives after the point where change is cheap.

*Tools are necessary. They are not sufficient.*

## What reducing decision latency looks like

*Reducing decision latency is not about moving faster. It is about deciding earlier and more clearly.*

### Make authority explicit and deliberate

Ownership is explicit. Authority is not only distributed but deliberately delegated. Product behaviour is discussed before implementation begins. Trade-offs are acknowledged rather than postponed.

*Delegation matters because authority exercised through constant oversight does not scale.*

### Delegation enables judgement

Micromanagement replaces judgement with compliance and suppresses the emergence of capable decision makers. Guidance enables learning. Control slows decisions and concentrates risk.

*When authority is delegated well, individuals are trusted to act within clear boundaries. Responsibility is taken rather than requested. Decisions happen closer to the information that motivates them, which reduces delay and improves product outcomes.*

### Treat responsiveness as a product concern

Questions about responsiveness and coordination are treated as product decisions, not technical details. When disagreement exists, it is surfaced early rather than deferred to measurement.

*This does not eliminate the need for governance. It makes governance purposeful rather than obstructive.*

## In closing

Slow systems are often the result of slow decisions reflected in code.

If performance problems persist despite repeated optimisation, the issue is rarely technical. It is almost always how long it takes an organisation to decide what it wants its product to do.

Runtime latency is visible and measurable. Decision latency is quieter and more powerful.

*Until organisations learn to see it, performance work will continue to treat symptoms while the cause remains untouched.*