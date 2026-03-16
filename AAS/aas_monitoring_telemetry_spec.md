# AAS Monitoring & Telemetry Specification

## Atrahasis Agent System (AAS)

This document defines the monitoring and telemetry system used by the
Atrahasis Agent System when running locally.

The telemetry system tracks swarm activity, proposal generation, task
execution, and architecture evolution events.

The goal is to provide visibility into system behavior without requiring
external infrastructure.

------------------------------------------------------------------------

# Monitoring Objectives

The telemetry system must track:

-   swarm execution progress
-   proposal generation
-   task creation and completion
-   architecture evolution events
-   system errors
-   reasoning loops

------------------------------------------------------------------------

# Logging Structure

All logs are written to the local filesystem.

Recommended directory:

/AAS/runtime/logs/

Example files:

swarm-alpha.log\
swarm-beta.log\
swarm-gamma.log\
tasks.log\
proposals.log\
system.log

------------------------------------------------------------------------

# Log Format

Logs should use JSONL (JSON Lines) format.

Each line represents one event.

Example:

{ "timestamp": "2026-03-13T12:05:23Z", "swarm": "alpha", "event":
"proposal_created", "proposal_id": "AEP-021", "cssm_state":
"AAS-State-v2.3" }

------------------------------------------------------------------------

# Telemetry Event Types

The system records several event types.

swarm_started\
swarm_completed\
task_created\
task_completed\
proposal_created\
proposal_approved\
proposal_rejected\
architecture_state_updated\
system_warning\
system_error

------------------------------------------------------------------------

# Swarm Telemetry

Each swarm maintains its own log file.

Example:

swarm-alpha.log

Events recorded:

-   swarm initialization
-   invention generation
-   proposal creation
-   council outcomes
-   swarm completion

------------------------------------------------------------------------

# Task Telemetry

Task events are recorded in tasks.log.

Each entry includes:

-   task_id
-   originating_proposal
-   assigned_agents
-   execution_status
-   completion_time

------------------------------------------------------------------------

# Proposal Telemetry

Proposal events are recorded in proposals.log.

Each entry includes:

-   proposal_id
-   proposal_type
-   originating_swarm
-   cssm_state_version
-   council_decision

------------------------------------------------------------------------

# System Telemetry

System-level events are recorded in system.log.

Examples:

-   CSSM state updates
-   kernel conflict detection
-   swarm launch events
-   recovery events

------------------------------------------------------------------------

# Reasoning Loop Detection

Telemetry must track repeated reasoning cycles.

If the same proposal or task is generated multiple times, the system
should record:

loop_detected

This allows the failure recovery protocol to intervene.

------------------------------------------------------------------------

# Log Rotation

Logs should rotate when file size exceeds a defined limit.

Recommended limit:

100 MB per file.

Older logs should be archived to:

/AAS/runtime/logs/archive/

------------------------------------------------------------------------

# Objective

The telemetry system ensures that the Atrahasis Agent System remains
observable, debuggable, and traceable during architecture evolution
cycles.
