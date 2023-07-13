from pyglet.text import Label
from ...constants import FONT_NAME, POPULATION_SIZE, WINDOW_HEIGHT


class DinosaurCountDisplay(Label):
    def __init__(self, batch, group, night_mode=False):
        """Create a HUD item that shows the number of dinosaurs."""
        self.dinosaur_count = POPULATION_SIZE
        super().__init__(
            f"DINOSAURS: {self.dinosaur_count:03}",
            font_name=FONT_NAME,
            font_size=20,
            color=(255, 255, 255, 255) if night_mode else (0, 0, 0, 255),
            x=10,
            y=WINDOW_HEIGHT - 40,
            anchor_x="left",
            anchor_y="top",
            batch=batch,
            group=group
        )

    def increment(self, value):
        """Update the count by adding the value to the current count."""
        self.set(self.dinosaur_count + value)

    def set(self, value):
        """Set the count to a specific value."""
        self.dinosaur_count = value
        self.text = f"DINOSAURS: {self.dinosaur_count:03}"
