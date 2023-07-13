from pyglet.text import Label
from ...constants import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME


class GameOverDisplay(Label):
    def __init__(self, batch, group, night_mode=False):
        """Create a Game Over button."""
        super().__init__(
            "G A M E  O V E R",
            font_name=FONT_NAME,
            font_size=30,
            color=(255, 255, 255, 255) if night_mode else (0, 0, 0, 255),
            x=WINDOW_WIDTH / 2,
            y=WINDOW_HEIGHT / 2 + 100,
            anchor_x="center",
            anchor_y="center",
            batch=batch,
            group=group
        )
