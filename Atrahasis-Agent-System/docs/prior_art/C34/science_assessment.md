# Science Assessment: C34 --- Seismographic Sentinel with PCM-Augmented Tier 2

| Field | Value |
|---|---|
| **Invention ID** | C34 |
| **Title** | Seismographic Sentinel with PCM-Augmented Tier 2 |
| **Assessor** | Science Advisor |
| **Date** | 2026-03-11 |
| **Protocol** | Atrahasis Agent System v2.2 |
| **Document Type** | SCIENCE_ASSESSMENT |

---

## 1. Executive Summary

C34 proposes a three-tier hierarchical anomaly detection pipeline for the Atrahasis distributed agent platform. Tier 1 adapts the STA/LTA ratio trigger from observational seismology to per-agent behavioral monitoring. Tier 2 introduces a Permitted Correlation Model (PCM) that estimates expected inter-agent correlation from structural covariates and detects anomalies via residual analysis, augmented by MIDAS streaming edge detection and a 4-channel quorum. Tier 3 performs epidemiological backward tracing using overdispersion analysis to identify operator-agent mappings. After assessment, the architecture is PARTIALLY_SOUND overall. The individual theoretical components are well-grounded: STA/LTA detection is a mature technique with well-understood ROC properties, PCM residual analysis is statistically principled, spectral clustering is appropriate for the non-adversarial partitioning use case with known caveats, and overdispersion analysis is valid epidemiological methodology. The primary scientific concerns are: (1) the fixed baseline in Tier 1 degrades predictably under distributional shift and the dual-baseline scheme has a formally unresolved decision fusion problem; (2) the PCM linear additive model makes implicit independence assumptions about structural covariates that are unlikely to hold; (3) the 4-channel quorum threshold is not statistically optimal under realistic channel correlation; (4) spectral clustering is vulnerable to specific adversarial graph perturbations; (5) Tier 3 overdispersion analysis requires sample sizes that may not be available at the stated 1K-100K scale for the 'rare' invocation condition. The scaling analysis is largely correct but has one hidden near-quadratic term in the PCM precomputation that must be bounded. Overall soundness: 3.5/5 -- a well-designed detection architecture grounded in real signal processing and statistical theory, with addressable but non-trivial formal gaps.

---

## 2. Individual Assessments

### SA-1: STA/LTA with Dual Baselines

**Question:** Is the fixed + adaptive parallel detection scheme mathematically sound? What are the detection theory properties?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Theoretical Basis:**

STA/LTA ratio detection originates in seismology (Allen 1978; Withers et al. 1998) and is standard practice in seismic event detection networks (e.g., ObsPy, SeisComP). The core principle is comparing short-term signal energy to long-term signal energy: when STA/LTA exceeds a threshold, a transient event is declared. The technique has well-characterized detection theory properties. Under the assumption that the background signal is stationary with variance sigma^2_bg and a transient event adds energy such that variance becomes sigma^2_bg + sigma^2_evt, the STA/LTA ratio follows a Fisher-Snedecor F-distribution with degrees of freedom proportional to the STA and LTA window lengths. The detection probability P_D and false alarm probability P_FA are directly derivable from the F-distribution CDF, giving a complete Neyman-Pearson characterization. This is textbook detection theory (Kay 1998, Statistical Signal Processing: Detection Theory).

**Dual Baseline Assessment:**

The proposal to maintain two parallel baselines -- one fixed at registration and one adaptive (rolling long-term average) -- is a reasonable architectural choice motivated by the desire to detect both absolute deviations (agent behavior departs from its registration-time profile) and relative deviations (agent behavior departs from its recent history). This dual approach has precedent in intrusion detection systems (Denning 1987, An Intrusion Detection Model) where both static and dynamic profiles are maintained. However, the proposal does not specify the decision fusion rule for combining the two STA/LTA triggers. This is a non-trivial detection theory problem. The two baselines produce two binary detection decisions per epoch. The four possible fusion rules are: (a) OR -- trigger if either fires (maximizes sensitivity, degrades specificity); (b) AND -- trigger if both fire (maximizes specificity, degrades sensitivity); (c) weighted score fusion -- combine STA/LTA ratios before thresholding (requires specifying a combining function); (d) sequential -- use one as a gate for the other. The optimal rule depends on the correlation structure between the two detectors, which in turn depends on the nature of the anomalous behavior. The OR rule is likely intended (trigger when either STA/LTA exceeds threshold), but this doubles the false positive rate under independence and more than doubles it under positive correlation.

**Fixed Baseline Degradation:**

The fixed baseline degrades under three well-characterized conditions: (1) Distributional shift -- if the agent's normal operating behavior evolves over time (model updates, infrastructure migration, workload changes), the fixed baseline becomes increasingly stale and the STA/LTA ratio against the fixed baseline produces rising false positives. The rate of degradation depends on the drift rate relative to the fixed baseline's variance estimate. Under linear drift at rate mu_drift per epoch, the expected false positive rate grows as Phi(mu_drift * t / sigma_bg) where t is epochs since registration. At typical parameter settings, this becomes problematic within O(sigma_bg / mu_drift) epochs. (2) Non-stationarity -- if the agent's metric distributions have time-varying variance (heteroscedasticity), the fixed baseline's variance estimate is incorrect and the STA/LTA threshold is miscalibrated. (3) Concept drift in the task distribution -- if the platform's task mix evolves, agents' behavioral profiles shift even without any change to the agent itself, causing the fixed baseline to fire spuriously.

**Adaptive Baseline Risks:**

The adaptive baseline is vulnerable to the well-known 'boiling frog' attack: an adversary who changes behavior gradually -- slowly enough that each epoch's change is within the adaptive LTA's accommodation -- can completely shift the agent's behavioral profile without ever triggering the adaptive STA/LTA. The adaptive window length determines the minimum gradient of change that is detectable. If the LTA window is W epochs, changes with gradient below approximately 2*sigma_bg / sqrt(W) per epoch will be absorbed into the baseline without triggering. This is the fundamental reason the fixed baseline exists: it catches gradual drift that the adaptive baseline misses. The two baselines are therefore complementary, which is the right design intuition.

**Roc Characteristics:**

Under stationary conditions with Gaussian-distributed metrics, the STA/LTA detector has a well-characterized ROC curve parameterized by the window ratio and the threshold. The area under the ROC curve (AUC) increases with the signal-to-noise ratio (SNR = sigma_evt / sigma_bg) and with the STA window length (longer STA integrates more signal, improving SNR at the cost of detection latency). For the O(1) per-agent-per-epoch claim to hold, the STA window must be fixed-length (not growing with agent count), which is satisfied. The detection latency is proportional to the STA window length. A typical STA/LTA configuration in seismology uses STA = 1-3 seconds and LTA = 10-60 seconds. Translating to the Atrahasis epoch regime: if STA = 1 SETTLEMENT_TICK (60s) and LTA = 10 SETTLEMENT_TICKs (600s), detection latency is 60 seconds, which is compatible with the stated SETTLEMENT_TICK cadence.

#### Key Risks

