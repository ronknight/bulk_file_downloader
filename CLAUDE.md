<!-- DOC-SYSTEM:START - managed by v9-init.py; content in this block is regenerated -->
# Repository Working Agreement

Canonical instructions for every AI assistant (Claude Code, GitHub Copilot,
Cursor, Windsurf, Cline, ...) working in this repository. Tool-specific folders
(`.cursor/`, `.copilot/`, `.roo/`, ...) contain only a pointer back to this file
so there is one source of truth, not nine drifting copies.

## Definition of Done — apply to EVERY change

These steps are part of doing the work, not a separate "documentation phase".
Carry them out as you complete a change; you do not need to ask permission first,
but DO say in one line what you updated so the user can see docs kept pace.

1. **Restore point** — before a significant or risky change, snapshot the project:
   `./archive-project.ps1` (Windows) or `./archive-project.sh` (Unix/macOS).
   Snapshots land in `archive/<YYYY-MM-DD_HHmmss>/` and are git-ignored, so the
   state can always be restored.
2. **Changelog** — add a dated entry under `## [Unreleased]` in `CHANGELOG.md`:
   `#### YYYY-MM-DD - <summary>`, naming the files/behavior that changed.
3. **Docs** — update any affected docs under `docs/` (`*.md`).
4. **Diagrams** — if data flow, control flow, or the user experience changed,
   update the relevant `openspec/diagram/*.md` (mermaid).
5. **ADR** — for an architectural decision, add a record at
   `docs/adr/YYYYMMDD-<kebab-title>.md` using the template already in `docs/adr/`.

Skip any step that genuinely does not apply (e.g. no architectural decision was
made) — but state that you did, rather than silently dropping it.

## File organization

- Root holds only `README.md`, `CHANGELOG.md`, `PRD.md`, and the app's own files.
- Documentation → `docs/`  ·  Specs & diagrams → `openspec/`  ·  Snapshots → `archive/`
- Do not create stray markdown at the repo root.

## Working style

- **New feature**: fit it to existing architecture (reference `openspec/` specs)
  → design API/data contracts → implement → tests → note deployment impact.
- **Bug fix**: reproduce → root-cause → minimal fix → regression test.
- **Security review**: secrets handling, input validation, dependency exposure.

## Python conventions

- Type hints on function signatures; raise specific exceptions, never fail silently.
- Tests with pytest under `tests/` (or co-located).
- Import order: standard library → third-party → local.
<!-- DOC-SYSTEM:END -->
