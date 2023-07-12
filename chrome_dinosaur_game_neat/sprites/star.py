from .sprite import BaseSprite
from ..utils import get_sprite_map
import random


class Star(BaseSprite):
    IMAGES = (
        get_sprite_map().get_region(1274, 74, 18, 18),
        get_sprite_map().get_region(1274, 92, 18, 18),
        get_sprite_map().get_region(1274, 110, 18, 18)
    )

    def __init__(self, *args, **kwargs):
        """Create a star."""
        image = random.choice(self.IMAGES)
        super().__init__(image, *args, **kwargs)

    def update(self, dt, opacity):
        """Update the star."""
        self.opacity = opacity
        super().update(dt)
