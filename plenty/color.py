from typing import Dict, Literal, Optional, Sequence, Tuple, Union
import re

from plenty.errors import ColorError


RGBType = Tuple[int, int, int]
Colorable = Union[str, Sequence[int]]
ColorDepthType = Literal["fg", "bg"]

# color hex string reg.
_COLOR_RE = re.compile(r"^#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{2})$")

COLOR_CODE: Dict[str, str] = {
    "plain": "",
    "light_pink": "#FFB6C1",
    "pink": "#FFC0CB",
    "crimson": "#DC143C",
    "lavender_blush": "#FFF0F5",
    "pale_violet_red": "#DB7093",
    "hot_pink": "#FF69B4",
    "deep_pink": "#FF1493",
    "medium_violet_red": "#C71585",
    "orchid": "#DA70D6",
    "thistle": "#D8BFD8",
    "plum": "#DDA0DD",
    "violet": "#EE82EE",
    "magenta": "#FF00FF",
    "fuchsia": "#FF00FF",
    "dark_magenta": "#8B008B",
    "purple": "#800080",
    "medium_orchid": "#BA55D3",
    "dark_violet": "#9400D3",
    "dark_orchid": "#9932CC",
    "indigo": "#4B0082",
    "blue_violet": "#8A2BE2",
    "medium_purple": "#9370DB",
    "medium_slateBlue": "#7B68EE",
    "slate_blue": "#6A5ACD",
    "dark_slate_blue": "#483D8B",
    "lavender": "#E6E6FA",
    "ghost_white": "#F8F8FF",
    "blue": "#0000FF",
    "medium_blue": "#0000CD",
    "midnight_blue": "#191970",
    "dark_blue": "#00008B",
    "navy": "#000080",
    "royal_blue": "#4169E1",
    "cornflower_blue": "#6495ED",
    "light_steel_blue": "#B0C4DE",
    "light_slate_gray": "#778899",
    "slate_gray": "#708090",
    "dodder_blue": "#1E90FF",
    "alice_blue": "#F0F8FF",
    "steel_blue": "#4682B4",
    "light_sky_blue": "#87CEFA",
    "sky_blue": "#87CEEB",
    "deep_sky_blue": "#00BFFF",
    "light_blue": "#ADD8E6",
    "powder_blue": "#B0E0E6",
    "cadet_blue": "#5F9EA0",
    "azure": "#F0FFFF",
    "light_cyan": "#E1FFFF",
    "pale_turquoise": "#AFEEEE",
    "cyan": "#00FFFF",
    "aqua": "#D4F2E7",
    "dark_turquoise": "#00CED1",
    "dark_slate_gray": "#2F4F4F",
    "dark_cyan": "#008B8B",
    "teal": "#008080",
    "medium_turquoise": "#48D1CC",
    "light_sea_green": "#20B2AA",
    "turquoise": "#40E0D0",
    "aquamarine": "#7FFFAA",
    "medium_aquamarine": "#00FA9A",
    "medium_spring_green": "#00FF7F",
    "mint_cream": "#F5FFFA",
    "spring_green": "#3CB371",
    "sea_green": "#2E8B57",
    "honeydew": "#F0FFF0",
    "light_green": "#90EE90",
    "pale_green": "#98FB98",
    "ok": "#98FB98",
    "good": "#98FB98",
    "right": "#98FB98",
    "dark_sea_green": "#8FBC8F",
    "lime_green": "#32CD32",
    "lime": "#00FF00",
    "forest_green": "#228B22",
    "green": "#008000",
    "dark_green": "#006400",
    "chartreuse": "#7FFF00",
    "lawn_green": "#7CFC00",
    "green_yellow": "#ADFF2F",
    "olive_drab": "#556B2F",
    "beige": "#F5F5DC",
    "light_goldenrod_yellow": "#FAFAD2",
    "ivory": "#FFFFF0",
    "light_yellow": "#FFFFE0",
    "yellow": "#FFFF00",
    "olive": "#808000",
    "dark_khaki": "#BDB76B",
    "lemon_chiffon": "#FFFACD",
    "pale_goldenrod": "#EEE8AA",
    "khaki": "#F0E68C",
    "gold": "#FFD700",
    "cornsilk": "#FFF8DC",
    "goldenrod": "#DAA520",
    "floral_white": "#FFFAF0",
    "old_lace": "#FDF5E6",
    "wheat": "#F5DEB3",
    "moccasin": "#FFE4B5",
    "orange": "#FFA500",
    "papaya_whip": "#FFEFD5",
    "blanched_almond": "#FFEBCD",
    "navajo_white": "#FFDEAD",
    "antique_white": "#FAEBD7",
    "tan": "#D2B48C",
    "burly_wood": "#DEB887",
    "bisque": "#FFE4C4",
    "dark_orange": "#FF8C00",
    "linen": "#FAF0E6",
    "peru": "#CD853F",
    "peach_puff": "#FFDAB9",
    "sandy_brown": "#F4A460",
    "chocolate": "#D2691E",
    "saddle_brown": "#8B4513",
    "sea_shell": "#FFF5EE",
    "sienna": "#A0522D",
    "light_salmon": "#FFA07A",
    "coral": "#FF7F50",
    "orange_red": "#FF4500",
    "dark_salmon": "#E9967A",
    "tomato": "#FF6347",
    "bad": "#FF6347",
    "error": "#FF6347",
    "misty_rose": "#FFE4E1",
    "salmon": "#FA8072",
    "snow": "#FFFAFA",
    "light_coral": "#F08080",
    "rosy_brown": "#BC8F8F",
    "indian_red": "#CD5C5C",
    "red": "#FF0000",
    "brown": "#A52A2A",
    "fire_brick": "#B22222",
    "dark_red": "#8B0000",
    "maroon": "#800000",
    "white": "#FFFFFF",
    "white_smoke": "#F5F5F5",
    "bright_gray": "#DCDCDC",
    "light_grey": "#D3D3D3",
    "silver": "#C0C0C0",
    "dark_gray": "#A9A9A9",
    "gray": "#808080",
    "dim_gray": "#696969",
    "black": "#000000",
}


