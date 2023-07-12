from .sprite import BaseSprite
from ..utils import get_sprite_map
from itertools import cycle


class Moon(BaseSprite):
    def __init__(self, *args, **kwargs):
        """Create a moon."""
        self.phases = cycle((
            get_sprite_map().get_region(1234, 47, 40, 82),
            get_sprite_map().get_region(1194, 47, 40, 82),
            get_sprite_map().get_region(1154, 47, 40, 82),
            get_sprite_map().get_region(1074, 47, 80, 82),
            get_sprite_map().get_region(1034, 47, 40, 82),
            get_sprite_map().get_region(994, 47, 40, 82),
            get_sprite_map().get_region(954, 47, 40, 82)
        ))
        image = next(self.phases)
        super().__init__(image, *args, **kwargs)

    def set_next_phase(self):
        """Set the next phase of the moon's cycle."""
        self.x += 3000
        self.image = next(self.phases)

    def update(self, dt):
        """Update the moon."""
        if self.x + 80 < 0:
            self.set_next_phase()

        super().update(dt)
