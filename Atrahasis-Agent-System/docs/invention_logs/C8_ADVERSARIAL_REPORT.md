# C8 — Deterministic Settlement Fabric (DSF): Adversarial Analysis

## TASK 1: ADVERSARIAL ANALYSIS

---

### Attack 1: CRDT Convergence Exploitation ("Phantom Balance Attack")

**Severity: FATAL**

**Attack Vector:** An adversary operating multiple nodes intentionally partitions itself from a subset of the network, executes AIC transfers on both sides of the partition, then reconnects. Because CRDTs guarantee eventual convergence via mathematical merge semantics (LUB on the semilattice), the merged state must accept all operations from both sides. The attacker effectively spends the same AIC balance twice — once on each side of the partition — and convergence produces a state where both spends are honored, violating conservation.

**Mechanism:** CRDTs — specifically G-Counters and PN-Counters — are designed so that all concurrent operations commute. A "transfer" operation that decrements one account and increments another cannot be made atomic across two CRDT replicas without coordination. The attacker exploits the gap between "local validity" (balance ≥ transfer at time of local check) and "global validity" (total conservation). During the partition window, both local checks pass. After merge, the source account may go negative or the system over-issues AIC.

**Impact:** Complete destruction of AIC conservation invariant. Economic collapse of the settlement layer. Every downstream system (C3, C5, C6, C7) that depends on AIC balances becomes unreliable. The CSO conservation law (Σ alloc + Σ pending_out - Σ pending_in + spent = total_supply) is violated at the root.

**Proposed Mitigation:** NONE as pure CRDT — this is a fundamental design flaw. CRDTs cannot enforce global invariants (like "no account goes negative") without coordination. The design MUST be amended to introduce a coordination layer for transfer operations. Options: (a) escrow-lock pattern where transfers go through a coordinated commit, (b) sharded ownership where each AIC unit has a single authoritative replica, (c) hybrid architecture where CRDTs handle read-path replication but a lightweight consensus handles write-path transfers.

---

### Attack 2: Capability Score Manipulation ("Reputation Laundering")

**Severity: CRITICAL**

**Attack Vector:** An adversary creates a cluster of Sybil agent identities. These agents perform small, cheap, easy-to-verify tasks amongst themselves, building up high capability_scores (reputation, verification_track_record, claim_class_accuracy). Once capability scores are high, the effective stake (AIC_collateral × capability_score) is amplified. The adversary then uses the inflated effective stake to dominate settlement validation or governance votes.

**Mechanism:** The capability_score function f(reputation, verification_track_record, claim_class_accuracy) creates a multiplicative amplifier on stake. If an attacker can cheaply farm any of the three inputs, they get leverage beyond their actual AIC commitment. Reputation is especially vulnerable because it depends on peer assessment — a Sybil cluster can mutually affirm each other. Claim_class_accuracy can be gamed by only attempting trivially correct verifications.

**Impact:** Subversion of settlement governance. An attacker with 100 AIC and a capability_score of 10.0 (farmed) has effective stake equivalent to a legitimate participant with 1,000 AIC and capability_score of 1.0. This breaks the economic security model: the cost of attack is decoupled from the value at risk.

**Proposed Mitigation:** (a) Cap the capability_score multiplier (e.g., max 3x) so AIC collateral remains the dominant factor. (b) Require capability scores to be earned against tasks with real economic value, not self-referential micro-tasks. (c) Introduce a minimum diversity requirement — capability scores only count if earned across multiple independent task sponsors. (d) Implement diminishing returns: capability_score = 1 + log(raw_score), preventing runaway amplification.

---

### Attack 3: Epoch Boundary Race Condition ("Settlement Sandwiching")

**Severity: CRITICAL**

**Attack Vector:** The multi-rate settlement system (B-class per-epoch, V-class N-epoch, G-class governance) creates discrete boundaries where state transitions occur. An attacker submits carefully timed transactions just before an epoch boundary to manipulate which settlement window processes them, then submits corrective or exploitative transactions immediately after the boundary.

**Mechanism:** At each epoch boundary, B-class settlement computes rewards based on scheduling compliance and verification quality during that epoch. An attacker who controls the timing of task completion reports can shift work recognition between epochs, concentrating apparent compliance in epochs where their competitors performed poorly (claiming disproportionate share of the reward pool) and deferring reports of poor performance to epochs where dilution is highest. In multi-rate settlement, V-class settlements that span N epochs can be gamed by strategically timing when verification challenges are filed.

