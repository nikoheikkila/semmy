<h1>🐊 Semmy</h1>

> Semantic versioning made easy for Python.

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

Semver(1, 0, 0).bump_minor()
Version (1.1.0)

Semver(1, 1, 0).bump_patch()
Version (1.1.1)
```

## Contributing

See [**here**](CONTRIBUTING.md) for instructions.
