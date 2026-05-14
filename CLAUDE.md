# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All tasks are run via [Task](https://taskfile.dev). Dependencies are managed with `uv`.

```sh
task install       # uv sync — install all dependencies
task format        # ruff format .
task lint          # ruff check . && mypy --strict -p semmy
task test          # runs lint then pytest
task build         # uv build
```

Run tests directly (skipping lint):

```sh
uv run pytest                          # all tests
uv run pytest tests/test_semmy.py      # single file
uv run pytest -k "test_name"           # single test by name
```

Mutation testing (runs on pre-push via lefthook):

```sh
uv run mutmut run
uv run mutmut results
```

## Architecture

The entire library lives in a single file: `semmy/__init__.py`.

**`Semver`** is a frozen dataclass with fields `major`, `minor`, `patch` (int), `pre_release`, `build` (str). Immutability is enforced by `frozen=True` — all bump methods return new instances rather than mutating.

Key design decisions:
- `__eq__` compares via `str(self) == str(other)`, so pre-release and build metadata are included in equality.
- Ordering operators (`>`, `<`, `>=`, `<=`) compare only `(major, minor, patch)` tuples — pre-release and build metadata do not affect ordering.
- `is_pre_release()` returns `True` if `pre_release` is set **or** `major == 0` (0.x versions are always pre-release per semver spec).
- `from_string()` uses the canonical regex from semver.org; raises `SemverException` on invalid input.

## Testing Conventions

Tests use `pytest` with `assertpy` for fluent assertions and `hypothesis` for property-based tests.

```python
from assertpy import assert_that
assert_that(str(Semver.from_string("1.2.3"))).is_equal_to("1.2.3")
```

Parametrize with `@pytest.mark.parametrize`. Test vectors for valid/invalid semver strings come from the semver.org spec — when adding new cases, follow that source.

Mypy runs in strict mode; all new code must pass `mypy --strict -p semmy` without ignores.

## Code Style

- Line length: 120 characters (black + ruff + flake8 all set to this)
- Ruff rule sets enabled: `E`, `W`, `F`, `I`, `B`, `C4`, `UP`, `RUF`
- Ruff per-file ignore: `tests/` ignores `S101` (assert statements are fine in tests)

## Release Process

Releases are automated via [Release Please](https://github.com/googleapis/release-please). Merging commits to `main` following [Conventional Commits](https://www.conventionalcommits.org/) will trigger a Release PR. Merging that PR publishes to PyPI via `uv publish` using `PYPI_API_TOKEN`.
