from solid import color

from utilities import REJECT_ALL

class ColorFilter:
    def __init__(self, selected_color=None):
        self.selected_color = selected_color

    def __call__(self, color_arg):
        if self.selected_color is None or self.selected_color == color_arg:
            return color(color_arg)
        else:
            return REJECT_ALL
