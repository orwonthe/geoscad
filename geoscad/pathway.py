from geoscad.node import OrientedNode
from geoscad.orientation import length, Orientation


class LinearPathway:
    def __init__(self, start=None, stop=None, normal=None, surface=None):
        self.delta = stop.position - start.position
        self._length = length(self.delta)
        self._orientation = Orientation(tangent=self.delta, normal=normal, surface=surface)
        self._start = OrientedNode(node=start, orientation=self._orientation)
        self._stop = OrientedNode(node=stop, orientation=self._orientation)

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    @property
    def length(self):
        return self._length

    def at_phase(self, phase):
        if phase <= 0:
            return self.start
        elif phase >= 1:
            return self.stop
        else:
            return OrientedNode(position=self.start.position + phase * self.delta, orientation=self._orientation)

    def at_distance(self, distance):
        return self.at_phase(distance / self.length)