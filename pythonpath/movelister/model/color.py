class Color:
    """
    Class to extract different color values from single value.
    In UNO api color values are represented by one long value.
    """
    def __init__(self, colorValue):
        self.value = colorValue

    @property
    def value(self):
        color = self.blue
        color |= self.green << (8 * 1)
        color |= self.red << (8 * 2)
        color |= self.alpha << (8 * 3)
        return color & 0xFFFFFFF

    @value.setter
    def value(self, value):
        self.blue = (value >> (8 * 0)) & 0xFF
        self.green = (value >> (8 * 1)) & 0xFF
        self.red = (value >> (8 * 2)) & 0xFF
        self.alpha = (value >> (8 * 3)) & 0xF
