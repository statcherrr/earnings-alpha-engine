"""Tests for the command-line interface."""

import subprocess
import sys

import pytest

from earnings_alpha import __version__
from earnings_alpha.cli import CURRENT_PHASE, RESEARCH_MODULES, main


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--version"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "earnings-alpha" in captured.out
    assert __version__ in captured.out


def test_phase_flag(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--phase"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert CURRENT_PHASE in captured.out


def test_modules_flag_lists_all_modules(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--modules"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Research modules:" in captured.out
    for name, status, _ in RESEARCH_MODULES:
        assert name in captured.out
        assert f"[{status.upper()}]" in captured.out


def test_default_output_shows_overview(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Earnings Alpha Engine" in captured.out
    assert __version__ in captured.out
    assert CURRENT_PHASE in captured.out


def test_unimplemented_work_is_not_claimed(capsys: pytest.CaptureFixture[str]) -> None:
    """The CLI must not imply that ingestion/NLP/backtesting already works."""
    main([])
    out = capsys.readouterr().out.lower()
    assert "planned" in out
    assert "not implemented" in out


def test_module_statuses_are_valid() -> None:
    for name, status, description in RESEARCH_MODULES:
        assert status in {"implemented", "planned"}, name
        assert name and description


def test_console_script_entry_point() -> None:
    """The installed ``earnings-alpha`` script must run and exit cleanly."""
    result = subprocess.run(
        [sys.executable, "-m", "earnings_alpha.cli", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert __version__ in result.stdout
