from .ui.window import Window


def run(enable_neat=False, night_mode=False):
    """Run the game"""
    Window(enable_neat=enable_neat, night_mode=night_mode)