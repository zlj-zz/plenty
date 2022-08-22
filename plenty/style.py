from typing import List, Optional, Match, Pattern, Union
import re

from plenty.color import Color, Colorable
from plenty.effect import TextEffect

from .errors import StyleSyntaxError


# If has special format string, will try to render the color and font style.
# If cannot to render the string will keep it.
#
# .+-----------------------------------> font style prefix (options).
#  |         +-------------------------> the content being rendered.
#  |         |             +-----------> color code or color name, like: blue (options).
#  |         |             |       +---> background color code.
#  |         |             |       |
#  |         |             |       |
#  b`This is a string.`<#FF0000,#00FF00>
#
# Must keep has one of font style or color for making sure can right render.
# If ignore the two both, it will do nothing.
# Only '`' with consecutive beginning and ending will be considered part of the content.
_STYLE_RE: Pattern[str] = re.compile(
    r"(([a-z]+|\((?:[a-z\s],?)+\))?`(`*.*?`*)`(?:<([a-zA-Z_]+|#[0-9a-fA-F]{6})?(?:,([a-zA-Z_]+|#[0-9a-fA-F]{6}))?>)?)",
    re.M | re.S,  # allow multi lines.
)

_STYLE_ANSI_RE: Pattern[str] = re.compile(r"\033\[\d+;\d?;?\d*;?\d*;?\d*m|\033\[\d+m")

# [yellow]Today[/yellow] is a nice [red]day[/red]


