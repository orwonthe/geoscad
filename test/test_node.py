from geoscad.node import Node


class TestNode:
    def test_position(self):
        pos = [2, 3, 4]
        node = Node(pos)
        assert pos == list(node.position)
