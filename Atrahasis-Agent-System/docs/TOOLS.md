# Tooling Conventions (v1.0)

## Goal
Make agent actions reproducible, reviewable, and safe.

## Read-before-write
Before editing any artifact:
- open it fully
- summarize current structure in the invention log

## Patch discipline
Prefer small, isolated edits:
- one logical change per commit
- avoid "mega commits"

## Standard prototyping tools
Keep the authoritative conventions in INVENTION_CONTEXT.

Typical:
- Python prototypes: `pip install -r requirements.txt`, `pytest`, `python demo.py`
- Node prototypes: `npm install`, `npm test`, `node demo.js`
- Rust prototypes: `cargo build`, `cargo test`

## Diff discipline
Before finishing:
- review all changes
- ensure no shared artifact edits slipped in
- ensure no secrets or proprietary content leaked

## No secrets or IP leakage
Never paste or commit secrets. Never include proprietary third-party content in specifications without proper attribution. If sensitive content appears in outputs, redact it and flag the issue.
