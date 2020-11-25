'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 21, 2020

This script runs the game contained in this package.
'''

# Imported modules
from .gameWindow import GameWindow


# Run the game
def run(enable_neat=False, night_mode=False):
    GameWindow(enable_neat=enable_neat, night_mode=night_mode)
