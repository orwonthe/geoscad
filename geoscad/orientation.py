import math
import numpy as np


def np_direction(v):
    return direction(as_numpy(v))


def as_numpy(v):
    return np.array(v, dtype=np.float64)


def direction(v):
    return v / length(v)


def length(v):
    return math.sqrt(np.dot(v, v))


def orthogonal_reduction(v, unit_vector):
    return v - component(v, unit_vector)


def component(v, unit_vector):
    return np.dot(v, unit_vector) * unit_vector

def distance(a, b):
    return length(a - b)

class Orientation:
    def __init__(self, tangent=None, normal=None, surface=None):
        if tangent is not None:
            self._tangent = np_direction(tangent)
        else:
            self._normal = np_direction(normal)
        if surface is None:
            self._normal = direction(orthogonal_reduction(as_numpy(normal), self._tangent))
            self._surface = np.cross(self._tangent, self._normal)
        elif normal is None:
            self._surface = direction(orthogonal_reduction(as_numpy(surface), self._tangent))
            self._normal = np.cross(self._surface, self._tangent)
        elif tangent is None:
            self._surface = direction(orthogonal_reduction(as_numpy(surface), self._normal))
            self._tangent = np.cross(self._normal, self._surface)
        else:
            raise ValueError("Exactly one Orientation parameter must be None")

    def __neg__(self):
        return Orientation(tangent=-self.tangent, normal=-self.normal)

    @property
    def tangent(self):
        return self._tangent

    @property
    def normal(self):
        return self._normal

    @property
    def surface(self):
        return self._surface
