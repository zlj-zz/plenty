import pytest

from plenty.console import Console
from plenty.table import Table, UintTable
from plenty import box


class TestTableModule:
    def test_table(self):
        console = Console()
        # print(Text("`1234`<yellow>"))
        res_t = Table(
            title="Search Result",
            title_style="red",
            # box=box.SIMPLE_HEAD,
            caption="good table",
            caption_style="purple dark",
            border_style="red",
            show_edge=False,
            # show_lines=True
            # show_header=False
        )
        res_t.add_column("Idx", style="green")
        res_t.add_column("Fiction Name", style="yellow")
        res_t.add_column("Last Update", style="cyan")
        res_t.add_column("Other Info")

        res_t.add_row("12", "34", "56", "1")
        res_t.add_row("56", "`sun`<red> is so big.", "10.dark`00`", "1")
        res_t.add_row(
            "我最棒", "9", "25", "100, this is a length test, get large length text."
        )

        console.echo(res_t, "`sun`<red> is so big.")

    def test_unittable(self):
        ut = UintTable(
            title="unit table",
            box=box.DOUBLE_EDGE,
            border_style="sky_blue",
        )

        unit1 = ut.add_unit(
            "Fruit true color", header_style="red bold", values_style="yellow"
        )
        unit1.add_kv("apple", "red, this is a length test.\n second line.")
        unit1.add_kv("grape", "purple")

        unit1 = ut.add_unit("Animal color")
        unit1.add_kv("cattle", "yellow")
        unit1.add_kv(
            "sheep", "white, this is a length test, get large length text." * 10
        )

        console = Console()
        console.echo(ut)
