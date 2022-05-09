import pytest
from plenty.str_utils import *


@pytest.mark.parametrize(
    ["chr", "wanted"],
    [
        ("a", 1),
        ("中", 2),
        ("Ç", 1),
    ],
)
def test_get_width(chr, wanted):
    assert get_width(ord(chr)) == wanted


def test_shorten():
    assert shorten("Hello world!", 9, placeholder="^-^") == "Hello ^-^"
    assert shorten("Hello world!", 9, placeholder="^-^", front=True) == "^-^world!"


def test_chop_cells():
    assert chop_cells("12345678", 4) == ["1234", "5678"]
    assert chop_cells("12345678", 10) == ["12345678"]


@pytest.mark.parametrize(
    ["cell", "size", "wanted"],
    [
        ("123456", 4, "1234"),
        ("123456", 6, "123456"),
        ("123456", 8, "123456  "),
        ("床前明月光", 4, "床前"),
    ],
)
def test_set_cell_size(cell, size, wanted):
    assert set_cell_size(cell, size) == wanted


def test_byte_str2str():
    s = byte_str2str(
        "test/\\346\\265\\213\\350\\257\\225\\344\\270\\255\\346\\226\\207.py"
    )
    print(s)
    assert s == "test/测试中文.py"
