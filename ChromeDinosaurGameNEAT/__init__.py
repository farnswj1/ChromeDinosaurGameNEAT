'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 21, 2020

This script runs the game contained in this package.
'''

# Imported modules
from .gameWindow import ChromeDinosaurGame
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT


# Run the game
def run(enable_neat=False, night_mode=False):
    ChromeDinosaurGame(enable_neat=enable_neat, night_mode=night_mode)
