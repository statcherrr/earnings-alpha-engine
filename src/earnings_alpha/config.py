"""Environment-based configuration for Earnings Alpha Engine.

All settings are read from environment variables (optionally loaded from a
local ``.env`` file via python-dotenv). Secrets are never logged or printed;
callers receive redacted representations only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ENV_PREFIX = "EARNINGS_ALPHA_"

VALID_ENVIRONMENTS = ("development", "testing", "production")

DEFAULT_DATA_DIR = "data"
DEFAULT_RANDOM_SEED = 42


def _env(name: str, default: str | None = None) -> str | None:
    """Read an EARNINGS_ALPHA_-prefixed env var, falling back to ``default``."""
    return os.environ.get(ENV_PREFIX + name, default)


def _load_dotenv(project_root: Path | None = None) -> None:
    """Load a local ``.env`` file if present. Real env vars take precedence."""
    if project_root is None:
        load_dotenv(override=False)
    else:
        load_dotenv(project_root / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    """Immutable snapshot of application configuration.

    Attributes:
        environment: Runtime environment name (development/testing/production).
        data_dir: Root directory for raw, processed, and market data.
        random_seed: Seed for any stochastic procedure, for reproducibility.
        api_key: Optional data-provider API key. Never printed; redacted in
            repr and str output.
    """

    environment: str = "development"
    data_dir: Path = field(default_factory=lambda: Path(DEFAULT_DATA_DIR))
    random_seed: int = DEFAULT_RANDOM_SEED
    api_key: str | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self.environment not in VALID_ENVIRONMENTS:
            raise ValueError(
                f"Invalid environment {self.environment!r}; expected one of {VALID_ENVIRONMENTS}."
            )

    # -- Convenience paths -------------------------------------------------
    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def market_data_dir(self) -> Path:
        return self.data_dir / "market_data"

    def redacted(self) -> dict[str, object]:
        """Return a dict of settings safe for logging (secrets redacted)."""
        return {
            "environment": self.environment,
            "data_dir": str(self.data_dir),
            "random_seed": self.random_seed,
            "api_key": "***redacted***" if self.api_key else None,
        }


def load_settings(*, load_env_file: bool = True, project_root: Path | None = None) -> Settings:
    """Build :class:`Settings` from the environment.

    Missing optional variables fall back to documented defaults, so this
    never fails in a fresh checkout with no ``.env`` file.

    Args:
        load_env_file: If True, load a local ``.env`` file before reading
            variables. Existing environment variables always win.
        project_root: Optional directory containing ``.env``. Defaults to
            the process working directory.
    """
    if load_env_file:
        _load_dotenv(project_root)

    environment = _env("ENV", "development") or "development"
    data_dir = Path(_env("DATA_DIR", DEFAULT_DATA_DIR) or DEFAULT_DATA_DIR)

    seed_raw = _env("RANDOM_SEED")
    try:
        random_seed = int(seed_raw) if seed_raw else DEFAULT_RANDOM_SEED
    except ValueError as exc:
        raise ValueError(f"{ENV_PREFIX}RANDOM_SEED must be an integer, got {seed_raw!r}.") from exc

    api_key = _env("API_KEY")

    return Settings(
        environment=environment,
        data_dir=data_dir,
        random_seed=random_seed,
        api_key=api_key,
    )


__all__ = [
    "DEFAULT_DATA_DIR",
    "DEFAULT_RANDOM_SEED",
    "ENV_PREFIX",
    "VALID_ENVIRONMENTS",
    "Settings",
    "load_settings",
]
