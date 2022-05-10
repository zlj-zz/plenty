class Fx(object):
    """Text effects
    * trans(string: str): Replace whitespace with escape move right to not
        overwrite background behind whitespace.

    """

    start = "\033["  # * Escape sequence start
    sep = ";"  # * Escape sequence separator
    end = "m"  # * Escape sequence end
    # * Reset foreground/background color and text effects
    reset = rs = "\033[0m"
    bold = b = "\033[1m"  # * Bold on
    unbold = ub = "\033[22m"  # * Bold off
    dark = d = "\033[2m"  # * Dark on
    undark = ud = "\033[22m"  # * Dark off
    italic = i = "\033[3m"  # * Italic on
    unitalic = ui = "\033[23m"  # * Italic off
    underline = u = "\033[4m"  # * Underline on
    ununderline = uu = "\033[24m"  # * Underline off
    blink = bl = "\033[5m"  # * Blink on
    unblink = ubl = "\033[25m"  # * Blink off
    strike = s = "\033[9m"  # * Strike / crossed-out on
    unstrike = us = "\033[29m"  # * Strike / crossed-out off

    supports = {
        "bold": "bold",
        "b": "bold",
        "dark": "dark",
        "d": "dark",
        "italic": "italic",
        "i": "italic",
        "underline": "underline",
        "u": "underline",
        "strike": "strike",
        "s": "strike",
        "blink": "blink",
    }

    code_map = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "9",
    }

    # * Precompiled regex for finding a 24-bit color escape sequence in a string

    @staticmethod
    def trans(string):
        return string.replace(" ", "\033[1C")

    @classmethod
    def by_name(cls, name: str) -> str:
        try:
            fx_code = getattr(cls, name)
        except AttributeError:
            fx_code = ""

        return fx_code
