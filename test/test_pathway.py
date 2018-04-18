import pytest

from geoscad.node import Node, Z_DIRECTION
from geoscad.orientation import as_numpy
from geoscad.pathway import LinearPathway


class TestLinearPathway:
    def setup(self):
        self.start = Node([10, 20, 30])
        self.middle = Node([13, 24, 30])
        self.stop = Node([16, 28, 30])

        self.normal = Z_DIRECTION
        self.pathway = LinearPathway(start=self.start, stop=self.stop, normal=self.normal)

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

