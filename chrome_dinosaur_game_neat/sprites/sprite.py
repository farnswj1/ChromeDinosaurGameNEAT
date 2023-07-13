from pyglet.sprite import Sprite


class BaseSprite(Sprite):
    def __init__(self, image, x, y, velx=0, vely=0, *args, **kwargs):
        """Create a base sprite."""
        # Inherit the sprite class
        super().__init__(image, x, y, *args, **kwargs)

        # Save the velocity of the sprite relative to the screen
        self.velx = velx
        self.vely = vely

    def update(self, dt):
        """Update the sprite."""
        self.x += self.velx * dt
        self.y += self.vely * dt

    def __del__(self):
        """Delete the sprite."""
        try:
            # Attempt to delete the sprite from video memory if available
            self.delete()
        except:
            pass
