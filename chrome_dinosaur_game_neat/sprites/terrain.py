from .sprite import BaseSprite
from ..utils import get_sprite_map


class Terrain(BaseSprite):
    IMAGES = [get_sprite_map().get_region(2, 0, 2402, 27)]

    def __init__(self, *args, **kwargs):
        """Create a terrain object."""
        image = self.IMAGES[0]
        super().__init__(image, *args, **kwargs)

    def update(self, dt):
        """Update the terrain."""
        if self.x + self.width < 0:
            self.x += 2 * self.width

        super().update(dt)
