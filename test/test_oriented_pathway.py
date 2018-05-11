import pytest

from geoscad.as_units import Degrees
from geoscad.node import Node, Z_DIRECTION, X_DIRECTION, Y_DIRECTION
from geoscad.orientation import as_numpy
from geoscad.oriented_pathway import LinearOrientedPathway, CircularOrientedPathway


class TestLinearOrientedPathway:
    def setup(self):
        self.start = Node([10, 20, 30])
        self.middle = Node([13, 24, 30])
        self.stop = Node([16, 28, 30])

        self.normal = Z_DIRECTION
        self.pathway = LinearOrientedPathway(start=self.start, stop=self.stop, normal=self.normal)

    def test_endpoints(self):
        assert self.pathway.start.position == pytest.approx(self.start.position)
        assert self.pathway.stop.position == pytest.approx(self.stop.position)

    def test_length(self):
        assert self.pathway.length == pytest.approx(10)

    def test_at_phase(self):
        assert self.pathway.at_phase(-1).position == pytest.approx(self.start.position)
        assert self.pathway.at_phase(0).position == pytest.approx(self.start.position)
        assert self.pathway.at_phase(0.5).position == pytest.approx(self.middle.position)
        assert self.pathway.at_phase(1).position == pytest.approx(self.stop.position)
        assert self.pathway.at_phase(2).position == pytest.approx(self.stop.position)

    def test_at_distance(self):
        assert self.pathway.at_distance(-1).position == pytest.approx(self.start.position)
        assert self.pathway.at_distance(0).position == pytest.approx(self.start.position)
        assert self.pathway.at_distance(5).position == pytest.approx(self.middle.position)
        assert self.pathway.at_distance(10).position == pytest.approx(self.stop.position)
        assert self.pathway.at_distance(11).position == pytest.approx(self.stop.position)

    def test_tangents(self):
        for phase in [-1, 0, 0.5, 1, 1.1]:
            assert self.pathway.at_phase(phase).tangent == pytest.approx(as_numpy([0.6, 0.8, 0.0]))

    def test_normals(self):
        for phase in [-1, 0, 0.5, 1, 1.1]:
            assert self.pathway.at_phase(phase).normal == pytest.approx(self.normal)

    def test_surfaces(self):
        for phase in [-1, 0, 0.5, 1, 1.1]:
            assert self.pathway.at_phase(phase).surface == pytest.approx(as_numpy([0.8, -0.6, 0.0]))


class TestCircularOrientedPathway:
    def setup(self):
        pass

    def test_180(self):
        start = Node(-5 * X_DIRECTION)
        stop = Node(5 * X_DIRECTION)
        normal = Z_DIRECTION
        path = CircularOrientedPathway(start=start, stop=stop, normal=normal, angle=180 * Degrees)
        midpoint = path.at_phase(0.5)

        assert path.start.position == pytest.approx(start.position)
        assert path.stop.position == pytest.approx(stop.position)
        assert midpoint.position == pytest.approx(-5 * Y_DIRECTION)

        assert path.start.tangent == pytest.approx(-Y_DIRECTION)
        assert path.stop.tangent == pytest.approx(Y_DIRECTION)
        assert midpoint.tangent == pytest.approx(X_DIRECTION)

        assert path.start.surface == pytest.approx(-X_DIRECTION)
        assert path.stop.surface == pytest.approx(X_DIRECTION)
        assert midpoint.surface == pytest.approx(-Y_DIRECTION)

        assert path.start.normal == pytest.approx(Z_DIRECTION)
        assert path.stop.normal == pytest.approx(Z_DIRECTION)
        assert midpoint.normal == pytest.approx(Z_DIRECTION)
