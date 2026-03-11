# Atrahasis Developer Onboarding Manual

Version: 1.0.0 Date: 2026-03-08 Status: Developer Guide

------------------------------------------------------------------------

# 1. Purpose

This manual helps engineers and AI coding agents begin working on the
Atrahasis AASL‑native runtime.

It explains:

-   system philosophy
-   repository structure
-   development workflow
-   coding expectations
-   how to run the system locally
-   how to contribute safely without breaking the architecture

This document should be the **first thing new contributors read**.

------------------------------------------------------------------------

# 2. What Atrahasis Is

Atrahasis is a **semantic intelligence runtime** where all knowledge is
represented in **AASL (Atrahasis Agent Semantic Language)**.

The system:

1.  converts input into AASL
2.  runs reasoning workflows through agents
3.  verifies semantic results
4.  stores verified knowledge in semantic memory
5.  reuses knowledge for future tasks

Atrahasis is not a traditional AI system based on raw text prompts.\
It is a **structured semantic intelligence architecture**.

------------------------------------------------------------------------

# 3. Key Concepts

## AASL

Machine‑native language for representing meaning.

Example object:

    CLM{id:c.correlation.001 type:correlation subject:var.temp object:var.co2}

## Semantic Bundle

Operational container for AASL objects.

Bundles move through the runtime and contain task context and outputs.

## Agents

Specialized components that perform semantic reasoning tasks.

Agent roles:

-   Coordinator
-   Research
-   Analysis
-   Verification
-   Memory

## Verification

Ensures claims are trustworthy before entering shared semantic memory.

------------------------------------------------------------------------

# 4. Repository Layout

Atrahasis uses a **monorepo architecture**.

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

Key directories:

### apps/

Entry points:

-   API gateway
-   operator console
-   CLI tools

### services/

Runtime services:

-   ingress-service
-   coordinator-service
-   agent-service
-   verification-service
-   memory-service
-   query-service
-   storage-service

### packages/

Shared libraries including:

-   AASL language implementation
-   query engine
-   storage contracts
-   agent contracts
-   security primitives

------------------------------------------------------------------------

# 5. Local Development Setup

### Step 1 --- Clone Repo

    git clone <repo>
    cd atrahasis-runtime

### Step 2 --- Install Dependencies

    install dependencies using package manager

### Step 3 --- Run Development Environment

    run local runtime using scripts/dev-start

### Step 4 --- Load Test Fixtures

    scripts/load-fixtures

### Step 5 --- Run System

    submit test task using CLI

------------------------------------------------------------------------

# 6. Development Workflow

### 1. Create branch

    feature/<description>

### 2. Implement feature

Follow semantic closure rules.

### 3. Run tests

    run test suite

### 4. Submit pull request

Pull requests must include:

-   description
-   semantic impact explanation
-   test coverage

------------------------------------------------------------------------

# 7. Coding Standards

All code must follow:

-   semantic closure policy
-   explicit schema usage
-   strict typing
-   documented contracts
-   deterministic behavior where required

Never introduce hidden semantic behavior.

------------------------------------------------------------------------

# 8. Testing

Testing occurs at multiple levels:

### Unit Tests

Parser, validator, canonicalizer, runtime modules.

### Integration Tests

Services interacting with each other.

### End‑to‑End Tests

Full runtime workflow.

Example E2E test:

1.  Submit task
2.  Run agents
3.  Produce claim
4.  Verify claim
5.  Store verified bundle
6.  Reuse knowledge on second request

------------------------------------------------------------------------

# 9. Observability

Runtime observability tracks:

-   workflow state
-   bundle counts
-   memory hit rate
-   verification success
-   agent execution time

Metrics should be added for every major subsystem.

------------------------------------------------------------------------

# 10. Debugging

Common debugging methods:

### Inspect Workflow

Use operator console to view workflow traces.

### Inspect Bundle

    aasl-cli inspect <bundle_id>

### Query Semantic Objects

    semantic query API

### Export Bundle

    export bundle as .aas

------------------------------------------------------------------------

# 11. Security Awareness

Engineers must respect the security architecture.

Never bypass:

-   verification
-   admission rules
-   canonicalization
-   provenance recording

Security checks exist to prevent semantic corruption.

------------------------------------------------------------------------

# 12. Common Mistakes

### Introducing Hidden Semantics

Meaning must not exist only in code or prompts.

### Bypassing Canonicalization

Canonical form must always be produced before hashing or storage.

### Direct Database Writes

All semantic writes must go through the memory service.

### Skipping Verification

Unverified claims must never enter trusted memory.

------------------------------------------------------------------------

# 13. Best Practices

-   prefer semantic objects over free text
-   use bundle‑centric workflows
-   preserve provenance
-   validate early
-   canonicalize consistently
-   keep reasoning explainable

These practices maintain the integrity of the system.

------------------------------------------------------------------------

# 14. Getting Help

If uncertain about architectural decisions:

1.  review Master Specification
2.  review Semantic Closure Policy
3.  review Architecture Diagram Set
4.  consult system maintainers

Do not guess when semantic integrity may be affected.

------------------------------------------------------------------------

# 15. Final Notes

Atrahasis is designed to accumulate verified knowledge over time.

Every contribution should strengthen:

-   semantic clarity
-   verification reliability
-   knowledge reuse
-   system transparency

The goal is not just building software.

The goal is building a **persistent machine intelligence substrate**.
