# Earnings Alpha Engine

A quantitative financial research platform investigating whether changes in
corporate earnings-call language contain predictive information about future
stock returns.

> **Status: Phase 1 — Project Foundation.** Only scaffolding, configuration,
> a status CLI, tests, and documentation exist. Transcript ingestion, NLP,
> event studies, signal generation, and backtesting are **not implemented**
> and produce no results yet.

## Research objective

The long-term goal is a reproducible research system that:

1. Ingests earnings-call transcripts and market data.
2. Engineers linguistic features (sentiment, uncertainty, readability).
3. Conducts event studies around earnings announcements.
4. Evaluates whether linguistic features predict post-earnings abnormal
   returns, using statistically rigorous backtesting.

The motivating hypotheses are documented in [RESEARCH_NOTES.md](RESEARCH_NOTES.md).
They are hypotheses to be tested — not established conclusions.

## Setup

Requires Python 3.11+.

```bash
# Create and activate a virtual environment
python3.11 -m venv .venv       # or: uv venv --python 3.11
source .venv/bin/activate

# Install the package with development tools
pip install -e ".[dev]"        # or: uv pip install -e ".[dev]"

# Optional: configure environment
cp .env.example .env           # edit with local values; never commit .env
```

## Usage

```bash
earnings-alpha               # overview: version, phase, modules
earnings-alpha --version     # project name and version
earnings-alpha --phase       # current implementation phase
earnings-alpha --modules     # research modules: implemented vs. planned
```

Example output of `earnings-alpha --modules`:

```
Research modules:
  config                [IMPLEMENTED]  Environment-based configuration loading.
  cli                   [IMPLEMENTED]  Project status command-line interface.
  transcript_ingestion  [PLANNED]  Earnings-call transcript acquisition and parsing.
  market_data           [PLANNED]  Price/volume data download and alignment.
  linguistic_features   [PLANNED]  Sentiment, uncertainty, and readability features.
  event_study           [PLANNED]  Post-earnings abnormal-return estimation.
  signal_evaluation     [PLANNED]  Predictive-signal testing with rigorous backtesting.
```

## Development

```bash
pytest                 # run the test suite
ruff check .           # lint
ruff format .          # format
```

## Project layout

```
src/earnings_alpha/    application package (config, cli)
tests/                 pytest test suite
docs/                  architecture and research methodology
scripts/               development utilities
data/raw/              raw data (git-ignored)
data/processed/        derived datasets (git-ignored)
data/market_data/      downloaded market data (git-ignored)
notebooks/             exploratory research
```

## Data and secrets policy

- `.env`, virtual environments, caches, downloaded datasets, and local
  databases are excluded from Git (see [.gitignore](.gitignore)).
- [.env.example](.env.example) documents placeholders only; no real
  credentials are committed or printed anywhere in this codebase.

## Documentation

- [ROADMAP.md](ROADMAP.md) — phased development plan
- [RESEARCH_NOTES.md](RESEARCH_NOTES.md) — hypotheses, assumptions, decisions
- [docs/architecture.md](docs/architecture.md) — system design
- [docs/research_methodology.md](docs/research_methodology.md) — planned
  methodology and research-integrity safeguards

## License

[MIT](LICENSE)
