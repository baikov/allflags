from colorsys import rgb_to_hls


class Colorize:
    def __init__(self, color=None, **kwargs):

        self._color = color if color else (255, 255, 255)

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def rgb(self):
        """An RGB representation of the color."""
        return self._color

    @rgb.setter
    def rgb(self, value):
        self._color = value

    @property
    def hex(self):
        """A 6-char HEX representation of the color."""
        return self.__rgb_to_hex(self.rgb)

    @hex.setter
    def hex(self, value):
        self._color = self.__hex_to_rgb(value)

    @property
    def cmyk(self) -> list:
        """A CMYK representation of the color."""
        return self.__rgb_to_cmyk(self.rgb)

    @cmyk.setter
    def cmyk(self, value):
        self._color = self.__cmyk_to_rgb(value)

    @property
    def hsl(self) -> list:
        return self.__rgb_to_hsl(self.rgb)

    def __rgb_to_hex(self, rgb: tuple) -> str:
        """
        Convert an RGB color representation to a HEX color representation.
        (r, g, b) :: r -> [0, 255]
                    g -> [0, 255]
                    b -> [0, 255]
        :param rgb: A tuple of three numeric values corresponding to the red, green, and blue value.
        :return: HEX representation of the input RGB value.
        :rtype: str
        """
        r, g, b = rgb
        return "%02x%02x%02x" % (r, g, b)

    def __hex_to_rgb(self, hex: str):
        # r, g, b = (int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        # return r, g, b
        return list(int(hex.lstrip("#")[i: i + 2], 16) for i in (0, 2, 4))  # E203

    def __rgb_to_cmyk(self, rgb: tuple):
        r, g, b = rgb
        k = 1 - (max(r, g, b) / 255)
        c = (1 - r / 255 - k) / (1 - k)
        m = (1 - g / 255 - k) / (1 - k)
        y = (1 - b / 255 - k) / (1 - k)
        return [round(c * 100), round(m * 100), round(y * 100), round(k * 100)]

    def __cmyk_to_rgb(self, cmyk: tuple):
        c, m, y, k = cmyk
        r = round(255 * (1 - c / 100) * (1 - k / 100))
        g = round(255 * (1 - m / 100) * (1 - k / 100))
        b = round(255 * (1 - y / 100) * (1 - k / 100))
        return r, g, b

    def __rgb_to_hsl(self, rgb: tuple) -> tuple:
        rgb_float = (x / 255 for x in rgb)
        hue, sat, light = tuple(round(x, 2) for x in rgb_to_hls(*rgb_float))
        return (round(360 * hue), sat * 100, light * 100)  # return HSL not HLS

    def __iter__(self):
        """Iterator"""
        return iter(self._color)

    def __str__(self):
        """String representation"""
        return "{}".format(self._color)

    def __repr__(self):
        """General representation"""
        return "<Color {}>".format(self._color)
