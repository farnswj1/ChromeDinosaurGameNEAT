from pyglet.image import ImageGrid, Animation
from .sprite import BaseSprite
from ..utils import get_sprite_map


class Bird(BaseSprite):
    IMAGES = [
        Animation.from_image_sequence(
            ImageGrid(
                image=get_sprite_map().get_region(260, 48, 184, 80),
                rows=1,
                columns=2,
                item_width=92,
                item_height=80
            ),
            duration=0.3,
            loop=True
        )
    ]

    def __init__(self, *args, **kwargs):
        """Create a bird."""
        image = self.IMAGES[0]
        super().__init__(image, *args, **kwargs)