**Impact:** Systematic extraction of above-fair-share rewards. Over many epochs, the attacker accumulates excess AIC at the expense of honest participants. If the reward pool is zero-sum within an epoch (percentage-based four-stream allocation), this directly reduces honest participant compensation, potentially driving them from the network.

**Proposed Mitigation:** (a) Randomize epoch boundaries within a window (±δ jitter) so exact timing is unpredictable. (b) Use overlapping evaluation windows rather than hard boundaries — each task's contribution is assessed over a sliding window centered on its completion, not the epoch it falls into. (c) Commit-reveal for completion reports: hash committed before epoch boundary, content revealed after. (d) Cross-epoch smoothing: no single epoch can deviate more than k% from the trailing average in per-participant reward allocation.

---

### Attack 4: Protocol Credit Farming ("PC Decay Arbitrage")

**Severity: HIGH**

**Attack Vector:** Protocol Credits have a 10%/epoch decay and are non-transferable. An adversary exploits the decay mechanism by timing high-volume spam-like activity to moments just after PC refresh, consuming network resources before decay takes effect, then going idle during the decay period. If PC refresh is tied to any renewable mechanism (participation, staking), the attacker maximizes resource consumption per unit of PC earned.

**Mechanism:** The 10%/epoch decay means PCs are a wasting asset. Rational actors will spend PCs as fast as possible. If the system grants PCs for participation (to prevent decay from depleting active participants), this creates a cycle: participate → earn PCs → spend PCs on resource-consuming activity → participate more to earn more PCs. The attacker's "participation" can be minimal-cost activity designed purely to trigger PC refresh. The non-transferability constraint is irrelevant because the attacker doesn't need to sell PCs — they consume them directly.

**Impact:** Network resource exhaustion. The spam-control mechanism (PCs) becomes a subsidy for spam if the PC-earning mechanism is gameable. At scale, this is a sustained denial-of-service that looks legitimate at the individual transaction level.

**Proposed Mitigation:** (a) PC earning rate must be sublinear — diminishing returns on participation within an epoch. (b) PC spending must be priced dynamically based on current network load (congestion pricing). (c) Implement a "quality gate" — PCs are only refreshed based on participation that produces measurable value (successful task completion, accepted verifications), not mere activity. (d) Hard cap on PC balance per identity to limit burst capacity.

---

### Attack 5: Capacity Market Cornering ("Thin Market Squeeze")

**Severity: HIGH**

**Attack Vector:** The capacity market clears at epoch boundaries for CSO resources. At target scale (the system's early deployment phase), the market will be thin — few participants, limited liquidity. An attacker with moderate capital buys up Capacity Slices in excess of their needs, creating artificial scarcity. Legitimate participants must either pay inflated prices, wait for the next epoch, or go without resources.

**Mechanism:** In a thin market with epoch-boundary clearing, supply is inelastic within an epoch (allocated resources cannot be reclaimed mid-epoch). The attacker bids aggressively at clearing, secures a large share of capacity, then either (a) resells at a premium via secondary market (if one exists), (b) holds capacity idle to deny it to competitors, or (c) uses the capacity monopoly to extract rents from task sponsors who have no alternative provider. The capacity market's own design (auction clearing) makes this straightforward — it's a standard cornering strategy adapted to compute resources.

**Impact:** Market failure at the infrastructure layer. Honest providers are unable to offer services. Task sponsors face inflated costs or unavailability. The settlement layer's purpose — efficient resource allocation — is subverted. This is especially dangerous during bootstrap when the number of capacity providers is small.

**Proposed Mitigation:** (a) Position limits — no single entity can hold more than X% of total Capacity Slices in a given epoch. (b) Use-it-or-lose-it: capacity not utilized within Y% of epoch is automatically released back to the market mid-epoch. (c) Reserve pricing floor set by protocol (minimum price below which capacity cannot be sold, preventing predatory undercutting in alternating squeeze-and-dump cycles). (d) Progressive capacity release — don't clear all capacity at epoch boundary; release in tranches throughout the epoch.

---

### Attack 6: Cross-Budget Arbitrage ("Budget Isolation Breach")

**Severity: HIGH**

**Attack Vector:** The three-budget model (SB/PC/CS) assumes isolation between budget types. However, real economic behavior creates implicit exchange rates. If sponsoring a task (SB) generates PCs as a side effect, and PCs grant resource access, and resource access produces settlement rewards (AIC), then an implicit SB→PC→CS→AIC conversion pathway exists. An attacker optimizes this conversion pathway to extract value in excess of what the protocol intends.

**Mechanism:** Secondary markets (identified as a risk in the science assessment) formalize what economic pressure creates informally. Even without explicit secondary markets, "PC-as-a-service" arrangements emerge: Entity A has excess PCs, Entity B needs resource access. A performs actions on B's behalf (using A's PCs), B compensates A via off-chain payment or SB transfer. The protocol's non-transferability constraint on PCs is circumvented not by transferring PCs but by transferring the *service* that PCs enable. Budget isolation exists in the protocol but not in the economy.

