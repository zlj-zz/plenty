class TextEffect:
    """Text effects
    * trans(string: str): Replace whitespace with escape move right to not
        overwrite background behind whitespace.

    """

    START = "\033["  # * Escape sequence start
    SEP = ";"  # * Escape sequence separator
    END = "m"  # * Escape sequence end
    # * Reset foreground/background color and text effects
    RESET = "\033[0m"
    BOLD = "\033[1m"  # * Bold on
    BOLD_OFF = "\033[22m"  # * Bold off
    DARK = "\033[2m"  # * Dark on
    DARK_OFF = "\033[22m"  # * Dark off
    ITALIC = "\033[3m"  # * Italic on
    ITALIC_OFF = "\033[23m"  # * Italic off
    UNDERLINE = "\033[4m"  # * Underline on
    UNDERLINE_OFF = "\033[24m"  # * Underline off
    BLINK = "\033[5m"  # * Blink on
    BLINK_OFF = "\033[25m"  # * Blink off
    STRIKE = "\033[9m"  # * Strike / crossed-out on
    STRIKE_OFF = "\033[29m"  # * Strike / crossed-out off

    Supports = {
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

    Code_Map = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
        5: "9",
    }

    @staticmethod
    def trans(string):
        return string.replace(" ", "\033[1C")

    @classmethod
    def by_name(cls, name: str) -> str:
        try:
            fx_code = getattr(cls, name.upper())
        except AttributeError:
            fx_code = ""

        return fx_code