- Decision fusion rule between fixed and adaptive baselines is unspecified. The OR fusion doubles false positive rate; AND fusion halves detection probability for single-baseline anomalies. The optimal rule depends on unknown correlation structure.
- Fixed baseline degrades predictably under distributional shift. Must specify a baseline refresh policy (e.g., annual re-registration SEB from C17) or accept monotonically increasing false positive rate.
- Adaptive baseline enables 'boiling frog' gradual evasion. The minimum detectable gradient is inversely proportional to sqrt(LTA_window). Longer LTA windows catch slower drift but increase detection latency for sudden changes.
- The O(1) complexity claim is accurate per agent per epoch for the STA/LTA computation itself, but assumes fixed-length feature vectors. If the feature dimensionality grows (e.g., new modalities added), the per-agent cost grows linearly with feature dimensions, not agent count.

#### Recommended Experiments

1. Measure the ROC curves (P_D vs P_FA) for the dual-baseline detector under four fusion rules (OR, AND, weighted, sequential) across three anomaly types: sudden shift, gradual drift, intermittent deviation. Determine which fusion rule maximizes AUC across all three anomaly types.
2. Measure fixed baseline degradation rate: inject known distributional drift at rates 0.01, 0.05, 0.10 sigma_bg per epoch and measure false positive rate over 100, 500, 1000 epochs. Determine the epoch count at which fixed-baseline FPR exceeds 5%.
3. Measure 'boiling frog' evasion: adversary shifts behavior by delta per epoch. Sweep delta from 0.001 to 0.1 sigma_bg. Measure detection latency as a function of delta and LTA window length. Identify the minimum detectable gradient for operationally acceptable detection latency (< 100 epochs).

---

### SA-2: Permitted Correlation Model (PCM)

**Question:** Is E[corr] = sum_k f_k(structural_overlap_k) a valid statistical model? What distributional assumptions does it make?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Theoretical Basis:**

The Permitted Correlation Model (PCM) posits that the expected correlation between two agents' behavioral metrics can be decomposed as a sum of functions of structural covariates: E[corr(a_i, a_j)] = sum_k f_k(structural_overlap_k). This is structurally a Generalized Additive Model (GAM; Hastie & Tibshirani 1990), where each f_k is a smooth function of a single structural covariate. GAMs are well-established in statistics and have strong theoretical foundations. The key statistical assumption is additivity: the expected correlation is the sum of individual covariate effects, with no interaction terms. This is formally: E[Y | X_1, ..., X_p] = alpha + sum_k f_k(X_k), where Y = observed correlation and X_k = structural overlap on covariate k.

**Distributional Assumptions:**

The PCM makes several implicit assumptions: (1) Additivity -- the effects of structural covariates on expected correlation are additive. If agent pairs that share both the same model lineage AND the same infrastructure provider have correlation higher (or lower) than the sum of the two individual effects, the model is misspecified. This is an interaction effect. In practice, infrastructure and model lineage are likely to interact: agents running the same model on the same infrastructure will show amplified correlation beyond what each factor contributes independently. (2) Homoscedasticity -- the variance of the residual R = observed - expected is constant across all structural configurations. If agents with high structural overlap have lower residual variance (because more of their correlation is explained), the residual threshold for anomaly detection must be heteroscedastic. A fixed threshold will be too loose for high-overlap pairs and too tight for low-overlap pairs. (3) Normality of residuals -- for the anomaly detection threshold to have interpretable false positive rates, the residual distribution must be approximately known. If the residual is non-Gaussian (e.g., heavy-tailed due to infrastructure outages or batch effects), the threshold-based detection will have higher-than-expected FPR in the tails.

**Multicollinearity Concern:**

The four structural covariates (verification co-occurrence, behavioral similarity from C17, infrastructure fingerprint, economic activity) are likely correlated with each other. Agents that share infrastructure are more likely to show C17 behavioral similarity. Agents that co-occur in verification committees are more likely to share economic activity patterns. When structural covariates are correlated (multicollinearity), the individual f_k functions become unstable: small changes in one covariate cause large changes in its estimated effect because the model cannot distinguish which correlated covariate is responsible. For prediction (estimating E[corr]), multicollinearity is tolerable because the combined prediction is still accurate even if individual f_k are unstable. For residual-based anomaly detection, multicollinearity is more problematic because the expected correlation estimate has higher variance for agent pairs with unusual covariate combinations (high leverage points in regression terminology), leading to inflated residuals and false detections.

**Pcm As Lookup Table:**

The proposal specifies PCM as a precomputed lookup table refreshed at CONSOLIDATION_CYCLE (36,000s) cadence. This means the f_k functions are estimated once per consolidation cycle from historical data and then applied as a static table until the next refresh. This is computationally efficient but introduces a staleness window: any structural change (new infrastructure provider, agent migration, economic regime shift) during the consolidation cycle produces incorrect expected correlations. The staleness window of 36,000s (10 hours) is acceptable for slowly-evolving structural relationships but may miss rapid structural changes.

**Robustness To Nonlinearity:**

GAMs with smooth f_k functions can capture arbitrary nonlinear relationships between each individual covariate and the response. The limitation is in the interactions, not in the per-covariate nonlinearity. If f_k are implemented as spline functions (the standard GAM approach), each structural overlap dimension can have an arbitrarily complex relationship with expected correlation. However, if f_k are implemented as simpler functions (linear, piecewise constant), the model will miss nonlinear per-covariate effects. The specification states f_k but does not specify the function class, which is a design gap.

**Coverage Metric And Fallback:**

The specification includes a PCM coverage metric with fallback to raw correlation below 0.70 threshold. This is a sound design choice: when the PCM has insufficient training data for a particular structural configuration (e.g., a novel infrastructure provider), it should not produce confident expected-correlation estimates. Falling back to raw correlation effectively reverts to a simpler anomaly detection model (absolute correlation threshold rather than residual threshold). The 0.70 coverage threshold is arbitrary and should be empirically calibrated against false negative rate.

#### Key Risks

- Additivity assumption is likely violated. Infrastructure and model lineage interact: same-model-same-infrastructure pairs will show amplified correlation that the additive model underpredicts, causing false FLAG residuals for benign same-provider clusters.
- Multicollinearity among the four structural covariates inflates residual variance for high-leverage (unusual structural configuration) agent pairs, causing elevated false positive rates for agents with rare structural profiles.
- Homoscedasticity assumption is unlikely to hold. Residual variance should decrease for high-overlap pairs (where PCM explains more variance) and increase for low-overlap pairs. A fixed residual threshold is suboptimal; should use standardized residuals (R / sigma_hat(X)).
- Function class of f_k is unspecified. Linear f_k will miss curvature in the covariate-correlation relationship. Spline-based f_k require sufficient data per structural configuration to fit the spline knots.
- PCM precomputation at CONSOLIDATION_CYCLE cadence introduces a 36,000s staleness window. Structural changes within this window produce incorrect expected correlations and potential missed detections.

#### Recommended Experiments

1. Fit both additive GAM and GAM-with-interactions (pairwise interaction terms) to simulated agent correlation data. Measure residual variance reduction from adding interaction terms. If interaction terms reduce residual variance by more than 15%, the additive model is materially misspecified and should include at least the dominant interaction.
2. Test for heteroscedasticity: plot residual variance as a function of predicted E[corr]. If variance is non-constant, implement studentized residuals (R / sigma_hat(X)) for the anomaly threshold.
3. Measure multicollinearity via Variance Inflation Factors (VIF) for the four structural covariates. If any VIF exceeds 5, consider ridge regularization or covariate orthogonalization.
4. Calibrate the 0.70 PCM coverage threshold: vary from 0.50 to 0.90 and measure false negative rate (anomalous pairs incorrectly cleared by raw-correlation fallback) at each threshold.

