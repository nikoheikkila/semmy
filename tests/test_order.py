from assertpy import assert_that as verify
from pytest import mark

from semmy import Semver


class TestOrder:
    @mark.parametrize(
        ("a", "b"),
        [
            [Semver(0, 1, 1), Semver(0, 1, 0)],
            [Semver(1, 2, 0), Semver(1, 1, 0)],
            [Semver(2, 0, 0), Semver(1, 0, 0)],
        ],
    )
    def test_greater(self, a: Semver, b: Semver) -> None:
        verify(a > b).is_true()
        verify(a <= b).is_false()

    @mark.parametrize(
        ("a", "b"),
        [
            [Semver(0, 1, 1), Semver(0, 1, 0)],
            [Semver(0, 1, 1), Semver(0, 1, 1)],
            [Semver(1, 2, 0), Semver(1, 1, 0)],
            [Semver(1, 2, 0), Semver(1, 2, 0)],
            [Semver(2, 0, 0), Semver(1, 0, 0)],
            [Semver(2, 0, 0), Semver(2, 0, 0)],
        ],
    )
    def test_greater_or_equal(self, a: Semver, b: Semver) -> None:
        verify(a >= b).is_true()
        verify(a < b).is_false()

    @mark.parametrize(
        ("a", "b"),
        [
            [Semver(0, 1, 1), Semver(0, 1, 2)],
            [Semver(1, 2, 0), Semver(1, 3, 0)],
            [Semver(2, 0, 0), Semver(3, 0, 0)],
        ],
    )
    def test_lesser(self, a: Semver, b: Semver) -> None:
        verify(a < b).is_true()
        verify(a >= b).is_false()

    @mark.parametrize(
        ("a", "b"),
        [
            [Semver(0, 1, 1), Semver(0, 1, 2)],
            [Semver(0, 1, 1), Semver(0, 1, 1)],
            [Semver(1, 2, 0), Semver(1, 3, 0)],
            [Semver(1, 2, 0), Semver(1, 2, 0)],
            [Semver(2, 0, 0), Semver(3, 0, 0)],
            [Semver(2, 0, 0), Semver(2, 0, 0)],
        ],
    )
    def test_lesser_or_equal(self, a: Semver, b: Semver) -> None:
        verify(a <= b).is_true()
        verify(a > b).is_false()
