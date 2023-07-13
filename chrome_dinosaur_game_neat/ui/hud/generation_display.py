from pyglet.text import Label
from ...constants import FONT_NAME, WINDOW_HEIGHT


class GenerationDisplay(Label):
    def __init__(self, batch, group, night_mode=False):
        """Create a HUD item that shows the generation number."""
        self.generation_number = -1
        super().__init__(
            f"GENERATION: {self.generation_number:02}",
            font_name=FONT_NAME,
            font_size=20,
            color=(255, 255, 255, 255) if night_mode else (0, 0, 0, 255),
            x=10,
            y=WINDOW_HEIGHT - 10,
            anchor_x="left",
            anchor_y="top",
            batch=batch,
            group=group
        )

    def increment(self, value):
        """Update the generation number by adding the value to the current generatio."""
        self.set(self.generation_number + value)

    def set(self, value):
        """Set the generation number to a specific value."""
        self.generation_number = value
        self.text = f"GENERATION: {self.generation_number:02}"
