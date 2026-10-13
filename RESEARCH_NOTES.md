# Research Notes

Working log of hypotheses, assumptions, decisions, and findings for
Earnings Alpha Engine.

> **Nothing in this file is an established finding.** The items under
> "Hypotheses" are open questions this project will test. As of Phase 1, no
> data has been ingested and no analysis has been run.

## Research questions (hypotheses to test)

1. **Sentiment changes.** Do quarter-over-quarter changes in management
   sentiment predict post-earnings abnormal returns?
2. **Linguistic uncertainty.** Does increasing linguistic uncertainty in
   management commentary carry information about future returns?
3. **Incremental value.** Do linguistic features add predictive value beyond
   earnings surprises (e.g., SUE, revenue surprise)?
4. **Heterogeneity.** Do these relationships differ across industries and
   market regimes (e.g., high- vs. low-volatility periods)?

These are hypotheses to test, not established conclusions. Any future finding
must survive the safeguards in
[docs/research_methodology.md](docs/research_methodology.md) before being
reported.

## Key assumptions (to be validated)

- Transcripts accurately reflect the call as delivered and are available
  without look-ahead relative to the analysis window.
- Market data can be aligned to announcement timestamps with sufficient
  precision to define event windows.
- Benchmark models for abnormal returns (market model, factor models) are
  specified before inspecting results, not tuned post hoc.

## Decisions log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-10-13 | Phase 1 delivers foundation only (config, CLI, docs, tests) | Establish reproducible, reviewable scaffolding before any research code. |
| 2026-10-13 | Python 3.11+, pandas/numpy/scipy/statsmodels | Standard, well-audited scientific stack; avoids niche dependencies. |
| 2026-10-13 | Configuration via environment variables with `.env` support | Keeps secrets out of code and Git. |
| 2026-10-13 | Data directories git-ignored; only `.gitkeep` tracked | Raw/processed data is private or licensed; repo stays clean. |

## Findings

_None yet. This section will record validated results, with the exact
commands and data versions needed to reproduce them._

## Open questions for future phases

- Which transcript source(s) offer reliable point-in-time availability?
- Minimum acceptable sample size per industry/regime cell?
- Choice of uncertainty lexicon vs. learned embeddings (trade-off:
  interpretability vs. flexibility)?
