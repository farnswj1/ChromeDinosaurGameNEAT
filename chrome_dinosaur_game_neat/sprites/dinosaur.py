from pyglet.image import ImageGrid, Animation
from neat.nn import FeedForwardNetwork
from .sprite import BaseSprite
from ..utils import get_sprite_map


class Dinosaur(BaseSprite):
    RUN_ANIMATION = Animation.from_image_sequence(
        ImageGrid(
            image=get_sprite_map().get_region(1854, 33, 176, 95),
            rows=1,
            columns=2,
            item_width=88,
            item_height=96
        ),
        duration=0.3,
        loop=True
    )
    DUCK_ANIMATION = Animation.from_image_sequence(
        ImageGrid(
            image=get_sprite_map().get_region(2203, 33, 240, 61),
            rows=1,
            columns=2,
            item_width=118,
            item_height=62
        ),
        duration=0.3,
        loop=True
    )
    JUMP_IMG = get_sprite_map().get_region(1678, 33, 88, 95)
    COLLISION_IMG = get_sprite_map().get_region(2030, 33, 88, 95)

    def __init__(self, *args, **kwargs):
        """Create a dinosaur."""
        # Inherit the game sprite class
        image = self.RUN_ANIMATION
        super().__init__(image, *args, **kwargs)

        # Jumping and ducking variables keep track of the dinosaur's actions
        self.jumping = False
        self.ducking = False

    def jump(self):
        """Make the dinosaur jump."""
        self.vely = 1200
        self.image = self.JUMP_IMG
        self.jumping = True

    def land(self):
        """Stop the dinosaur from falling."""
        self.y = 45
        self.vely = 0
        self.image = self.RUN_ANIMATION
        self.jumping = False

    def duck(self):
        """Make the dinosaur duck."""
        self.image = self.DUCK_ANIMATION
        self.ducking = True

    def rise(self):
        """Make the dinosaur stand up straight."""
        self.image = self.RUN_ANIMATION
        self.ducking = False

    def collided(self):
        """Update the dinosaur if it collided with an object."""
        self.image = self.COLLISION_IMG

    def reset(self, y):
        """Reset the dinosaur."""
        self.y = y
        self.vely = 0
        self.image = self.RUN_ANIMATION
        self.jumping = False
        self.ducking = False

    def has_collided(self, obstacle):
        """Check if the dinosaur runs into the obstacle."""
        # If one sprite is on left side of other, then no collision is possible
        if self.x + self.width <= obstacle.x or obstacle.x + obstacle.width <= self.x:
            return False

        # If one sprite is above other, then no collision is possible
        if self.y + self.height <= obstacle.y or obstacle.y + obstacle.height <= self.y:
            return False

        # The only other outcome is that they overlap
        return True

    def update(self, dt, controller):
        """Update the dinosaur. If an output is provided, use it to control the dinosaur."""
        if self.jumping:
            # Check if it has landed
            if self.y <= 45 and self.vely <= 0:
                self.land()
            else:
                # Decrement the dinosaur's vertical velocity
                self.vely -= 75

        if controller:
            # Determine if the dinosaur should duck or jump
            if controller[0] > 0.5 and not self.jumping and not self.ducking:
                # Start ducking animation
                self.duck()
            elif controller[0] <= 0.5 and not self.jumping and self.ducking:
                # End duck animation
                self.rise()
            elif controller[1] > 0.5 and not self.jumping and not self.ducking:
                # Start jumping animation
                self.jump()

        super().update(dt)


class DinosaurAI(Dinosaur):
    def __init__(self, *args, **kwargs):
        """Create a dinosaur that is controlled by AI."""
        genome = kwargs.pop('genome', None)
        config = kwargs.pop('config', None)

        if genome is None:
            raise ValueError('A genome must be provided!')
        elif config is None:
            raise ValueError('A config must be provided!')

        super().__init__(*args, **kwargs)
        genome.fitness = 0  # Start with fitness value at 0
        self.neural_net = FeedForwardNetwork.create(genome, config)
        self.genome = genome

    def think(self, obstacle):
        """Let the AI make a decision by itself."""
        return self.neural_net.activate((
            self.y,
            obstacle.y,
            obstacle.width,
            obstacle.height,
            abs(self.x + self.width - obstacle.x),  # Distance
            obstacle.velx
        )) if obstacle else None

    def reward(self, dt):
        """Reward the dinosaur for surviving."""
        self.genome.fitness += dt
