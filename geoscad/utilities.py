from solid import cube, mirror, union
from solid.utils import up, left, right, forward


def grounded_cube(shape):
    half_height = shape[2] / 2
    return up(half_height)(
        cube(shape, center=True))


def left_right_symmetric(offset, target):
    left_target = left(offset)(mirror([1, 0, 0])(target))
    right_target = right(offset)(target)
    return left_target + right_target


def raised_shape(
        shape,
        thickness
):
    return [shape[0], shape[1], shape[2] + thickness]


def replicate_along_y_axis(y_locations, source_object):
    return union()([forward(offset)(source_object) for offset in y_locations])


def thickened_shape(
        shape,
        thickness
):
    return [dim + thickness for dim in shape]
