# Research Methodology and Integrity Safeguards

This document states the methodological standards for Earnings Alpha Engine.
As of Phase 1 these are **plans and commitments**, not results.

## Hypotheses under investigation

1. Quarter-over-quarter changes in management sentiment predict
   post-earnings abnormal returns.
2. Increasing linguistic uncertainty carries information about future
   returns.
3. Linguistic features add predictive value beyond earnings surprises.
4. Relationships differ across industries and market regimes.

These are hypotheses to test, not established conclusions.

## Planned safeguards

### Look-ahead bias

- All features computed using only information available at the simulated
  decision timestamp (transcript availability time, not just call date).
- Point-in-time universe membership; as-of joins for all reference data.
- Automated checks that feature timestamps precede return windows.

### Survivorship bias

- Universe constructed from point-in-time constituents, including firms that
  were later delisted, acquired, or went bankrupt.
- Delisting returns incorporated where available rather than dropped.

### Data leakage

- Strict separation of training and evaluation periods.
- Any learned transformation (scaling, PCA, vocabulary) fit on training data
  only.
- No use of restated financials unless the restatement date is respected.

### Multiple testing

- Hypotheses and primary specifications registered in RESEARCH_NOTES.md
  before running tests.
- Multiple-comparison corrections (e.g., Bonferroni, Benjamini–Hochberg)
  applied across families of tests.
- Full reporting of null results, not only significant ones.

### Transaction costs and implementability

- Portfolio simulations include configurable transaction costs and
  turnover constraints.
- Signals evaluated net of costs; capacity considerations documented.
- No assumption of instant fills at closing prices without justification.

### Insufficient sample sizes

- Minimum sample-size thresholds defined per test before analysis.
- Results reported with confidence intervals, not just point estimates.
- Industry/regime subgroup analyses pre-specified to avoid data-mined
  splits.

## Reproducibility requirements

- Fixed random seeds (see `EARNINGS_ALPHA_RANDOM_SEED`).
- Pinned dependency versions.
- Every reported result accompanied by the exact commands, data versions,
  and code revision used to produce it.
- No fabricated data, simulated results presented as real, or performance
  metrics that were not computed from actual data.
