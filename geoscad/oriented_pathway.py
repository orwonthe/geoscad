import math

import numpy as np

from geoscad.node import OrientedNode
from geoscad.orientation import length, Orientation, direction, distance

PRECISION_CRITERIA = 0.00001


class OrientedPathway:
    def __init__(self, start, stop, length):
        self._start = start
        self._stop = stop
        self._length = length

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    @property
    def length(self):
        return self._length

    def at_distance(self, distance):
        return self.at_phase(distance / self.length)

    def at_phase(self, phase):
        if phase <= 0:
            return self.start
        elif phase >= 1:
            return self.stop
        else:
            return self._interpolation(phase)

    def _interpolation(self, phase):
        raise NotImplementedError()

    def append(self, node, angle=None):
        if angle is None or angle == 0.0:
            continuation = LinearOrientedPathway(start=self.stop, stop=node, normal=self.stop.normal)
        else:
            continuation = CircularOrientedPathway(start=self.stop, stop=node, normal=self.stop.normal, angle=angle)
        return JoinedOrientedPathway(self, continuation)

    def prepend(self, node, angle=None):
        if angle is None or angle == 0.0:
            continuation = LinearOrientedPathway(stop=self.start, start=node, normal=self.stop.normal)
        else:
            continuation = CircularOrientedPathway(stop=self.start, start=node, normal=self.start.normal, angle=angle)
        return JoinedOrientedPathway(continuation, self)


class LinearOrientedPathway(OrientedPathway):
    def __init__(self, start, stop, normal=None, surface=None):
        self._delta = stop.position - start.position
        self._orientation = Orientation(tangent=self._delta, normal=normal, surface=surface)
        super().__init__(
            start=OrientedNode(node=start, orientation=self._orientation),
            stop=OrientedNode(node=stop, orientation=self._orientation),
            length=length(self._delta),
        )

    def _interpolation(self, phase):
        return OrientedNode(position=self.start.position + phase * self._delta, orientation=self._orientation)


class CircularOrientedPathway(OrientedPathway):
    def __init__(self, start, stop, normal, angle):
        self._normal = direction(normal)
        self._angle = angle
        delta = stop.position - start.position
        midpoint = (stop.position + start.position) / 2
        half_height = length(delta) / 2
        half_angle = angle / 2
        self._radius = half_height / math.sin(half_angle)
        center_displacement = self._radius * math.cos(half_angle)
        toward_center = direction(np.cross(self._normal, delta))
        self._center = midpoint + center_displacement * toward_center
        self._radial = direction(start.position - self._center)
        self._rotary = np.cross(self._normal, self._radial)
        super().__init__(
            start=OrientedNode(node=start, normal=self._normal, surface=self._radial),
            stop=OrientedNode(node=stop, normal=self._normal, surface=direction(stop.position - self._center)),
            length=self._radius * self._angle,
        )

    def _interpolation(self, phase):
        angle = self._angle * phase
        surface = math.cos(angle) * self._radial + math.sin(angle) * self._rotary
        position = self._center + self._radius * surface
        return OrientedNode(position=position, normal=self._normal, surface=surface)


class JoinedOrientedPathway(OrientedPathway):
    def __init__(self, leading_path, trailing_path):
        length = leading_path.length + trailing_path.length
        if PRECISION_CRITERIA * self.length > distance(leading_path.stop, trailing_path.start):
            raise ValueError("Disjoint path connection")
        self.leading_path = leading_path
        self.trailing_path = trailing_path
        self.breaking_phase = leading_path.length / length
        self.leading_scale = 1.0 / self.breaking_phase
        self.trailing_scale = length / trailing_path.length
        super().__init__(start=leading_path.start, stop=trailing_path.stop, length=length)

    def _interpolation(self, phase):
        if phase < self.breaking_phase:
            return self.leading_path.at_phase(phase * self.leading_scale)
        else:
            return self.trailing_path((phase - self.breaking_phase) * self.trailing_scale)
