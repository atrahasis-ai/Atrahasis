# Atrahasis AASL Runtime Master Specification

Version: 1.0.0\
Status: Canonical Architecture Specification\
Date: 2026-03-08

------------------------------------------------------------------------

# 1. Overview

Atrahasis is a distributed collective intelligence system whose internal
language is **AASL (Atrahasis Agent Semantic Language)**.\
This document defines the **complete architecture, runtime model,
communication contracts, storage model, governance rules, and
implementation plan** for the first working AASL-native Atrahasis
runtime.

The system converts external information into **structured semantic
knowledge**, executes reasoning workflows through cooperating agents,
verifies results, and stores trusted knowledge in a reusable semantic
memory.

Core architectural principle:

> All internal knowledge in Atrahasis is represented as AASL semantic
> objects.

------------------------------------------------------------------------

# 2. Core System Layers

Atrahasis operates through a layered architecture:

External Inputs → AASC Compiler → AASL Semantic Layer → CIOS
Orchestration → Agent Layer → Verification Layer → Semantic Memory →
Distributed Federation

Once data enters the system it is converted into AASL semantic
structures and all reasoning operates on those structures.

------------------------------------------------------------------------

# 3. AASL Language

AASL is a machine-native semantic language used to represent:

-   agents
-   datasets
-   tasks
-   actions
-   claims
-   evidence
-   verification states
-   provenance chains

## Core Object Types

AGT -- agent identity\
MOD -- model definition\
DS -- dataset\
TSK -- task\
ACT -- action\
CLM -- claim\
EVD -- evidence\
CNF -- confidence\
PRV -- provenance\
VRF -- verification\
CST -- constraint\
TIM -- timestamp

## Document Structure

HEADER\
LEXICON\
OBJECTS\
RELATIONS\
PROVENANCE\
VERIFICATION\
FOOTER

AASL documents are canonicalized before hashing, storage, or federation.

------------------------------------------------------------------------

# 4. AASL Parser

The parser converts raw AASL text into structured semantic objects.

Responsibilities include:

-   lexical tokenization
-   grammar parsing
-   AST construction
-   reference detection
-   diagnostics reporting

Outputs include:

-   CST (Concrete Syntax Tree)
-   AST (Semantic Object Graph)
-   Symbol Table
-   Parse Diagnostics

------------------------------------------------------------------------

# 5. AASL Validator

The validator ensures artifacts meet language rules.

Validation layers include:

1.  structural validation\
2.  template validation\
3.  ontology validation\
4.  reference validation\
5.  canonicalization validation\
6.  document validation

Artifacts failing validation are rejected or quarantined.

------------------------------------------------------------------------

# 6. AASL Canonicalization

Canonicalization guarantees deterministic representation of semantic
meaning.

Normalization rules include:

-   field ordering
-   identifier normalization
-   timestamp normalization
-   numeric normalization
-   canonical section ordering

Canonical representation enables semantic hashing, deduplication,
verification comparison, and distributed equivalence detection.

------------------------------------------------------------------------

# 7. AASC Compiler

The Atrahasis Semantic Compiler converts external inputs into AASL.

Supported inputs include:

-   natural language
-   markdown documents
-   structured datasets
-   JSON payloads
-   draft AASL

Compiler stages:

Source Adapter → Semantic Extraction → Ontology Mapping → Identity
Assignment → Canonicalization → Validation → AASL Generation

------------------------------------------------------------------------

# 8. Runtime Object Model

The runtime converts parsed AASL objects into a live semantic graph.

Responsibilities:

-   object registry
-   reference resolution
-   lifecycle state management
-   mutation control
-   query access

Object lifecycle states include parsed, validated, canonical, verified,
and immutable.

------------------------------------------------------------------------

# 9. Agent Model

The first runtime contains five agent types:

Coordinator Agent -- workflow orchestration\
Research Agent -- evidence extraction\
Analysis Agent -- claim generation\
Verification Agent -- claim validation\
Memory Agent -- semantic storage and reuse

Agents operate exclusively on AASL bundles.

------------------------------------------------------------------------

# 10. AACP Messaging Protocol

Atrahasis agents communicate using AACP.

Structure:

HEADER + PAYLOAD

