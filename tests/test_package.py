"""Tests for package importability and metadata."""


def test_package_imports() -> None:
    import earnings_alpha
    import earnings_alpha.cli
    import earnings_alpha.config

    assert earnings_alpha.__version__


def test_version_matches_metadata() -> None:
    from importlib.metadata import version

    from earnings_alpha import __version__

    assert __version__ == version("earnings-alpha")
