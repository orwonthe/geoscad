from solid import cube, mirror, union, cylinder, intersection, translate, minkowski, sphere
from solid.utils import up, left, right, forward


def grounded_cube(shape):
    half_height = shape[2] / 2
    return up(half_height)(
        cube(shape, center=True))


def rounded_cube(shape, radius, segments=24):
    diameter = 2 * radius
    long_shape = [shape[0] - diameter, shape[1], shape[2]]
    wide_shape = [shape[0], shape[1] - diameter, shape[2]]
    half_width = shape[0] / 2 - radius
    half_length = shape[1] / 2 - radius
    half_height = shape[2] / 2
    corner = cylinder(r=radius, h=shape[2], center=True, segments=segments)
    corners = replicate_along_xy_axes([-half_width, half_width], [-half_length, half_length], corner)
    return up(half_height)(
        cube(long_shape, center=True) \
        + cube(wide_shape, center=True) \
        + corners
    )


def y_symmetric_intersection(target):
    return intersection()([target, y_symmetric(target)])


def y_symmetric_union(target):
    return union()([target, y_symmetric(target)])


def y_symmetric(target):
    return mirror([0, 1, 0])(target)


def rounded_platter(shape, radius, segments=16):
    parts = []
    diameter = 2 * radius
    width, length, height = shape
    short_width = width - diameter
    short_length = length - diameter
    if short_width > 0:
        x_centers = [-0.5 * short_width, 0.5 * short_width]
        parts.append(grounded_cube([short_width, length, height]))
    else:
        x_centers = [0]
    if short_length > 0:
        y_centers = [-0.5 * short_length, 0.5 * short_length]
        parts.append(grounded_cube([width, short_length, height]))
    else:
        y_centers = [0]
    corner_cylinder = cylinder(r=radius, h=height, segments=segments)
    for x in x_centers:
        for y in y_centers:
            parts.append(right(x)(forward(y)(corner_cylinder)))
    return union()(parts)


def smudge(thickness, target):
    return grow(thickness, shrink(thickness, target))


def shrink(thickness, target):
    return intersection()([translate(corner)(target) for corner in corners([thickness, thickness, thickness])])


def corners(shape):
    for x in [-0.5, 0.5]:
        for y in [-0.5, 0.5]:
            for z in [-0.5, 0.5]:
                yield [x * shape[0], y * shape[1], z * shape[2]]


def grow(thickness, target):
    radius = thickness / 2
    return minkowski()(target, sphere(r=radius, segments=24))


def left_right_symmetric(offset, target):
    left_target = left(offset)(mirror([1, 0, 0])(target))
    right_target = right(offset)(target)
    return left_target + right_target


def raised_shape(
        shape,
        thickness
):
    return [shape[0], shape[1], shape[2] + thickness]


def replicate_along_xy_axes(x_locations, y_locations, source_object):
    return replicate_along_x_axis(x_locations, replicate_along_y_axis(y_locations, source_object))


def replicate_along_x_axis(x_locations, source_object):
    return union()([right(offset)(source_object) for offset in x_locations])


def replicate_along_y_axis(y_locations, source_object):
    return union()([forward(offset)(source_object) for offset in y_locations])


def thickened_shape(
        shape,
        thickness
):
    return [dim + thickness for dim in shape]
