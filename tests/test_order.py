from pytest import mark

from semmy import Semver


@mark.parametrize(
    ("a", "b"),
    [
        [Semver(0, 1, 1), Semver(0, 1, 0)],
        [Semver(1, 2, 0), Semver(1, 1, 0)],
        [Semver(2, 0, 0), Semver(1, 0, 0)],
    ],
)
def test_greater(a: Semver, b: Semver) -> None:
    assert a > b
    assert not a < b


def test_not_greater_than_object() -> None:
    assert not Semver().__gt__(object())


@mark.parametrize(
    ("a", "b"),
    [
        [Semver(0, 1, 1), Semver(0, 1, 2)],
        [Semver(1, 2, 0), Semver(1, 3, 0)],
        [Semver(2, 0, 0), Semver(3, 0, 0)],
    ],
)
def test_lesser(a: Semver, b: Semver) -> None:
    assert a < b
    assert not a > b
