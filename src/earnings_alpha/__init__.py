"""Earnings Alpha Engine — quantitative financial research platform.

Phase 1 status: project foundation only. No ingestion, NLP, signal
generation, or backtesting functionality is implemented yet.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("earnings-alpha")
except PackageNotFoundError:  # pragma: no cover - only when run from source w/o install
    __version__ = "0.0.0.dev0"

__all__ = ["__version__"]
