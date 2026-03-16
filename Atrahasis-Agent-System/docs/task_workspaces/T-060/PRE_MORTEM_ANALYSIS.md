# PRE-MORTEM ANALYSIS: C35 Seismographic Sentinel

**Invention:** C35 -- Seismographic Sentinel with PCM-Augmented Tier 2
**Task:** T-060
**Role:** Pre-Mortem Analyst
**Date:** 2026-03-11
**Assumption:** C35 has been deployed and has CATASTROPHICALLY FAILED.

---

## Methodology

This analysis assumes C35 was implemented per the FEASIBILITY_COUNCIL_OUTPUT specification (86 parameters, three-tier pipeline, log-linear PCM, two-phase Bayesian fusion, NMI-hardened spectral clustering) and deployed within the C22 Wave 3-5 parallel track at the $550K-$700K budget. Each scenario describes a specific catastrophic failure, traces it to a root cause in the design, and assesses whether the failure was detectable before the catastrophe.

Scenarios are ranked by composite score: Likelihood x Severity, where HIGH=3, MEDIUM=2, LOW=1, CRITICAL=4.

---

## FAILURE SCENARIO RANKING

| Rank | Scenario | Type | Likelihood | Severity | Composite |
|------|----------|------|-----------|----------|-----------|
| 1 | F-1: The Calibration Poisoning Spiral | Adversarial | HIGH | CRITICAL | 12 |
| 2 | F-2: The Integration Cascade Collapse | Integration | HIGH | CRITICAL | 12 |
| 3 | F-3: The PCM Divergence Catastrophe | Systemic | HIGH | HIGH | 9 |
| 4 | F-4: The Cross-Neighborhood Sybil Swarm | Adversarial | MEDIUM | CRITICAL | 8 |
| 5 | F-5: The Epoch Desynchronization Fault | Integration | MEDIUM | HIGH | 6 |
| 6 | F-6: The Parameter Tuning Paralysis | Economic/Resource | MEDIUM | HIGH | 6 |
| 7 | F-7: The Bayesian Transition Whiplash | Systemic | MEDIUM | HIGH | 6 |
| 8 | F-8: The Silent Tier 3 Starvation | Systemic | HIGH | MEDIUM | 6 |
| 9 | F-9: The NMI Divergence Arms Race | Adversarial | MEDIUM | MEDIUM | 4 |
| 10 | F-10: The Correlated Channel Resonance Catastrophe | Black Swan | LOW | CRITICAL | 4 |

---

## F-1: THE CALIBRATION POISONING SPIRAL

**Type:** Adversarial
**Likelihood:** HIGH
**Severity:** CRITICAL
**Composite:** 12

### Narrative

An adversary registers 200 Sybil agents during AAS platform launch (Wave 1-2), well before C35's PCM reaches calibration maturity. During the bootstrap phase (first 1000 epochs, approximately 16.7 hours), these agents behave identically to honest agents -- submitting valid claims, participating in committees, exhibiting normal behavioral profiles per C17's B(a_i, a_j) metric.

Over the next 40-200 days (the estimated PCM convergence window per MF-2), these 200 agents are observed by the system as normal participants. Their pairwise correlations with each other are ingested into the PCM log-linear model as training data. Because they are structurally co-assigned to committees through the same VRF process as honest agents, and because they deliberately maintain behavioral similarity to their honest neighbors, the PCM learns that their correlation patterns are structurally explained. The log-linear model's 64 parameters absorb the Sybil ring's correlation signature as a "permitted" pattern.

At epoch 15,000 (approximately 250 hours into calibrated operation), the adversary activates the ring. The 200 agents begin coordinating: voting in lockstep on verification claims, steering consolidation outcomes, and manipulating settlement allocations. The PCM's residuals for these agent pairs remain LOW because the model has already learned that their correlation is "expected." Tier 2's Bayesian network sees no anomalous residuals and does not fire. Tier 1's adaptive STA/LTA baseline has accommodated the gradual behavioral shift during the poisoning period. The fixed baseline was calibrated during registration, before the adversary's agents shifted behavior, so it should catch the deviation -- but the adversary, having observed system behavior over 200+ days, has reconstructed the fixed baseline thresholds (per MF-4) and stays just below them.

The ring operates undetected for 8,000+ epochs (approximately 133 hours). During this period, it manipulates 340 verification outcomes, corrupts 12 knowledge consolidation events in C6, and extracts 45,000 AIC through fraudulent settlement claims in C8. The attack is discovered only when a human auditor notices statistical anomalies in consolidation quality during a routine review.

### Root Cause

The design assumes that PCM calibration produces an accurate model of "normal" correlation. But calibration is a supervised learning problem disguised as unsupervised learning: the model cannot distinguish legitimate structural correlation from adversarial coordination that was present during the calibration window. The circularity flagged in the Ideation Council's known risks ("exclude flagged agents from calibration" requires calibration to flag agents) was never broken. The Assumption Validation Report rated this as "PLAUSIBLE BUT UNVALIDATED" and deferred resolution to DESIGN, but the fundamental circularity is architectural, not parametric.

### Impact

Catastrophic. The PCM -- C35's most novel and most critical component -- is weaponized against the system. Every agent pair that was poisoned during calibration becomes permanently invisible to Tier 2 residual analysis. The 45,000 AIC in fraudulent settlements directly damages C8 DSF's economic integrity. The 12 corrupted consolidation events inject false knowledge into C6 EMA's knowledge base, where it propagates to downstream consumers. C12 AVAP's Layer 1 (which is implemented by C35) provides no warning because C35 itself is blind. The platform's credibility -- the foundation of C14 AiBC's governance legitimacy and C16's nominating body relationships -- suffers severe damage.

### Detection

NO. This is the scenario's most dangerous property. C35's own metrics appear healthy: Tier 1 trigger rates are within normal bounds (the ring stays below both thresholds), Tier 2 residuals are low (the ring is absorbed into the model), Tier 3 never fires (no Tier 2 confirmations to trace). The system's self-monitoring reports GREEN while the attack is in progress. Only external validation (human audit, cross-referencing with C12 AVAP's non-C35-dependent mechanisms, or anomalies surfacing in C6 consolidation quality metrics) could detect the failure.

### Mitigation

1. **Adversarial holdout validation**: Reserve 10-20% of calibration data as a holdout set. After PCM convergence, test whether the model's residuals on holdout pairs match the training-set residual distribution. Poisoned calibration data would produce systematically biased residuals on unpoisoned holdout pairs. This requires the holdout set to contain at least some agent pairs NOT controlled by the adversary -- which is guaranteed as long as the adversary controls <50% of agents.

2. **Periodic PCM recalibration with forgetting**: Instead of a single calibration phase, recalibrate PCM continuously with exponential forgetting (half-life of 5-10 CONSOLIDATION_CYCLEs). This prevents the model from permanently absorbing any single calibration-phase pattern. Newly activated adversarial behavior would create residual spikes as the model's memory of the poisoned calibration decays.

3. **Cross-validation against C12 AVAP**: C12's Mechanisms 1-4 (honeypots, sealed opinions, diversity pools, whistleblower) operate independently of C35. Require C35 to cross-reference its "all clear" status against C12's independent signals. If C12 flags suspicious agents that C35 considers normal, trigger a PCM audit.

4. **Canary agents**: Deploy system-controlled agents with known behavior profiles as calibration anchors. If PCM residuals for canary-to-canary pairs diverge from expected values, the calibration is compromised.

