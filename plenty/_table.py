from typing import List, Optional
from dataclasses import dataclass

from .box import HEAVY_HEAD, Box
from .segment import Segment
from .ratio import ratio_reduce


@dataclass
class BaseTb:
    """A base class of all table class."""

    title: Optional[str] = ""
    caption: Optional[str] = ""
    box: Box = HEAVY_HEAD
    width: Optional[int] = None
    show_edge: bool = True
    show_lines: bool = False
    show_header: bool = True
    title_style: Optional[str] = None
    caption_style: Optional[str] = None
    border_style: Optional[str] = None

    def _collapse_widths(
        self, widths: List[int], wrapable: List[bool], max_width: int
    ) -> List[int]:
        """Reduce widths so that the total is under max_width.

        Args:
            widths (List[int]): List of widths.
            wrapable (List[bool]): List of booleans that indicate if a column may shrink.
            max_width (int): Maximum width to reduce to.

        Returns:
            List[int]: A new list of widths.
        """

        total_width = sum(widths)
        excess_width = total_width - max_width

        if any(wrapable):
            while total_width and excess_width > 0:
                max_column = max(
                    width for width, allow_wrap in zip(widths, wrapable) if allow_wrap
                )
                second_max_column = max(
                    width if allow_wrap and width != max_column else 0
                    for width, allow_wrap in zip(widths, wrapable)
                )
                column_difference = max_column - second_max_column

                ratios = [
                    (1 if (width == max_column and allow_wrap) else 0)
                    for width, allow_wrap in zip(widths, wrapable)
                ]
                if not any(ratios) or not column_difference:
                    break
                max_reduce = [min(excess_width, column_difference)] * len(widths)
                widths = ratio_reduce(excess_width, ratios, max_reduce, widths)

                total_width = sum(widths)
                excess_width = total_width - max_width

        return widths

    def set_shape(self, height: int, lines: List, width: int) -> List[Segment]:
        extra_lines = height - len(lines)
        blank = [Segment(" " * width)]
        shaped_lines = lines[:height]
        if extra_lines:
            shaped_lines = lines + [blank * extra_lines]

        return shaped_lines
