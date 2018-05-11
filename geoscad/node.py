from geoscad.orientation import as_numpy, Orientation

X_DIRECTION = as_numpy([1, 0, 0])
Y_DIRECTION = as_numpy([0, 1, 0])
Z_DIRECTION = as_numpy([0, 0, 1])


class Node:
    def __init__(self, position=None):
        if position is None:
            position = [0, 0, 0]
        self.position = as_numpy(position)


class OrientedNode(Node, Orientation):
    def __init__(self, position=None, node=None, orientation=None, tangent=None, normal=None, surface=None):
        if position is None:
            position = node.position
        Node.__init__(self, position=position)
        if orientation is None:
            orientation = Orientation(tangent=tangent, normal=normal, surface=surface)
        Orientation.__init__(self, tangent=orientation.tangent, normal=orientation.normal)
