# T-063 PRE-IDEATION: Prior Art Quick Scan
**Role:** Prior Art Researcher | **Tier:** OPERATIONAL
**Date:** 2026-03-12

## Problem
Identity is fragmented across 6 AAS specs (C5, C7, C8, C14, C17, C31). No canonical agent registration protocol, no unified AgentID format, no single lifecycle from creation through citizenship to retirement.

## Known Solutions

| System | Relevance | Solves | Doesn't Solve |
|--------|-----------|--------|---------------|
| W3C DID / Verifiable Credentials | HIGH | Identifier format, key management, credential issuance/verification | AI-specific lifecycle, behavioral fingerprinting, reputation, model upgrade continuity |
| SPIFFE/SPIRE | MEDIUM | Runtime workload attestation, automated credential rotation | Persistent reputation, governance, earned citizenship |
| Substrate Identity Pallet | HIGH | On-chain registrar attestation, staking/governance weight | AI agent lifecycle, behavioral Sybil defense |
| FIPA AMS/AID | MEDIUM | Agent registration, capability advertisement | Modern crypto identity, reputation, Sybil resistance |
| Actor Model (Erlang/Akka) | MEDIUM | Lifecycle management, location-transparent identity | Trust, reputation, persistent identity |
| OAuth 2.0 Machine Identity | LOW | Authentication flows | Everything else |

## Closest Prior Art Combination
DID + Verifiable Credentials + Substrate Identity Pallet. No known system combines cryptographic self-sovereign identity with behavioral fingerprinting, epistemic reputation, economic stake, and graduated citizenship for AI agents.

## Critical Gap in All Prior Art
No known system addresses **model upgrade identity continuity** — the concept that an AI agent's fundamental nature can change while retaining accumulated identity and reputation. This is unique to AI agents and has no precedent in human, organizational, or workload identity systems.
