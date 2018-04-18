import numpy as np
import pytest

from geoscad.orientation import length, as_numpy, direction, component, orthogonal_reduction, Orientation, distance

EPSILON = 0.0000001


def is_all_unit_length(hhh):
    is_unit_length(hhh.tangent)
    is_unit_length(hhh.normal)
    is_unit_length(hhh.surface)


def is_unit_length(v):
    assert np.dot(v, v) == pytest.approx(1.0)


def is_all_orthogonal(hhh):
    tt = hhh.tangent
    nn = hhh.normal
    ss = hhh.surface
    is_orthogonal(tt, nn)
    is_orthogonal(ss, nn)
    is_orthogonal(tt, ss)


def is_orthogonal(a, b):
    assert np.dot(a, b) == pytest.approx(0.0, EPSILON)


def has_same_direction(a, b):
    length(a) * length(b) == pytest.approx(np.dot(a, b))


def is_right_handed(hhh):
    assert np.dot(np.cross(hhh.tangent, hhh.normal), hhh.surface) == pytest.approx(1.0)


def test_length():
    assert length(as_numpy([3, 4, 12])) == pytest.approx(13)


def test_direction():
    aaa = [3, 4, 12]
    ddd = direction(as_numpy(aaa))
    for iii in range(3):
        ddd[iii] == pytest.approx(aaa[iii] / 13)


def test_component():
    ccc = component(as_numpy([3, 4, 99]), as_numpy([0.6, 0.8, 0.0]))
    assert ccc[0] == pytest.approx(3)
    assert ccc[1] == pytest.approx(4)
    assert ccc[2] == pytest.approx(0.0)

def test_numpy_compare():
    aa = as_numpy([1,2,3])
    bb = as_numpy([1,2,4])
    cc = as_numpy([1,2,3])
    assert aa != pytest.approx(bb)
    assert aa == pytest.approx(cc)

def test_reduction():
    ccc = orthogonal_reduction(as_numpy([3, 4, 99]), as_numpy([0.6, 0.8, 0.0]))
    assert ccc[0] == pytest.approx(0.0)
    assert ccc[1] == pytest.approx(0.0)
    assert ccc[2] == pytest.approx(99.0)


class TestOrientation:
    def setup(self):
        self.a = as_numpy([1, 2, 4])
        self.b = as_numpy([3, 3, 3])
        self.ab = as_numpy([2, 1, -1])
        self.example_tn = Orientation(tangent=self.a, normal=self.b)
        self.example_sn = Orientation(surface=self.b, normal=self.a)
        self.example_ts = Orientation(tangent=self.a, surface=self.b)

    def test_have_unit_length(self):
        is_all_unit_length(self.example_tn)
        is_all_unit_length(self.example_sn)
        is_all_unit_length(self.example_ts)

    def test_orthogonality(self):
        is_all_orthogonal(self.example_tn)
        is_all_orthogonal(self.example_sn)
        is_all_orthogonal(self.example_ts)

    def test_handedness(self):
        is_right_handed(self.example_tn)
        is_right_handed(self.example_sn)
        is_right_handed(self.example_ts)

    def test_primary_component(self):
        has_same_direction(self.a, self.example_tn.tangent)
        has_same_direction(self.a, self.example_ts.tangent)
        has_same_direction(self.a, self.example_sn.normal)

    def test_secondary_component(self):
        has_same_direction(self.ab, self.example_tn.normal)
        has_same_direction(self.ab, self.example_sn.surface)
        has_same_direction(self.ab, self.example_ts.surface)

    def test_derived_component(self):
        is_orthogonal(self.a, self.example_tn.surface)
        is_orthogonal(self.a, self.example_sn.tangent)
        is_orthogonal(self.a, self.example_ts.normal)
        is_orthogonal(self.b, self.example_tn.surface)
        is_orthogonal(self.b, self.example_sn.tangent)
        is_orthogonal(self.b, self.example_ts.normal)

    def test_negate(self):
        neg_tn = -self.example_tn
        is_all_unit_length(neg_tn)
        is_all_orthogonal(neg_tn)
        assert distance(self.example_tn.tangent, neg_tn.tangent) == pytest.approx(2.0)
        assert distance(self.example_tn.normal, neg_tn.normal) == pytest.approx(2.0)
        assert distance(self.example_tn.surface, neg_tn.surface) == pytest.approx(0.0)
        is_right_handed(neg_tn)
