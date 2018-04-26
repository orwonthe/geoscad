import pytest

from geoscad.utilities import thickened_shape, raised_shape


def test_thickened_shape():
    shape = [1, 2, 3.0]
    thick_shape = thickened_shape(shape, 0.1)
    assert [1.1, 2.1, 3.1] == pytest.approx(thick_shape)


def test_raised_shape():
    shape = [1, 2, 3.0]
    high_shape = raised_shape(shape, 0.1)
    assert [1, 2, 3.1] == pytest.approx(high_shape)