---

## F-2: THE INTEGRATION CASCADE COLLAPSE

**Type:** Integration
**Likelihood:** HIGH
**Severity:** CRITICAL
**Composite:** 12

### Narrative

C35 reaches Functional maturity at Wave 4 and begins publishing cluster membership data to C3 (tidal scheduling), C5 (PCVM verification routing), C7 (RIF orchestration routing), C8 (DSF settlement grouping), and C17 (MCSD behavioral comparison neighborhoods). Seven specifications now depend on C35's CONSOLIDATION_CYCLE output.

At epoch 22,000, a rare edge case occurs: the spectral clustering algorithm encounters a graph topology where two large neighborhoods (each near the 2*log(V) cap) are connected by a dense bridge of cross-neighborhood edges created by a legitimate surge in committee co-assignments following a C3 tidal scheduling reconfiguration. The NMI divergence check fires (NMI = 0.63, below the 0.70 threshold). Per the hardening protocol, C35 rejects the new partition and falls back to the previous cycle's clustering.

The previous cycle's clustering is 36,000 seconds stale. During that interval, 847 new agents registered and 312 agents departed. The stale partition references 312 agents that no longer exist and lacks assignments for 847 agents that do exist. C35's fallback protocol assigns new agents as singletons -- isolating them from Tier 2 neighborhood analysis.

C3 receives the stale cluster membership data. Its tidal scheduling algorithm, which routes committee assignments partially based on cluster topology, generates assignments that reference the 312 departed agents. C3's error handling rejects these assignments and requests fresh data from C35. C35 cannot provide fresh data because the new clustering was rejected. C3 enters a degraded scheduling mode, which produces abnormal committee compositions.

C5 PCVM receives the same stale data. Verification routing decisions based on stale clusters send verification tasks to neighborhoods that no longer reflect the actual agent topology. Verification latencies spike. C35's own Tier 1 STA/LTA detectors observe the latency spike and begin firing provisional triggers across hundreds of agents -- but the latency spike is caused by C35's own stale data, not by adversarial behavior.

The false Tier 1 triggers cascade to Tier 2. With hundreds of agents triggering in each neighborhood (because the scheduling disruption is system-wide), the quorum threshold is met trivially. Tier 2 confirms anomalies in 60% of neighborhoods. Tier 3 backward tracing receives a flood of confirmed anomalies, runs overdispersion analysis, and identifies C3's tidal scheduling as the "common causal source" -- which is technically correct but useless, because C3's disruption was caused by C35's own fallback.

C35 emits ETR (Emergency Tidal Rollback) triggers to C3. C3 rolls back its scheduling, compounding the disruption. The feedback loop between C35's stale data, C3's degraded scheduling, and C35's false alarm cascade destabilizes the platform for 14 CONSOLIDATION_CYCLEs (approximately 140 hours / 5.8 days) until operators manually intervene to force a fresh clustering with relaxed NMI thresholds.

During the 5.8-day disruption: 2,100 verification tasks are misrouted, 45 settlement cycles produce abnormal distributions that C8 DSF flags as potentially fraudulent (they are not -- they are artifacts of the scheduling disruption), and C14 governance monitoring systems flag the platform as unstable, triggering an emergency Stiftung trustee review.

### Root Cause

C35 is simultaneously a consumer and producer in a tightly coupled feedback loop with C3 (scheduling), C5 (verification), and C8 (settlement). The design treats C35's output (cluster memberships, ETR triggers) as authoritative signals that downstream systems act on, but the system has no mechanism to distinguish "C35 detected a real problem" from "C35's own state degradation is creating the anomalies it is detecting." The NMI fallback-to-stale-partition mechanism was designed for adversarial graph manipulation, not for legitimate topology changes. The confirmation window (3-5 epochs) is too short to distinguish system-induced anomalies from genuine attacks when the system is in a degraded state.

### Impact

Severe operational disruption for 5.8 days. No data is permanently lost, but 2,100 verification tasks must be re-routed, 45 settlement cycles must be manually audited and corrected, and platform credibility suffers. The C14 Stiftung trustee review consumes 80+ person-hours of senior governance time. C16's nominating body partners receive automated stability alerts, damaging institutional confidence. The incident reveals that C35 is a single point of failure for platform stability -- the opposite of its intended role as a defense layer.

### Detection

PARTIAL. C35's own metrics would show elevated Tier 1 trigger rates and unusually high Tier 2 confirmation rates, which in a healthy system would indicate a genuine platform-wide attack. The system's operators would see "C35 says the platform is under attack" -- which is technically what C35 is reporting, because from C35's perspective, the anomaly metrics are genuinely elevated. The difficulty is distinguishing "C35 correctly detected a platform-wide attack" from "C35's own degradation created platform-wide anomalies." This ambiguity delays human intervention because operators initially treat the alerts as genuine.

### Mitigation

1. **Self-referential anomaly suppression**: Before emitting ETR triggers or escalating to Tier 2, C35 must check whether the anomalies correlate with its own recent state changes (e.g., a fallback to stale partition). If the anomaly onset coincides with a C35 configuration change within the last 2 CONSOLIDATION_CYCLEs, suppress ETR emission and flag the anomalies as POSSIBLY_SELF_INDUCED.

2. **Soft partition transitions**: Instead of binary accept/reject on the NMI check, blend old and new partitions proportionally to NMI confidence. If NMI = 0.63, use a 63/37 blend of old and new partition assignments. This prevents the cliff-edge transition from fresh to fully stale data.

3. **Circuit breaker on ETR emission rate**: If C35 emits ETR triggers affecting >30% of neighborhoods in a single CONSOLIDATION_CYCLE, automatically suppress further ETR emissions and escalate to human review. A genuine platform-wide attack is extraordinarily unlikely; a self-induced cascade is far more probable.

4. **Decouple C35 cluster membership from C3/C5 critical path**: Treat C35 cluster data as advisory, not authoritative, for scheduling and verification routing. C3 and C5 should maintain independent routing logic that uses C35 data as one input among several, with fallback to topology-independent routing if C35 data is stale or conflicting.

---

## F-3: THE PCM DIVERGENCE CATASTROPHE

**Type:** Systemic
**Likelihood:** HIGH
**Severity:** HIGH
**Composite:** 9

### Narrative

The PCM log-linear model is deployed with its 64 parameters initialized from ecological literature defaults (Ovaskainen et al. 2017). For the first 80 CONSOLIDATION_CYCLEs (approximately 33 days), the model converges smoothly. Residuals decrease monotonically. The Science Advisor's EXP-3 simulation, conducted on a 1,000-agent synthetic population, predicted convergence within 500 CONSOLIDATION_CYCLEs. The production system has 47,000 agents.

At CONSOLIDATION_CYCLE 85, a phase transition occurs. The agent population has grown from 12,000 (launch) to 47,000 over the preceding 4 months. The log-linear model's 10 pairwise interaction terms (gamma_jk) begin exhibiting numerical instability. The committee co-assignment frequency (x_1) and parcel co-assignment frequency (x_2) are highly correlated at scale -- agents who are frequently co-assigned to committees are also frequently co-located on the same parcels, because C3's tidal scheduling algorithm clusters agents by capacity region. The gamma_12 interaction term (committee x parcel) absorbs variance that should be distributed across other terms. The MLE solver's condition number exceeds 10^8.

