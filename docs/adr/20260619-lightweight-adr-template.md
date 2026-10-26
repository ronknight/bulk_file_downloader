# ADR: Lightweight Architecture Decision Records

## Date (ISO)
2026-06-19

**Context**: We need a lightweight, version-controlled way to capture
architectural decisions without heavy ceremony.

## Decision
Adopt single-page markdown ADRs in `docs/adr/`, named `YYYYMMDD-<title>.md`,
each including: ISO date, context, decision, consequences, owner, and an optional
git tag.

## Consequences
**Positive**: decisions are explicit, searchable, and version-controlled.
**Tradeoffs**: ADRs are living documents and can drift if not updated with code.

## Decision Owner
Project Lead

## Git Tag
adr/lightweight-adr-template
