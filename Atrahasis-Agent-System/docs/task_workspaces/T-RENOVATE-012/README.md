# T-RENOVATE-012 Workspace

## Purpose

Audit the `C19` through `C42` range for residual assumptions that contradict the sovereign four-membrane doctrine, with special attention to:

- public agent marketplace assumptions,
- uncontrolled external API assumptions,
- stale pre-pivot execution and rollout language.

This task is narrower than a wholesale rewrite. The later protocol stack (`C38` through `C42`) already contains bounded compatibility language for legacy bridges, and that posture remains canonical unless a later retrofit retires it explicitly.

## Actual scoped surfaces

The shorthand range `C19 - C42` resolves in the repo to:

- `C19`, `C20`, `C21`, `C22`, `C23`, `C24`,
- `C31`, `C32`, `C33`, `C34`, `C35`, `C36`,
- `C38`, `C39`, `C40`, `C41`, `C42`,
- with `C25` through `C30` and `C37` absent.

## Audit questions

1. Which remaining specs still assume public marketplaces or open/public protocol control as if those were normative?
2. Which references to bridges or external systems are still valid compatibility posture rather than stale doctrine?
3. Which changes should become canonical in an audit artifact versus patched directly in the affected specs?
