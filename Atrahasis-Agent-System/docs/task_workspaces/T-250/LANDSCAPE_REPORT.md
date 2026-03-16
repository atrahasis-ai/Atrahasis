# T-250 Landscape Report

## Current repo landscape

Alternative B already has the upstream authorities that `C43` must consume:
- `C39` for message-family and `provenance_mode` rules,
- `C40` for bridge-limited trust and anti-spoofing admission,
- `C41` for manifest disclosure of bridge posture,
- `C42` for the native tool target that bridged tools must not impersonate,
- `T-301` for retrofit order and repo-wide old-stack dependency mapping.

`T-250` is the missing invention that converts those rules into a canonical MCP
migration bridge.

## External and ecosystem landscape

### MCP ecosystem
- strongest current real-world baseline for agent-to-tool interoperability
- large installed tool surface makes bridge coverage strategically important
- source systems vary in metadata richness and operational behavior, which makes
  generic bridge honesty harder than simple method translation

### Generic gateway / adapter landscape
- many translation layers optimize for convenience and breadth
- few make trust ceilings or semantic provenance first-class
- most compatibility layers assume the translated endpoint can be treated as if
  it were native after mapping

### Semantic accountability gap
- Alternative B's strategic argument depends on preserving explicit semantic
  accountability and native-versus-bridge distinction
- that means the bridge is not just an ecosystem convenience layer; it is a
  trust boundary that later tasks (`T-281`, `T-307`, `T-303`) will rely on

## Immediate downstream consumers

### Wave 5
- `T-251` defines the sister bridge on the A2A side; `C43` should stay bridge
  honest in a way that can later align with that work
- `T-260` must expose native server behavior distinct from bridge behavior

### Wave 6
- `T-262` must shape SDK surfaces around bridge discovery, translated tool
  identity, and bridge posture visibility
- `T-281` needs certification and conformance targets for the bridge
- `T-290` will need cross-layer native-versus-bridge semantics for verification,
  runtime, and memory consumers

### Wave 7 and later
- `T-307` depends on `C43` to define cutover, coexistence, and bridge
  retirement policy credibly

## Existing Atrahasis stack obligations

### C39 LCML
- `C43` must consume the existing tool classes instead of inventing a second
  bridge-specific message family

### C40 DAAF
- `C43` must remain under `SP-BRIDGE-LIMITED` or other explicitly bounded
  bridge posture; it cannot silently satisfy native-only trust policy

### C41 LSCM
- bridge manifests must publish bridge origin, bridge posture, and bounded
  capability disclosure without pretending to be native manifests

### C42 LPEM
- `C43` must translate toward the native target without claiming native snapshot
  authority or native execution priming when the source system cannot justify it

## Landscape risks

1. If the bridge hides non-native posture, it undermines the Alternative B
   integrity argument.
2. If the bridge requires bespoke per-server configuration, the migration story
   becomes operationally weak.
3. If the bridge invents high-confidence semantics from thin source metadata,
   downstream trust consumers will be misled.
4. If the bridge accumulates too much state, it starts duplicating future native
   framework/runtime work.
5. If the bridge is too weak, it will fail to support meaningful migration of
   real MCP tool inventories.

## Landscape conclusion

The design opportunity is narrow but important:
`C43` can be valuable if it becomes the canonical custody boundary that makes
the existing MCP ecosystem usable inside Atrahasis without collapsing the
distinction between:
- native `AACP` tool authority,
- bridge-generated structure,
- and source-observed MCP behavior.