---

### SA-3: Spectral Clustering for Neighborhood Partitioning

**Question:** Is spectral clustering appropriate for adversarially-influenced graphs? What are known attacks and mitigations?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Theoretical Basis:**

Spectral clustering (Shi & Malik 2000, Normalized Cuts; von Luxburg 2007, Tutorial on Spectral Clustering) partitions a graph by computing the eigenvectors of the graph Laplacian and clustering nodes in the spectral embedding space. It has well-characterized theoretical properties: it approximates the normalized graph cut (NP-hard) and is consistent under certain random graph models (Rohe et al. 2011). The choice of spectral clustering for neighborhood partitioning is architecturally natural: it groups agents that are densely connected (high mutual correlation or co-occurrence) into neighborhoods, which is the desired semantics for Tier 2 regional correlation analysis.

**Adversarial Vulnerability:**

Spectral clustering is known to be vulnerable to adversarial graph perturbation. The relevant literature includes: (1) Bojchevski & Gunnemann (2019, Adversarial Attacks on Node Embeddings via Graph Poisoning) -- demonstrated that adding or removing a small number of edges can significantly alter spectral embeddings, causing nodes to be reassigned to different clusters. The attack requires O(sqrt(n)) edge modifications to change O(n) node assignments in the worst case. (2) Chen et al. (2017) -- showed that spectral clustering degrades gracefully under random noise but is vulnerable to targeted perturbation of bridge edges (edges between clusters). Removing bridge edges causes over-segmentation; adding false bridge edges causes under-segmentation. (3) Spielman (2012) -- spectral gap (lambda_2 / lambda_k+1 where k is the number of clusters) determines robustness: larger spectral gaps mean perturbations have less effect on cluster boundaries.

**Attack Surface In C34 Context:**

In the C34 context, an adversary who controls multiple agents can manipulate the interaction graph to influence neighborhood partitioning. Specific attack strategies: (a) Fragmentation -- by withholding interactions between controlled agents and honest agents, the adversary can cause controlled agents to form their own neighborhood, isolating them from cross-neighborhood correlation detection. (b) Diffusion -- by creating artificial interactions with many honest agents across neighborhoods, the adversary can spread controlled agents across many neighborhoods, diluting their per-neighborhood anomaly signal below the quorum threshold. (c) Bridge manipulation -- by creating or severing connections that serve as bridges between neighborhoods, the adversary can force specific partitioning that is favorable (e.g., splitting a neighborhood that contains evidence of coordinated behavior).

**Mitigation Factors:**

Several design choices in C34 mitigate the spectral clustering vulnerability: (1) The 2*log(V) neighborhood size cap forces neighborhoods to split when they grow too large, limiting the adversary's ability to create very large neighborhoods that dilute anomaly signals. (2) Spectral clustering is performed at CONSOLIDATION_CYCLE cadence (36,000s), so the adversary must maintain graph manipulation continuously across many epochs. (3) The PCM precomputation is based on the same graph, so neighborhood boundaries and expected correlations are jointly determined -- an adversary who manipulates the graph to change neighborhoods also changes the PCM expectations, partially canceling the benefit. (4) Tier 3 backward tracing operates across neighborhood boundaries, so even if an adversary successfully distributes controlled agents across neighborhoods, Tier 3 can still trace the common origin.

**Size Cap Analysis:**

The 2*log(V) neighborhood size cap deserves specific analysis. At V=1,000 agents, neighborhoods are capped at ~20 agents; at V=100,000 agents, ~34 agents. The logarithmic scaling means neighborhoods grow slowly with platform scale. This is appropriate for detection sensitivity (smaller neighborhoods have higher signal-to-noise for correlated behavior) but may produce many neighborhoods (approximately V / (2*log(V)) ~ 50 at V=1,000 and ~2,900 at V=100,000), increasing the Tier 2 computational load. The split-on-overflow policy should specify how the split is performed: random bisection, spectral sub-clustering, or balanced partition. Each has different adversarial implications.

#### Key Risks

- Spectral clustering is vulnerable to targeted edge manipulation by adversaries controlling multiple agents. O(sqrt(n)) edge modifications can change O(n) node assignments in the worst case.
- Fragmentation attack: adversary creates isolated neighborhoods of controlled agents, evading cross-neighborhood correlation detection.
- Diffusion attack: adversary spreads controlled agents thinly across many neighborhoods, diluting per-neighborhood anomaly signal below quorum.
- The split-on-overflow policy for the 2*log(V) cap is unspecified. The choice of split algorithm has adversarial implications.
- At 100K agents, the number of neighborhoods (~2,900) may produce a Tier 2 computational load that is not adequately bounded.

#### Recommended Experiments

1. Simulate adversarial graph perturbation: adversary controls 5%, 10%, 20% of agents and attempts fragmentation and diffusion attacks. Measure the detection rate change compared to non-adversarial baseline under each attack.
2. Measure spectral gap robustness: compute lambda_2 / lambda_{k+1} for realistic interaction graphs at 1K, 10K, 100K agents. Determine the minimum spectral gap required for stable partitioning under adversarial perturbation.
3. Compare split-on-overflow policies (random bisection, spectral sub-clustering, balanced partition) under adversarial graph manipulation. Determine which policy is most robust to targeted splitting attacks.
4. Evaluate alternative partitioning algorithms (Louvain community detection, label propagation) as drop-in replacements for spectral clustering. Measure robustness-to-adversarial-perturbation vs. computational cost tradeoff.

---

### SA-4: 4-Channel Quorum Threshold

**Question:** Is the >=3-of-4 channels statistically justified? What is the joint false-positive rate?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Independent Channel Analysis:**

Under the assumption of channel independence, the joint false positive rate for a k-of-n quorum follows the binomial distribution. For 3-of-4 with per-channel false positive rate p: P(FP_joint) = C(4,3)*p^3*(1-p) + C(4,4)*p^4 = 4*p^3*(1-p) + p^4. For p = 0.05 (5% per-channel FPR): P(FP_joint) = 4*(0.05)^3*(0.95) + (0.05)^4 = 4*0.000125*0.95 + 0.00000625 = 0.000475 + 0.00000625 = 0.000481, or approximately 0.048%. This is excellent -- the quorum achieves approximately 100x FPR reduction relative to single-channel detection. For p = 0.10: P(FP_joint) = 4*0.001*0.90 + 0.0001 = 0.0036 + 0.0001 = 0.0037, or 0.37%. Still very low.

**Correlated Channel Analysis:**

The independence assumption is almost certainly violated. The four channels are: (a) verification co-occurrence, (b) C17 behavioral similarity B(a_i,a_j), (c) infrastructure fingerprint, (d) economic activity. Channels (b) and (c) are positively correlated: agents sharing infrastructure are more likely to show behavioral similarity. Channels (a) and (d) are positively correlated: agents that co-occur in verification committees are more likely to share economic activity patterns (because verification generates AIC income). Under positive correlation, the joint false positive rate is HIGHER than the independence calculation suggests. The mathematical framework for correlated binary detectors is the multivariate Bernoulli model. If the average pairwise correlation between channels is rho, the joint FPR for 3-of-4 is approximately: P(FP_joint) ~ C(4,3)*p^3*(1-p) * (1 + 3*rho*(1-p)/p) (first-order Bahadur approximation). For p=0.05 and rho=0.30: P(FP_joint) ~ 0.000481 * (1 + 3*0.30*0.95/0.05) = 0.000481 * (1 + 17.1) = 0.000481 * 18.1 = 0.0087 = 0.87%. This is approximately 18x worse than the independent case. For rho = 0.50: P(FP_joint) ~ 0.000481 * (1 + 3*0.50*0.95/0.05) = 0.000481 * 29.5 = 0.014 = 1.4%.

