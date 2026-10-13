# Architecture

## Overview

Earnings Alpha Engine is a single Python package (src layout) organized as a
data-research pipeline, not a service. Phase 1 ships only the foundation:
configuration and a status CLI. Each pipeline stage below is planned.

```
src/earnings_alpha/
├── __init__.py               # package metadata, version
├── config.py                 # environment-based Settings (implemented)
└── cli.py                    # status CLI (implemented)

Planned modules (not implemented):
├── ingestion/                # transcript acquisition and parsing
├── market/                   # price/volume download and alignment
├── features/                 # linguistic feature engineering
├── event_study/              # abnormal-return estimation
└── evaluation/               # predictive testing and backtesting
```

## Design principles

1. **Simple by default.** A plain Python package with a CLI; no
   microservices, message queues, or cloud infrastructure in this phase.
   SQLite can be introduced when persistence is actually needed.
2. **Point-in-time correctness.** Every pipeline stage must be computable
   using only data available at the simulated decision time. This shapes
   data schemas (timestamps everywhere) and API design (as-of joins).
3. **Reproducibility.** Pinned dependencies, fixed random seeds via
   configuration, deterministic pipeline ordering, and documented data
   versions.
4. **Testability.** Pure functions for transformations; I/O isolated at the
   edges so logic can be unit-tested without network or disk access.

## Configuration flow

```
.env (git-ignored) ──┐
                     ├──> load_settings() ──> Settings (frozen dataclass)
process env vars ────┘
```

- Real environment variables always override `.env`.
- `Settings` is immutable; secrets are excluded from `repr`/`str` and
  redacted in `.redacted()` for logging.
- Missing optional settings fall back to documented defaults so a fresh
  clone works with no configuration at all.

## Planned data flow

```
transcripts (raw) ──┐
                    ├──> clean/align ──> features ──> event study ──> evaluation
market data (raw) ──┘
```

Each arrow is a separate, tested module writing versioned outputs under
`data/processed/`, with provenance metadata recording inputs and parameters.
