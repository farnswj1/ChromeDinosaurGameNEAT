'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a subclass of the game sprite in gameObject.py.
'''

# Imported modules
from .gameSprite import GameSprite
from .constants import (
    DINOSAUR_RUN_ANIMATION,
    DINOSAUR_JUMP_IMG,
    DINOSAUR_DUCK_ANIMATION,
    DINOSAUR_COLLISION_IMG
)


# Subclass of the GameSprite class
class Dinosaur(GameSprite):
    # Constructor
    def __init__(self, *args, **kwargs):
        # Inherit the game sprite class
        super().__init__(*args, **kwargs)

        # Jumping and ducking variables keep track of the dinosaur's actions
        self.jumping = False
        self.ducking = False

    
    # Make the dinosaur jump
    def jump(self):
        self.vely = 1200
        self.image = DINOSAUR_JUMP_IMG
        self.jumping = True
    

    # Stop the dinosaur from falling
    def land(self):
        self.y = 45
        self.vely = 0
        self.image = DINOSAUR_RUN_ANIMATION
        self.jumping = False
    

    # Make the dinosaur duck
    def duck(self):
        self.image = DINOSAUR_DUCK_ANIMATION
        self.ducking = True
    

    # Stop the dinosaur from ducking
    def rise(self):
        self.image = DINOSAUR_RUN_ANIMATION
        self.ducking = False
    

    # Update the dinosaur if it collided with an object
    def collided(self):
        self.image = DINOSAUR_COLLISION_IMG

    
    # Reset the dinosaur
    def reset(self, y):
        self.y = y
        self.vely = 0
        self.image = DINOSAUR_RUN_ANIMATION
        self.jumping = False
        self.ducking = False
    
    
    # Check if the dinosaur runs into the obstacle
    def collide(self, obstacle): 
        # If one sprite is on left side of other, then no collision is possible
        if self.x + self.width <= obstacle.x or obstacle.x + obstacle.width <= self.x: 
            return False
        
        # If one sprite is above other, then no collision is possible 
        if self.y + self.height <= obstacle.y or obstacle.y + obstacle.height <= self.y: 
            return False
        
        # The only other outcome is that they overlap
        return True
