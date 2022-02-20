# -*- coding: utf-8 -*-
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Tuple

# See: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEMVER_REGEX = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
    re.MULTILINE,
)


class SemverException(Exception):
    """Raised for invalid semantic version numbers"""

    pass


@dataclass(frozen=True)  # pragma: no mutate
class Semver:
    major: int = 0
    minor: int = 1
    patch: int = 0
    pre_release: str = ""
    build: str = ""

    @classmethod
    def from_string(cls, version: str) -> Semver:
        """Parses a new semantic version object from input string

        Raises
            SemverException: for invalid input
        """
        if not SEMVER_REGEX.fullmatch(version):
            raise SemverException(f"Version string {version} is not a valid semantic version")

        major, minor, patch, pre_release, build = SEMVER_REGEX.findall(version).pop()

        return Semver(int(major), int(minor), int(patch), pre_release, build)

    def as_tuple(self) -> Tuple[int, int, int]:
        """Exports version as integer tuple"""
        return (self.major, self.minor, self.patch)

    def is_pre_release(self) -> bool:
        """Checks whether the version is considered pre-release"""
        if self.pre_release:
            return True

        return self.major == 0

    def bump_major(self, **kwargs: str) -> Semver:
        """Bumps the major version component"""
        return Semver(major=self.major + 1, minor=0, patch=0, **kwargs)

    def bump_premajor(self, metadata: str = "rc-1") -> Semver:
        """Bumps the major version component and adds pre-release tag"""
        return self.bump_major(pre_release=metadata)

    def bump_minor(self, **kwargs: str) -> Semver:
        """Bumps the minor version component"""
        return Semver(major=self.major, minor=self.minor + 1, patch=0, **kwargs)

    def bump_preminor(self, metadata: str = "rc-1") -> Semver:
        """Bumps the minor version component and adds pre-release tag"""
        return self.bump_minor(pre_release=metadata)

    def bump_patch(self, **kwargs: str) -> Semver:
        """Bumps the patch version component"""
        return Semver(major=self.major, minor=self.minor, patch=self.patch + 1, **kwargs)

    def bump_prepatch(self, metadata: str = "rc-1") -> Semver:
        """Bumps the patch version component and adds pre-release tag"""
        return self.bump_patch(pre_release=metadata)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return str(self) == str(other)

        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.__greater__(other)

        return False

    def __ge__(self, other: object) -> bool:
        return self == other or self > other

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.__lesser__(other)

        return False

    def __le__(self, other: object) -> bool:
        return self == other or self < other

    def __greater__(self, other: Semver) -> bool:
        for a, b in self.__zip_with(other):
            if a > b:
                return True

        return False

    def __lesser__(self, other: Semver) -> bool:
        for a, b in self.__zip_with(other):
            if a < b:
                return True

        return False

    def __zip_with(self, other: Semver) -> zip[Tuple[int, int]]:
        return zip(self.as_tuple(), other.as_tuple())

    def __str__(self) -> str:
        result = f"{self.major}.{self.minor}.{self.patch}"

        if self.pre_release:
            result += f"-{self.pre_release}"
        if self.build:
            result += f"+{self.build}"

        return result

    def __repr__(self) -> str:
        return f"Version ({self})"