**Detection Power Analysis:**

The 3-of-4 quorum requires at least 3 channels to independently detect the anomaly. If the true positive rate (sensitivity) of each channel is q, the joint detection probability under independence is: P(TP_joint) = C(4,3)*q^3*(1-q) + C(4,4)*q^4. For q=0.80: P(TP_joint) = 4*0.512*0.20 + 0.4096 = 0.4096 + 0.4096 = 0.8192, or 81.9%. For q=0.70: P(TP_joint) = 4*0.343*0.30 + 0.2401 = 0.4116 + 0.2401 = 0.6517, or 65.2%. The 3-of-4 quorum preserves most of the detection power when individual channels have high sensitivity but degrades significantly when individual channels have moderate sensitivity (below 0.70). The question of whether individual channels achieve >0.70 sensitivity is empirical and depends on the specific anomaly type.

**Optimality Of 3 Vs 2:**

The choice of k=3 (out of 4) is conservative. Comparing k=2 and k=3 under independence: At p=0.05: k=2 gives FPR = C(4,2)*0.0025*0.9025 + ... = 0.014 (1.4%); k=3 gives FPR = 0.048%. At q=0.80: k=2 gives TPR = 0.9728; k=3 gives TPR = 0.8192. The k=3 choice strongly favors specificity over sensitivity. This is appropriate if false positives are very costly (they are: false FLAGs lead to Citicate suspension per C17 Section 10.3) and false negatives are recoverable (they are: undetected anomalies may be caught in subsequent cycles or by Tier 3). The 3-of-4 threshold is therefore a defensible but not uniquely optimal choice. A Bayesian decision-theoretic analysis incorporating the relative costs of false positives and false negatives would determine the optimal k.

**Midas Augmentation:**

MIDAS (Microcluster-based Detector of Anomalies in Edge Streams; Bhatia et al. 2020) is a streaming edge anomaly detector that maintains count-min sketch structures to detect sudden bursts of edges. Its augmentation of PCM is well-motivated: PCM detects persistent anomalous correlation (slow onset), while MIDAS detects sudden correlated bursts (fast onset). The combination covers both temporal regimes. MIDAS has O(1) per-edge processing time and O(w*d) memory where w is sketch width and d is depth, making it compatible with the streaming computation model. The interaction between MIDAS detections and the PCM residual is unspecified: does a MIDAS alert on an edge automatically count as one 'channel' toward the quorum, or does it trigger a full 4-channel evaluation?

#### Key Risks

- Channel independence is violated. Under realistic positive correlation (rho=0.30-0.50), the joint FPR is 18x-30x worse than the independence calculation suggests, potentially reaching 1-2% per pair per cycle.
- The 3-of-4 quorum strongly favors specificity over sensitivity. If any individual channel has sensitivity below 0.70 for certain anomaly types, joint detection probability drops below 65%, creating blind spots.
- The choice of k=3 is defensible but not analytically justified. No cost-benefit analysis of false positive vs. false negative costs is presented to support 3 over 2.
- The interaction between MIDAS burst detection and the 4-channel PCM quorum is unspecified.
- Different anomaly types may trigger different channel subsets. A fixed k=3 threshold may be optimal for some anomaly types and suboptimal for others. Anomaly-type-specific thresholds would improve overall detection but add complexity.

#### Recommended Experiments

1. Estimate pairwise channel correlations from simulated or historical data. Compute the Bahadur-corrected joint FPR for 3-of-4 under estimated correlations. Determine if the corrected FPR is within acceptable bounds (< 1% per pair per cycle).
2. Compute ROC curves for each of the 4 channels independently against a suite of anomaly types (sudden coordination, gradual collusion, infrastructure-masked Sybil, economic manipulation). Determine per-channel sensitivity for each anomaly type.
3. Compare k=2 and k=3 quorum thresholds under a formal decision-theoretic framework with specified costs: C_FP (Citicate suspension of innocent agent) and C_FN (undetected anomalous behavior for one cycle). Determine the optimal k for the AAS cost structure.
4. Specify and test the MIDAS-PCM interaction: does MIDAS contribute to the quorum, or does it trigger an out-of-band evaluation? Measure the combined detection latency under burst anomalies.

---

### SA-5: Epidemiological Backward Tracing (Tier 3)

**Question:** Is overdispersion analysis valid for estimating operator control span? What sample sizes are needed?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Theoretical Basis:**

Overdispersion analysis tests whether a count variable (here: number of anomalous neighborhoods containing a particular source agent or operator) exhibits more variance than expected under a Poisson or binomial null model. If an agent appears in anomalous neighborhoods more often than expected by chance, this is evidence of a common cause. The technique is standard in epidemiology (Breslow 1984; Dean 1992) for identifying outbreak sources by detecting over-representation. The key statistic is the dispersion ratio: variance(count) / mean(count). Under Poisson, this equals 1. Overdispersion (ratio > 1) indicates clustering beyond what random variation explains. The negative binomial model is the standard parametric alternative for overdispersed count data, with the overdispersion parameter alpha characterizing the degree of clustering.

**Validity For Operator Mapping:**

The application to operator-agent mapping is conceptually sound: if an operator controls multiple agents, those agents will appear together in anomalous neighborhoods more frequently than chance predicts, producing overdispersion in the per-agent anomalous-neighborhood count. However, there are several caveats. (1) The null model must account for non-random agent placement. Agents are not randomly distributed across neighborhoods -- they are placed by spectral clustering based on interaction patterns. This means even honest agents may show non-Poisson neighborhood co-occurrence because spectral clustering creates non-random groupings. The null model must condition on the spectral clustering result, not assume uniform random placement. (2) The method detects co-occurrence in anomalous neighborhoods but cannot distinguish 'controlled by the same operator' from 'legitimately correlated because they share infrastructure or task domain.' This is a fundamental identifiability problem that overdispersion analysis alone cannot resolve.

**Sample Size Requirements:**

The power of overdispersion tests depends critically on the number of anomalous events available for analysis. The Fisher dispersion test has power approximately: 1 - beta ~ Phi(sqrt(n) * (alpha - 1) / (1 + alpha) - z_{1-alpha_test}) where n is the number of anomalous neighborhoods, alpha is the overdispersion parameter, and Phi is the normal CDF. For moderate overdispersion (alpha = 2, meaning variance is 2x the mean): n=10 gives power ~0.30 (insufficient); n=30 gives power ~0.65 (marginal); n=50 gives power ~0.85 (adequate); n=100 gives power ~0.97 (good). The specification states Tier 3 is 'rare' -- invoked only for confirmed Tier 2 anomalies. If Tier 2 confirmations are rare (say 5-10 per consolidation cycle at 1K agents), the sample size for overdispersion analysis will be insufficient. At 100K agents with more frequent anomalies, sample sizes may be adequate, but the specification does not analyze this scaling relationship.

**Confidence Score Calibration:**