class Color:
    """Holds representations for a 24-bit color value.

    * Values:
        .hex: str
        .dec: Tuple[int, int, int]
        .red: int
        .green: int
        .blue: int
        .depth: str
        .escape: str
    """

    hex: str
    rgb: RGBType
    red: int
    green: int
    blue: int
    depth: str
    escape: str
    default: bool

    TRUE_COLOR: bool = False

    def __init__(
        self,
        value: Optional[Colorable] = None,
        depth: ColorDepthType = "fg",
        default: bool = False,
    ) -> None:
        """Initial a Color object.

        Args:
            color (Optional[ColorType], optional): color value. Defaults to None.
            depth (ColorDepthType, optional): color type. Defaults to "fg".
            default (bool, optional): whether has default value. Defaults to False.
        """

        self.depth = depth
        self.default = default

        # If `color` is None or empty.
        if not value:
            self.rgb = (-1, -1, -1)
            self.hex = ""
            self.red = self.green = self.blue = -1
            self.escape = "\033[49m" if depth == "bg" and default else ""
            return

        # Check the color code whether right.
        if not self.is_color(value):
            raise ColorError(f"Not valid color: {value}.") from None

        if isinstance(value, str):
            if value in COLOR_CODE:
                value = COLOR_CODE[value]

            self.rgb = rgb = self.generate_rgb(value)
            self.hex = value

        elif isinstance(value, (list, tuple)):
            self.rgb = rgb = (value[0], value[1], value[2])

            # sourcery skip: replace-interpolation-with-fstring
            self.hex = "#%s%s%s" % (
                hex(rgb[0]).lstrip("0x").zfill(2),
                hex(rgb[1]).lstrip("0x").zfill(2),
                hex(rgb[2]).lstrip("0x").zfill(2),
            )

        elif isinstance(value, Color):
            raise ColorError("The color is already Color.") from None

        else:
            raise ColorError(
                "The type of color not support translate to Color."
            ) from None

        self.escape = self.escape_color(r=rgb[0], g=rgb[1], b=rgb[2], depth=depth)

    def __str__(self):
        return self.escape

    def __repr__(self):
        return f"<Color hex={self.hex} rgb={self.rgb} escape={repr(self.escape)} >"

    def __iter__(self):
        yield from self.rgb

    @staticmethod
    def generate_rgb(hex: str) -> Tuple[int, int, int]:
        hex_len = len(hex)
        try:
            if hex_len == 3:
                c = int(hex[1:], base=16)
                rgb = (c, c, c)
            elif hex_len == 7:
                rgb = (
                    int(hex[1:3], base=16),
                    int(hex[3:5], base=16),
                    int(hex[5:7], base=16),
                )
        except ValueError:
            raise ColorError(f"The hex `{hex}` of color can't to be parsing.") from None
        else:
            return rgb

    @staticmethod
    def true_color_to_256(rgb: Tuple[int, int, int]) -> int:

        grayscale = (rgb[0] // 11, rgb[1] // 11, rgb[2] // 11)
        if grayscale[0] == grayscale[1] == grayscale[2]:
            return 232 + grayscale[0]
        else:
            return (
                round(rgb[0] / 51) * 36
                + round(rgb[1] / 51) * 6
                + round(rgb[2] / 51)
                + 16
            )

    @classmethod
    def escape_color(
        cls,
        hex: Optional[str] = None,
        r: int = 0,
        g: int = 0,
        b: int = 0,
        depth: ColorDepthType = "fg",
    ) -> str:
        """Returns escape sequence to set color

        Args:
            hex (str): accepts either 6 digit hexadecimal hex="#FF0000",
                        2 digit hexadecimal: hex="#FF".
            r (int): 0-255, the r of decimal RGB.
            g (int): 0-255, the g of decimal RGB.
            b (int): 0-255, the b of decimal RGB.

        Returns:
            color (str): ascii color code.
        """

        dint = 38 if depth == "fg" else 48
        rgb = cls.generate_rgb(hex) if hex else (r, g, b)

        if not Color.TRUE_COLOR:
            return "\033[{};5;{}m".format(dint, Color.true_color_to_256(rgb=rgb))

        return "\033[{};2;{};{};{}m".format(dint, *rgb)

    @classmethod
    def fg(cls, value: Colorable) -> "Color":
        return cls(value, depth="fg")

    @classmethod
    def bg(cls, value: Colorable) -> "Color":
        return cls(value, depth="bg")

    @classmethod
    def by_name(cls, name: str, depth: ColorDepthType = "fg") -> "Color":
        """Get color ascii code by support color name."""

        color_hex = COLOR_CODE.get(name, "")

        if depth == "fg":
            return cls.fg(color_hex)
        elif depth == "bg":
            return cls.bg(color_hex)
        else:
            return cls()

    @staticmethod
    def is_color(code: Optional[Colorable]) -> bool:
        """Return True if code is color else False.
        Like: '#FF0000', '#FF', 'red', [255, 0, 0], (0, 255, 0)
        """

        if type(code) == str:
            return (
                code.startswith("#") and _COLOR_RE.match(str(code)) is not None
            ) or COLOR_CODE.get(code) is not None

        elif isinstance(code, (list, tuple)):
            return len(code) == 3 and all(0 <= c <= 255 for c in code)

        else:
            return False
