# C43 Simplification Report

## Simplest version that preserves the claim

The core invention survives if `C43` keeps only:

1. signed bridge-scoped inventory snapshots
2. pinned translation identity for invocation
3. source-observed vs bridge-inferred semantic separation
4. explicit bridge posture on every bridged result

## What can be reduced

### Optional advanced bridge state
- warm-state reuse can be profile-gated rather than mandatory
- only snapshot cache and translation-policy reuse are essential

### Derated continuation handles
- these are valuable, but not required for the core claim
- the invention still stands without them as long as the bridge honesty model is
  preserved

### Rich bridge-side optimization
- no need for quasi-native session orchestration
- no need for bridge-managed execution priming

## What must remain

- signed translated state
- explicit custody boundary
- bridge trust ceiling
- bounded semantic enrichment

## Simplification verdict

`C43` remains valid if it is kept as a custody-bound bridge rather than a rich
bridge-resident execution environment.
