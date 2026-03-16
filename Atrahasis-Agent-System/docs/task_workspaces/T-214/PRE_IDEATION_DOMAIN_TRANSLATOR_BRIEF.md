# T-214 Domain Translator Brief

## 1. USB Device Descriptor + Capability Enumeration

Source domain:
- USB device discovery and driver negotiation

Structural parallel:
- A device publishes a compact machine-readable identity and capability surface
  before higher-level interaction begins.

Design insight:
- The manifest should declare enough canonical capability structure that a
  client can decide whether and how to interact before invoking deeper flows.
- For `T-214`, that favors explicit sections for transport bindings, encodings,
  security profiles, and semantic capability families rather than a prose-only
  card.

Where the analogy breaks:
- USB descriptors are relatively static and low-semantic. Atrahasis needs
  trust-chain disclosure, bridge posture, ontology alignment, and update
  lineage.

## 2. Aircraft Type Certificate + Filed Flight Plan

Source domain:
- aviation certification and operations

Structural parallel:
- One layer certifies what the craft is allowed to be, while another declares
  how this specific flight will operate.

Design insight:
- Separate enduring capability truth from live operational state.
- For `T-214`, the manifest should capture durable agent capability and trust
  posture, while session state, health, quotas, and transient workload data stay
  elsewhere.

Where the analogy breaks:
- Aviation certification is slower and more centralized than a protocol
  ecosystem. Atrahasis must support faster update and supersession cycles.

## 3. Nutrition Label + Allergen Warning

Source domain:
- packaged food labeling

Structural parallel:
- The label is useful because it shows both what is present and what risks or
  limits attach to consumption.

Design insight:
- Capability disclosure should include bounded caveats, not just optimistic
  marketing.
- For `T-214`, this supports machine-readable declaration of auth schemes,
  required security profiles, native-versus-bridge posture, and important
  capability limits.

Where the analogy breaks:
- Food labels do not have cryptographic trust chains or lineage semantics.

## 4. Certificate of Origin + Bill of Lading

Source domain:
- international trade documentation

Structural parallel:
- One document says where something comes from; another tracks how it is being
  moved and by whom.

Design insight:
- Native identity, issuer trust, and bridge provenance should be explicit and
  separable.
- For `T-214`, a manifest should distinguish native agent truth from translated
  or bridged capability disclosure instead of flattening them into one trust
  level.

Where the analogy breaks:
- Trade documents are still largely document-centric and do not represent live
  protocol capability negotiation.

## 5. Museum Placard + Provenance Label

Source domain:
- exhibit curation

Structural parallel:
- A good placard tells a viewer what the object is, while provenance tells the
  viewer why to trust the object and how it got here.

Design insight:
- Human-readable summary and machine-verifiable provenance are both needed, but
  they should not be confused.
- For `T-214`, the manifest should support human-facing summaries while keeping
  authoritative trust, key-chain, and compatibility facts in structured fields.

Where the analogy breaks:
- Museums tolerate interpretive ambiguity; protocol discovery should not.

## Net synthesis

The cross-domain pattern is consistent:
- discovery works best when the first document is compact but structured,
- durable capability truth should not be mixed with live operational telemetry,
- trust and provenance need their own explicit disclosure surface,
- and translated/bridge posture must stay visible instead of being normalized
  into native identity.

That pattern favors a manifest design with:
- explicit layered sections,
- signed trust posture and issuer chain,
- clear separation between capability truth and runtime status,
- machine-readable bridge/native distinction,
- and enough semantic detail to drive later registry, bridge, and tooling work.