Payloads contain AASL semantic bundles.

Core message classes:

task_submission\
task_assignment\
task_result\
verification_request\
verification_result\
memory_lookup_request\
memory_lookup_result\
memory_admission_request\
memory_admission_result\
state_update\
error_report

------------------------------------------------------------------------

# 11. Semantic Bundle Model

Bundles are the operational container for AASL objects.

Bundle metadata includes:

-   bundle_id
-   bundle_type
-   workflow_id
-   task_id
-   produced_by
-   validation_state
-   canonical_state
-   verification_state
-   storage_tier
-   canonical_hash

Bundles preserve workflow context and semantic cohesion.

------------------------------------------------------------------------

# 12. Semantic Memory

Atrahasis stores verified semantic bundles in shared memory.

Storage tiers:

draft -- intermediate artifacts\
canonical -- normalized artifacts\
verified -- trusted knowledge\
archived -- historical artifacts

Memory operations include lookup reuse, duplicate detection, admission
decisions, and retrieval.

------------------------------------------------------------------------

# 13. Storage Model

The first runtime storage schema includes:

Bundle Store\
Document Store\
Object Store\
Reference Store\
Provenance Store\
Verification Store\
Execution Store

Indexes support lookup by object ID, bundle ID, canonical hash, claim
type, and verification state.

------------------------------------------------------------------------

# 14. Query Engine

The query engine retrieves semantic knowledge.

Supported queries include:

-   object lookup
-   type queries
-   attribute filters
-   relationship traversal
-   provenance retrieval
-   verification inspection

Example query: retrieve all verified correlation claims for dataset
ds.climate.44.

------------------------------------------------------------------------

# 15. Verification Layer

Verification ensures trustworthiness of semantic knowledge.

Process:

candidate bundle → independent evaluation → evidence comparison →
verification record (VRF)

Verification results may be verified, pending, disputed, or rejected.

------------------------------------------------------------------------

# 16. Distributed Federation

Atrahasis nodes synchronize knowledge through federation.

Federation capabilities:

-   artifact exchange
-   canonical equivalence detection
-   conflict detection
-   provenance propagation
-   version synchronization

This allows distributed semantic knowledge networks.

------------------------------------------------------------------------

# 17. Governance

Governance controls language evolution.

Version model:

MAJOR.MINOR.PATCH

Governance responsibilities include ontology registry management,
proposal review, compatibility guarantees, extension modules, and
deprecation policy enforcement.

------------------------------------------------------------------------

# 18. Security Architecture

Security ensures artifact authenticity and integrity.

Security mechanisms include:

-   canonical semantic hashes
-   digital signatures
-   artifact checksums
-   provenance verification
-   node authentication
-   replay protection

These mechanisms prevent semantic tampering and forged knowledge
artifacts.

------------------------------------------------------------------------

# 19. Testing and Certification

Testing ensures consistent implementations.

Test suites include:

-   parser tests
-   compiler tests
-   canonicalization tests
-   validator tests
-   runtime tests
-   federation tests
-   security tests

Certification levels include core language compliance, runtime
compliance, and full ecosystem compliance.

------------------------------------------------------------------------

# 20. Implementation Milestones

The first working runtime should be built in this order:

1.  repo scaffolding\
2.  AASL language implementation\
3.  runtime object model\
4.  storage persistence\
5.  AACP messaging\
6.  query + memory retrieval\
7.  coordinator + agents\
8.  verification + trusted memory\
9.  external APIs\
10. operator tooling

The first architecturally complete runtime appears at milestone 7.

------------------------------------------------------------------------

# 21. End-to-End Workflow

User Input → AASC Compilation → AASL Task Bundle → Coordinator
Assignment → Research & Analysis Agents → Candidate Claim → Verification
→ Verified Bundle → Semantic Memory → Future Reuse

This loop creates cumulative machine knowledge.

------------------------------------------------------------------------

# 22. Conclusion

The Atrahasis AASL Runtime combines:

-   AASL semantic language
-   distributed agent orchestration
-   verification networks
-   persistent semantic memory
-   federation protocols
-   governance and security frameworks

Together these components form a scalable semantic intelligence
infrastructure capable of accumulating, verifying, and reusing
machine-readable knowledge across distributed systems.
