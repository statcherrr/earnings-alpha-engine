# Roadmap

Phased development plan for Earnings Alpha Engine. Each phase delivers
testable, documented functionality. Later phases are plans, not commitments
to specific tools or vendors.

## Phase 1 — Project foundation (current) ✅

- Repository structure, packaging, and tooling (pytest, ruff)
- Environment-based configuration with secret hygiene
- Status CLI
- Documentation of hypotheses, methodology, and safeguards

## Phase 2 — Data acquisition

- Transcript ingestion pipeline (source to be chosen; licensing considered)
- Market data download (daily OHLCV at minimum)
- Point-in-time universe definition to avoid survivorship bias
- Raw/processed data schemas and provenance metadata

## Phase 3 — Linguistic feature engineering

- Sentiment, uncertainty, and readability features from transcripts
- Quarter-over-quarter change features
- Feature documentation with economic rationale for each
- Strict point-in-time computation (no look-ahead)

## Phase 4 — Event study

- Earnings-announcement event windows
- Market- and size/BTM-matched benchmark models for abnormal returns
- Statistical tests of abnormal-return distributions

## Phase 5 — Signal evaluation and backtesting

- Predictive regressions controlling for earnings surprises
- Walk-forward / out-of-sample evaluation
- Multiple-testing corrections (e.g., Bonferroni, Benjamini–Hochberg)
- Transaction-cost-aware portfolio simulations
- Industry and market-regime heterogeneity analysis

## Cross-cutting concerns (all phases)

- Reproducibility: pinned dependencies, fixed seeds, deterministic pipelines
- Research integrity: safeguards documented in
  [docs/research_methodology.md](docs/research_methodology.md)
- Testing: unit tests for every implemented module
- Documentation: update README status and RESEARCH_NOTES findings each phase
