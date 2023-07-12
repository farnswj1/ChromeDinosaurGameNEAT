from .sprite import BaseSprite
from ..utils import get_sprite_map


class Cloud(BaseSprite):
    IMAGES = [get_sprite_map().get_region(165, 100, 95, 28)]

    def __init__(self, *args, **kwargs):
        """Create a cloud."""
        image = self.IMAGES[0]
        super().__init__(image, *args, **kwargs)
