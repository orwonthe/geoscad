# geoscad
*Geometry Tools for SolidPython wrapping for OpenSCAD*

[OpenSCAD](http://www.openscad.org) is a great tool for defining 3 dimensional shapes. 

[Solid Python](https://github.com/SolidCode/SolidPython) is a great tool for creating OpenSCAD descriptions
using Python.

The goal of **geoscad** is to provide a set
of general purpose aids useful across many 3d projects.

The *geoscad* library uses *numpy* for speed.

Source is maintained at [geoscad](https://github.com/orwonthe/geoscad>).

Examples of use can be found at [print3d](https://github.com/orwonthe/print3d).

## as units
Most 3d printer software expect dimensions to be millimeters,
while for design purposes some other scale is more conceptually useful.
The `as_units` module makes this translation to millimeters easy.

A collection of objects in `as_units` function as scaling tools when used as
the right hand side of a multiplication. For example
```python
from geoscad.as_units import inches
width = 3.5 * inches
```
will set `width` to a 88.9 which is the millimeter equivalent of 3.5 inches.

To determine the size in millimeters of an 8 foot railroad tie modeled in nscale at a
ratio of 1:160 one can use `nscale_feet`
```python
tie_length = 8 * nscale_feet
```

The division operation can be used to reverse the calculation:
```python
width_in_inches = width / inches
```

Sometimes it is useful to have a measurement which exactly equals
an even number of printing layers, An example would be a design
that uses a repeating pattern. Making the pattern repeat on
even layers means the printing will have less interaction with
the pattern frequency. The `layers2` object can be used to achieve this:
```python
pattern_height = 12.345 @ even_layer
```
Note the use of the `@` operation. When this is used instead of `*` then
the measurement will snap to the nearest even layer.
The same result can be achieved using `@` with dimensional layers:
```python
width = 3.5 @ inches
```

You can also make your own scaling objects:
```python
ho_scale_inches = AsUnits(1 / 87.1 * inches, 'ho"')
tie_length = 8 * ho_scale_inches
```

The `@` operator will invoke the snapping function of an `AsUnits` object.
You can define your own snapping function to accomodate different needs, such as
a printer with resolution that differs from the default assumption of 0.1 millimieters.

Units can be applied to either numbers or lists. 
For example `[1, 2, 3] * inches` will return `[25.4, 50.8, 76.2]`
