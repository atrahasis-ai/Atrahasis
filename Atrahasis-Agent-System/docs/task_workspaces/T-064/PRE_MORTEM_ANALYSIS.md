# T-064 Pre-Mortem Analysis: EMA-I
**Agent:** Adapa | **Date:** 2026-03-12

## Top Failure Scenarios (20)

### Category 1: Scope & Complexity (5)
| # | Scenario | Probability | Severity | Mitigation |
|---|----------|------------|----------|------------|
| 1 | Spec tries to define every receptor for every persona, becoming 5,000+ lines | HIGH | HIGH | Define receptor contract + 5 exemplar receptors. Leave concrete receptors to implementation. |
| 2 | Session type formalism adds complexity without practical benefit | MEDIUM | MEDIUM | Provide session type examples in familiar pseudocode, not formal notation. Formal proofs in appendix. |
| 3 | Persona lattice doesn't match real-world access patterns | MEDIUM | MEDIUM | Lattice is configurable. Document override mechanism for institutional partners. |
| 4 | Translation engine scope creeps into NL/AI territory | LOW | HIGH | Hard boundary: v1.0 is structured-only. NL deferred to v2.0 with separate task. |
| 5 | Architecture overlaps with C33 OINC operational views | MEDIUM | LOW | Clear boundary: OINC owns incident capsule lifecycle; EMA-I projects OINC state to Operator persona. |

### Category 2: Integration Risk (5)
| # | Scenario | Probability | Severity | Mitigation |
|---|----------|------------|----------|------------|
| 6 | C14 governance operations don't map cleanly to receptors | MEDIUM | HIGH | Work from C14's GTP taxonomy. Each GTP template maps to one receptor. |
| 7 | C8 DSF settlement semantics too complex for receptor model | LOW | HIGH | Provider receptors produce settlement operation descriptors, not raw DSF calls. |
| 8 | Evidence chain conflicts with C23 EEB format | LOW | MEDIUM | IEC extends EEB, doesn't replace. Shared base fields, membrane-specific extensions. |
| 9 | Transport bindings fragment the membrane (REST vs gRPC vs MCP behave differently) | MEDIUM | MEDIUM | Transport is a binding, not the architecture. All transports go through same receptor pipeline. |
| 10 | C22 Wave schedule can't accommodate EMA-I incrementally | LOW | MEDIUM | EMA-I is already wave-aligned (W1: Developer, W2: Agent, W3: Operator, W4: Provider, W5: Trustee). |

### Category 3: Security (5)
| # | Scenario | Probability | Severity | Mitigation |
|---|----------|------------|----------|------------|
| 11 | Membrane bypass via internal component exposure | MEDIUM | CRITICAL | Constitutional parameter: MEMBRANE_BYPASS_ALERT_THRESHOLD=1. C35 Sentinel monitors. |
| 12 | Persona escalation via receptor spoofing | LOW | HIGH | Authentication before receptor binding. MIA AgentID for agents, OAuth 2.1 for humans. |
| 13 | Evidence chain storage becomes attack vector (sensitive data) | MEDIUM | MEDIUM | Evidence records contain hashes and operation descriptors, not raw input data. Raw input retention policy separate. |
| 14 | Rate limiting bypassed via distributed identities | MEDIUM | MEDIUM | Rate limiting per persona + per source IP + per AgentID. C17 MCSD detects Sybil identities. |
| 15 | Receptor version downgrade to exploit known vulnerabilities | LOW | HIGH | MIN_RECEPTOR_VERSION_LAG enforced. Sunset notification 2 epochs before enforcement. |

### Category 4: Performance (3)
| # | Scenario | Probability | Severity | Mitigation |
|---|----------|------------|----------|------------|
| 16 | Evidence generation on critical path adds unacceptable latency | MEDIUM | MEDIUM | Write-behind (async) evidence generation. Response sent before evidence committed. |
| 17 | Projection computation too expensive for Operator persona (many layers to query) | LOW | MEDIUM | Lazy computation + epoch-boundary caching. Operator projections precomputed at epoch boundary. |
| 18 | Receptor validation overhead at agent-scale traffic (6000 RPM) | LOW | LOW | Session type validation is O(n) in message size. Pre-compiled validators. |

### Category 5: Adoption (2)
| # | Scenario | Probability | Severity | Mitigation |
|---|----------|------------|----------|------------|
| 19 | Developers find session types unfamiliar and avoid receptor model | MEDIUM | MEDIUM | SDK generation hides session types. Developers interact via generated TypeScript/Python clients. |
| 20 | MCP gateway ecosystem makes custom membrane architecture unnecessary | MEDIUM | MEDIUM | EMA-I's moat is epistemic-native binding (claim classes, tidal epochs). MCP gateways are generic. If MCP evolves epistemic awareness, EMA-I adapts to become an MCP-native membrane. |

## Pre-Mortem Verdict

**No FATAL scenarios.** 1 CRITICAL (membrane bypass — mitigated by constitutional parameter + Sentinel). 5 HIGH (all mitigated). Risk profile is consistent with MEDIUM (4/10) assessment.

**Top risk to monitor:** Scenario 1 (scope explosion) — this is the most likely failure mode. The spec must resist the urge to define every receptor and instead define the receptor *contract* with exemplars.
