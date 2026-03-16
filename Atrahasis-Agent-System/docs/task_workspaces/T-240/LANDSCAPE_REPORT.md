# T-240 Landscape Report

## Current repo landscape

Alternative B now has the upstream pieces that `C42` needs:
- `C38` as root communication authority,
- `C39` as message-class authority,
- `T-212` as `TL{}` semantic tool descriptor authority,
- `C40` as capability-grant and no-ambient-authority authority,
- `C41` as manifest disclosure authority,
- `C23` as lease-bound runtime execution authority.

`T-240` is the missing invention that composes those surfaces into a native tool
protocol.

## External protocol landscape

### MCP
- strongest current baseline for agent-to-tool interoperability
- good tool discovery and invocation ergonomics
- weaker on native provenance, policy continuity, and governed execution

### gRPC / HTTP/2
- strongest current baseline for high-throughput, multiplexed, long-lived RPC
- good fit for warm channels, deadlines, flow control, and streaming
- not a semantic tool protocol

### LSP
- strongest mainstream example of long-lived protocol collaboration with
  server-driven progress and partial results
- useful pattern for continuation and progressive work reporting
- not built for trust-bound execution governance

### SPIFFE
- strongest workload-identity prior art in dynamic systems
- useful for short-lived trust material and automatic rotation
- not a tool protocol

## Immediate downstream consumers

### Wave 4
- `T-243` may need to absorb stream and continuation carriage that `C42`
  intentionally foregrounds.
- `T-231` will need to analyze richer attack surfaces once `C42` is specified.

### Wave 5
- `T-250` must translate MCP tools into whatever continuation/execution posture
  `C42` standardizes.
- `T-260` must expose the native server/runtime framework needed to publish and
  operate `C42`-style tools.

### Wave 6
- `T-262` must shape SDKs around invocation, continuation, and channel/context
  management.
- `T-290` must integrate the resulting tool fabric into `C23`, `C36`, `C5`,
  and the rest of the stack.

### Proposed future module
- the queued `Atrahasis First-Party Tool Suite` proposal should consume `C42` if
  this invention becomes the canonical tool-authority surface.

## Existing Atrahasis stack obligations

### C39 LCML
- `C42` must consume its tool message classes, not replace them.

### C40 DAAF
- `C42` must preserve explicit capability grants and no ambient authority.

### C41 LSCM
- manifests may advertise tool support and posture, but must not absorb the full
  continuation/execution tool fabric.

### C23 SCR
- runtime isolation, execution leases, and broker enforcement remain with `C23`,
  even if `C42` primes the handoff more aggressively than earlier concepts did.

## Landscape risks

1. If `C42` becomes "transport cleverness without semantic accountability," it
   fails the Atrahasis mission.
2. If `C42` fully absorbs runtime semantics, `C23` loses ownership and the stack
   blurs.
3. If warm channels or continuation contexts are not revocable, trust quality
   collapses.
4. If bridges cannot honestly represent degraded provenance compared with native
   `C42` execution, `T-250` becomes unsafe.
5. If the protocol is only optimal for advanced workflows, simple tool cases may
   become needlessly expensive.

## Landscape conclusion

The repo and external landscape both point to the same design opportunity:
`C42` can be valuable if it becomes the narrow but powerful seam between
semantic tool invocation and governed downstream execution.

That is where the current ecosystem is weakest:
- MCP is tool-aware but execution-light,
- gRPC is transport-strong but semantics-light,
- LSP is continuation-aware but trust-light,
- SPIFFE is identity-strong but tool-light.