The specification outputs 'candidate operator-agent mappings with confidence scores.' The calibration of these confidence scores is critical for downstream use (presumably by human investigators or governance processes). Overdispersion-derived p-values are notoriously sensitive to model specification: incorrect null models produce miscalibrated p-values. If the null model does not account for spectral clustering structure, the confidence scores will be overconfident (too many low-p-value false positives). Calibration requires either: (a) simulation-based null distributions (permutation tests), which are computationally expensive but correctly account for the spectral clustering structure; or (b) analytic null distributions conditioned on the clustering, which are hard to derive in closed form.

#### Key Risks

- Sample sizes for reliable overdispersion analysis may be unavailable when Tier 3 is invoked rarely. At fewer than 30 anomalous neighborhoods, power is below 65% and false negative rates are unacceptably high.
- The null model must condition on spectral clustering structure, not assume uniform random placement. Unconditional null models will produce miscalibrated confidence scores.
- Overdispersion analysis cannot distinguish 'same operator' from 'legitimately correlated' (shared infrastructure, task domain). This is a fundamental identifiability limitation.
- Confidence score calibration requires either expensive simulation-based null distributions or difficult-to-derive analytic conditionals.
- At the 'rare' invocation frequency specified, Tier 3 may not accumulate sufficient statistical evidence within a single consolidation cycle. Temporal aggregation across multiple cycles is needed but introduces latency.

#### Recommended Experiments

1. Simulate the Tier 3 pipeline at 1K, 10K, and 100K agents with known operator-agent mappings (ground truth). Measure the detection rate as a function of: (a) number of anomalous neighborhoods, (b) operator control span (2, 5, 10 controlled agents), (c) overdispersion test power. Determine the minimum number of Tier 2 confirmations needed for 80% detection power.
2. Compare unconditional Poisson null vs. conditional null (conditioned on spectral clustering) for overdispersion testing. Measure the false positive rate difference. If the unconditional null produces >2x the FPR, the conditional null is mandatory.
3. Implement permutation-based confidence score calibration and measure computational cost at 1K, 10K, 100K agents. Determine if simulation-based calibration is feasible within CONSOLIDATION_CYCLE time budget.
4. Test whether aggregating Tier 2 confirmations across multiple consolidation cycles improves Tier 3 power to acceptable levels. Measure the detection latency (in consolidation cycles) as a function of operator control span.

---

### SA-6: Scaling Analysis

**Question:** Verify claimed complexity bounds. Are there hidden quadratic terms?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Tier 1 Verification:**

Tier 1 claims O(1) per agent per epoch, O(V) total. The STA/LTA computation requires maintaining two running statistics (STA and LTA) per agent per metric. Each epoch, one new data point is incorporated (O(1) update) and the ratio is compared to a threshold (O(1) comparison). With D metrics per agent, the per-agent cost is O(D), which is O(1) when D is treated as a constant. Total: O(V * D) = O(V). VERIFIED. The claim holds if the feature dimensionality D does not grow with V, which is a reasonable assumption.

**Tier 2 Verification:**

Tier 2 claims O(V log V) amortized. This decomposes into several sub-operations: (a) Spectral clustering: computing the k smallest eigenvectors of the graph Laplacian costs O(V * k^2) using Lanczos iteration, where k = number of clusters ~ V / (2*log(V)). This gives O(V * (V / (2*log(V)))^2) = O(V^3 / log^2(V)), which is SUPER-QUADRATIC for large k. However, spectral clustering is performed at CONSOLIDATION_CYCLE cadence (36,000s) and is amortized over 600 SETTLEMENT_TICKs (36,000/60). The amortized per-tick cost is O(V^3 / (600 * log^2(V))). For V=100,000: V^3/log^2(V) ~ 10^15 / 289 ~ 3.5 * 10^12, amortized over 600 gives ~5.8 * 10^9 operations per tick. This is high but may be feasible with optimized sparse eigensolvers. PARTIALLY VERIFIED -- the amortized bound is not O(V log V) for the spectral clustering component; it is higher.

**Pcm Precomputation Hidden Quadratic:**

PCM precomputation requires estimating E[corr(a_i, a_j)] for all agent pairs that share at least one neighborhood. In the worst case (dense graph), this is O(V^2). With spectral clustering into ~V/(2*log(V)) neighborhoods of size ~2*log(V), the total number of within-neighborhood pairs is approximately V/(2*log(V)) * C(2*log(V), 2) = V/(2*log(V)) * (2*log(V))*(2*log(V)-1)/2 ~ V * log(V). This gives O(V * log(V)) pairs, each requiring O(K) covariate lookups where K=4 covariates. Total PCM precomputation: O(V * log(V) * K) = O(V * log(V)). VERIFIED under the assumption that neighborhoods are bounded at 2*log(V). However, cross-neighborhood pairs (agents in adjacent/overlapping neighborhoods) may need PCM estimates too if the monitoring extends beyond strictly within-neighborhood analysis. If cross-neighborhood pairs are included, the pair count depends on neighborhood connectivity and could approach O(V^2) in dense graphs.

**Midas Streaming Cost:**

MIDAS processes edge arrivals in O(1) per edge using count-min sketches. The total edges per epoch depends on the interaction rate. At V=100,000 with average degree d, there are O(V*d) edge events per epoch. If d ~ log(V), this is O(V * log(V)) per epoch. VERIFIED.

**Tier 3 Verification:**

Tier 3 is invoked rarely and operates on a small subset of agents (those appearing in confirmed Tier 2 anomalies). The backward tracing cost depends on the interaction history depth and the number of candidate agents. For H interactions per agent and C candidate agents: O(C * H). If C and H are small (C ~ 10-100, H ~ 100-1000), this is negligible. VERIFIED under the rare-invocation assumption.

**Overall Scaling Verdict:**

The claimed O(V log V) amortized for Tier 2 is approximately correct for the PCM and MIDAS components but UNDERCOUNTS the spectral clustering cost. The true amortized Tier 2 cost is dominated by spectral clustering at O(V^3 / (consolidation_cycle_ticks * log^2(V))). For V=100,000, this is a significant computational cost that should be explicitly acknowledged and bounded. Sparse eigensolvers (ARPACK, randomized SVD) can reduce the constant factor but not the asymptotic complexity. Alternative: use only the k smallest eigenvectors where k is a fixed constant (e.g., k=50) rather than k ~ V/(2*log(V)), reducing spectral clustering to O(V * k^2) = O(V) amortized.

#### Key Risks

- Spectral clustering cost is O(V * k^2) where k = number of clusters. If k scales as V/log(V), this is super-quadratic. The claimed O(V log V) bound does not account for this.
- PCM precomputation is O(V * log V) for within-neighborhood pairs but could approach O(V^2) if cross-neighborhood pairs are included.
- At V=100,000, the spectral clustering step within a single CONSOLIDATION_CYCLE may exceed practical time budgets unless sparse/approximate eigensolvers are used with a fixed-k cutoff.
- The amortization argument (divide by consolidation_cycle_ticks) reduces per-tick cost but does not eliminate the burst cost at each consolidation cycle boundary.

#### Recommended Experiments

