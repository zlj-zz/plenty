# -*- coding:utf-8 -*-
import pytest

# from .utils import analyze_it

from plenty.console import Console
from plenty.markup import render_markup


@pytest.mark.parametrize(
    "text",
    [
        "Today is a b`nice` `day`<green,red>. bye.",
    ],
)
def test_style_render_markup(text: str):
    print("\n", text)
    render_markup(text)


def test_console():
    console = Console()
    console.echo([1, 2, 3, 4, 5])
