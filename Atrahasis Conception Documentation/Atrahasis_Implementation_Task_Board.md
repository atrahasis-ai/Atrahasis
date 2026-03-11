# Atrahasis Implementation Task Board / Execution Plan

Version: 1.0.0\
Date: 2026-03-08\
Status: Canonical Build Plan

This document converts the Atrahasis runtime architecture into an
**executable development plan**.\
Tasks are structured so they can be imported into GitHub Issues, Linear,
or Jira.

Each task contains:

-   Task ID
-   Title
-   Description
-   Owner Role
-   Dependencies
-   Deliverables
-   Acceptance Criteria

Tasks are grouped by milestone but ordered by **real dependency flow**.

------------------------------------------------------------------------

# Milestone 0 --- Repository and Project Scaffolding

## T-0001 Create Monorepo Structure

**Owner:** Platform Engineering

Create repository:

    atrahasis-runtime/
    apps/
    services/
    packages/
    schemas/
    tests/
    testdata/
    docs/
    infra/
    scripts/
    tools/

Deliverables: - Repository initialized - Base README

Acceptance: - Repo clones successfully - Basic build script runs

------------------------------------------------------------------------

## T-0002 Initialize Core Packages

Create packages:

    aasl-core
    aasl-parser
    aasl-validator
    aasl-canonicalizer
    aasl-runtime
    aasl-compiler
    aasl-query
    aasl-storage-contracts
    aasl-security
    aacp-contracts
    agent-contracts
    shared-types
    observability

Acceptance: - Packages compile - Dependency boundaries enforced

------------------------------------------------------------------------

## T-0003 Initialize Services

Create service directories:

    ingress-service
    coordinator-service
    agent-service
    verification-service
    memory-service
    query-service
    storage-service

Acceptance: - Each service runs stub process

------------------------------------------------------------------------

## T-0004 Setup CI Pipeline

CI steps:

-   install dependencies
-   lint
-   build
-   run tests

Acceptance: - CI passes on main branch

------------------------------------------------------------------------

# Milestone 1 --- AASL Language Core

## T-1001 Define Core Object Types

Define objects:

AGT, MOD, DS, TSK, ACT, CLM, EVD, CNF, PRV, VRF, CST, TIM

Acceptance: - Types compile in `aasl-core`

------------------------------------------------------------------------

## T-1002 Implement Parser

Implement:

-   lexer
-   grammar parser
-   AST model
-   diagnostics

Acceptance: - `.aas` files parse into AST

------------------------------------------------------------------------

## T-1003 Implement Validator

Validation rules:

-   object template validation
-   ontology validation
-   reference validation

Acceptance: - Invalid artifacts rejected

------------------------------------------------------------------------

## T-1004 Implement Canonicalizer

Canonical rules:

-   field ordering
-   identifier normalization
-   timestamp normalization

Acceptance: - Canonical output deterministic

------------------------------------------------------------------------

# Milestone 2 --- Runtime Object Model

## T-2001 Runtime Object Registry

Implement:

-   object registry
-   type registry

Acceptance: - Lookup by object ID works

------------------------------------------------------------------------

## T-2002 Reference Resolution

Implement:

-   outbound reference resolution
-   inbound reference tracking

Acceptance: - Graph traversal works

------------------------------------------------------------------------

## T-2003 Runtime State Model

States:

parsed → validated → canonical → verified

Acceptance: - State transitions recorded

------------------------------------------------------------------------

# Milestone 3 --- Storage Layer

## T-3001 Bundle Store

Fields:

-   bundle_id
-   bundle_type
-   workflow_id
-   canonical_hash
-   storage_tier

Acceptance: - Bundles persist

------------------------------------------------------------------------

## T-3002 Object Store

Store:

-   object_id
-   object_type
-   field_map
-   canonical_text

Acceptance: - Objects retrievable

------------------------------------------------------------------------

## T-3003 Reference Store

Store:

-   source_object
-   target_object
-   reference_type

Acceptance: - Reference queries function

------------------------------------------------------------------------

