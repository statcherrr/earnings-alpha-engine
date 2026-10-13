"""Command-line interface for Earnings Alpha Engine.

Phase 1 provides status introspection only. No research functionality is
exposed yet; planned modules are listed explicitly as planned.
"""

from __future__ import annotations

import argparse

from earnings_alpha import __version__

CURRENT_PHASE = "Phase 1 — Project Foundation"

# (name, status, description). Status is "implemented" or "planned".
RESEARCH_MODULES: list[tuple[str, str, str]] = [
    ("config", "implemented", "Environment-based configuration loading."),
    ("cli", "implemented", "Project status command-line interface."),
    ("transcript_ingestion", "planned", "Earnings-call transcript acquisition and parsing."),
    ("market_data", "planned", "Price/volume data download and alignment."),
    ("linguistic_features", "planned", "Sentiment, uncertainty, and readability features."),
    ("event_study", "planned", "Post-earnings abnormal-return estimation."),
    ("signal_evaluation", "planned", "Predictive-signal testing with rigorous backtesting."),
]


def _module_lines() -> list[str]:
    width = max(len(name) for name, _, _ in RESEARCH_MODULES)
    return [
        f"  {name.ljust(width)}  [{status.upper()}]  {description}"
        for name, status, description in RESEARCH_MODULES
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="earnings-alpha",
        description="Earnings Alpha Engine — quantitative financial research platform.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the project name and version, then exit.",
    )
    parser.add_argument(
        "--phase",
        action="store_true",
        help="Print the current implementation phase, then exit.",
    )
    parser.add_argument(
        "--modules",
        action="store_true",
        help="List research modules and whether each is implemented or planned.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.version:
        print(f"earnings-alpha {__version__}")
        return 0

    if args.phase:
        print(CURRENT_PHASE)
        return 0

    if args.modules:
        print("Research modules:")
        for line in _module_lines():
            print(line)
        return 0

    # Default: overview.
    print("Earnings Alpha Engine")
    print(f"Version:          {__version__}")
    print(f"Current phase:    {CURRENT_PHASE}")
    print()
    print("Research modules:")
    for line in _module_lines():
        print(line)
    print()
    print("Note: modules marked PLANNED are not implemented yet. No ingestion,")
    print("NLP, signal generation, or backtesting functionality currently works.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
