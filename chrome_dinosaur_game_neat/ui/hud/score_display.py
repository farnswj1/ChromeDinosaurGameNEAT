from pyglet.text import Label
from ...constants import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME


class ScoreDisplay(Label):
    def __init__(self, batch, group, night_mode=False):
        """Create a HUD item that shows the score."""
        self.score = 0
        super().__init__(
            f"{self.score:05}",
            font_name=FONT_NAME,
            font_size=20,
            color=(255, 255, 255, 255) if night_mode else (0, 0, 0, 255),
            x=WINDOW_WIDTH - 10,
            y=WINDOW_HEIGHT - 10,
            anchor_x="right",
            anchor_y="top",
            batch=batch,
            group=group
        )

    def increment(self, value):
        """Update the score by adding the value to the current score."""
        self.set(self.score + value)

    def set(self, value):
        """Set the score to a specific value."""
        self.score = value
        self.text = f"{self.score:05}"
