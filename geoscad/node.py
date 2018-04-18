from geoscad.orientation import as_numpy, Orientation

X_DIRECTION = as_numpy([1, 0, 0])
Y_DIRECTION = as_numpy([0, 1, 0])
Z_DIRECTION = as_numpy([0, 0, 1])


class Node:
    def __init__(self, position=None):
        if position is None:
            position = [0, 0, 0]
        self.position = as_numpy(position)


class OrientedNode:
    def __init__(self, position=None, node=None, orientation=None, tangent=None, normal=None, surface=None):
        if node is None:
            node = Node(position)
        if orientation is None:
            orientation = Orientation(tangent=tangent, normal=normal, surface=surface)
        self._node = node
        self._orientation = orientation

    @property
    def node(self):
        return self._node

    @property
    def orientation(self):
        return self._orientation

    @property
    def position(self):
        return self.node.position

    @property
    def tangent(self):
        return self.orientation.tangent

    @property
    def normal(self):
        return self.orientation.normal

    @property
    def surface(self):
        return self.orientation.surface