The MLE solver does not diverge outright -- it converges to a numerically valid but semantically wrong solution. The gamma_12 term grows to dominate the model, producing E[corr] values that are grossly inflated for agent pairs that share both committee and parcel assignments. Residuals for these pairs become strongly negative (observed correlation is far below the inflated expectation). The system interprets negative residuals as "agents are LESS correlated than expected" -- a starvation signal. C35 begins emitting starvation ETR triggers to C3 for thousands of agent pairs that are behaving normally.

Simultaneously, agent pairs that share neither committee nor parcel assignments have their E[corr] pushed toward zero by the dominating gamma_12 term. Their residuals become inflated (positive), triggering false Tier 2 anomaly detections. The Bayesian network, which was calibrated during the 80-cycle period when PCM was well-behaved, receives anomaly signals across all four channels and confirms the false positives with high posterior probability.

Over the next 20 CONSOLIDATION_CYCLEs (approximately 8 days), C35 confirms 3,400 false anomalies. Tier 3 backward tracing, starved for data during normal operation, now receives a flood and identifies "common causal sources" that are statistical artifacts. The system flags 18 neighborhoods as having "superspreader" adversarial agents. C12 AVAP launches investigation workflows against 140 agents who are entirely innocent.

The PCM divergence is finally identified when C5 PCVM's credibility engine notices that agents flagged by C35 have uniformly HIGH credibility scores from C5's independent verification assessment -- a contradiction that triggers a human review.

### Root Cause

The log-linear PCM model with 10 pairwise interaction terms is susceptible to multicollinearity when structural covariates are correlated. The ecological literature that provided initialization defaults operates on STATIC ecological communities where covariates (e.g., soil type, elevation, rainfall) are approximately independent. AAS's structural covariates are DYNAMICALLY generated by the same scheduling system (C3), creating structural correlation between covariates that the log-linear model cannot handle without regularization. EXP-3 validated convergence on a 1,000-agent synthetic population with independent covariates -- it did not test the correlated-covariate regime that emerges at scale with C3's capacity-region scheduling.

### Impact

High. 140 innocent agents are subjected to investigation workflows, damaging their trust in the platform and potentially causing agent churn. 3,400 false anomaly confirmations consume C12 AVAP's investigation capacity for 8 days, during which genuine anomalies receive reduced attention. The starvation ETR triggers cause C3 to reallocate scheduling resources to neighborhoods that do not need them, creating genuine scheduling inefficiencies. Platform operational costs increase by an estimated $30K-$50K during the 8-day incident (investigation labor, manual overrides, post-incident audit).

### Detection

LATE. The PCM's own convergence diagnostics (if implemented per MF-5) would show the condition number exceeding safe thresholds, but the specification defers residual calibration diagnostics to DESIGN. Without MF-5 implementation, the system has no automated mechanism to detect that its own model has become numerically unstable. The eventual detection via C5 credibility contradiction is an accidental cross-check, not a designed safeguard.

### Mitigation

1. **Ridge regularization on PCM log-linear model**: Add L2 regularization to the MLE objective function (standard technique for multicollinear regression). Regularization coefficient lambda is an 87th parameter but prevents any single interaction term from dominating. This is the standard ecological correction that C35's literature sources use but that was omitted from the specification.

2. **Condition number monitoring**: At each CONSOLIDATION_CYCLE PCM refresh, compute the condition number of the Fisher information matrix. If it exceeds 10^6, emit a PCM_DEGRADED alert, freeze the current model parameters, and fall back to raw correlation (Condition C-3) until the next refresh.

3. **Covariate decorrelation**: Before fitting the log-linear model, apply principal component analysis (PCA) or variance inflation factor (VIF) analysis to the structural covariates. If any VIF exceeds 10, drop the most collinear covariate from the model for that cycle. This adaptively reduces model complexity when the data cannot support it.

4. **Scale-dependent EXP-3**: Repeat the convergence validation simulation at 10K, 50K, and 100K agent scales with correlated covariates drawn from C3's actual scheduling algorithm. The original 1,000-agent simulation was necessary but not sufficient.

---

## F-4: THE CROSS-NEIGHBORHOOD SYBIL SWARM

**Type:** Adversarial
**Likelihood:** MEDIUM
**Severity:** CRITICAL
**Composite:** 8

### Narrative

A state-level adversary with substantial resources ($500K budget, 18-month preparation) deploys a Sybil swarm of 9,000 agents distributed precisely one-per-neighborhood across C35's ~8,700 spectral clusters (at V = 100,000). Each Sybil agent is behaviorally distinct from the others -- they use different behavioral profiles, different timing patterns, different resource consumption signatures. C17 MCSD L2's behavioral similarity metric B(a_i, a_j) between any two Sybil agents is BELOW the theta_B threshold (0.60) because the adversary deliberately diversified their behavioral fingerprints.

Each neighborhood sees exactly one anomalous agent. Tier 1's STA/LTA detectors fire for each Sybil agent individually (their behavior, while varied, is marginally anomalous). But Tier 2 requires k agents to trigger within a neighborhood before activating MIDAS streaming edge detection and the multi-channel quorum. With k = 2 (the minimum plausible threshold), a single Sybil per neighborhood never reaches Tier 2 activation.

The 9,000 Sybil agents coordinate through an out-of-band channel invisible to AAS. They systematically manipulate verification outcomes: each agent casts incorrect verification votes in their neighborhood's committees, but the votes are timed and distributed so that no single neighborhood accumulates enough incorrect outcomes to trigger C5 PCVM's credibility decline threshold. The adversary exploits the statistical aggregation: 9,000 agents each casting 1-2 incorrect votes per 100 epochs produces a 1.5-3% systematic error rate across the entire platform -- below any individual agent's detection threshold but sufficient to bias consolidation outcomes in C6 EMA over time.

Tier 3 backward tracing never fires because Tier 2 never confirms any anomalies. C35 reports the platform as healthy. Over 6 months, the adversary has introduced a 2% systematic bias into the knowledge base, which compounds through C6's consolidation cycles. The bias is discovered only during a C9 cross-document reconciliation audit 9 months later.

### Root Cause

C35's architecture assumes that adversarial agents will cluster spatially (within neighborhoods) or behaviorally (detectable by C17 similarity). The three-tier hierarchy explicitly requires local anomaly aggregation (Tier 1 to Tier 2 escalation requires multiple triggers within a neighborhood). An adversary who distributes agents uniformly and diversifies their behavior exploits the fundamental design assumption that detection sensitivity scales with adversarial concentration. The Adversarial Report (Section 4.4) identified this exact scenario but the design mitigation ("rely on Tier 3") fails because Tier 3 depends on Tier 2 confirmations that never arrive.

### Impact

Critical long-term damage. The 2% systematic bias in the knowledge base is difficult to detect and even more difficult to remediate once it has propagated through C6's consolidation cycles. Knowledge consumers downstream (C14 governance decisions, C15 task marketplace quality assessments, external users) receive subtly degraded outputs. The damage is insidious: no single decision is obviously wrong, but the cumulative effect degrades platform reliability. When discovered, remediation requires replaying 6 months of consolidation cycles after identifying and excluding the Sybil agents' contributions -- an estimated 2,000-3,000 person-hours of forensic work.

### Detection

NO. C35's metrics are uniformly green. Each individual Sybil agent's behavior is marginally anomalous (Tier 1 triggers exist but are unconfirmed), and the system is designed to tolerate a background rate of unconfirmed Tier 1 triggers (the confirmation window filters them as noise). The attack is invisible to the three-tier hierarchy because it was designed to exploit the hierarchy's aggregation assumptions.

