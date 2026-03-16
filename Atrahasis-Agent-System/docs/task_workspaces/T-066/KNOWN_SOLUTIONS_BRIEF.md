# T-066 Known Solutions Brief

## Purpose

Quick scan of obvious existing solution families before ideation promotion.

## Known Solution Family 1 - Observability Stacks

- Examples: OpenTelemetry, Prometheus, Grafana, Elastic, Datadog.
- What they solve well: metrics, logs, traces, dashboards, alert routing, retention policies.
- Why they are insufficient alone: they do not understand Atrahasis concepts like claim classes, epoch hierarchy, constitutional triggers, governance tracks, or Sentinel/PCVM/DSF semantics.

## Known Solution Family 2 - Incident Management Platforms

- Examples: PagerDuty, incident.io, Opsgenie, Statuspage.
- What they solve well: alert dispatch, escalation trees, on-call workflows, incident timelines, postmortems.
- Why they are insufficient alone: they assume a conventional service fleet, not a constitutional multi-layer AI infrastructure with automated-but-bounded response authority.

## Known Solution Family 3 - SIEM / SOAR

- Examples: Splunk ES, Chronicle, Sentinel, Cortex XSOAR.
- What they solve well: security event correlation, case management, forensic retention, automated response playbooks.
- Why they are insufficient alone: they are security-heavy and do not naturally model governance health, settlement integrity, or cross-layer epistemic failures as first-class incident objects.

## Known Solution Family 4 - SRE / Control-Plane Operations

- Examples: Google SRE incident command, Kubernetes control-plane health, service mesh observability.
- What they solve well: error budgets, degradation handling, runbooks, automated rollback, controller health.
- Why they are insufficient alone: Atrahasis needs incident semantics that span governance, verification, economics, knowledge, and orchestration, not only service uptime.

## Common Pattern

Across all known solutions, the recurring pattern is:

1. normalize signals,
2. correlate them into cases,
3. assign severity,
4. execute or recommend playbooks,
5. preserve evidence,
6. produce reports and postmortems.

## Gap Relative to Atrahasis

The missing Atrahasis-specific invention surface is not telemetry collection itself. It is the system-native control model that binds:

- layer-aware signal normalization,
- incident classification tied to constitutional and economic consequences,
- bounded response authority,
- audit-grade evidence chains,
- governance-safe operational playbooks.

That gap appears real enough to justify ideation rather than a pure direct-spec edit.
