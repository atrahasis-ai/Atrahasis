# AAS Failure Recovery Protocol

## Atrahasis Agent System (AAS)

This document defines the recovery procedures for the Atrahasis Agent
System when running locally.

Failures may include:

-   Codex process crash
-   reasoning loop detection
-   corrupted architecture state
-   swarm execution failure
-   task dependency deadlock

The goal is to allow the system to resume work from the most recent
stable system state.

------------------------------------------------------------------------

# Recovery Principles

The recovery system follows these principles:

1.  Always restore from the latest valid Canonical System State Model
    (CSSM).
2.  Never discard proposal history.
3.  Preserve swarm outputs for later analysis.
4.  Restart swarms deterministically.

------------------------------------------------------------------------

# Recovery Sources

The system restores state using:

-   CSSM snapshot
-   task graph snapshot
-   proposal registry snapshot
-   telemetry logs

Primary directory:

/AAS/runtime/

------------------------------------------------------------------------

# Recovery Triggers

Recovery procedures are triggered when:

-   Codex process terminates unexpectedly
-   reasoning loop detected
-   corrupted CSSM state detected
-   swarm execution halts unexpectedly

------------------------------------------------------------------------

# Recovery Procedure

Step 1 --- Load Canonical System State

Load the latest CSSM snapshot.

Example:

AAS-State-v2.14

------------------------------------------------------------------------

Step 2 --- Restore Task Graph

Load the most recent task graph snapshot.

Resume incomplete tasks.

------------------------------------------------------------------------

Step 3 --- Restore Proposal Registry

Reload all proposals generated before failure.

Mark unresolved proposals for review.

------------------------------------------------------------------------

Step 4 --- Restart Swarms

Restart PAEE swarms using their most recent state snapshots.

Example:

Swarm Alpha → resume from CSSM-A\
Swarm Beta → resume from CSSM-B\
Swarm Gamma → resume from CSSM-C

------------------------------------------------------------------------

# Reasoning Loop Recovery

If repeated reasoning loops are detected:

1.  pause affected swarm
2.  analyze repeated proposals
3.  modify swarm directive
4.  resume swarm exploration

Loop detection events are recorded in telemetry logs.

------------------------------------------------------------------------

# Corrupted State Recovery

If the CSSM becomes corrupted:

1.  revert to the previous valid CSSM version
2.  restore task graph
3.  restart swarm exploration

Example:

Corrupted: AAS-State-v3.1\
Recovered: AAS-State-v3.0

------------------------------------------------------------------------

# Manual Recovery

If automatic recovery fails:

1.  restart Codex
2.  run the AAS Bootstrapping Protocol
3.  load latest CSSM snapshot
4.  resume swarm exploration

------------------------------------------------------------------------

# Objective

The AAS Failure Recovery Protocol ensures that the Atrahasis Agent
System can recover from interruptions without losing architecture
reasoning progress.
