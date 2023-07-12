from .sprite import BaseSprite
from ..utils import get_sprite_map
import random


class Cactus(BaseSprite):
    IMAGES = [
        get_sprite_map().get_region(446, 58, 34, 70),   # Small cacti 1
        get_sprite_map().get_region(480, 58, 68, 70),   # Small cacti 2
        get_sprite_map().get_region(548, 58, 102, 70),  # Small cacti 3
        get_sprite_map().get_region(652, 32, 50, 98),   # Large cacti 1
        get_sprite_map().get_region(702, 32, 100, 98),  # Large cacti 2
        get_sprite_map().get_region(802, 30, 150, 98),  # Large cacti 3
    ]

    def __init__(self, *args, **kwargs):
        """Create a cactus."""
        image = random.choice(self.IMAGES)
        super().__init__(image, *args, **kwargs)
