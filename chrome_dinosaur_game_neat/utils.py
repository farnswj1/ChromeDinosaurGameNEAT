from pyglet.image import load
from functools import cache
import os


@cache
def get_sprite_map():
    path = "chrome_dinosaur_game_neat/assets/images/sprites.png"
    return load(os.path.abspath(path))
