# T-066 Domain Analogy Brief

## Purpose

Find structural analogies for the missing operational monitoring and incident-response layer before ideation promotion.

## Analogy 1 - Air Traffic Control

- Structural parallel: many semi-autonomous actors operate concurrently under shared safety constraints while a control layer watches trajectories, separation minima, and conflict risk.
- Useful transfer: normalize heterogeneous telemetry into common hazard states, escalate early from weak signals, and distinguish advisory from mandatory interventions.
- Limitation: air traffic control manages movement conflicts more than epistemic or governance integrity.

## Analogy 2 - Hospital Triage + Intensive Care

- Structural parallel: weak symptoms become structured severity classes, escalation depends on rate of deterioration, and different teams intervene under bounded authority.
- Useful transfer: incident severity should reflect both current harm and probable cascade speed; dashboards should surface trend and instability, not only point-in-time alarms.
- Limitation: hospitals center on individual patients, while Atrahasis incidents can span parcels, committees, ledgers, and governance tracks simultaneously.

## Analogy 3 - Immune System / Inflammatory Cascade

- Structural parallel: local detectors trigger targeted response first, then escalate to systemic containment only if the threat exceeds local capacity or persistence thresholds.
- Useful transfer: default to local containment, but escalate to cross-layer or constitutional response when multi-signal correlation shows systemic risk. Avoid "autoimmune" overreaction by requiring evidence-weighted escalation.
- Limitation: biological immunity is adaptive but not audit-friendly; Atrahasis needs explicit evidence chains and replayable decision rationale.

## Analogy 4 - Nuclear Plant Control Room

- Structural parallel: a control layer watches a small set of high-value invariants, uses layered alarm states, and never confuses observation with permission to change protected systems.
- Useful transfer: separate observation, recommendation, and action authority. Some playbooks may auto-execute; governance-sensitive actions must remain bounded by constitutional gates.
- Limitation: nuclear systems are much more closed-world than Atrahasis and have fewer open-ended external actors.

## Analogy 5 - Black Box + Incident Command System

- Structural parallel: incidents need both an immutable event recorder and a standardized command structure for containment, investigation, communication, and recovery.
- Useful transfer: every incident should mint a single durable case object that carries evidence, timeline, responders, decisions, and postmortem outputs. Response roles should be explicit even when partially automated.
- Limitation: standard incident command assumes human organizations; Atrahasis must accommodate mixed human/agent operators and machine-triggered escalations.

## Recommendation

The most useful synthesis is:

- hazard-state tracking from air traffic control,
- severity and deterioration logic from clinical triage,
- local-to-systemic escalation from immune response,
- strict authority separation from nuclear operations,
- evidence-centered case management from black-box and incident-command practice.

This points toward an invention where the core object is not merely an alert or dashboard widget, but an incident capsule that unifies signals, escalation state, response playbooks, and audit evidence under explicit authority boundaries.