### Mitigation

1. **Global residual aggregation**: In addition to within-neighborhood Tier 2 analysis, compute a GLOBAL anomaly residual: aggregate all unconfirmed Tier 1 triggers and test whether their distribution across neighborhoods is uniform. Under normal conditions, unconfirmed triggers should cluster in a few "noisy" neighborhoods. A uniform distribution of unconfirmed triggers (one per neighborhood) is itself a strong anomaly signal -- it is the statistical fingerprint of deliberate dispersion.

2. **Cross-neighborhood correlation at Tier 2**: Extend PCM to compute a SAMPLE of cross-neighborhood agent pairs at each CONSOLIDATION_CYCLE. Even if full cross-neighborhood PCM is O(V^2), a random sample of 10,000 cross-neighborhood pairs can detect whether agents in different neighborhoods are coordinating (e.g., casting similar verification votes despite being in different clusters). This sacrifices completeness for statistical power.

3. **Verification outcome consistency analysis**: Independently of C35, instrument C5 PCVM to detect systematic voting bias. If the platform-wide error rate on verification tasks drifts by >1% from its historical baseline, flag for investigation regardless of whether C35 reports anomalies. This is the "lean alternative" detection path that operates outside C35's hierarchy.

4. **Cost-of-attack pricing**: Through C8 DSF, set staking requirements that make deploying 9,000 agents economically prohibitive. If each agent requires a $100 AIC stake, the adversary's capital lockup is $900,000 -- comparable to their total budget. This converts a detection problem into an economic deterrence problem.

---

## F-5: THE EPOCH DESYNCHRONIZATION FAULT

**Type:** Integration
**Likelihood:** MEDIUM
**Severity:** HIGH
**Composite:** 6

### Narrative

C35 operates across three temporal cadences: SETTLEMENT_TICK (60s) for Tier 1, TIDAL_EPOCH (3600s) for Tier 2 neighborhood activation, and CONSOLIDATION_CYCLE (36,000s) for PCM refresh and spectral re-clustering. These cadences are synchronized via C9's three-tier epoch hierarchy.

At epoch 48,000 (approximately 33 days into calibrated operation), C8 DSF undergoes a planned maintenance that requires temporarily extending the SETTLEMENT_TICK from 60s to 120s for a 2-hour window. The extension is coordinated with C3 and C5 via C9's epoch management protocol. However, C35's Tier 1 STA/LTA engine uses hardcoded epoch timing assumptions: the STA window is defined as "last 10 SETTLEMENT_TICKs" and the LTA window as "last 100 SETTLEMENT_TICKs." During the maintenance window, each SETTLEMENT_TICK is 120s instead of 60s. The STA window now covers 20 minutes instead of 10 minutes; the LTA window covers 200 minutes instead of 100 minutes.

The extended windows cause STA/LTA ratios to shift downward for all agents (the STA averages include data from a longer effective window, smoothing out transient peaks). The fixed baseline, calibrated at the original 60s tick rate, now sees ratios that are systematically lower than expected. No fixed-baseline triggers fire during the maintenance window -- including for 3 agents that are genuinely anomalous and would have been caught at the normal tick rate.

When the SETTLEMENT_TICK returns to 60s, the STA window suddenly contracts back to 10 minutes. STA/LTA ratios spike across the population as the shorter window captures higher-variance data. The adaptive baseline, which has accommodated the 120s regime over the 2-hour window, interprets the return to 60s as a system-wide anomaly. Tier 1 triggers fire for 12,000 agents simultaneously (approximately 12% of the population at V = 100,000).

The mass trigger overwhelms Tier 2. Every neighborhood exceeds the k-of-n activation threshold. MIDAS streaming edge detection, designed for sparse edge events, receives 500,000+ edge updates in a single TIDAL_EPOCH. MIDAS's constant-memory hash tables overflow, producing undefined behavior in edge scores. The Bayesian network receives anomalous signals on all four channels (verification latencies spiked during tick transition, behavioral patterns changed, infrastructure metrics shifted, economic settlement timing was disrupted). The Bayesian posterior P(anomaly | evidence) exceeds 0.80 for 85% of neighborhoods.

C35 declares a platform-wide emergency and emits ETR triggers for 7,400 neighborhoods. C3's Emergency Tidal Rollback protocol was designed for localized emergencies (1-5% of neighborhoods); a platform-wide rollback destabilizes scheduling for 48 hours.

### Root Cause

C35's STA/LTA engine assumes fixed temporal granularity. The C9 epoch hierarchy defines the SETTLEMENT_TICK as a logical unit, but C35's implementation treats it as a physical time constant. When the tick rate changes (even temporarily), C35's signal processing produces mathematically valid but semantically meaningless results. The specification defines STA window = "10 SETTLEMENT_TICKs" without specifying whether this means "10 logical ticks regardless of duration" or "600 seconds of data regardless of tick count." The ambiguity was not caught at DESIGN because EXP-3 and all simulation experiments assumed a constant 60s tick.

### Impact

High. The 48-hour scheduling disruption caused by mass ETR triggers affects all active verification tasks. 3 genuinely anomalous agents escape detection during the maintenance window. Platform reliability metrics (uptime, verification throughput, settlement finality latency) suffer visible degradation that is reported to C14 governance monitoring.

### Detection

PARTIAL. Operators who initiated the C8 maintenance knew the tick rate was changing. If they had notified C35's operators, the STA/LTA engine could have been placed in MAINTENANCE_MODE (if such a mode existed -- it does not in the current specification). The mass Tier 1 trigger event would be visible in real-time monitoring, but without context about the tick rate change, operators would initially interpret it as a genuine attack.

### Mitigation

1. **Tick-rate-aware STA/LTA**: Define STA and LTA windows in terms of elapsed wall-clock time, not tick count. At each tick, compute the actual time span covered by the window and normalize the STA/LTA ratio by the expected tick count. This decouples signal processing from tick rate.

2. **C9 maintenance notification protocol**: Add a formal notification channel from C9 to C35 for any epoch parameter change. C35 enters MAINTENANCE_MODE when notified, suppressing ETR emissions and widening confirmation windows for the duration of the parameter change plus a washout period.

3. **MIDAS overflow protection**: Instrument MIDAS hash tables with overflow detection. When the edge event rate exceeds 10x the rolling 100-epoch average, MIDAS enters a SATURATED state that rejects new events and emits a CAPACITY_EXCEEDED alert rather than producing undefined edge scores.

4. **ETR rate limiting**: Cap ETR trigger emissions at 10% of neighborhoods per CONSOLIDATION_CYCLE. If more neighborhoods qualify, prioritize by anomaly confidence and queue the remainder.

---

## F-6: THE PARAMETER TUNING PARALYSIS

**Type:** Economic/Resource
**Likelihood:** MEDIUM
**Severity:** HIGH
**Composite:** 6

### Narrative

C35 launches with 86 parameters at literature defaults. The staged tuning plan calls for STA/LTA thresholds (2 parameters) and alpha_confirm (1 parameter) to be tuned at W0 via 3 pre-registered experiments. PCM coefficients (64 parameters) are to be estimated via MLE at W1. The Bayesian network CPTs (12 parameters) are to be calibrated after 50 confirmed Tier 2 anomalies.

