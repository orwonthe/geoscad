import math

import numpy as np

from geoscad.node import OrientedNode
from geoscad.orientation import length, Orientation, direction


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
