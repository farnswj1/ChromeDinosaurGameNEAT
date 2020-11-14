'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a subclass of the game sprite in gameObject.py.
'''

# Imported modules
from gameObject import GameSprite


class Dinosaur(GameSprite):
    # Constructor
    def __init__(self, *args, **kwargs):
        # Inherit the game sprite class
        super().__init__(*args, **kwargs)

        # Jumping and ducking variables keep track of the dinosaur's actions
        self.jumping = False
        self.ducking = False

    
    # Make the dinosaur jump (only if it isn't already jumping or ducking)
    def jump(self):
        if not self.jumping and not self.ducking:
            self.vely = 1200
            self.jumping = True
    

    # Stop the dinosaur from falling
    def land(self):
        self.y = 45
        self.vely = 0
        self.jumping = False
    

    # Make the dinosaur duck (only if it isn't already ducking or jumping)
    def duck(self):
        if not self.ducking and not self.jumping:
            self.ducking = True
            self.change_image
    

    # Stop the dinosaur from ducking
    def rise(self):
        self.ducking = False
