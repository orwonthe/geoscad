from solid import color

from color_filter import ColorFilter
from utilities import REJECT_ALL


def same_scad_color(a, b):
    return a.name == b.name and a.params == b.params


class TestColorFilter:
    def setup(self):
        self.alpha = color("red")
        self.beta = color("red")
        self.gamma = color("green")

    def test_comparison(self):
        assert same_scad_color(self.alpha, self.beta)
        assert not same_scad_color(self.alpha, self.gamma)
        assert not same_scad_color(self.beta, self.gamma)

    def test_empty_color_filter(self):
        color_filter = ColorFilter()
        assert same_scad_color(self.alpha, color_filter("red"))

    def test_colored_filter(self):
        red_color_filter = ColorFilter("red")
        green_color_filter = ColorFilter("green")
        assert same_scad_color(self.alpha, red_color_filter("red"))
        assert same_scad_color(self.gamma, green_color_filter("green"))
        assert red_color_filter("green") == REJECT_ALL
        assert green_color_filter("red") == REJECT_ALL
