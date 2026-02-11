---
date: 2026-02-11 21:00
emoji: 🧮
one_liner: Decision authority should be designed around decision type not job title.
tags:
- cat:leadership
- decision-making
- authority
- operating-model
- cto
title: Authority mapped to decision type
---

# Design authority around decision type not role title

Most organisations assign decision authority through hierarchy.

Titles imply ownership. Seniority implies final say.

This feels intuitive.

*It is also structurally imprecise.*

Authority works best when it is mapped to decision type rather than organisational chart.

The CTO should not decide more because they are senior.

*The CTO should decide where decision types change domain.*

## Start with decision categories

Technology organisations repeatedly generate the same kinds of decisions.

Product behaviour decisions.  
Domain local technical decisions.  
Cross domain architectural trade offs.  
Operational risk tolerance decisions.  
Commercial constraint decisions.

Confusion begins when these are blurred.

*Blurred decision types create upward drift.*

When a domain lead cannot tell whether a choice is local or cross domain it escalates. When product ambition conflicts with technical constraint without a defined resolution surface it escalates. When operational risk tolerance is implicit it escalates.

Escalation is rarely about capability.

*It is about classification failure.*

## Domain local technical decisions

These belong within a bounded context.

Library selection inside a service.  
Data modelling within a defined domain.  
Refactoring strategy internal to a team.  
Implementation approach.

If these escalate routinely either trust is weak or boundaries are unclear.

The CTO should not participate here.

*If the CTO is required for local design the surface is not closed.*

Authority at this level belongs to the domain engineering lead or architect. The boundary must be explicit. The non escalation zone must be visible.

## Cross domain architectural trade offs

These are different.

Shared platform strategy.  
API conventions across services.  
Security posture spanning teams.  
Performance targets that affect multiple domains.

These decisions change the shape of more than one system at once.

They cannot sit safely within a single team.

This is where the CTO should operate.

*The CTO owns the intersections not the interiors.*

The value is leverage not volume.

## Product and engineering trade offs

This surface is often the least defined.

Performance versus feature depth.  
Delivery pace versus architectural debt.  
Resilience versus time to market.

These are not purely technical decisions. They are not purely product decisions.

If ownership is unclear escalation becomes habitual and tension becomes cultural.

The CTO should own the technical side of the trade off. The product lead should own behavioural intent. Resolution must be explicit.

*Ambition versus constraint requires a named authority surface.*

Without one the CTO absorbs both risk and friction.

## Operational risk tolerance

Risk decisions require defined bands.

Launching with known debt.  
Accepting temporary degradation.  
Deferring resilience work.

If every operational risk call escalates the tolerance surface has not been designed.

The CTO should define acceptable ranges. Others should operate within them.

*Setting tolerance is different from adjudicating every exception.*

When tolerance is implicit escalation becomes routine and centrality becomes structural rather than deliberate. Authority stops being designed and starts being absorbed.

## The structural test

Ask a simple question.

What decisions would the organisation still make correctly if the CTO were absent for two weeks.

If the answer is very few authority is concentrated rather than designed.

Healthy systems continue to function within defined domains. Escalation occurs at intersections not at volume.

*The CTO designs decision surfaces rather than absorbing decision load.*

Authority should be mapped to decision type.

Role title is an implementation detail.

If escalation volume is high classification is weak.

*Fix the classification and the load reduces.*
