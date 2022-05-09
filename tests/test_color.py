import pytest
from plenty.color import Color, COLOR_CODE


@pytest.mark.parametrize(
    ["input_", "wanted"],
    [
        ["#FF0000", True],
        ["#FF0", False],
        ["#F0", True],
        [[255, 0, 0], True],
        [(255, 0, 0), True],
        [[-1, 0, 0], False],
        ["red", True],
        [None, False],
        [123456, False],
    ],
)
def test_is_color(input_, wanted):
    assert Color.is_color(input_) == wanted


@pytest.mark.parametrize(
    "color_string",
    [
        None,
        "#FF0000",
        "#f0",
        (205, 255, 0),
        "green",
    ],
)
def test_instance(color_string):
    color = Color(color_string)
    print(color.hex, color.rgb, repr(color.escape))
    print(repr(color))


def test_generator():
    print(repr(Color.fg("#ff0000")))
    print(repr(Color.bg("#ff000f")))
    print(repr(Color.by_name("red", depth="aa")))
    print(repr(Color.by_name("#ff0000")))
    print(Color.escape_color(None))
