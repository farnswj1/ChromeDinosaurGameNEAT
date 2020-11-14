'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a subclass of the sprite object in pyglet.
'''

# Imported modules
from pyglet.sprite import Sprite


# Subclass of the sprite class
class GameSprite(Sprite):
    # Constructor
    def __init__(self, image, x, y, velx=0, vely=0, *args, **kwargs):
        # Inherit the sprite class
        super().__init__(image, x, y, *args, **kwargs)
        
        # Save the velocity of the sprite relative to the screen
        self.velx = velx
        self.vely = vely
    

    # Change the sprite image
    def change_image(self, image):
        self.image = image
    
    
    # Update the sprite
    def update(self, dt):
        # Update the sprite's position
        self.x += self.velx * dt
        self.y += self.vely * dt