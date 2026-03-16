# T-250 Domain Translator Brief

Domain:
- protocol bridge architecture
- semantic enrichment across a migration boundary
- native-versus-bridge trust disclosure for tool connectivity

Problem statement:
- How should `AACP v2` wrap an existing `MCP` server so that Atrahasis agents
  can discover and invoke tools through canonical `AACP` surfaces, receive
  semantically enriched outputs, and still know exactly which guarantees are
  native versus bridge-generated?

## Analogy 1: Bonded warehouse relabeling in customs logistics

Source domain:
- import/export bonded warehouse handling and customs relabeling

Structural parallel:
- goods arrive under one authority regime,
- the warehouse re-labels and stages them for a new destination system,
- chain-of-custody must remain visible,
- bonded status limits what the warehouse may claim about the goods,
- repackaging does not erase origin.

Where the analogy breaks:
- protocol translation is faster and reversible in ways physical logistics is
  not.
- software metadata can be generated dynamically rather than physically stamped.

Design insight:
- the bridge should act like a bonded transfer surface: it can repackage and
  annotate, but it must preserve source identity and trust limits explicitly.

## Analogy 2: Electrical transformer with protective derating

Source domain:
- power transformers and substations

Structural parallel:
- one side of the boundary speaks a different voltage and current profile,
- the transformer makes the systems interoperable,
- protective equipment limits what can safely pass across the boundary,
- downstream consumers need to know rated versus derated capacity.

Where the analogy breaks:
- semantic contracts are more complex than voltage conversion.
- tool metadata can be structurally transformed, not just scaled.

Design insight:
- the bridge should not be a transparent wire. It should expose a rated,
  policy-visible conversion boundary with explicit degraded or limited modes.

## Analogy 3: Court interpreter plus certified transcript

Source domain:
- legal interpreting and certified transcript production

Structural parallel:
- spoken content is translated into another language for a new audience,
- the interpreter preserves who said what,
- ambiguity or uncertainty must remain attributable,
- the certified transcript is a mediated artifact, not the original utterance.

Where the analogy breaks:
- human interpretation is less deterministic than protocol mapping.
- legal testimony has social context that tool invocation does not.

Design insight:
- semantic enrichment should look more like certified translation than native
  authorship: preserve source identity, preserve ambiguity boundaries, and mark
  what the bridge contributed.

## Analogy 4: Museum conservation label on restored artifacts

Source domain:
- museum restoration and conservation practice

Structural parallel:
- a damaged artifact is stabilized and made legible for display,
- restoration adds structure that helps later viewers,
- professional practice requires clear disclosure of what is original versus
  what is restored or inferred.

Where the analogy breaks:
- software tool results are often live and reproducible rather than historical
  one-off objects.
- bridge translation can be automated in ways restoration is not.

Design insight:
- the bridge should enrich results enough for use inside Atrahasis while
  keeping a sharp boundary between source-produced facts and bridge-added
  semantic scaffolding.

## Cross-domain synthesis

Shared structural lessons:
1. Conversion boundaries need explicit trust ceilings, not hidden convenience.
2. Repackaged outputs stay useful only if origin and mediation remain visible.
3. Stable inventory labels matter as much as per-call translation.
4. The adapter should preserve admissibility for downstream consumers without
   overstating what the source system guaranteed.

Translation guidance for the Ideation Council:
- prefer concepts that treat the bridge as a visible custody boundary rather
  than a perfect emulator,
- keep snapshot identity, call translation, and result enrichment separate but
  linked,
- avoid concepts that collapse bridge-generated semantics into native
  equivalence,
- preserve a path for bounded degraded continuations without promising full
  native priming.
