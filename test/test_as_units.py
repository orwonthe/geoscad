import pytest

from geoscad.as_units import inches, nscale_feet, AsUnits, snap_to_double_resolution, layer, even_layer, \
    snap_to_single_resolution


def test_snap_to_double_resolution():
    assert pytest.approx(0.8) == snap_to_double_resolution(0.8)
    assert pytest.approx(0.8) == snap_to_double_resolution(0.71)
    assert pytest.approx(0.8) == snap_to_double_resolution(0.899)
    assert pytest.approx(0.6) == snap_to_double_resolution(0.601)
    assert pytest.approx(0.4) == snap_to_double_resolution(0.3999)


def test_snap_to_single_resolution():
    assert pytest.approx(0.8) == snap_to_single_resolution(0.8)
    assert pytest.approx(0.7) == snap_to_single_resolution(0.71)
    assert pytest.approx(0.9) == snap_to_single_resolution(0.899)
    assert pytest.approx(0.6) == snap_to_single_resolution(0.601)
    assert pytest.approx(0.4) == snap_to_single_resolution(0.3999)


class TestAsUnits:
    def test_scale_inches(self):
        assert 25.4 == 1.0 * inches
        assert 50.8 == 2 * inches
        assert pytest.approx([25.4, 50.8]) == [1.0, 2.0] * inches

    def test_snapped_inches(self):
        assert 25.4 == 1.0 @ inches
        assert 25.4 == 1.001 @ inches
        assert 25.4 == 0.999 @ inches
        assert 50.8 == 2 @ inches
        assert pytest.approx([25.4, 50.8]) == [0.999, 2.001] @ inches

    def test_nscale_feet(self):
        assert pytest.approx(76.2) == 40 * nscale_feet
        assert pytest.approx(76.2) == 40.05 @ nscale_feet

    def test_compostion(self):
        def foo_snapper(mm):
            return 3 * mm

        def bar_snapper(mm):
            return -mm

        foo = AsUnits(3, 'foo', snapper=foo_snapper)
        bar = AsUnits(5, 'bar', snapper=bar_snapper)
        foobar = foo * bar
        assert 30.0 == 2.0 * foobar
        assert -90 == 2.0 @ foobar
        assert 'foo bar' == foobar.name

    def test_inverse(self):
        assert pytest.approx(1.0) == 25.4 / inches
        assert pytest.approx([2.0, 3.0]) == [50.8, 76.2] / inches

    def test_layer(self):
        assert pytest.approx(123.5) == 123.456789 @ layer
        assert pytest.approx(123.7) == 123.67 @ layer

    def test_even_layer(self):
        assert pytest.approx(123.4) == 123.456789 @ even_layer
        assert pytest.approx(123.6) == 123.67 @ even_layer
