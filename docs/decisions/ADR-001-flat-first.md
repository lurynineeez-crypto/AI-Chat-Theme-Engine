# ADR-001: Flat First

Status: Accepted  
Date: 2026-07-23

## Context

High-detail AI-generated theme artwork looked attractive but repeatedly caused production problems:

- difficult transparent extraction
- inconsistent edges
- poor SVG translation
- composition drift between assets
- UI components being redesigned in every render
- weak inheritance from the source master to the phone interface

## Decision

Every official theme begins with a Flat Asset Master and a Flat Mobile Landing Master.

Flat Design is the source of truth for:

- composition
- hierarchy
- shape language
- palette
- decorative grammar
- component mapping

Premium Design is optional and may only enhance presentation after the Flat system is approved.

## Consequences

Positive:

- easier asset extraction
- better visual consistency
- clearer AI-to-Codex handoff
- Flat themes can ship as products
- Premium upgrades do not redefine the system

Trade-off:

- the first design stage may appear less spectacular than a fully rendered concept
- the workflow requires discipline before visual polish

## Review Trigger

Revisit this decision only after multiple real Theme Packs demonstrate that a different sequence produces equal consistency and better production efficiency.
