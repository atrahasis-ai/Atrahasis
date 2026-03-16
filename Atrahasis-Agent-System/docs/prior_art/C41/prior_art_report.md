# C41 Prior Art Report - Layered Semantic Capability Manifest (LSCM)

## Scope

This report evaluates prior art relevant to `T-214`: agent discovery documents,
capability manifests, signed metadata, trust-chain disclosure, and semantic
capability advertisement for Alternative B.

## Primary comparison set

1. A2A Agent Cards and adjacent AI plugin manifests
2. OpenAPI / AsyncAPI / gRPC discovery descriptors
3. OCI manifests, SBOMs, and signed artifact attestations
4. OIDC discovery metadata and key-discovery documents
5. service registry and marketplace metadata records
6. existing Atrahasis surfaces (`C38`, `C39`, `C40`, `T-212`, `C36`)

## Findings

### 1. Discovery cards exist, but they are usually shallow

A2A-style cards and plugin manifests show that well-known discovery documents
are practical, but they usually stop at endpoint, auth, and coarse capability
claims. They do not express semantic object support, ontology snapshots, or
bridge-honest trust posture.

### 2. API descriptors solve operation shape, not trust posture

OpenAPI, AsyncAPI, and gRPC descriptors are strong at operation and schema
enumeration, but they do not serve well as the one canonical signed discovery
contract for multi-binding semantic agents.

### 3. Signed artifact manifests contribute the update and issuer pattern

OCI manifests and SBOM-style attestations show good patterns for signatures,
hash-linked metadata, and visible supersession. Their gap is that they describe
artifacts, not live protocol capability surfaces.

### 4. Identity metadata solves only one section of the problem

OIDC discovery and key-distribution metadata help with issuer and auth-scheme
disclosure, but they are too narrow to describe supported message families,
semantic types, verification posture, or native-versus-bridge disclosure.

### 5. Registry listings are useful but not authoritative enough

Service catalogs and marketplace entries are excellent discovery indexes, but
they tend to flatten self-asserted capability, registry judgment, and runtime
status into one mutable record.

## Prior-art conclusion

The component patterns are known. The novelty in `C41` is their bounded
Atrahasis-native synthesis:
- one signed endpoint-scoped manifest,
- explicit trust posture tied to `C40`,
- explicit message-family and semantic-capability disclosure tied to `C39` and
  `T-212`,
- native-versus-bridge distinction as a first-class field,
- visible supersession without runtime-state overload.

## Confidence

Confidence: `4/5`

Reason:
- strong prior art exists for each primitive,
- no direct match was found for the exact combined Alternative B manifest
  surface,
- novelty is architectural and integrative rather than cryptographically
  foundational.