class Style(object):
    def __init__(
        self,
        *,
        color: Optional[Colorable] = None,
        bg_color: Optional[Colorable] = None,
        bold: Optional[bool] = None,
        dark: Optional[bool] = None,
        italic: Optional[bool] = None,
        underline: Optional[bool] = None,
        blink: Optional[bool] = None,
        strick: Optional[bool] = None,
    ) -> None:
        self.color = color if Color.is_color(color) else None
        self.bg_color = bg_color if Color.is_color(bg_color) else None

        self._set_attributes: int = sum(
            (
                bold is not None and 1,
                dark is not None and 2,
                italic is not None and 4,
                underline is not None and 8,
                blink is not None and 16,
                strick is not None and 32,
            )
        )
        self._attributes: int = sum(
            (
                bold and 1 or 0,
                dark and 2 or 0,
                italic and 4 or 0,
                underline and 8 or 0,
                blink and 16 or 0,
                strick and 32 or 0,
            )
        )

        self._style_definition: Optional[str] = None
        self._ansi: Optional[str] = None
        self._null = not (self._set_attributes or color or bg_color)

    def __str__(self) -> str:
        if self._style_definition is None:
            style_res: List[str] = []
            append = style_res.append

            bits = self._set_attributes
            bits2 = self._attributes
            if bits & 0b000001111:
                if bits & 1:
                    append("bold" if bits2 & 1 else "not bold")
                if bits & (1 << 1):
                    append("dark" if bits2 & (1 << 1) else "not dark")
                if bits & (1 << 2):
                    append("italic" if bits2 & (1 << 2) else "not italic")
                if bits & (1 << 3):
                    append("underline" if bits2 & (1 << 3) else "not underline")
            if bits & 0b111110000:
                if bits & (1 << 4):
                    append("blink" if bits2 & (1 << 4) else "not blink")
                if bits & (1 << 5):
                    append("strick" if bits2 & (1 << 5) else "not strick")

            if self.color:
                style_res.append(str(self.color))
            if self.bg_color:
                style_res.extend(("on", str(self.bg_color)))

            self._style_definition = " ".join(style_res) or "none"

        return self._style_definition

    def _make_ansi_code(self) -> str:
        if self._ansi is None:
            sgr: List[str] = []
            fx_map = TextEffect.Code_Map

            if attributes := self._set_attributes & self._attributes:
                sgr.extend(fx_map[bit] for bit in range(6) if attributes & (1 << bit))

            self._ansi = f"{TextEffect.START}{TextEffect.SEP.join(sgr)}{TextEffect.END}"
            if self.color:
                self._ansi += Color.fg(self.color).escape
            if self.bg_color:
                self._ansi += Color.bg(self.bg_color).escape

        # print(repr(self._ansi))
        return self._ansi

    def render(self, text: str) -> str:
        attrs = self._make_ansi_code()
        return f"{attrs}{text}{TextEffect.RESET}" if attrs else text

    def test(self, text: Optional[str] = None) -> None:
        text = text or str(self)
        print(self.render(text))

    def __add__(self, style: Optional["Style"]) -> "Style":
        if not (isinstance(style, Style) or Style is None):
            return NotImplemented

        if style is None or style._null:
            return self

        new_style: Style = self.__new__(Style)
        new_style._ansi = None
        new_style._style_definition = None
        new_style.color = style.color or self.color
        new_style.bg_color = style.bg_color or self.bg_color
        new_style._attributes = (self._attributes & ~style._set_attributes) | (
            style._attributes & style._set_attributes
        )
        new_style._set_attributes = self._set_attributes | style._set_attributes
        new_style._null = style._null or self._null

        return new_style

    @classmethod
    def plain(cls, text: str):
        """Remove color ansi code from text."""
        return _STYLE_ANSI_RE.sub("", text)

    @classmethod
    def parse(cls, style_definition: str) -> "Style":
        FX_ATTRIBUTES = TextEffect.Supports
        color = ""
        bg_color = ""
        attributes = {}

        words = iter(style_definition.split())
        for original_word in words:
            word = original_word.lower()

            if word == "on":
                word = next(words, "")
                if not word:
                    raise StyleSyntaxError("color expected after 'on'")
                if Color.is_color(word):
                    bg_color = word
                else:
                    raise StyleSyntaxError(
                        f"unable to parse {word!r} as background color."
                    )

            elif word in FX_ATTRIBUTES:
                attributes[FX_ATTRIBUTES[word]] = True

            elif Color.is_color(word):
                color = word
            else:
                raise StyleSyntaxError(f"unable to parse {word!r} as color.")

        return Style(color=color, bg_color=bg_color, **attributes)

    @classmethod
    def null(cls) -> "Style":
        return NULL_STYLE

    @staticmethod
    def render_style(_msg: str, /, *, _style_sub=_STYLE_RE.sub) -> str:
        def do_replace(match: Match[str]) -> str:
            raw, fx_tag, content, color_code, bg_color_code = match.groups()
            # print(raw, fx_tag, content, color_code, bg_color_code)

            if not color_code and not fx_tag and not bg_color_code:
                return raw

            try:
                if fx_tag is None:
                    # No fx then get empty.
                    font_style = ""
                elif fx_tag.startswith("(") and fx_tag.endswith(")"):
                    # Has multi fx tags.
                    fx_tag = fx_tag[1:-1]
                    font_style = "".join(
                        TextEffect.by_name(fx_code.strip())
                        for fx_code in fx_tag.split(",")
                    )
                else:
                    # Only one.
                    font_style = TextEffect.by_name(fx_tag)

                # Get color hex.
                if color_code and color_code.startswith("#"):
                    color_style = Color.fg(color_code)
                else:
                    color_style = Color.by_name(color_code, depth="fg")

                if bg_color_code and bg_color_code.startswith("#"):
                    bg_color_style = Color.bg(bg_color_code)
                else:
                    bg_color_style = Color.by_name(bg_color_code, depth="bg")

                return f"{font_style}{color_style}{bg_color_style}{content}\033[0m"
            except KeyError:
                return raw

        return _style_sub(do_replace, _msg)

    @classmethod
    def remove_style(cls, _msg: str, /, *, _style_sub=_STYLE_RE.sub) -> str:
        def do_replace(match: Match[str]) -> str:
            raw, fx, content, color_code, color_bg_code = match.groups()

            if not color_code and not fx and not color_bg_code:
                return raw

            return content

        return _style_sub(do_replace, _msg)

    @classmethod
    def clear_text(cls, _msg: str) -> str:
        return cls.plain(cls.remove_style(_msg))


NULL_STYLE = Style()

StyleType = Union[Style, str]
