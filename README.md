<h1>🐊 Semmy</h1>

> [Semantic versioning](https://semver.org) made easy for Python.

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Install](#install)
* [Usage](#usage)
  * [Importing](#importing)
  * [Initializing a raw object](#initializing-a-raw-object)
  * [Initializing from string](#initializing-from-string)
  * [Exporting as tuple](#exporting-as-tuple)
  * [Validating input](#validating-input)
  * [Comparing versions](#comparing-versions)
  * [Bumping versions](#bumping-versions)
* [Contributing](#contributing)
* [Release Setup](#release-setup)

## Features

With `semmy` you can...

* Parse semantic version domain objects from valid strings
* Check if two versions are equal
* Check if version is greater (newer) or lesser (older) than other version
* Check if version is a pre-release
* Bump (pre-)major, (pre-)minor, and (pre-)patch versions

## Prerequisites

* **Python** >=3.8 or later

## Install

```sh
poetry add semmy
```

Alternatively, for older projects.

```sh
pip install semmy
pip freeze > requirements.txt
```

## Usage

Below are the most common use cases. Please, check [**the unit tests**](tests/test_semmy.py) for complete examples.

### Importing

```python
>>> from semmy import Semver
```

### Initializing a raw object

Plain objects are easy to initialize given three semantic version components.

```python
>>> Semver(1, 2, 3)
Version (1.2.3)
```

Keyword arguments are supported, too.

```python
>>> Semver(major=1, minor=2, patch=3)
Version (1.2.3)
```

Versions may contain pre-release tag and build number.

```python
>>> Semver(1, 0, 0, pre_release="rc-1")
Version (1.0.0-rc-1)

>>> Semver(1, 0, 0, build="6c231887917e472da7f299c934b20f29")
Version (1.0.0+6c231887917e472da7f299c934b20f29)
```

### Initializing from string

You can pass a string and have it transformed to a valid object.

```python
>>> Semver.from_string("1.0.0")
Version (1.0.0)
```

### Exporting as tuple

Versions can be exported as integer tuples.

```python
>>> Semver(1, 2, 3).as_tuple()
(1, 2, 3)
```

### Validating input

I recommend using `Semver.from_string()` whenever possible as it includes a strict input validation.

For invalid inputs, instance of `SemverException` is raised, which should be caught.

```python
>>> from semmy import Semver, SemverException
>>> try:
...     Semver.from_string("not-a-version")
... except SemverException as e:
...     print(e)
...
Version string not-a-version is not a valid semantic version
```

### Comparing versions

Two versions are ordered by comparing their major, minor, and patch numbers respectively.

```python
>>> Semver.from_string("1.2.3") == Semver(1, 2, 3)
True

>>> Semver.from_string("1.1.0") > Semver(1, 0, 0)
True

>>> Semver.from_string("0.9.0") < Semver(0, 9, 1)
True
```

You may also want to sort a list of versions where Python's tuple ordering is helpful.

```python
>>> versions: list[Semver] = [
...     Semver(1, 2, 3),
...     Semver(2, 0, 0),
...     Semver(0, 1, 0),
... ]
>>>
>>> sorted(versions, key=lambda v: v.as_tuple(), reverse=True)
[Version (2.0.0), Version (1.2.3), Version (0.1.0)]
```

### Bumping versions

Typically, you want to bump major version for breaking changes, minor version for new features, and patch version for new fixes. These are supported.

```python
>>> Semver(0, 1, 0).bump_major()
Version (1.0.0)

>>> Semver(1, 0, 0).bump_minor()
Version (1.1.0)

>>> Semver(1, 1, 0).bump_patch()
Version (1.1.1)
```

## Contributing

See [**here**](CONTRIBUTING.md) for instructions.

## Release Setup

This project uses automated releases with [Release Please](https://github.com/googleapis/release-please) and GitHub Actions.

### Required GitHub Repository Secrets

Before the release workflow can function properly, you need to configure the following secrets in your GitHub repository:

#### PYPI_API_TOKEN

**Purpose**: Authenticate with PyPI for publishing packages

**Setup Instructions**:

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Navigate to the "API tokens" section
3. Click "Add API token"
4. Set the token name (e.g., "semmy-github-actions")
5. Set the scope to "Entire account" or specific to the "semmy" project
6. Copy the generated token (it starts with `pypi-`)
7. Add it to your GitHub repository secrets as `PYPI_API_TOKEN`

**Alternative: PyPI Trusted Publishing** (Recommended)

Instead of using an API token, you can set up trusted publishing which is more secure:

1. Go to your project on PyPI: https://pypi.org/manage/project/semmy/
2. Navigate to "Publishing" → "Add a new pending publisher"
3. Fill in the details:
   - **Owner**: `nikoheikkila` (your GitHub username)
   - **Repository name**: `semmy`
   - **Workflow name**: `release.yml`
   - **Environment name**: Leave empty (unless you use environments)
4. Save the publisher

If you use trusted publishing, you can remove the `UV_PUBLISH_TOKEN` environment variable from the workflow.

### How the Release Process Works

#### 1. Release Please Phase

When you push commits to the `main` branch:

1. **Release Please** analyzes conventional commit messages since the last release
2. If release-worthy changes are found, it creates/updates a "Release PR"
3. The Release PR contains:
   - Updated version in `pyproject.toml`
   - Updated `CHANGELOG.md`
   - Any other version-related files

#### 2. Release Creation Phase

When you merge the Release PR:

1. **Release Please** creates a GitHub Release and Git tag
2. The workflow triggers the **Publish** job
3. The publish job:
   - Runs tests to ensure quality
   - Builds the package with `uv build`
   - Publishes to PyPI with `uv publish`
   - Creates a workflow summary

### Conventional Commit Types

The workflow recognizes these conventional commit types:

| Type | Description | Release Impact | Changelog Section |
|------|-------------|----------------|-------------------|
| `feat` | New feature | Minor version bump | ✨ Features |
| `fix` | Bug fix | Patch version bump | 🐛 Bug Fixes |
| `perf` | Performance improvement | Patch version bump | ⚡ Performance Improvements |
| `revert` | Revert previous change | Patch version bump | ⏪ Reverts |
| `docs` | Documentation changes | Patch version bump | 📚 Documentation |
| `style` | Code style changes | Patch version bump | 🎨 Styles |
| `refactor` | Code refactoring | Patch version bump | ♻️ Code Refactoring |
| `test` | Test changes | Patch version bump | ✅ Tests |
| `build` | Build system changes | Patch version bump | 👷 Build System |
| `ci` | CI configuration changes | Patch version bump | 💚 Continuous Integration |
| `chore` | Maintenance tasks | No release | (Hidden from changelog) |

#### Breaking Changes

To trigger a **major version bump**, use:

- `feat!:` or `fix!:` (with exclamation mark)
- Include `BREAKING CHANGE:` in the commit message body

### Example Commits

```bash
# Patch release (1.0.0 → 1.0.1)
git commit -m "fix: resolve null pointer exception in parser"

# Minor release (1.0.0 → 1.1.0) 
git commit -m "feat: add support for YAML configuration files"

# Major release (1.0.0 → 2.0.0)
git commit -m "feat!: remove deprecated API methods"

# Or with body:
git commit -m "feat: new API design

BREAKING CHANGE: The old API methods have been removed."
```

### Manual Release

If you need to create a release manually:

```bash
# Create a commit that bumps the version
git commit -m "chore(release): 1.2.3" --allow-empty

# Push to main
git push origin main
```

### Troubleshooting

#### Release PR not created

- Ensure your commits follow conventional commit format
- Check that you have release-worthy commit types (not just `chore`)
- Verify the workflow has proper permissions

#### PyPI publish fails

- Verify `PYPI_API_TOKEN` is correctly set
- Ensure the package name isn't already taken by another user
- Check that the version doesn't already exist on PyPI

#### Tests fail during release

- All tests must pass before publishing
- Fix the failing tests and push the fix to main
- The workflow will retry on the next push
