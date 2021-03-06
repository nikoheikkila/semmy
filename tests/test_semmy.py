from pytest import mark, raises
from hypothesis import given
from hypothesis.strategies import builds, integers, text, just

from semmy import Semver, SemverException

VALID_VERSIONS = [
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
    ["1.2.3----RC-SNAPSHOT.12.9.1--.12+788", Semver(1, 2, 3, pre_release="---RC-SNAPSHOT.12.9.1--.12", build="788")],
    ["1.2.3----R-S.12.9.1--.12+meta", Semver(1, 2, 3, pre_release="---R-S.12.9.1--.12", build="meta")],
    ["1.2.3----RC-SNAPSHOT.12.9.1--.12", Semver(1, 2, 3, pre_release="---RC-SNAPSHOT.12.9.1--.12")],
    ["1.0.0+0.build.1-rc.10000aaa-kk-0.1", Semver(1, 0, 0, build="0.build.1-rc.10000aaa-kk-0.1")],
    [
        "99999999999999999999999.999999999999999999.99999999999999999",
        Semver(99999999999999999999999, 999999999999999999, 99999999999999999),
    ],
    ["1.0.0-0A.is.legal", Semver(1, 0, 0, pre_release="0A.is.legal")],
]

INVALID_VERSIONS = [
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


def test_initial_semver() -> None:
    assert Semver() == Semver.from_string("0.1.0")


def test_initial_pre_release() -> None:
    assert Semver().pre_release == ""


def test_initial_build() -> None:
    assert Semver().build == ""


def test_inequality() -> None:
    assert Semver() != object()


@mark.parametrize("version,expected", VALID_VERSIONS)
def test_semver_from_string(version: str, expected: Semver) -> None:
    semver = Semver.from_string(version)

    assert semver == expected
    assert str(semver) == version


@mark.parametrize("version", INVALID_VERSIONS)
def test_invalid_semver(version: str) -> None:
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
def test_major_bump(original: Semver, expected: Semver) -> None:
    assert original.bump_major() == expected


@mark.parametrize(
    ("original", "expected"),
    [
        [Semver(0, 1, 0), Semver(0, 2, 0)],
        [Semver(1, 0, 0), Semver(1, 1, 0)],
        [Semver(2, 1, 0), Semver(2, 2, 0)],
        [Semver(3, 1, 1), Semver(3, 2, 0)],
    ],
)
def test_minor_bump(original: Semver, expected: Semver) -> None:
    assert original.bump_minor() == expected


@mark.parametrize(
    ("original", "expected"),
    [
        [Semver(0, 1, 0), Semver(0, 1, 1)],
        [Semver(1, 0, 0), Semver(1, 0, 1)],
        [Semver(2, 1, 0), Semver(2, 1, 1)],
        [Semver(3, 1, 1), Semver(3, 1, 2)],
    ],
)
def test_patch_bump(original: Semver, expected: Semver) -> None:
    assert original.bump_patch() == expected


def test_premajor_bump() -> None:
    metadata = "rc-2"
    assert Semver(0, 1, 0).bump_premajor(metadata) == Semver(1, 0, 0, pre_release=metadata)


def test_preminor_bump() -> None:
    metadata = "rc-2"
    assert Semver(0, 1, 0).bump_preminor(metadata) == Semver(0, 2, 0, pre_release=metadata)


def test_prepatch_bump() -> None:
    metadata = "rc-2"
    assert Semver(0, 1, 0).bump_prepatch(metadata) == Semver(0, 1, 1, pre_release=metadata)


@given(builds(Semver, major=just(0), minor=integers(), patch=integers(), pre_release=text(), build=text()))
def test_0_x_is_pre_release(semver: Semver) -> None:
    assert semver.is_pre_release()


@given(builds(Semver, major=integers(), minor=integers(), patch=integers(), pre_release=text(min_size=1), build=text()))
def test_is_marked_pre_release(semver: Semver) -> None:
    assert semver.is_pre_release()