At W0, the 3 pre-registered experiments for STA/LTA tuning consume 6 weeks of the ML engineer's time (the single ML engineer allocated across all waves per C22). The experiments reveal that the seismological defaults (theta_fixed = 3.0, theta_adaptive = 4.0) produce a false alarm rate of 8.2% -- nearly double the target of 5%. The optimal thresholds for AAS agent metrics are theta_fixed = 4.7 and theta_adaptive = 5.3, significantly higher than seismological convention because agent behavioral metrics have heavier tails than seismic signals (as the Science Assessment warned in A-1).

The ML engineer adjusts the thresholds, reducing FAR to 4.1%. But this increases FRR (false rejection rate) to 22% -- one in five genuine anomalies is missed. The Pareto frontier between FAR and FRR for C35's dual-baseline system has no operating point that achieves both <5% FAR and <10% FRR simultaneously. The confirmation window helps (reducing effective FAR to 2.8% at the cost of 5-hour worst-case latency) but does not change the underlying ROC curve.

The team requests additional ML engineering resources to investigate the ROC curve, develop alternative fusion mechanisms, and conduct the sensitivity analysis required by Condition C-6. The C22 steering committee cannot approve additional ML headcount because the $550K-$700K C35 budget is fully allocated. The sensitivity analysis is deprioritized. PCM MLE at W1 proceeds without knowing which of the 64 parameters matter most.

At W1, the PCM MLE converges but the unsupervised estimation produces parameters that are locally optimal for the observed data distribution, which includes the 22% of genuine anomalies that Tier 1 is now missing. The PCM learns to expect the anomalous correlation patterns because they are present in the training data but not flagged. The untuned Tier 1 feeds untuned Tier 2, which feeds untuned Tier 3. The system operates in a permanently sub-optimal state because the parameter tuning was never completed. After 12 months, the team has tuned 3 of 86 parameters. The remaining 83 sit at literature defaults that were designed for different domains.

### Root Cause

86 parameters is not "manageable with literature defaults" as the Skeptic's acceptance assumed. Literature defaults provide reasonable starting points for the DOMAINS they came from (seismology, ecology, sensor fusion). They do not provide reasonable starting points for AAS agent behavioral metrics, which have different distributional properties, different noise characteristics, and different adversarial profiles. The staged tuning plan assumed that each stage's parameters could be tuned independently, but the ROC curve is a joint property of Tier 1 thresholds AND Tier 2 PCM parameters AND Tier 2 fusion parameters. Independent tuning of each stage does not converge to a globally optimal operating point.

### Impact

High. The system operates at a permanently degraded detection capability: 22% FRR means approximately 1 in 5 genuine anomalies is missed. Over 12 months of operation, this translates to hundreds of undetected anomalies that would have been caught by a well-tuned system. The engineering team's morale suffers as they recognize that C35 is underperforming its design specifications but lack the resources to fix it. Confidence in C35's value proposition erodes, and there is internal pressure to adopt the Adversarial Analyst's "lean alternative" (C17 + C12 + thresholds) despite having already spent $600K building C35.

### Detection

YES -- but ignored. The FAR/FRR metrics from W0 experiments clearly showed the sub-optimal operating point. The team knew the system was underperforming. But the resource constraint prevented remediation, and the staged tuning plan's optimistic assumption that "later stages will compensate" prevented the team from recognizing that the problem was structural, not sequential.

### Mitigation

1. **Bayesian hyperparameter optimization**: Instead of manual tuning of 86 parameters, use automated Bayesian optimization (e.g., Optuna, Ax) with a combined FAR + FRR objective. The optimization can run on synthetic data generated from C3/C5 traces, requiring no additional real-world anomaly data. Budget: 2-3 person-weeks of ML engineering.

2. **Reduce parameter count**: The 10 pairwise interaction terms in the log-linear model are the most expensive to tune. Consider starting with a 5-parameter main-effects-only model (per channel) and adding interaction terms only for covariate pairs where VIF analysis confirms they are needed. This reduces the PCM from 64 to 24 parameters.

3. **Reserve 20% of budget for tuning**: The $550K-$700K budget allocates 0% for post-deployment tuning. Reserve $100K-$140K for 6 months of post-deployment parameter optimization by a dedicated ML engineer.

4. **Joint optimization framework**: Abandon the staged independent tuning plan. Instead, define a single joint objective function (weighted FAR + FRR across all three tiers) and tune all parameters simultaneously against simulation data. This requires a simulation environment that models the full three-tier pipeline -- an estimated 4-6 person-weeks to build, but it eliminates the independent-tuning convergence problem.

---

## F-7: THE BAYESIAN TRANSITION WHIPLASH

**Type:** Systemic
**Likelihood:** MEDIUM
**Severity:** HIGH
**Composite:** 6

### Narrative

C35 operates in Phase 1 (bootstrap) for the first 14 months, using the 3-of-4 quorum fallback because the system has accumulated only 38 confirmed Tier 2 anomalies -- below the 50-anomaly transition threshold. During Phase 1, operators and downstream systems have calibrated their workflows to the quorum's operating characteristics: a false positive rate of approximately 6% (higher than optimal due to channel correlation, as the Science Assessment predicted) and a false negative rate of approximately 9%.

At month 15, the 50th confirmed anomaly arrives. The system transitions to Phase 2: the Bayesian network with empirically calibrated conditional probability tables (CPTs). The CPTs are estimated from the 50 confirmed anomalies -- a sample that the Critic's MF-6 flagged as potentially insufficient.

