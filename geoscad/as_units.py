import math


def snap_to_double_resolution(mm, layers_per_millimeter=10):
    layer_pairs_per_millimeter = layers_per_millimeter / 2
    return round(layer_pairs_per_millimeter * mm) / layer_pairs_per_millimeter


def snap_to_single_resolution(mm, layers_per_millimeter=10):
    return round(layers_per_millimeter * mm) / layers_per_millimeter


def snap_to_integral_degrees(angle):
    return math.pi * round(180 * angle / math.pi) / 180.0


class AsUnits:
    def __init__(self, in_millimeters, name, snapper=snap_to_double_resolution):
        self.name = name
        self._in_millimeters = in_millimeters
        self.snapper = snapper

    def __str__(self):
        return self.name

    def __repr__(self):
        return "AsUnits({},'{}')".format(self._in_millimeters, self.name)

    def __rtruediv__(self, other):
        try:
            return [element / self for element in other]
        except:
            return other / self._in_millimeters

    def __rmul__(self, other):
        try:
            return [element * self for element in other]
        except:
            return other * self._in_millimeters

    def __rmatmul__(self, other):
        try:
            return [element @ self for element in other]
        except:
            return self.snapper(other * self)

    def __mul__(self, other):
        if isinstance(other, AsUnits):
            def snapper(mm):
                return other.snapper(self.snapper(mm))

            return AsUnits(
                self._in_millimeters * other._in_millimeters,
                ' '.join([self.name, other.name]),
                snapper=snapper
            )


# Unit translation is into millimeters
inches = AsUnits(25.4, '"')
feet = AsUnits(12.0 * inches, "'")
nscale_inches = AsUnits(1 / 160 * inches, 'n"')
nscale_feet = AsUnits(3 / 40 * inches, "n'")
mm = AsUnits(1.0, "mm")

# Used with @ operator will snap to nearest layer or even numbered layer
layer = AsUnits(1, 'layer', snap_to_single_resolution)
even_layer = AsUnits(1, 'layer2', snap_to_double_resolution)

# Unit translation is into radians
Degrees = AsUnits(math.pi / 180.0, 'degrees', snap_to_integral_degrees)
