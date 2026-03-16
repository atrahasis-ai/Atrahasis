# T-214 PRE-IDEATION Quick Scan

## Problem frame

`T-214` must define the canonical Atrahasis Agent Manifest for Alternative B.
The manifest replaces A2A Agent Cards and becomes the signed capability
disclosure surface published at `/.well-known/atrahasis.json`.

It has to satisfy all of these at once:
- `C39` discovery-family message obligations for publish, query, and update,
- `C40` trust rules for signed manifests, profile advertisement, endpoint keys,
  and registry conflict failure,
- `C38` separation of concerns so manifest structure does not silently absorb
  session, transport, or payload semantics,
- `T-212` semantic object growth for `TL{}`, `PMT{}`, and `SES{}`,
- compatibility with the rest of the Atrahasis stack, especially `C36` external
  interface posture and later registry / bridge tasks.

## Known solution families

### 1. Agent cards and plugin manifests

Typical mechanisms:
- A2A Agent Cards
- AI plugin manifests
- `.well-known` capability documents

Strengths:
- Clear discovery entry point
- Easy for clients and registries to fetch
- Familiar pattern for endpoint advertisement

Gaps relative to Atrahasis:
- Usually describe endpoints and coarse capabilities, not semantic object
  surfaces, ontology snapshots, or verification posture
- Weak distinction between native, federated, and bridge-limited trust states
- Often underspecify signing, supersession, and capability lineage

### 2. API and event catalog specifications

Typical mechanisms:
- OpenAPI
- AsyncAPI
- gRPC service descriptors

Strengths:
- Good at enumerating operations, schemas, and transport bindings
- Mature tool generation ecosystem

Gaps relative to Atrahasis:
- Center on interface methods, not semantic-capability identity
- Poor fit for multi-binding capability disclosure across `AASL-T`,
  `AASL-J`, and `AASL-B`
- Usually separate security, ontology, and trust posture into external docs

### 3. Signed package and artifact manifests

Typical mechanisms:
- OCI image manifests
- SBOMs
- signed release attestations

Strengths:
- Strong experience with hash-linked metadata, signatures, and supersession
- Good model for immutable snapshots plus update chains

Gaps relative to Atrahasis:
- Typically describe shipped artifacts, not live agent capabilities
- Do not model runtime endpoint exposure, message classes, or auth negotiation
- Trust chains alone do not express semantic support or protocol behavior

### 4. Identity and workload metadata documents

Typical mechanisms:
- OIDC discovery metadata
- JWKS endpoints
- SPIFFE / workload identity descriptors

Strengths:
- Strong fit for auth-scheme advertisement and key distribution
- Good basis for issuer and trust-anchor disclosure

Gaps relative to Atrahasis:
- Identity metadata is narrower than full capability disclosure
- Does not capture supported message classes, tools, prompts, resources, or
  ontology versions
- Risks reducing the manifest to a security sidecar instead of a true
  capability contract

### 5. Marketplace and service registry records

Typical mechanisms:
- service catalog entries
- marketplace app listings
- internal service registry metadata

Strengths:
- Useful for discovery, categorization, and search
- Good at human-readable summaries and coarse policy hints

Gaps relative to Atrahasis:
- Registry entries often flatten or duplicate source-of-truth capability data
- Weak provenance around what is self-asserted versus registry-verified
- Usually blur static identity, live status, and commercial metadata into one
  mutable document

## Atrahasis-specific gap summary

No standard manifest family alone gives Atrahasis all of the following:
- signed endpoint-scoped disclosure chained to native or accepted issuer trust,
- explicit advertisement of `C40` security profiles and auth schemes,
- semantic capability disclosure tied to `C39` message families and `T-212`
  types,
- native-versus-bridge posture as a first-class machine-readable distinction,
- stable separation between static capability truth and dynamic operational
  status,
- update and supersession rules that preserve provenance rather than overwrite
  history,
- enough structure for later registry, bridge, SDK, and conformance tasks.

## Design axes for ideation

The concept space is defined by five tensions:
1. lightweight discovery card versus full semantic contract,
2. self-hosted endpoint truth versus registry-mediated trust,
3. inline capability disclosure versus reference-heavy modular manifests,
4. static capability advertisement versus live operational state,
5. human-readable simplicity versus machine-verifiable completeness.
