# T-250 Ideation Council Comparison Addendum

Purpose:
- compare `IC-2` and `IC-3` on the dimensions raised by the user before any
  concept approval decision
- determine whether the richer bridge-cell path is actually better than the
  bounded provenance bridge for this task
- keep the analysis inside `IDEATION`; no invention has been promoted

Method note:
- this is a council comparison based on architectural expectations, not
  benchmark data
- scores below reflect expected behavior if the concept were carried forward as
  currently framed

## Side-by-side comparison

| Dimension | IC-2: Snapshot-Bound Provenance Bridge | IC-3: Bridge-Resident Semantic Cell | Council read |
|---|---|---|---|
| Core shape | Explicit custody bridge with signed bridge snapshots, invocation translation, bounded enrichment, visible bridge posture | Stateful quasi-native bridge with bridge-side continuation and richer internal lifecycle | `IC-2` is narrower and cleaner; `IC-3` is broader and more ambitious |
| Universal MCP coverage expectation | Better for the generic long tail because the contract stays close to inventory/call/result translation | Worse if many MCP servers need bridge-specific state assumptions to look useful | `IC-2` is stronger for the "universal" requirement |
| Zero per-server configuration likelihood | Higher | Lower | `IC-2` better matches the task's generic bridge objective |
| Bridge honesty | Stronger because trust ceiling is central to the concept | Riskier because quasi-native behavior can blur source-versus-bridge guarantees | `IC-2` wins clearly |
| Semantic enrichment discipline | Easier to keep source-aware and bounded | Easier to over-infer confidence, evidence, or provenance from weak MCP sources | `IC-2` is safer |
| Warm-state / repeated-call performance | Good if bridge snapshots and translation policy are reusable | Potentially better for hot-path repeated calls because more bridge-side state can stay resident | `IC-3` has an advantage only if the extra state is justified and governable |
| Continuation / advanced workflow support | Limited but honest; can point downstream to later tasks | Strongest immediate support for continuation-like bridge behavior | `IC-3` is richer, but also pushes harder into downstream scope |
| Scope fit to T-250 | Strong | Weak | `IC-3` overlaps `T-260`, `T-262`, and `C23` too early |
| Downstream fit to C40/C41/C42 | Strong because bridge-limited trust and native-vs-bridge posture stay explicit | Risky because it can look like a shadow native tool host | `IC-2` aligns better with current canon |
| Certification and interoperability burden | Moderate | High | `IC-3` would be much harder to certify generically |
| Failure surface | Snapshot staleness, enrichment bounds, translation gaps | All of IC-2 plus continuation drift, orphaned bridge state, quasi-native trust confusion | `IC-2` is materially safer |
| Long-term expressive power | Good foundation | Highest | `IC-3` wins only if the task is allowed to intentionally shape future framework/runtime architecture |

## Council summary

### What IC-3 gets right

`IC-3` correctly sees that a universal bridge cannot be purely stateless. To be
useful at scale, it likely needs:
- bridge-side inventory caching,
- durable translation policy,
- and some bounded warm-state handling for repeated calls.

That is the strongest argument in favor of `IC-3`.

### Why IC-3 alone is still not the best choice

As a full concept, `IC-3` does too much:
- it risks duplicating future native server-framework behavior,
- it risks implying stronger trust than a bridge should claim,
- it raises the odds of per-server adaptation logic,
- and it pushes `T-250` into `T-260` / `C23` territory before those surfaces are
  designed.

For this task, that is architectural overreach, not strength.

### Council judgment

`IC-3` alone is **not** the best concept for `T-250`.

The council's view is:
- keep `IC-2` as the governing base,
- absorb only the necessary bridge-side state advantages from `IC-3`,
- and reject the quasi-native bridge-cell posture as the default bridge
  architecture.

That means a hybrid is better than pure `IC-3`.

## Quick scorecard

| Category | IC-2 | IC-3 |
|---|---:|---:|
| Universal bridge viability | 5/5 | 2/5 |
| Bridge honesty / trust clarity | 5/5 | 2/5 |
| Zero-config migration fit | 4/5 | 2/5 |
| Bounded semantic enrichment | 5/5 | 2/5 |
| Warm-state future headroom | 3/5 | 5/5 |
| Complex workflow richness | 3/5 | 5/5 |
| Scope discipline | 5/5 | 1/5 |
| Fit to current Alternative B canon | 5/5 | 2/5 |

Interpretation:
- `IC-2` is the stronger base architecture
- `IC-3` contributes useful statefulness ideas
- the best answer is a constrained hybrid, not `IC-3` alone