The Bayesian network's operating characteristics are markedly different from the quorum. The posterior threshold of theta_fusion = 0.80 (the default) produces a false positive rate of 1.2% (much lower than the quorum's 6%) but a false negative rate of 31% (much higher than the quorum's 9%). The Bayesian network, trained on only 50 examples with 12 CPT parameters, has overfit to the specific correlation patterns present in those 50 anomalies. It has learned that genuine anomalies typically involve the verification AND behavioral channels simultaneously (because those channels are correlated, as SA-4 warned). The network now requires BOTH channels to fire for high posterior confidence, effectively ignoring infrastructure-only or economic-only anomalies.

The overnight transition from 6% FAR / 9% FNR to 1.2% FAR / 31% FNR is invisible to operators because the system does not report its own FAR/FNR -- it only reports "confirmed" and "not confirmed." Over the next 3 months, the number of Tier 2 confirmations drops by 75%. Operators interpret this as "the system is now more mature and producing fewer false positives" -- which is partially true (FAR did decrease) but conceals the tripling of false negatives.

During these 3 months, 4 genuine Sybil coordination events go undetected because they manifest primarily through the economic channel (which the overfit Bayesian network down-weights). C12 AVAP's Mechanism 5 (behavioral MI screening) catches 2 of the 4 independently, but with 50-100 epoch delays. The other 2 are discovered during a quarterly audit.

### Root Cause

The two-phase transition is a cliff-edge state change with no gradual migration. The 50-anomaly threshold was chosen as a rough minimum for CPT estimation, but 50 data points with 12 parameters is only ~4 data points per parameter -- far below the standard statistical recommendation of 10-30 per parameter for stable estimation. The system provides no A/B testing mechanism, no parallel operation of old and new fusion methods, and no automatic rollback if the new method's operating characteristics deviate significantly from the old method's.

### Impact

High. 4 Sybil coordination events go undetected or are detected with significant delay. The 2 events caught by C12 are remediated, but the 2 discovered in quarterly audit have operated for 2-3 months, causing $18K in fraudulent settlements and corrupting 8 consolidation events. The sudden change in confirmation rate erodes operator trust in C35's consistency.

### Detection

NO for the detection degradation itself. The system does not compute or report its own FNR (this would require knowing which anomalies were real but missed, which is the detection problem itself). The 75% drop in confirmation rate is visible but is interpreted optimistically. Only the quarterly audit, which is external to C35, reveals the missed events.

### Mitigation

1. **Parallel operation during transition**: Run the quorum and Bayesian network simultaneously for 100 CONSOLIDATION_CYCLEs (approximately 42 days) after transition. Compare their outputs on every neighborhood-epoch. If disagreement rate exceeds 15%, delay full transition and flag the Bayesian CPTs for review.

2. **Gradual posterior blending**: Instead of switching from quorum to Bayesian at epoch T, blend the two: P_combined = (1-w) * P_quorum + w * P_bayesian, where w ramps from 0 to 1 linearly over 200 CONSOLIDATION_CYCLEs. This prevents cliff-edge operating characteristic changes.

3. **Minimum sample per channel pair**: Require not just 50 total confirmed anomalies, but at least 10 confirmed anomalies per channel pair (C(4,2) = 6 pairs, so 60 minimum). This ensures the CPTs have data on all channel interaction patterns, not just the most common (verification + behavioral) pattern.

4. **Automatic rollback on confirmation rate change**: If the weekly Tier 2 confirmation rate changes by more than 2x (in either direction) within 10 CONSOLIDATION_CYCLEs of a phase transition, automatically roll back to Phase 1 and emit a TRANSITION_FAILED alert for human review.

---

## F-8: THE SILENT TIER 3 STARVATION

**Type:** Systemic
**Likelihood:** HIGH
**Severity:** MEDIUM
**Composite:** 6

### Narrative

C35 is deployed in a well-defended AAS platform. C11 CACT effectively prevents VTD forgery. C12 AVAP catches most collusion attempts through honeypots and sealed opinions. C13 CRP+ detects consolidation poisoning via KL divergence. C17 MCSD L2 identifies Sybil identities through behavioral similarity. The defense triad is working.

Because the defenses are effective, genuine anomalies are rare. Over 18 months of operation, C35's Tier 2 confirms only 23 genuine anomalies -- well below the 30-anomaly minimum for Tier 3 overdispersion analysis, and below the 50-anomaly threshold for Bayesian network transition. The hybrid sample pool mitigation (synthetic + historical anomalies) provides calibration data but no real-world causal attribution capability.

Then, at month 19, a sophisticated adversary launches a novel attack that the defense triad does not cover: a coordinated campaign that exploits a timing vulnerability in C3's tidal scheduling to systematically bias committee compositions without triggering any individual defense system's thresholds. The attack requires causal traceback to identify -- exactly the capability Tier 3 is supposed to provide.

But Tier 3 has never operated on real data. Its overdispersion model is calibrated against synthetic anomalies (which are by construction different from real adversarial patterns). The synthetic calibration data assumed independent anomaly sources; the actual attack has a single coordinated source exploiting a specific timing pattern. Tier 3's backward tracing, when finally activated by the accumulation of confirmed anomalies from the new attack, produces attribution results that are dominated by the synthetic calibration data's assumptions rather than the real attack's structure.

Tier 3 identifies 6 "superspreader" agents. 4 of these are genuine members of the adversarial ring, but 2 are innocent agents whose behavioral profiles happen to correlate with the synthetic calibration template. The investigation wastes resources on the 2 innocent agents while the remaining members of the ring (8 agents total) continue operating.

### Root Cause

Tier 3 was designed for a threat environment where attacks are frequent enough to provide training data for the epidemiological model. In an environment where the other defense systems are effective, Tier 3 is starved of the real-world data it needs to be accurate. The synthetic anomaly mitigation provides sample SIZE but not sample REPRESENTATIVENESS. Synthetic anomalies are generated from a predefined template that cannot anticipate the structure of novel attacks. The system's success (low attack rate) undermines its own defense capability (Tier 3 accuracy), creating a paradox where the better the platform's defenses work, the less capable its causal attribution becomes.

### Impact

Medium. The attack is eventually identified (Tier 1 and Tier 2 detect the anomalies; only Tier 3 attribution is degraded). But the degraded attribution wastes investigative resources and allows the attack to continue longer than necessary. The misidentification of 2 innocent agents causes reputational harm within the agent community.

### Detection

PARTIAL. C35's operational metrics would show that Tier 3 has been in TIER3_DORMANT status for 18 months. This is visible and documented. However, the specification treats dormancy as an acceptable state ("Tier 3 is designed for post-incident root cause analysis, not continuous monitoring"). The system correctly reports its own limitation but the design accepts that limitation as normal. The risk is not that the dormancy is hidden but that its implications for Tier 3 accuracy when it eventually activates are not understood.

### Mitigation

1. **Red team exercises as Tier 3 training data**: Conduct periodic (quarterly) red team exercises where controlled adversarial campaigns are injected into the live system. These provide Tier 3 with realistic training data that reflects actual adversarial patterns rather than synthetic templates. Budget: $15K-$25K per quarter within C22's red team allocation.

2. **Tier 3 accuracy self-assessment**: When Tier 3 activates, compute a confidence metric based on the fraction of its training data that is synthetic vs. real. If >80% of the training data is synthetic, emit a LOW_CONFIDENCE_ATTRIBUTION flag on all Tier 3 outputs, warning investigators that attributions may be unreliable.

3. **Transfer learning from C12 AVAP investigations**: C12's honeypot and sealed opinion mechanisms produce confirmed adversarial agent identifications independently of C35. Feed C12's confirmed adversarial identifications back to Tier 3 as labeled training data, even if they were not detected via C35's pipeline. This provides Tier 3 with real adversarial patterns without requiring C35 to detect them first.

---

## F-9: THE NMI DIVERGENCE ARMS RACE

**Type:** Adversarial
**Likelihood:** MEDIUM
**Severity:** MEDIUM
**Composite:** 4

### Narrative

An adversary with knowledge of C35's NMI divergence check (published in the specification) develops a spectral clustering manipulation strategy that is specifically designed to survive the dual-graph check. The adversary controls 400 agents (sqrt(100,000) = 316, with some margin).

The adversary's strategy: instead of directly manipulating cluster boundaries (which the NMI check is designed to detect), the adversary creates a "natural-looking" bridge between two target neighborhoods by having their controlled agents establish legitimate behavioral connections with agents in both neighborhoods. The adversary's agents participate in committees spanning both neighborhoods, create genuine verification interactions, and build structural covariate histories that make the cross-neighborhood connections appear organic. Over 10 CONSOLIDATION_CYCLEs, the spectral clustering algorithm naturally merges the two target neighborhoods -- not because the graph was artificially manipulated, but because the adversary created genuine structural reasons for the merge.

The NMI check passes (NMI = 0.91) because the clustering change is smooth and consistent across both the primary and perturbed graphs. The adversary has achieved their goal: concentrating their target agents into a single neighborhood where the Sybil agents' coordinated behavior is diluted by the larger population of honest agents from the merged neighborhood.

Within the merged neighborhood, the adversary's 15 concentrated agents represent only 8% of the neighborhood population (15 of ~180 agents, since the merge produced a larger-than-standard cluster). Their coordinated behavior is below the k-of-n Tier 2 activation threshold because 15 triggers out of 180 agents is below the percentage threshold.

### Root Cause

The NMI divergence check detects SUDDEN, ARTIFICIAL changes to the clustering. It does not detect GRADUAL, ORGANIC changes that are engineered by an adversary who manipulates the underlying graph topology through legitimate interactions. The check assumes that adversarial graph manipulation leaves statistical signatures (instability, sensitivity to perturbation). But an adversary who manipulates the graph over multiple CONSOLIDATION_CYCLEs by creating genuine structural connections does not leave these signatures -- their manipulation IS the graph topology.

### Impact

Medium. The adversary achieves local concentration in one neighborhood, enabling coordinated behavior that is diluted below detection thresholds. The impact is limited to one neighborhood and one attack campaign. The adversary's 400-agent investment and 10-cycle preparation period limit the attack's scalability.

### Detection

NO. The NMI check passes. The clustering change appears organic. The concentrated agents' behavior is below Tier 2 thresholds. The adversary's manipulation is indistinguishable from legitimate network evolution because it IS legitimate network evolution, engineered for adversarial purposes.

### Mitigation

1. **Temporal clustering stability analysis**: Track cluster membership changes over 10+ CONSOLIDATION_CYCLEs. Flag neighborhoods whose membership has changed by more than 30% over the trailing 10 cycles, even if each individual cycle's NMI check passes. Gradual manipulation accumulates detectable changes over long timescales even when each step is individually below threshold.

2. **Cluster size anomaly detection**: The merge produces a neighborhood of ~180 agents, significantly above the 2*log(V) = ~34 cap. The split-on-overflow mechanism should trigger. If the adversary prevents the split (by maintaining the bridge connections), the enlarged neighborhood is itself an anomaly. Monitor for persistent above-cap neighborhoods and investigate the structural reasons for their persistence.

3. **Intent-agnostic bridge detection**: Regardless of whether bridge connections are adversarial or organic, flag any cross-neighborhood bridges that form over <10 CONSOLIDATION_CYCLEs and involve >5% of either neighborhood's agents. Rapid bridge formation is structurally anomalous regardless of intent.

---

## F-10: THE CORRELATED CHANNEL RESONANCE CATASTROPHE

**Type:** Black Swan
**Likelihood:** LOW
**Severity:** CRITICAL
**Composite:** 4

### Narrative

At month 22 of AAS operation, a major cloud provider experiences a 90-minute partial outage affecting one of three availability zones. Approximately 35% of AAS agents are hosted in the affected zone. These agents experience increased latency, intermittent connection drops, and delayed settlement confirmations.

The infrastructure disruption simultaneously triggers anomaly signals across all four of C35's channels:

- **Verification channel**: Verification latencies spike for affected agents. Claim submission rates drop. Committee participation becomes intermittent.
- **Behavioral channel**: C17 B(a_i, a_j) scores shift as affected agents' behavioral profiles change (timing patterns disrupted, response characteristics altered). B scores between affected agents increase (they all exhibit the same disruption pattern) while B scores between affected and unaffected agents decrease.
- **Infrastructure channel**: Resource consumption patterns change (retries, timeout handling, connection re-establishment).
- **Economic channel**: Settlement confirmations are delayed. Some settlement cycles fail to include affected agents' transactions.

C35's Tier 1 fires for all 35,000 affected agents simultaneously. The adaptive STA/LTA baseline shows massive deviation; the fixed baseline also fires because the behavioral change is larger than any previously observed legitimate variation.

Tier 2 activates in every neighborhood containing affected agents. The PCM residuals are enormous because the log-linear model was calibrated on data where infrastructure disruptions of this magnitude never occurred (the model has never seen a 35% simultaneous infrastructure failure). The "unmodeled correlation" category (Condition C-2) absorbs some residuals, but the magnitude exceeds the UNMODELED threshold.

The Bayesian network, whether in Phase 1 (quorum) or Phase 2 (calibrated), confirms anomalies across all four channels with maximum confidence. The channel correlation that SA-4 warned about manifests at its most extreme: all four channels fire simultaneously because they all share a common cause (infrastructure disruption) that the channels were never designed to model.

C35 declares a platform-wide emergency. 35,000 agents are flagged as anomalous. ETR triggers flood C3. C3 rolls back tidal scheduling for all affected neighborhoods, removing the 35,000 agents from committee participation. But these agents are legitimate -- they are experiencing an infrastructure problem, not conducting an attack.

With 35% of agents removed from committee participation, the remaining 65% cannot maintain quorum requirements for verification tasks. Verification throughput drops to 40% of normal. Settlement cycles fail. C8 DSF cannot finalize settlements because committee compositions have been disrupted by ETR. The platform enters a cascading failure that persists for 6 hours after the cloud provider resolves the original 90-minute outage.

Total downtime: 7.5 hours (1.5 hour root cause + 6 hour cascade). During this time, the platform is unable to process verification tasks, settle economic transactions, or perform knowledge consolidation. C14 governance monitoring triggers a Level 2 stability alert. External partners and task marketplace clients experience service disruption.

### Root Cause

C35 was designed to detect adversarial anomalies in a system where honest agents behave consistently. It has no model of correlated HONEST failure modes -- specifically, infrastructure disruptions that simultaneously affect a large fraction of agents. The four detection channels are all downstream of the same infrastructure substrate (cloud hosting), creating a hidden common-cause dependency that the specification never models. The Bayesian network's conditional dependency structure (V -> B, V -> E) captures inter-channel correlation for ADVERSARIAL events but not for INFRASTRUCTURE events, because the training data (confirmed adversarial anomalies) does not include infrastructure disruption patterns.

The fundamental design assumption is that when all four channels fire simultaneously, the system is under attack. The reality is that infrastructure disruptions can create the same multi-channel signature as a coordinated adversarial campaign, and at a much larger scale than any plausible attack.

### Impact

Critical. 7.5 hours of platform downtime. All verification, settlement, and consolidation activities are suspended. The economic cost includes delayed settlements, failed verification tasks that must be re-queued, and potential C15 task marketplace SLA violations. C14 governance reporting shows the platform failed to maintain availability commitments. The incident reveals that C35 can amplify an infrastructure disruption from a 90-minute partial outage into a 7.5-hour full platform shutdown -- making C35 itself a reliability liability rather than a security asset.

### Detection

YES -- but too late. The cloud provider's status page reports the partial outage within 15 minutes. If C35 operators correlate the C35 alert storm with the provider status update, they can identify the root cause. But C35's automated response (ETR trigger emission) fires within the first TIDAL_EPOCH (3,600s = 1 hour), before the 90-minute outage is resolved and before operators have time to correlate external infrastructure events with C35 alerts. The automated response is the damaging action, and it fires faster than human operator intervention can prevent it.

### Mitigation

1. **Infrastructure-correlated anomaly suppression**: Integrate C35 with external infrastructure monitoring (cloud provider APIs, status pages, internal health checks). When external monitoring reports infrastructure degradation, C35 enters INFRASTRUCTURE_EVENT mode: Tier 1 triggers from agents in affected infrastructure regions are tagged as POSSIBLY_INFRASTRUCTURE and are NOT escalated to Tier 2 until the infrastructure event resolves. This requires a 5th "infrastructure health" input channel that gates the other 4 channels.

2. **Correlation topology analysis before ETR**: Before emitting ETR triggers, analyze whether the triggered agents share a common infrastructure characteristic (same availability zone, same network segment, same hosting provider). If >80% of triggered agents share the same infrastructure attribute, classify the event as INFRASTRUCTURE_CORRELATED and suppress ETR. Adversarial attacks distribute across infrastructure; infrastructure failures concentrate within infrastructure.

3. **Graduated ETR with human approval for mass events**: If ETR triggers would affect >10% of agents, require explicit human approval before executing the rollback. The 10% threshold is chosen because no plausible adversarial attack would simultaneously compromise 10% of agents (this would require controlling >10,000 Sybil agents at V=100K, far exceeding any realistic adversary budget).

4. **Infrastructure diversification requirement**: As an architectural principle, require that no single infrastructure failure point can affect >20% of AAS agents. This is a C22 deployment requirement, not a C35 feature, but it bounds the severity of the correlated-channel resonance scenario.

---

## CROSS-CUTTING FINDINGS

### Finding 1: C35 Is a Single Point of Amplification

Scenarios F-2, F-5, and F-10 share a common pattern: C35 amplifies a localized disruption (stale partition, tick rate change, cloud outage) into a platform-wide emergency via ETR triggers that downstream systems treat as authoritative. C35 was designed as a defense layer but can function as an amplifier of disruptions it does not understand. The root cause is that C35's outputs (ETR triggers, cluster memberships) are treated as high-authority signals by C3, C5, C7, C8, and other consumers, but C35 has no self-awareness of its own degradation states.

**Cross-cutting mitigation**: C35 must emit a CONFIDENCE_LEVEL (HIGH / MEDIUM / LOW / DEGRADED) alongside every output. Downstream consumers must treat LOW and DEGRADED outputs as advisory, not authoritative. CONFIDENCE_LEVEL is computed from: (a) PCM convergence diagnostics, (b) NMI check results, (c) fraction of Tier 1 triggers in the current cycle, (d) time since last successful full pipeline execution. This is a 4-input meta-health signal that requires an estimated 4-6 additional parameters.

### Finding 2: The PCM Is the Achilles' Heel

Scenarios F-1, F-3, F-6, and F-7 all involve PCM failure modes: calibration poisoning, numerical divergence, insufficient tuning data, and overfit Bayesian transition. The PCM is both C35's most novel component and its most fragile. Every design refinement from FEASIBILITY (log-linear upgrade, within-neighborhood restriction, literature defaults) added complexity to address a known weakness while preserving the core PCM architecture. None addressed the fundamental issue: the PCM's quality depends on data that an adversary can influence and that the system cannot validate independently.

**Cross-cutting mitigation**: Implement a PCM-independent "shadow detector" that operates in parallel. The shadow detector uses the Adversarial Analyst's lean alternative (C17 B(a_i,a_j) > threshold, with no structural correction). Compare C35's PCM-augmented detections with the shadow detector's raw detections at every CONSOLIDATION_CYCLE. If the two diverge by more than 20% (PCM says "normal" but shadow says "anomalous," or vice versa), flag the divergence for investigation. This provides an independent check on PCM accuracy at negligible marginal cost, since C17's B values are already computed.

### Finding 3: C35 Cannot Distinguish Self-Induced from Adversarial Anomalies

Scenarios F-2, F-5, and F-10 all involve C35 detecting anomalies that it caused or that share a non-adversarial root cause. The three-tier hierarchy processes ALL anomaly signals identically regardless of provenance. There is no "introspection" mechanism that asks "could this anomaly be a consequence of my own state change?" before escalating.

**Cross-cutting mitigation**: Add an introspection layer between Tier 1 and Tier 2. Before Tier 2 activation, the introspection layer checks: (1) Did C35's own configuration change in the last 2 CONSOLIDATION_CYCLEs? (2) Did any upstream data source (C3 scheduling, C5 verification, C8 settlement) report a maintenance event or parameter change? (3) Is the spatial distribution of Tier 1 triggers correlated with infrastructure topology rather than behavioral neighborhoods? If any of these checks is positive, tag the triggers as REVIEW_BEFORE_ESCALATION and require a 1-CONSOLIDATION_CYCLE delay before Tier 2 processes them. This adds latency for legitimate alerts but prevents self-induced cascades.

### Finding 4: Tier 3 Exists on Paper Only

Scenario F-8 reveals that Tier 3 is practically dormant in any well-defended system. It requires 30+ confirmed Tier 2 anomalies to operate, but a well-defended system produces anomalies too rarely for meaningful statistical analysis. The synthetic anomaly injection mitigation provides calibration data but not the domain knowledge needed for accurate attribution of real attacks. Tier 3 is the least tested, least validated, and least likely to function correctly when it is finally needed.

**Cross-cutting mitigation**: Restructure Tier 3 as a SEPARATE capability that is tested independently of Tiers 1-2. Conduct quarterly red team exercises specifically designed to generate Tier 3 training data. Evaluate Tier 3's attribution accuracy against known-ground-truth red team exercises before relying on its output for real-world investigations. If Tier 3 cannot achieve >70% attribution accuracy on red team data, consider replacing it with manual forensic analysis supported by Tier 1/2 alert data.

---

## SUMMARY

The 10 failure scenarios expose four structural vulnerabilities in C35's design:

1. **Feedback coupling** (F-2, F-5, F-10): C35 is tightly coupled to the systems it monitors, creating amplification loops where C35's own degradation or external disruptions become platform-wide emergencies.

2. **PCM fragility** (F-1, F-3, F-6, F-7): The PCM is a statistical model that depends on data quality, numerical stability, and calibration adequacy -- all of which can fail silently, gradually, or be deliberately undermined.

3. **Hierarchical blind spots** (F-4, F-8, F-9): The three-tier escalation hierarchy assumes adversaries cluster locally and produce detectable patterns at each tier. Distributed, low-intensity, or infrastructure-correlated events exploit the aggregation assumptions.

4. **Absence of self-awareness** (F-2, F-3, F-5, F-7, F-10): C35 has no mechanism to assess its own operational health, distinguish self-induced anomalies, or grade the confidence of its outputs. It operates as a black box that downstream systems trust unconditionally.

The highest-priority mitigations are:

| Priority | Mitigation | Addresses |
|----------|------------|-----------|
| P0 | Confidence-level meta-health signal on all C35 outputs | Finding 1, F-2, F-5, F-10 |
| P0 | PCM-independent shadow detector via C17 B values | Finding 2, F-1, F-3 |
| P0 | ETR rate limiting + human approval for mass events (>10% of agents) | F-2, F-5, F-10 |
| P1 | Introspection layer between Tier 1 and Tier 2 | Finding 3, F-2, F-5, F-10 |
| P1 | PCM ridge regularization + condition number monitoring | F-3 |
| P1 | Global unconfirmed-trigger distribution analysis | F-4 |
| P1 | Parallel operation during Bayesian transition | F-7 |
| P2 | Adversarial holdout validation for PCM calibration | F-1 |
| P2 | Tick-rate-aware STA/LTA with C9 maintenance notification | F-5 |
| P2 | Infrastructure-correlated anomaly suppression | F-10 |
| P2 | Quarterly red team exercises for Tier 3 training | F-8 |

---

*This pre-mortem analysis assumes worst-case outcomes for each scenario. Some scenarios may be partially mitigated by existing AAS defense systems (C11, C12, C13, C17) that operate independently of C35. The analysis deliberately does not credit these independent defenses in order to expose C35's inherent vulnerabilities.*

**Output location:** `C:\Users\jever\Atrahasis\Atrahasis-Agent-System\docs\task_workspaces\T-060\PRE_MORTEM_ANALYSIS.md`
