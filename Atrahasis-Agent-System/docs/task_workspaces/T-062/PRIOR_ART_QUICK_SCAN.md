# T-062 Prior Art Brief: Recovery & State Assurance in Distributed Systems

**Task:** T-062 — Recovery & State Assurance
**Stage:** PRE-IDEATION Quick Scan
**Date:** 2026-03-12
**Role:** Prior Art Researcher (Operational Tier)

---

## 1. Consensus-Based Recovery Architectures

**Raft (Ongaro & Ousterhout, 2014)**
- Log-based state machine replication. Recovery = replay committed log entries from last snapshot.
- Snapshots are per-state-machine; no native cross-service snapshot coordination.

**Paxos / Multi-Paxos (Lamport, 1998; Chandra et al., 2007)**
- Checkpointing via "state transfer." Recovery of a node = request current state from quorum.
- Multi-shard Paxos (Google Spanner) uses 2PC atop per-shard Paxos. Recovery is still per-shard.

**Virtual Synchrony (Birman & Joseph, 1987)**
- Group membership + total ordering. Recovery = state transfer within a "view change."
- Cross-group consistency requires additional flush protocols.

**Gap:** All consensus protocols handle recovery within a single replicated group. None natively address ordered recovery across heterogeneous layers.

---

## 2. Microservices Recovery Patterns

**Saga Pattern (Garcia-Molina & Salem, 1987)**
- Long-lived transactions decomposed into local transactions + compensating actions.
- Choreography (event-driven) vs orchestration (central coordinator).
- Limitation: compensating actions must be idempotent; semantic rollback only.

**CQRS / Event Sourcing (Young, 2010; Fowler, 2005)**
- State = projection of immutable event log. Recovery = replay from any point.
- Cross-service recovery requires correlated event streams and global sequence numbers.

**Temporal.io (formerly Cadence, Uber 2018)**
- Durable execution: workflow state automatically checkpointed. On failure, replay from last checkpoint.
- Closest existing system to a "recovery coordinator" for microservices.

---

## 3. Database Recovery Techniques

**ARIES WAL (Mohan et al., 1992)**
- Three phases: Analysis → Redo → Undo. LSN monotonically orders all operations.
- Fuzzy checkpointing without halting operations.

**Calvin Deterministic Databases (Thomson et al., 2012)**
- Pre-order transactions before execution. Recovery = replay deterministic order. No undo log needed.

**Key insight:** ARIES-style WAL with LSN ordering is the closest analogy to a cross-layer delta journal. Challenge: each AAS layer has a different "state" concept.

---

## 4. Safety-Critical Layered Recovery

**DO-178C / ARINC 653 (Aerospace)**
- Hierarchical Health Monitor: module-level > partition-level > process-level.
- Recovery ordering is explicit and configured in system tables. Lower-criticality partitions recover after higher-criticality ones.

**IEC 61508 (Industrial Functional Safety)**
- "Safe state" concept — system must reach known safe state within Fault Tolerance Time Interval.
- Diagnostic coverage and graceful degradation to lower-capability safe states.

**Erlang/OTP Supervision Trees (Armstrong, 2003)**
- Recovery strategies: one-for-one, one-for-all, rest-for-one.
- "rest-for-one" encodes recovery ordering based on dependency — directly relevant to T-062.

---

## 5. Multi-Agent System Recovery Research

**Chandy-Lamport Distributed Snapshots (1985)**
- Consistent global snapshot via marker messages. Produces a consistent cut.
- Limitation: assumes FIFO channels and no message loss.

**Coordinated vs Uncoordinated Checkpointing (Elnozahy et al., 2002)**
- Coordinated: all agents checkpoint simultaneously. Expensive but simple recovery.
- Uncoordinated: agents checkpoint independently. Risk of "domino effect" cascading rollbacks.
- Communication-induced checkpointing: piggyback checkpoint info on messages to prevent domino effect.

---

## Gap Summary

| Capability Needed | Closest Known Solution | Gap |
|---|---|---|
| Cross-layer global snapshot | Chandy-Lamport (1985) | Assumes FIFO, homogeneous channels |
| Delta journal spanning layers | ARIES WAL + LSN | Single-database; no cross-system LSN |
| Recovery ordering | Erlang supervision trees; DO-178C | Need adaptation for heterogeneous layers |
| Recovery coordinator | Temporal.io / Saga orchestrator | Assumes stateless workers |
| Cross-layer verification | TMR / 2oo3 voting | Designed for identical replicas |
| State reconstruction | Event Sourcing replay | Per-service only |

**Conclusion:** Individual techniques exist for every sub-problem, but no known system combines cross-layer consistent snapshots, ordered hierarchical recovery, delta journaling, and witness verification into a unified architecture for heterogeneous stateful layers.