**Impact:** Erosion of the three-budget model's intended properties. PCs no longer function as spam control if they can be effectively purchased. CS allocation no longer reflects genuine capacity needs if slices are acquired for arbitrage rather than use. The entire economic design degrades toward a single-token model with extra complexity but no additional guarantees.

**Proposed Mitigation:** (a) Accept that perfect budget isolation is impossible and design for "sufficient friction" rather than hard separation. (b) Make PC-earning actions identity-bound and non-delegatable (cryptographic attestation that the earner performed the work). (c) Tax implicit conversions: if an entity's SB expenditure correlates suspiciously with their PC accumulation, apply a friction fee. (d) Monitor cross-budget flow metrics and trigger governance alerts when implicit exchange rates stabilize (indicating market formation). (e) Re-examine whether three budgets are necessary — if isolation cannot be maintained, a simpler two-budget model (transferable + non-transferable) may be more honest.

---

### Attack 7: Slashing Ordering Attack ("Punishment Race")

**Severity: CRITICAL**

**Attack Vector:** The graduated slashing mechanism requires determining the order of violations to apply escalating penalties. In a CRDT-based system without consensus on ordering, two replicas may observe the same set of violations in different orders, producing different slashing amounts. An attacker exploits this by committing multiple minor violations simultaneously, then arguing (on the replica that saw them in the most favorable order) that the total penalty should be minimal.

**Mechanism:** Graduated slashing implies a state machine: first offense → warning, second → X% slash, third → 2X% slash, etc. In a CRDT system, "first" and "second" depend on causal ordering, which CRDTs do not guarantee for concurrent operations across replicas. If violations V1 and V2 are detected by different replicas at approximately the same time, Replica A may compute slash(V1, first) + slash(V2, second) while Replica B computes slash(V2, first) + slash(V1, second). If violation severity differs, the total penalty differs. The attacker can appeal using whichever ordering produces the lower penalty.

**Impact:** Slashing becomes non-deterministic, undermining the entire accountability framework. If participants cannot be reliably penalized, the incentive structure collapses. Honest participants who accept deterministic penalties are disadvantaged relative to adversaries who exploit ordering ambiguity.

**Proposed Mitigation:** (a) Slashing MUST be processed through a coordination layer, not CRDTs. This is a second confirmation that pure-CRDT settlement is architecturally unsound for operations requiring ordering. (b) Use epoch-scoped slashing: all violations within an epoch are collected, ordered deterministically (e.g., by hash), and processed as a batch at epoch boundary. (c) Make slashing penalties order-independent: each violation carries a fixed penalty regardless of history, eliminating the ordering dependency (but sacrificing graduated deterrence).

---

### Attack 8: Intent Budget Exhaustion ("RIF Draining")

**Severity: MEDIUM**

**Attack Vector:** In intent-budgeted settlement, RIF intent resource_bounds serve as the budget ceiling. An attacker submits intents with artificially tight resource_bounds, causing legitimate work to be done but settlement rewards to be capped at the low budget. Workers who accepted the task (based on the intent) receive minimal compensation for full effort.

**Mechanism:** The settlement system "computes rewards based on completion quality" against the intent's resource_bounds. If an attacker sets resource_bounds low but the task description is ambiguous enough to require full effort, workers bear the cost. This is a classic "underbidding" attack adapted to the intent framework. The attacker benefits if they are also a task sponsor who wants cheap labor, or if they want to degrade network quality by making honest work unprofitable.

**Impact:** Worker exploitation and network quality degradation. Rational workers learn to avoid tasks with low resource_bounds, but distinguishing legitimate low-budget tasks from exploitative ones requires information the worker may not have at acceptance time. Over time, the market for task execution becomes adversely selected.

**Proposed Mitigation:** (a) Minimum resource_bounds floor based on task class and historical completion costs. (b) Workers can reject tasks after partial inspection without penalty. (c) Reputation penalty for sponsors whose tasks consistently under-budget relative to actual completion effort. (d) Escrow mechanism: resource_bounds are locked at intent submission, and if actual effort exceeds bounds by >Y%, the sponsor's reputation score is adjusted downward.

---

### Attack 9: Conservation Law Bypass via Pending State ("Limbo Attack")

