from typing import Generator, Iterable, List, Optional, Tuple
import re

from .emoji import Emoji
from .style import _STYLE_RE, Style, StyleType
from .segment import Segment
from .errors import MarkupError


def _parse(markup: str) -> Generator:
    position = 0

    for match in _STYLE_RE.finditer(markup):
        full_text, fx, pure_text, color, bg_color = match.groups()
        start, end = match.span()
        if start > position:
            yield markup[position:start], None, None, None
        if fx or color or bg_color:
            yield pure_text, fx, color, bg_color
            position = end

    if position < len(markup):
        yield markup[position:], None, None, None


def render_markup(
    markup: str, style: Optional[StyleType] = None, emoji: bool = True
) -> List[Segment]:
    if emoji:
        markup = Emoji.render_emoji(markup)

    if isinstance(style, str):
        style = Style.parse(style)

    renderables: List[Segment] = []
    for text, fx, color, bg_color in _parse(markup):
        sgr = []
        if fx:
            sgr.append(fx)
        if color:
            sgr.append(color)
        if bg_color:
            sgr.extend(("on", bg_color))

        if style:
            sep_style = style + Style.parse(" ".join(sgr))
        else:
            sep_style = Style.parse(" ".join(sgr))

        renderables.append(Segment(text, style=sep_style))

    return renderables


tag_re = re.compile(r"((\\*)\[([a-z#/@][^[]*?)])", re.VERBOSE)


def parse(string: str) -> Iterable[Tuple[int, Optional[str], Optional[str]]]:
    position: int = 0

    for match in tag_re.finditer(string):
        full_text, escapes, tag_text = match.groups()
        start, end = match.span()

        if start > position:
            # start position, text, tag
            yield start, string[position:start], None
        if escapes:
            backslashes, escaped = divmod(len(escapes), 2)
            if backslashes:
                #  Literal backslashes
                yield start, "\\" * backslashes, None
                start += backslashes * 2
            if escaped:
                # Escape of tag
                yield start, full_text[len(escapes) :], None
                position = end
                continue

        text, equals, parameters = tag_text.partition("=")
        yield start, None, text
        position = end

    if position < len(string):
        yield position, string[position:], None


def markup(string: str, style: Optional[str] = None, emoji: bool = True):

    text: List = []
    text_append = text.append

    style_stack: List = []
    style_pop = style_stack.pop

    spans: List = []
    append_span = spans.append

    for position, plain_text, tag in parse(string):
        if plain_text is not None:
            plain_text = plain_text.replace("\\[", "[")
            text.append(plain_text)
        elif tag is not None:
            if tag.startswith("/"):
                style_name = tag[1:].strip()

                if not style_name:
                    # Invalid closing tag
                    raise MarkupError("Invalid tag without any content") from None

                style_name = style_name
                try:
                    start, open_tag = style_pop()
                except IndexError:
                    # No corresponding open tag found
                    raise MarkupError("tag not have open") from None

                # The closing tag needs to be the same as the nearest opening tag
                if style_name != open_tag.strip():
                    raise MarkupError(
                        f"the closing tag '{tag}' not same with the open tag '{open_tag}'"
                    ) from None

                append_span((start, len(text), open_tag))

            else:  # Open Tag
                style_stack.append((len(text), tag))

    text_length = len(text)
    while style_stack:
        start, tag = style_pop()
        if style := str(tag):
            append_span((start, text_length, style))

    print(text, spans)
