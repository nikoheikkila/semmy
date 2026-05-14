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
            [Semver(2, 0, 0), Semver(1, 9, 9)],
            [Semver(1, 3, 0), Semver(1, 2, 9)],
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
            [Semver(1, 9, 9), Semver(2, 0, 0)],
            [Semver(1, 2, 9), Semver(1, 3, 0)],
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

    @mark.parametrize(
        ("pre", "release"),
        [
            [Semver(1, 0, 0, pre_release="alpha"), Semver(1, 0, 0)],
            [Semver(1, 0, 0, pre_release="rc.1"), Semver(1, 0, 0)],
            [Semver(2, 3, 4, pre_release="beta"), Semver(2, 3, 4)],
        ],
    )
    def test_pre_release_has_lower_precedence_than_release(self, pre: Semver, release: Semver) -> None:
        verify(pre < release).is_true()
        verify(release > pre).is_true()
        verify(pre > release).is_false()
        verify(release < pre).is_false()

    @mark.parametrize(
        ("lower", "higher"),
        [
            # Spec §11.4 canonical chain
            [Semver(1, 0, 0, pre_release="alpha"), Semver(1, 0, 0, pre_release="alpha.1")],
            [Semver(1, 0, 0, pre_release="alpha.1"), Semver(1, 0, 0, pre_release="alpha.beta")],
            [Semver(1, 0, 0, pre_release="alpha.beta"), Semver(1, 0, 0, pre_release="beta")],
            [Semver(1, 0, 0, pre_release="beta"), Semver(1, 0, 0, pre_release="beta.2")],
            [Semver(1, 0, 0, pre_release="beta.2"), Semver(1, 0, 0, pre_release="beta.11")],
            [Semver(1, 0, 0, pre_release="beta.11"), Semver(1, 0, 0, pre_release="rc.1")],
            [Semver(1, 0, 0, pre_release="1"), Semver(1, 0, 0, pre_release="alpha")],
            [Semver(1, 0, 0, pre_release="0.3.7"), Semver(1, 0, 0, pre_release="x.7.z.92")],
        ],
    )
    def test_pre_release_ordering(self, lower: Semver, higher: Semver) -> None:
        verify(lower < higher).is_true()
        verify(higher > lower).is_true()
        verify(lower > higher).is_false()
        verify(higher < lower).is_false()

    @mark.parametrize(
        ("a", "b"),
        [
            [Semver(1, 0, 0, build="001"), Semver(1, 0, 0, build="002")],
            [Semver(1, 0, 0, pre_release="alpha", build="001"), Semver(1, 0, 0, pre_release="alpha", build="999")],
        ],
    )
    def test_build_metadata_ignored_in_precedence(self, a: Semver, b: Semver) -> None:
        verify(a < b).is_false()
        verify(a > b).is_false()
        verify(a >= b).is_true()
        verify(a <= b).is_true()
