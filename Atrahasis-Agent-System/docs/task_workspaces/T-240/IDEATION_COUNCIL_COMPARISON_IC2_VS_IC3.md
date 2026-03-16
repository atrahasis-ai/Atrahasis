# T-240 Ideation Council Comparison Addendum

Purpose:
- compare `IC-2` and `IC-3` on the dimensions the user requested before any
  concept approval decision
- keep the analysis inside `IDEATION`; no invention has been promoted

Method note:
- this is a council comparison based on architectural expectations, not measured
  benchmark data
- scores below reflect expected behavior if the concept were taken through
  design as currently framed

## Side-by-side comparison

| Dimension | IC-2: Capability-Bound Semantic Tool Exchange | IC-3: Negotiated Tool Session Mesh | Council read |
|---|---|---|---|
| Core shape | Bounded four-part lifecycle: discovery, invocation, result, change notification | Rich negotiated sub-session for each tool interaction | `IC-2` is narrower and cleaner; `IC-3` is broader and more ambitious |
| Runtime latency expectation | Lower for simple and medium-complexity tool calls; fewer protocol turns before execution | Higher on average because negotiation, continuation, or step-up flows add turns | `IC-2` wins on baseline responsiveness |
| Wire efficiency | Better for straightforward calls because fewer control messages are needed | Worse for common-case calls if session setup and continuation metadata become routine | `IC-2` is more efficient unless the tool truly needs multi-step negotiation |
| Server resource efficiency | Easier to keep mostly stateless or lightly stateful between request and result | More server-side state tracking for reservations, continuations, partial completion, and sub-session lifecycle | `IC-2` has lower memory and coordination overhead |
| Simple-tool fit | Excellent for search, retrieval, conversion, validation, and bounded action tools | Overbuilt for simple tools | `IC-2` fits the direct MCP-replacement target better |
| Long-running / interactive tool fit | Adequate if paired later with `T-243` streaming or push surfaces | Strongest option for highly interactive or continuation-heavy tools | `IC-3` wins only for the complex tail of the tool spectrum |
| Authorization efficiency | Clear `C40` grant checks at invocation time; bounded policy surface | More opportunities for step-up auth, but more repeated checks and context tracking | `IC-2` is simpler; `IC-3` is richer but costlier |
| Canonicalization burden | Predictable: canonicalize inputs/results around one invocation/result contract | Higher: canonicalization may need to span session state, partial inputs, and continuations | `IC-2` is easier to validate and reason about |
| Result accountability | Strong and deterministic: every result becomes `CLM + CNF + EVD + PRV` | Potentially richer, but also more complex because partial or staged results need additional rules | `IC-2` has the cleaner accountability story |
| SDK ergonomics | Easier client/server SDK surface; easier builders, validators, and auto-wrapping | Harder SDK because clients must understand sub-sessions, continuations, and richer control states | `IC-2` is materially easier for `T-262` |
| Server framework ergonomics | Strong fit for `T-260` decorator model and "plain function + wrapper" experience | Pushes `T-260` toward workflow engine behavior, not just tool exposure | `IC-2` aligns better with minimal-boilerplate server goals |
| Bridge friendliness | Easier bridge from `MCP` because lifecycle is closer to list/call/result/update translation | Harder bridge because most MCP servers do not expose rich negotiated session behavior natively | `IC-2` is much better for `T-250` |
| Interoperability with existing canon | Stays within current `C39`, `C40`, `C41`, and `T-212` boundaries | Risks spilling into `T-243`, `T-260`, and `C23` territory early | `IC-2` is the safer scope fit |
| Operational complexity | Moderate | High | `IC-3` has materially higher implementation and operator burden |
| Failure surface | Smaller and easier to debug because lifecycle states are fewer | Larger: continuation drift, orphaned sub-sessions, partial-state mismatch, reservation expiry | `IC-2` is safer for early standardization |
| Extensibility | Good: leaves room for later streaming, push, and advanced session behavior | Very high, but at the cost of committing early to a broad control model | `IC-3` has more future headroom, but too early for core replacement |
| Time-to-standardize | Faster | Slower | `IC-2` is more likely to reach a stable spec quickly |
| Benefit profile | Best balance of sovereignty, clarity, and deployability | Best for advanced future workflows and complex interactive tools | `IC-2` is the stronger near-term platform foundation |

## Council summary

### Performance and efficiency

`IC-2` is expected to outperform `IC-3` for the common case because it uses a
bounded lifecycle and fewer protocol turns. That means lower average latency,
lower wire overhead, less server-side state retention, and simpler timeout or
retry handling. `IC-3` only becomes performance-competitive when the tool
interaction genuinely needs multi-step negotiation or long-lived conversational
execution.

### Benefits

`IC-2` delivers the best immediate platform benefit:
- strongest fit to the direct `MCP` replacement goal
- clearer input validation and result accountability rules
- easier SDK and server-framework adoption
- better compatibility with bridge work and downstream spec tasks

`IC-3` delivers a different kind of benefit:
- richer support for interactive, long-running, step-up-authorized tool work
- more expressive future model for complex agents and operational workflows

### Council judgment

If the goal is:
- `clean sovereign replacement for MCP-style tool connectivity now`, `IC-2` is stronger
- `maximum future expressiveness even at significant complexity cost`, `IC-3` is stronger

The council still recommends `IC-2` because it captures the core sovereign tool
protocol without prematurely absorbing streaming, continuation, and runtime
orchestration responsibilities that belong to later tasks.

## Quick scorecard

| Category | IC-2 | IC-3 |
|---|---:|---:|
| Expected common-case performance | 4/5 | 2/5 |
| Efficiency / overhead control | 4/5 | 2/5 |
| Simplicity of implementation | 4/5 | 2/5 |
| Benefit for simple-to-medium tools | 5/5 | 2/5 |
| Benefit for complex interactive tools | 3/5 | 5/5 |
| Bridge compatibility | 5/5 | 2/5 |
| Fit to current task scope | 5/5 | 2/5 |
| Long-term expressive power | 4/5 | 5/5 |

Interpretation:
- `IC-2` is the best foundation concept
- `IC-3` is the best stretch concept
- the main trade is efficiency and scope discipline versus maximum workflow richness
