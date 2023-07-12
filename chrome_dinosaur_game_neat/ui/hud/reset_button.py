from pyglet.sprite import Sprite as BaseSprite
from ...utils import get_sprite_map


class ResetButton(BaseSprite):
    IMAGES = [get_sprite_map().get_region(2, 63, 72, 65)]

    def __init__(self, *args, **kwargs):
        """Create a Reset button."""
        image = self.IMAGES[0]
        super().__init__(image, *args, **kwargs)

    def clicked(self, x, y):
        """Check if the button was clicked based on the coordinates."""
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
