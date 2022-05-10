from plenty.emoji import Emoji


def test_right_render():
    print(Emoji.render_emoji("Today is a nice day :rainbow:."))


def test_error_render():
    print(Emoji.render_emoji(" Bad emoji :abcde:"))
