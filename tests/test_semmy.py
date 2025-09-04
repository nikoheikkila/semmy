from typing import ClassVar

from assertpy import assert_that as verify
from hypothesis import given
from hypothesis.strategies import builds, integers, just, text
from pytest import mark, raises

from semmy import Semver, SemverException


class TestSemmy:
    VALID_VERSIONS: ClassVar[list[list[str | Semver]]] = [
        ["0.0.4", Semver(0, 0, 4)],
        ["1.2.3", Semver(1, 2, 3)],
        ["10.20.30", Semver(10, 20, 30)],
        ["1.1.2-prerelease+meta", Semver(1, 1, 2, pre_release="prerelease", build="meta")],
        ["1.1.2+meta", Semver(1, 1, 2, build="meta")],
        ["1.1.2+meta-valid", Semver(1, 1, 2, build="meta-valid")],
        ["1.0.0-alpha", Semver(1, 0, 0, pre_release="alpha")],
        ["1.0.0-beta", Semver(1, 0, 0, pre_release="beta")],
        ["1.0.0-alpha.beta", Semver(1, 0, 0, pre_release="alpha.beta")],
        ["1.0.0-alpha.beta.1", Semver(1, 0, 0, pre_release="alpha.beta.1")],
        ["1.0.0-alpha.1", Semver(1, 0, 0, pre_release="alpha.1")],
        ["1.0.0-alpha0.valid", Semver(1, 0, 0, pre_release="alpha0.valid")],
        ["1.0.0-alpha.0valid", Semver(1, 0, 0, pre_release="alpha.0valid")],
        [
            "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay",
            Semver(1, 0, 0, pre_release="alpha-a.b-c-somethinglong", build="build.1-aef.1-its-okay"),
        ],
        ["1.0.0-rc.1+build.1", Semver(1, 0, 0, pre_release="rc.1", build="build.1")],
        ["2.0.0-rc.1+build.123", Semver(2, 0, 0, pre_release="rc.1", build="build.123")],
        ["1.2.3-beta", Semver(1, 2, 3, pre_release="beta")],
        ["10.2.3-DEV-SNAPSHOT", Semver(10, 2, 3, pre_release="DEV-SNAPSHOT")],
        ["1.2.3-SNAPSHOT-123", Semver(1, 2, 3, pre_release="SNAPSHOT-123")],
        ["1.0.0", Semver(1, 0, 0)],
        ["2.0.0", Semver(2, 0, 0)],
        ["1.1.7", Semver(1, 1, 7)],
        ["2.0.0+build.1848", Semver(2, 0, 0, build="build.1848")],
        ["2.0.1-alpha.1227", Semver(2, 0, 1, pre_release="alpha.1227")],
        ["1.0.0-alpha+beta", Semver(1, 0, 0, pre_release="alpha", build="beta")],
        [
            "1.2.3----RC-SNAPSHOT.12.9.1--.12+788",
            Semver(1, 2, 3, pre_release="---RC-SNAPSHOT.12.9.1--.12", build="788"),
        ],
        ["1.2.3----R-S.12.9.1--.12+meta", Semver(1, 2, 3, pre_release="---R-S.12.9.1--.12", build="meta")],
        ["1.2.3----RC-SNAPSHOT.12.9.1--.12", Semver(1, 2, 3, pre_release="---RC-SNAPSHOT.12.9.1--.12")],
        ["1.0.0+0.build.1-rc.10000aaa-kk-0.1", Semver(1, 0, 0, build="0.build.1-rc.10000aaa-kk-0.1")],
        [
            "99999999999999999999999.999999999999999999.99999999999999999",
            Semver(99999999999999999999999, 999999999999999999, 99999999999999999),
        ],
        ["1.0.0-0A.is.legal", Semver(1, 0, 0, pre_release="0A.is.legal")],
    ]

    INVALID_VERSIONS: ClassVar[list[str]] = [
        "1",
        "1.2",
        "1.2.3-0123",
        "1.2.3-0123.0123",
        "1.1.2+.123",
        "+invalid",
        "-invalid",
        "-invalid+invalid",
        "-invalid.01",
        "alpha",
        "alpha.beta",
        "alpha.beta.1",
        "alpha.1",
        "alpha+beta",
        "alpha_beta",
        "alpha.",
        "alpha..",
        "beta",
        "1.0.0-alpha_beta",
        "-alpha.",
        "1.0.0-alpha..",
        "1.0.0-alpha..1",
        "1.0.0-alpha...1",
        "1.0.0-alpha....1",
        "1.0.0-alpha.....1",
        "1.0.0-alpha......1",
        "1.0.0-alpha.......1",
        "01.1.1",
        "1.01.1",
        "1.1.01",
        "1.2",
        "1.2.3.DEV",
        "1.2-SNAPSHOT",
        "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788",
        "1.2-RC-SNAPSHOT",
        "-1.0.3-gamma+b7718",
        "+justmeta",
        "9.8.7+meta+meta",
        "9.8.7-whatever+meta+meta",
        "99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.",
        "1--------------------------------..12",
    ]

    def test_initial_semver(self) -> None:
        verify(Semver()).is_equal_to(Semver.from_string("0.1.0"))

    def test_initial_pre_release(self) -> None:
        verify(Semver()).has_pre_release("")

    def test_initial_build(self) -> None:
        verify(Semver()).has_build("")

    def test_inequality(self) -> None:
        verify(Semver()).is_not_equal_to(object())

    @mark.parametrize("version,expected", VALID_VERSIONS)
    def test_semver_from_string(self, version: str, expected: Semver) -> None:
        semver = Semver.from_string(version)

        verify(semver).is_equal_to(expected)
        verify(str(semver)).is_equal_to(version)

    @mark.parametrize("version", INVALID_VERSIONS)
    def test_invalid_semver(self, version: str) -> None:
        with raises(SemverException, match=r"Version string .+ is not a valid semantic version"):
            Semver.from_string(version)

    @mark.parametrize(
        ("original", "expected"),
        [
            [Semver(0, 1, 0), Semver(1, 0, 0)],
            [Semver(1, 0, 0), Semver(2, 0, 0)],
            [Semver(2, 1, 0), Semver(3, 0, 0)],
            [Semver(3, 1, 1), Semver(4, 0, 0)],
        ],
    )
    def test_major_bump(self, original: Semver, expected: Semver) -> None:
        verify(original.bump_major()).is_equal_to(expected)

    @mark.parametrize(
        ("original", "expected"),
        [
            [Semver(0, 1, 0), Semver(0, 2, 0)],
            [Semver(1, 0, 0), Semver(1, 1, 0)],
            [Semver(2, 1, 0), Semver(2, 2, 0)],
            [Semver(3, 1, 1), Semver(3, 2, 0)],
        ],
    )
    def test_minor_bump(self, original: Semver, expected: Semver) -> None:
        verify(original.bump_minor()).is_equal_to(expected)

    @mark.parametrize(
        ("original", "expected"),
        [
            [Semver(0, 1, 0), Semver(0, 1, 1)],
            [Semver(1, 0, 0), Semver(1, 0, 1)],
            [Semver(2, 1, 0), Semver(2, 1, 1)],
            [Semver(3, 1, 1), Semver(3, 1, 2)],
        ],
    )
    def test_patch_bump(self, original: Semver, expected: Semver) -> None:
        verify(original.bump_patch()).is_equal_to(expected)

    def test_premajor_bump(self) -> None:
        metadata = "rc-2"

        verify(Semver(0, 1, 0).bump_premajor(metadata)).is_equal_to(Semver(1, 0, 0, pre_release=metadata))

    def test_preminor_bump(self) -> None:
        metadata = "rc-2"

        verify(Semver(0, 1, 0).bump_preminor(metadata)).is_equal_to(Semver(0, 2, 0, pre_release=metadata))

    def test_prepatch_bump(self) -> None:
        metadata = "rc-2"

        verify(Semver(0, 1, 0).bump_prepatch(metadata)).is_equal_to(Semver(0, 1, 1, pre_release=metadata))

    @given(builds(Semver, major=just(0), minor=integers(), patch=integers(), pre_release=text(), build=text()))
    def test_0_x_is_pre_release(self, semver: Semver) -> None:
        verify(semver.is_pre_release()).is_true()

    @given(
        builds(Semver, major=integers(), minor=integers(), patch=integers(), pre_release=text(min_size=1), build=text())
    )
    def test_is_marked_pre_release(self, semver: Semver) -> None:
        verify(semver.is_pre_release()).is_true()
