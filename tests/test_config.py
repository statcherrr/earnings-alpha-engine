"""Tests for environment-based configuration loading."""

import pytest

from earnings_alpha.config import (
    DEFAULT_DATA_DIR,
    DEFAULT_RANDOM_SEED,
    ENV_PREFIX,
    Settings,
    load_settings,
)


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure no EARNINGS_ALPHA_* vars leak in from the developer's shell."""
    import os

    for key in list(os.environ):
        if key.startswith(ENV_PREFIX):
            monkeypatch.delenv(key, raising=False)
    # Also prevent a local .env from affecting tests.
    monkeypatch.setattr("earnings_alpha.config._load_dotenv", lambda *a, **k: None)


def test_defaults_with_empty_environment() -> None:
    settings = load_settings(load_env_file=False)
    assert settings.environment == "development"
    assert str(settings.data_dir) == DEFAULT_DATA_DIR
    assert settings.random_seed == DEFAULT_RANDOM_SEED
    assert settings.api_key is None


def test_reads_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_PREFIX + "ENV", "testing")
    monkeypatch.setenv(ENV_PREFIX + "DATA_DIR", "/tmp/ea-data")
    monkeypatch.setenv(ENV_PREFIX + "RANDOM_SEED", "7")
    monkeypatch.setenv(ENV_PREFIX + "API_KEY", "super-secret-value")

    settings = load_settings(load_env_file=False)
    assert settings.environment == "testing"
    assert str(settings.data_dir) == "/tmp/ea-data"
    assert settings.random_seed == 7
    assert settings.api_key == "super-secret-value"


def test_missing_optional_settings_use_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_PREFIX + "ENV", "production")
    settings = load_settings(load_env_file=False)
    assert settings.environment == "production"
    assert settings.random_seed == DEFAULT_RANDOM_SEED
    assert settings.api_key is None


def test_invalid_environment_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_PREFIX + "ENV", "staging")
    with pytest.raises(ValueError, match="Invalid environment"):
        load_settings(load_env_file=False)


def test_invalid_seed_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENV_PREFIX + "RANDOM_SEED", "not-a-number")
    with pytest.raises(ValueError, match="RANDOM_SEED"):
        load_settings(load_env_file=False)


def test_api_key_never_appears_in_repr() -> None:
    secret = "super-secret-value"
    settings = Settings(api_key=secret)
    assert secret not in repr(settings)
    assert secret not in str(settings)


def test_redacted_hides_secret_but_shows_structure() -> None:
    settings = Settings(api_key="super-secret-value", random_seed=7)
    redacted = settings.redacted()
    assert redacted["api_key"] == "***redacted***"
    assert redacted["random_seed"] == 7
    assert "super-secret-value" not in str(redacted)


def test_derived_data_paths() -> None:
    settings = load_settings(load_env_file=False)
    assert settings.raw_data_dir == settings.data_dir / "raw"
    assert settings.processed_data_dir == settings.data_dir / "processed"
    assert settings.market_data_dir == settings.data_dir / "market_data"