1. Benchmark spectral clustering (Lanczos + k-means in spectral space) at V = 1K, 10K, 100K on realistic interaction graphs. Measure wall-clock time and determine if the CONSOLIDATION_CYCLE time budget (36,000s) is sufficient at each scale.
2. Compare fixed-k spectral clustering (k=20, 50, 100) vs. adaptive-k (k ~ V/log(V)) in terms of: (a) wall-clock time, (b) neighborhood quality (measured by modularity or conductance), (c) detection sensitivity. Determine the minimum fixed k that preserves detection quality.
3. Measure PCM precomputation time at each scale. Determine whether cross-neighborhood pairs need PCM estimates and, if so, the pair count scaling.
4. Profile the total Tier 2 computation at each CONSOLIDATION_CYCLE boundary. Identify the dominant cost component and determine if it fits within the time budget with available hardware.

---

### SA-7: Adversarial Robustness and Game-Theoretic Equilibrium

**Question:** What is the equilibrium between a rational attacker and this detection system? Are there dominant evasion strategies?

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Attacker Model:**

Consider a rational adversary controlling M agents within a platform of V total agents. The adversary's goal is to coordinate controlled agents' behavior (for collusion, Sybil governance manipulation, or economic extraction) while avoiding detection by the three-tier pipeline. The adversary observes: (a) the detection architecture (Kerckhoffs' principle -- assume the adversary knows the system design), (b) the current neighborhood partitioning (public information after spectral clustering), (c) the PCM covariate structure (public information since structural covariates are observable). The adversary does NOT observe: (d) specific STA/LTA thresholds or window lengths (private parameters), (e) PCM residual thresholds per channel (private parameters), (f) which agents are currently in WATCH status (private).

**Evasion Strategies:**

*Tier 1 Evasion:* Against Tier 1 STA/LTA: the adversary can gradually shift behavior to avoid triggering the adaptive baseline (boiling frog, discussed in SA-1). The cost is slow coordination buildup. Against the fixed baseline: the adversary must eventually deviate from registration-time behavior to coordinate, and large deviations will trigger. The adversary's optimal strategy is to change behavior as slowly as possible while still achieving coordination goals within a useful timeframe. This is a rate-limited evasion: the adversary trades coordination speed for detection avoidance.

*Tier 2 Evasion:* Against Tier 2 PCM: the adversary can attempt to make anomalous correlation appear as 'permitted' by manipulating structural covariates. If two controlled agents share infrastructure (high structural overlap), their correlation is partially explained by PCM, reducing the residual. The adversary's optimal strategy is to maximize structural overlap between controlled agents to maximize PCM's expected correlation estimate, thereby minimizing the residual. This is the 'hiding in plain sight' strategy: make anomalous coordination look like expected infrastructure-driven correlation. The limit of this strategy is that PCM explains only correlation attributable to known structural factors; novel coordination patterns that are not explained by any structural covariate will still produce large residuals.

*Tier 2 Quorum Evasion:* Against the 4-channel quorum: the adversary targets the weakest channel(s) for evasion. If only 2 of 4 channels can detect the adversary's coordination pattern, the 3-of-4 quorum is never met. The adversary's optimal strategy is to identify which 2 channels are most susceptible to evasion and focus evasion effort there. Given the channels (verification co-occurrence, behavioral similarity, infrastructure fingerprint, economic activity), the most evadable channels are likely economic activity (can be obscured by routing through intermediary transactions) and verification co-occurrence (can be randomized). Behavioral similarity and infrastructure fingerprint are harder to evade (per C17 analysis). If the adversary can evade 2 channels, the 3-of-4 quorum creates a detection gap.

*Spectral Clustering Manipulation:* Against neighborhood partitioning: the adversary can manipulate the interaction graph to influence spectral clustering (discussed in SA-3). The optimal strategy is diffusion: spread controlled agents across many neighborhoods to keep per-neighborhood anomaly counts below the quorum threshold in each.

*Tier 3 Evasion:* Against Tier 3 overdispersion analysis: the adversary must avoid having controlled agents co-occur in anomalous neighborhoods disproportionately. The optimal strategy is to ensure that controlled agents' neighborhoods are anomalous at the same rate as the platform average, which requires either: (a) operating at sufficiently low coordination intensity that Tier 2 rarely flags the controlled agents' neighborhoods, or (b) creating diversionary anomalies in neighborhoods not containing controlled agents.


**Equilibrium Analysis:**

The detection system forces the adversary into a multi-constraint optimization: (a) evade Tier 1 by limiting behavioral change rate, (b) maximize structural overlap to minimize PCM residuals, (c) evade at least 2 of 4 quorum channels, (d) diffuse across neighborhoods to avoid Tier 3 overdispersion. These constraints are partially contradictory: maximizing structural overlap (b) concentrates controlled agents (bad for (d)), and limiting change rate (a) slows coordination (bad for the adversary's utility). The Nash equilibrium depends on the adversary's utility function (coordination benefit per epoch) and the detection cost function (probability of detection per epoch as a function of coordination intensity). Under reasonable assumptions (linear coordination benefit, sigmoidal detection probability), the equilibrium has the adversary operating at moderate coordination intensity -- below the STA/LTA trigger threshold, above zero -- extracting sublinear utility. The detection system does not eliminate the adversary but imposes a coordination tax that reduces the adversary's payoff.

**Dominant Strategy Assessment:**

There is no single dominant evasion strategy because the three tiers create complementary constraints. However, the combination of 'gradual behavioral shift + structural overlap maximization + 2-channel evasion targeting + neighborhood diffusion' constitutes a near-dominant composite strategy that is difficult to defend against without either: (a) lowering the quorum from 3-of-4 to 2-of-4 (increasing FPR), or (b) adding a 5th channel that is orthogonal to existing channels, or (c) implementing cross-neighborhood correlation analysis that detects diffused coordination patterns.

#### Key Risks

- The 'hiding in plain sight' strategy (maximizing structural overlap to inflate PCM expected correlation) is effective against Tier 2 and has no obvious counter within the current design.
- A 2-channel evasion strategy against the 3-of-4 quorum creates a permanent detection gap for adversaries who can reliably evade 2 specific channels.
- The diffusion attack against spectral clustering (spreading controlled agents across many neighborhoods) directly counteracts Tier 3 overdispersion analysis.
- The composite evasion strategy (gradual shift + structural overlap + 2-channel evasion + diffusion) is near-dominant and imposes only moderate cost on the adversary.
- No cross-neighborhood correlation mechanism exists in the current design to detect diffused coordination patterns.

#### Recommended Experiments

1. Implement a red-team simulation with an adversary pursuing the composite evasion strategy. Measure detection rate and detection latency across 100 consolidation cycles at 10K agents. Determine the adversary's effective coordination tax (utility reduction vs. unconstrained coordination).
2. Evaluate a 5th detection channel (candidate: temporal trajectory divergence from C19, or CACT commitment pattern analysis from C11) for orthogonality to existing 4 channels. Measure the joint detection rate under 2-channel evasion with and without the 5th channel.
3. Implement cross-neighborhood correlation analysis: track whether agents in different neighborhoods show correlated anomalous behavior that would not be visible within any single neighborhood. Measure detection rate for the diffusion attack.
4. Compute the Nash equilibrium numerically for a parametric game with adversary utility = coordination_intensity * benefit_per_epoch - detection_probability * penalty. Determine how detection sensitivity and penalty magnitude affect the equilibrium coordination intensity.

---

### SA-8: Overall Scientific Soundness

**Question:** Rate overall scientific soundness 1-5 with explanation.

**Soundness Verdict:** `PARTIALLY_SOUND`

#### Detailed Analysis

**Score:** 3.5/5

**Explanation:**

C34 is a well-designed hierarchical detection architecture that draws appropriately from established scientific domains: seismological STA/LTA detection (Allen 1978, Withers et al. 1998), Generalized Additive Models for expected correlation (Hastie & Tibshirani 1990), spectral graph partitioning (Shi & Malik 2000, von Luxburg 2007), MIDAS streaming anomaly detection (Bhatia et al. 2020), and epidemiological overdispersion analysis (Breslow 1984). Each component has genuine theoretical grounding and the compositions are architecturally natural.

**Strengths:**

- The three-tier hierarchical design (local -> regional -> global) is the correct architecture for scaling anomaly detection. Each tier has a clear role and the information flow (Tier 1 local alerts feed Tier 2 correlation analysis, which feeds Tier 3 causal tracing) is well-motivated.
- STA/LTA ratio detection is a mature, well-characterized technique with decades of operational validation in seismology. The adaptation to agent behavioral metrics is a natural and sound analogy.
- The PCM concept -- modeling expected correlation as a function of structural covariates and detecting anomalies via residuals -- is statistically principled. It addresses the fundamental problem that some inter-agent correlation is normal and expected, which pure correlation thresholds cannot handle.
- The 4-channel quorum provides strong FPR control under the independence assumption and reasonable FPR control even under moderate correlation.
- Integrating C17 B(a_i,a_j) as one of the four channels leverages existing AAS infrastructure effectively. The behavioral similarity function provides a well-specified, independently-validated input to the detection pipeline.
- MIDAS augmentation for burst detection complements the PCM's steady-state residual analysis, covering two distinct temporal anomaly regimes.
- The O(V) Tier 1 and approximately O(V log V) amortized Tier 2 scaling is appropriate for the 1K-100K target range.
- Emitting both raw and residual values for auditability is a sound engineering practice that supports Constitutional Tribunal adjudication.

**Weaknesses:**

- The dual-baseline decision fusion rule is unspecified, leaving a critical detection theory parameter undetermined.
- The PCM additivity assumption is likely violated due to structural covariate interactions (infrastructure x model lineage), and the function class of f_k is unspecified.
- The 3-of-4 quorum threshold is defensible but not analytically justified via decision theory. Channel correlation is not accounted for.
- Spectral clustering is vulnerable to adversarial graph manipulation (fragmentation, diffusion, bridge manipulation) and the split-on-overflow policy is unspecified.
- Tier 3 overdispersion analysis requires sample sizes (30+ anomalous neighborhoods) that may not be available under the 'rare invocation' design, creating a power gap at small scale.
- The spectral clustering complexity is under-reported: the true cost is super-quadratic when k scales with V, not O(V log V) as claimed.
- The composite evasion strategy (gradual shift + structural overlap + 2-channel evasion + diffusion) is near-dominant and not adequately countered by the current design.
- No cross-neighborhood correlation mechanism exists to detect the diffusion attack, which is the most concerning adversarial strategy.

**Comparison to Prior Art:**

The closest prior art is the Sentinel Graph in C10 (infrastructure fingerprinting, behavioral clustering) which C34 extends. C34's PCM residual analysis is a genuine advance over C10's raw correlation thresholds because it accounts for expected structural correlation. The integration of STA/LTA from seismology is a novel cross-domain transfer that is well-adapted to the agent monitoring use case. The 4-channel quorum draws on multi-sensor fusion literature (Durrant-Whyte & Henderson 2008). MIDAS (Bhatia et al. 2020) is recent (published 2020) and appropriate for the streaming edge detection use case. Overall, C34 represents a meaningful scientific advance over C10's detection capabilities while inheriting some of C10's architectural limitations (single-neighborhood focus, no cross-neighborhood correlation analysis).

---

## 3. Cross-Assessment Interactions

### XI-1: SA-1 + SA-7

**Components:** SA-1, SA-7

Tier 1 boiling-frog evasion and Tier 2 structural-overlap maximization are synergistic for the adversary. An adversary who gradually shifts behavior (evading Tier 1) while maximizing structural overlap (hiding Tier 2 residuals) faces the weakest possible combined detection. The two tiers do not cross-reinforce against this composite strategy because Tier 1 never fires (gradual shift) and Tier 2's PCM explains the correlation (structural overlap). Only the 4-channel quorum's non-PCM channels (raw behavioral similarity, MIDAS burst) might catch this, but only if coordination produces non-structural correlation signatures.

### XI-2: SA-3 + SA-5

**Components:** SA-3, SA-5

Adversarial manipulation of spectral clustering (SA-3 diffusion attack) directly undermines Tier 3 overdispersion analysis (SA-5). If controlled agents are successfully diffused across many neighborhoods, the per-agent anomalous-neighborhood count follows a Poisson distribution (no overdispersion) even though coordination is occurring. The two components are coupled: if SA-3 is compromised, SA-5 loses its statistical basis.

### XI-3: SA-2 + SA-4

**Components:** SA-2, SA-4

PCM multicollinearity (SA-2) and channel correlation (SA-4) share a common root cause: the structural covariates that PCM uses to estimate expected correlation are the same covariates that drive channel correlation. If infrastructure overlap drives both high PCM expected correlation (reducing residuals) and positive correlation between the infrastructure and behavioral channels (inflating joint FPR), the combined effect is: real anomalies in high-overlap pairs are under-detected (PCM absorbs the signal) while false alarms in low-overlap pairs are over-detected (correlated channels amplify noise).

### XI-4: SA-6 + SA-3

**Components:** SA-6, SA-3

The spectral clustering complexity (SA-6 finding: super-quadratic when k ~ V/log(V)) is driven by the neighborhood size cap (SA-3: 2*log(V)). If the cap is relaxed to allow larger neighborhoods (reducing k), spectral clustering becomes cheaper but detection sensitivity decreases (larger neighborhoods dilute per-neighborhood anomaly signals). This is a fundamental tradeoff between computational cost and detection quality that should be explicitly parameterized.

---

## 4. Integration with Existing Specifications

### C17 --- Behavioral Similarity (MCSD Layer 2)

**Compatibility:** `HIGH`

C17 B(a_i,a_j) is consumed as one of four Tier 2 channels. The interface is clean: B(a_i,a_j) produces a continuous score in [0,1] that C34 thresholds for anomaly detection. C17's graduated response (CLEAR/WATCH/FLAG) aligns with C34's per-channel binary anomaly decision. C17's LSH pre-filtering operates independently of C34's spectral clustering, which is appropriate since they serve different purposes (C17 LSH finds similar pairs; C34 spectral clustering groups correlated agents). One potential tension: C17's threshold theta_B (0.70-0.75) and C34's per-channel anomaly threshold on the B channel should be co-calibrated to avoid either redundant detection or detection gaps.

### C12 --- AVAP (Collusion Defense)

**Compatibility:** `MEDIUM`

C34 and C12 operate in partially overlapping domains. C12 AVAP detects collusion in verification committees; C34 detects anomalous inter-agent correlation more broadly. The two systems share one conceptual input (behavioral similarity from C17) but operate on different temporal and spatial scales. C12 operates per-committee per-verification; C34 operates per-neighborhood per-consolidation-cycle. No conflict exists, but the interaction between C12 M5 (conditional behavioral analysis, pairwise mutual information) and C34 Tier 2 (PCM residual analysis) should be coordinated to avoid double-counting the same behavioral signal.

### C9 --- Temporal Hierarchy (Cross-Layer Reconciliation)

**Compatibility:** `HIGH`

C34 aligns with the C9 canonical three-tier epoch hierarchy: Tier 1 operates at SETTLEMENT_TICK cadence (60s), Tier 2 aggregates at CONSOLIDATION_CYCLE cadence (36,000s) for spectral clustering and PCM refresh, and Tier 3 operates across multiple consolidation cycles. This is consistent with C9's temporal authority hierarchy.

### C3 --- Tidal Noosphere

**Compatibility:** `MEDIUM`

C34's spectral clustering partitions the interaction graph independently of C3's parcel model. Neighborhoods and parcels are different partitionings of the same agent population, which could cause confusion. C3 parcels are coordination units (elastic, topology-driven); C34 neighborhoods are detection units (correlation-driven). The two partitionings may overlap significantly but are not identical. This dual-partitioning adds cognitive and computational complexity. Consider whether C34 neighborhoods should be aligned with C3 parcels (using parcel boundaries as neighborhood boundaries) or deliberately kept independent (for detection diversity).

---

## 5. Proposed Experiments

| ID | Title | Priority | Addresses |
|---|---|---|---|
| EXP-1 | Dual-Baseline Decision Fusion ROC Analysis | HIGH | SA-1 |
| EXP-2 | PCM Interaction Terms and Heteroscedasticity | HIGH | SA-2 |
| EXP-3 | Adversarial Spectral Clustering Robustness | HIGH | SA-3, SA-7 |
| EXP-4 | Channel Correlation Estimation and Quorum Calibration | MEDIUM | SA-4 |
| EXP-5 | Tier 3 Statistical Power Analysis | MEDIUM | SA-5 |
| EXP-6 | Spectral Clustering Scalability Benchmark | HIGH | SA-6 |
| EXP-7 | Composite Evasion Red-Team Simulation | HIGH | SA-7, XI-1, XI-2 |
| EXP-8 | Cross-Neighborhood Correlation Detection Prototype | HIGH | SA-7, XI-2 |

### EXP-1: Dual-Baseline Decision Fusion ROC Analysis

**Priority:** `HIGH`

**Addresses:** SA-1

Measure ROC curves for four fusion rules (OR, AND, weighted, sequential) across three anomaly types (sudden shift, gradual drift, intermittent deviation). Determine optimal fusion rule for the AAS threat model.

### EXP-2: PCM Interaction Terms and Heteroscedasticity

**Priority:** `HIGH`

**Addresses:** SA-2

Fit additive GAM and GAM-with-interactions to simulated agent correlation data. Test for heteroscedasticity. Determine if the additive model is materially misspecified.

### EXP-3: Adversarial Spectral Clustering Robustness

**Priority:** `HIGH`

**Addresses:** SA-3, SA-7

Simulate fragmentation and diffusion attacks at 5%, 10%, 20% adversary control. Measure detection rate change. Compare spectral clustering to Louvain and label propagation.

### EXP-4: Channel Correlation Estimation and Quorum Calibration

**Priority:** `MEDIUM`

**Addresses:** SA-4

Estimate pairwise channel correlations from simulated data. Compute Bahadur-corrected joint FPR. Compare k=2 and k=3 under decision-theoretic framework with AAS-specific costs.

### EXP-5: Tier 3 Statistical Power Analysis

**Priority:** `MEDIUM`

**Addresses:** SA-5

Simulate overdispersion analysis at 1K, 10K, 100K agents with known ground truth. Determine minimum Tier 2 confirmations needed for 80% detection power across operator control spans 2-10.

### EXP-6: Spectral Clustering Scalability Benchmark

**Priority:** `HIGH`

**Addresses:** SA-6

Benchmark spectral clustering wall-clock time at V = 1K, 10K, 100K with fixed-k and adaptive-k. Determine if CONSOLIDATION_CYCLE time budget is sufficient.

### EXP-7: Composite Evasion Red-Team Simulation

**Priority:** `HIGH`

**Addresses:** SA-7, XI-1, XI-2

Implement the composite evasion strategy (gradual shift + structural overlap + 2-channel evasion + diffusion) and measure detection rate and coordination tax across 100 consolidation cycles.

### EXP-8: Cross-Neighborhood Correlation Detection Prototype

**Priority:** `HIGH`

**Addresses:** SA-7, XI-2

Design and test a cross-neighborhood correlation mechanism that detects coordinated behavior diffused across multiple neighborhoods. Measure detection rate for the diffusion attack.

---

## 6. Overall Verdict

| Metric | Score | Scale |
|---|---|---|
| Scientific Soundness | **3.5** | 1-5 |
| Integration Coherence | **3.5** | 1-5 |

### Summary

C34 is a scientifically grounded hierarchical detection architecture that makes appropriate use of established techniques (STA/LTA, GAM, spectral clustering, MIDAS, overdispersion analysis). The three-tier design is architecturally sound and the scaling target (1K-100K) is achievable with the stated algorithms, subject to the spectral clustering complexity caveat. The primary scientific gaps are: (1) unspecified decision fusion for dual baselines, (2) PCM additivity assumption likely violated, (3) quorum threshold not analytically justified under channel correlation, (4) Tier 3 power insufficient at small scale, (5) spectral clustering complexity under-reported, (6) no defense against the composite evasion strategy combining gradual shift, structural overlap maximization, 2-channel evasion, and neighborhood diffusion. The most concerning gap is the composite evasion strategy (SA-7, XI-1, XI-2), which exploits the lack of cross-neighborhood correlation analysis. None of these gaps are fundamental -- all are addressable through the recommended experiments and design refinements.

---

## 7. Sources Consulted

1. Allen 1978 (STA/LTA ratio, seismic event detection)
2. Withers et al. 1998 (comparison of STA/LTA algorithms)
3. Kay 1998 (Statistical Signal Processing: Detection Theory)
4. Denning 1987 (An Intrusion Detection Model -- dual profile baselines)
5. Hastie & Tibshirani 1990 (Generalized Additive Models)
6. Shi & Malik 2000 (Normalized Cuts and Image Segmentation -- spectral clustering)
7. von Luxburg 2007 (Tutorial on Spectral Clustering)
8. Bojchevski & Gunnemann 2019 (Adversarial Attacks on Node Embeddings via Graph Poisoning)
9. Rohe et al. 2011 (Spectral clustering consistency under stochastic block models)
10. Bhatia et al. 2020 (MIDAS: Microcluster-Based Detector of Anomalies in Edge Streams)
11. Breslow 1984 (Extra-Poisson variation in log-linear models -- overdispersion)
12. Dean 1992 (Testing for overdispersion in Poisson and binomial regression models)
13. Durrant-Whyte & Henderson 2008 (Multi-sensor data fusion)
14. Karger et al. 1997 (Consistent hashing)
15. Spielman 2012 (Spectral graph theory -- spectral gap robustness)
16. Chen et al. 2017 (Adversarial perturbation of spectral clustering)
17. C17 MASTER_TECH_SPEC v1.0 (B(a_i,a_j) behavioral similarity algorithm)
18. C12 MASTER_TECH_SPEC v1.0 (AVAP anti-collusion architecture)
19. C9 MASTER_TECH_SPEC v2.0 (Cross-layer reconciliation -- temporal hierarchy)
20. C3 Science Assessment (spectral gap, VRF post-filter, hash ring analysis)
