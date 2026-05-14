import re
from dataclasses import dataclass
from typing import Self, override

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
    def from_string(cls, version: str) -> Self:
        """Parses a new semantic version object from input string

        Raises
            SemverException: for invalid input
        """
        if not SEMVER_REGEX.fullmatch(version):
            raise SemverException(f"Version string {version} is not a valid semantic version")

        major, minor, patch, pre_release, build = SEMVER_REGEX.findall(version).pop()

        return cls(int(major), int(minor), int(patch), pre_release, build)

    def as_tuple(self) -> tuple[int, int, int]:
        """Exports version as integer tuple"""
        return (self.major, self.minor, self.patch)

    def is_pre_release(self) -> bool:
        """Checks whether the version is considered pre-release"""
        if self.pre_release:
            return True

        return self.major == 0

    def bump_major(self, **kwargs: str) -> Self:
        """Bumps the major version component"""
        return self.__class__(major=self.major + 1, minor=0, patch=0, **kwargs)

    def bump_premajor(self, metadata: str = "rc-1") -> Self:
        """Bumps the major version component and adds pre-release tag"""
        return self.bump_major(pre_release=metadata)

    def bump_minor(self, **kwargs: str) -> Self:
        """Bumps the minor version component"""
        return self.__class__(major=self.major, minor=self.minor + 1, patch=0, **kwargs)

    def bump_preminor(self, metadata: str = "rc-1") -> Self:
        """Bumps the minor version component and adds pre-release tag"""
        return self.bump_minor(pre_release=metadata)

    def bump_patch(self, **kwargs: str) -> Self:
        """Bumps the patch version component"""
        return self.__class__(major=self.major, minor=self.minor, patch=self.patch + 1, **kwargs)

    def bump_prepatch(self, metadata: str = "rc-1") -> Self:
        """Bumps the patch version component and adds pre-release tag"""
        return self.bump_patch(pre_release=metadata)

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return str(self) == str(other)

        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.__compare(other) > 0
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.__compare(other) >= 0
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.__compare(other) < 0
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, Semver):
            return self.__compare(other) <= 0
        return False

    def __compare(self, other: Self) -> int:
        s, o = self.as_tuple(), other.as_tuple()
        if s != o:
            return (s > o) - (s < o)
        return self.__compare_pre_release(other)

    def __compare_pre_release(self, other: Self) -> int:
        if not self.pre_release and not other.pre_release:
            return 0
        if not self.pre_release:
            return 1
        if not other.pre_release:
            return -1

        self_ids = self.pre_release.split(".")
        other_ids = other.pre_release.split(".")

        for self_id, other_id in zip(self_ids, other_ids, strict=False):
            if self_id == other_id:
                continue
            self_numeric = self_id.isdigit()
            other_numeric = other_id.isdigit()

            if self_numeric and other_numeric:
                result = int(self_id) - int(other_id)
            elif self_numeric:
                result = -1
            elif other_numeric:
                result = 1
            else:
                result = (self_id > other_id) - (self_id < other_id)

            if result != 0:
                return result

        return len(self_ids) - len(other_ids)

    @override
    def __str__(self) -> str:
        result = f"{self.major}.{self.minor}.{self.patch}"

        if self.pre_release:
            result += f"-{self.pre_release}"
        if self.build:
            result += f"+{self.build}"

        return result

    @override
    def __repr__(self) -> str:
        return f"Version ({self})"