**Severity: HIGH**

**Attack Vector:** The CSO conservation law is: Σ alloc + Σ pending_out - Σ pending_in + spent = total_supply. The "pending" states create a limbo where resources are neither allocated nor spent. An attacker deliberately creates a large volume of pending transactions (pending_out or pending_in) and then prevents them from resolving, effectively locking resources in limbo indefinitely.

**Mechanism:** The attacker initiates many CSO transfers or allocations, moving resources into pending_out. They then stall the completion (by becoming unresponsive, filing disputes, or exploiting timeout mechanisms). The conservation law is technically satisfied — the pending amounts are accounted for — but the resources are unusable. This is economic griefing: the attacker doesn't steal resources but denies them to others.

**Impact:** Resource lockup. Capacity that should be available for productive use is trapped in pending state. At sufficient scale, this is equivalent to a denial-of-service on the capacity market. The conservation law, while formally correct, fails to guarantee resource *availability*.

**Proposed Mitigation:** (a) Mandatory timeout on all pending states — pending_out that doesn't resolve within T epochs is automatically reverted. (b) Cap on total pending volume per entity (no single actor can lock more than Z% of total supply in pending). (c) Require collateral for initiating pending states — the collateral is slashed if the pending state times out (making the attack costly). (d) Add a "usable supply" metric alongside total supply: usable = total_supply - Σ pending, and alert when usable drops below threshold.

---

### Attack 10: Multi-Rate Settlement Arbitrage ("Speed Class Gaming")

**Severity: MEDIUM**

**Attack Vector:** The three settlement speeds (B-class fast, V-class standard, G-class slow) create arbitrage opportunities. An attacker manipulates which speed class their transactions settle in to gain timing advantages. For example, they might structure a verification challenge (V-class, N-epoch) to delay an opponent's reward while their own scheduling compliance (B-class, per-epoch) rewards flow immediately.

**Mechanism:** The four-stream settlement allocates rewards across scheduling compliance (40%), verification quality (40%), communication efficiency (10%), governance participation (10%). By concentrating activity in B-class streams (scheduling compliance) while filing V-class challenges against competitors' verification quality, the attacker ensures their own rewards settle quickly while competitors' rewards are locked in slower settlement. The attacker enjoys compound returns (reinvesting fast-settled rewards) while competitors' capital is tied up.

**Impact:** Unfair timing advantage. Honest participants who do both scheduling and verification work see 40% of their rewards settle fast and 40% settle slow, while the attacker optimizes for 80%+ fast settlement. Over many epochs, compound timing advantage accumulates into material economic advantage.

**Proposed Mitigation:** (a) Normalize settlement timing in reward calculations — fast-settled rewards receive a slight discount, slow-settled rewards receive a slight premium, such that the NPV is equivalent regardless of speed class. (b) Limit the rate at which any single entity can file V-class challenges (preventing weaponized delay). (c) Require V-class challengers to post a bond that is forfeited if the challenge is found to be frivolous. (d) Track the ratio of fast-to-slow settlement per participant and flag statistical outliers for review.

---

### OVERALL ADVERSARIAL VERDICT: CONDITIONAL_SURVIVAL

**Fatal flaws identified:** Attack 1 (Phantom Balance) exposes a fundamental architectural deficiency — the pure-CRDT ledger cannot enforce conservation invariants for transfer operations. Attacks 3 and 7 (Epoch Boundary Race, Slashing Ordering) further confirm that operations requiring ordering or atomicity are incompatible with coordination-free CRDTs.

**Conditions for survival:**

1. **MANDATORY: Replace pure-CRDT ledger with hybrid architecture.** CRDTs may handle read-path replication and non-contentious state propagation, but all transfer operations, slashing computations, and conservation-critical state transitions MUST pass through a lightweight coordination layer (e.g., sharded consensus, optimistic execution with fraud proofs, or epoch-boundary batch processing with deterministic ordering).

2. **MANDATORY: Cap capability_score multiplier** to prevent reputation laundering from undermining economic security. Maximum multiplier of 3x with logarithmic scaling.

3. **MANDATORY: Implement position limits and use-it-or-lose-it rules** in the capacity market to prevent cornering during thin-market bootstrap.

4. **REQUIRED: Add timeouts and collateral requirements** for all pending states in the CSO conservation framework.

5. **REQUIRED: Normalize settlement timing** across speed classes to eliminate compound timing arbitrage.

6. **RECOMMENDED: Accept imperfect budget isolation** and redesign the three-budget model for "sufficient friction" rather than hard separation, or reduce to two budgets.

---

---