## T-3004 Rehydration

Load persisted bundle → runtime graph

Acceptance: - Runtime reload reproduces objects

------------------------------------------------------------------------

# Milestone 4 --- Messaging Protocol

## T-4001 Implement AACP Header

Fields:

-   protocol_version
-   message_id
-   workflow_id
-   sender_id
-   receiver_id
-   message_class

Acceptance: - Headers validated

------------------------------------------------------------------------

## T-4002 Implement Bundle Wrapper

Bundle metadata:

-   bundle_id
-   bundle_type
-   validation_state

Acceptance: - Bundle wrapper parsed

------------------------------------------------------------------------

## T-4003 Implement Message Classes

Implement:

task_submission\
task_assignment\
task_result\
verification_request\
verification_result\
memory_lookup_request\
memory_lookup_result\
memory_admission_request\
memory_admission_result

Acceptance: - Message routing works

------------------------------------------------------------------------

# Milestone 5 --- Query and Memory

## T-5001 Query Engine

Implement:

-   object lookup
-   type lookup
-   graph traversal

Acceptance: - Semantic queries succeed

------------------------------------------------------------------------

## T-5002 Memory Lookup

Implement:

-   canonical hash lookup
-   reusable bundle retrieval

Acceptance: - Memory hit detection works

------------------------------------------------------------------------

# Milestone 6 --- Agent Execution

## T-6001 Ingress Service

Features:

-   accept external input
-   compile via AASC
-   emit task bundle

Acceptance: - Tasks enter system

------------------------------------------------------------------------

## T-6002 Coordinator Service

Responsibilities:

-   workflow orchestration
-   task assignment
-   state tracking

Acceptance: - Workflow progresses correctly

------------------------------------------------------------------------

## T-6003 Research Agent

Responsibilities:

-   extract evidence
-   emit EVD + PRV

Acceptance: - Evidence bundles produced

------------------------------------------------------------------------

## T-6004 Analysis Agent

Responsibilities:

-   generate claims
-   emit CLM + CNF

Acceptance: - Claim bundles produced

------------------------------------------------------------------------

# Milestone 7 --- Verification and Memory Admission

## T-7001 Verification Agent

Produces:

VRF objects

Acceptance: - Claim verification recorded

------------------------------------------------------------------------

## T-7002 Memory Admission

Admission states:

accepted\
duplicate_reused\
rejected

Acceptance: - Verified bundles stored

------------------------------------------------------------------------

## T-7003 Trusted Tier

Implement storage tiers:

draft → canonical → verified

Acceptance: - Verified knowledge reusable

------------------------------------------------------------------------

# Milestone 8 --- External APIs

## T-8001 API Gateway

Routes:

/ingress\
/workflows\
/semantic\
/memory\
/export\
/ops

Acceptance: - Gateway operational

------------------------------------------------------------------------

## T-8002 Core Endpoints

Examples:

POST /v1/ingress/tasks\
GET /v1/workflows/{id}\
POST /v1/semantic/query\
POST /v1/memory/lookup\
GET /v1/export/bundles/{id}

Acceptance: - Endpoints return expected results

------------------------------------------------------------------------

# Milestone 9 --- Operator Tooling

## T-9001 Runtime Metrics

Track:

-   tasks
-   bundles
-   memory hit rate
-   verification success

Acceptance: - Metrics exported

------------------------------------------------------------------------

## T-9002 Operator Console

Features:

-   workflow trace
-   bundle inspection
-   verification failures

Acceptance: - Console shows runtime state

------------------------------------------------------------------------

# Final Acceptance Scenario

System passes when the following succeeds:

1.  Submit natural language task
2.  Compile to AASL
3.  Execute research + analysis agents
4.  Produce claim bundle
5.  Verify claim
6.  Store verified bundle
7.  Submit equivalent task again
8.  Runtime retrieves stored bundle instead of recomputing

This proves Atrahasis is **cumulative semantic intelligence**, not just
an agent pipeline.

------------------------------------------------------------------------

# End of Implementation Plan
