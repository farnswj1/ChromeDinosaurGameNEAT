'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 21, 2020

This script contains the constants used in the package.
'''

# Imported modules
import os
from pyglet.image import load, ImageGrid, Animation
from itertools import cycle


# Constant values
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 400
GENERATIONS = 25
FONT_NAME = os.path.join(os.path.dirname(__file__), "data/fonts/press_start_2p.ttf") 


# Sprites
GAME_SPRITES = load(os.path.join(os.path.dirname(__file__), "data/images/sprites.png"))
TERRAIN_IMG = GAME_SPRITES.get_region(2, 0, 2402, 27)
DINOSAUR_RUN_ANIMATION = Animation.from_image_sequence(
    ImageGrid(GAME_SPRITES.get_region(1854, 33, 176, 95), 1, 2, item_width=88, item_height=96),
    0.3,
    loop=True
)
DINOSAUR_DUCK_ANIMATION = Animation.from_image_sequence(
    ImageGrid(GAME_SPRITES.get_region(2203, 33, 240, 61), 1, 2, item_width=118, item_height=62),
    0.3,
    loop=True
)
DINOSAUR_JUMP_IMG = GAME_SPRITES.get_region(1678, 33, 88, 95)
DINOSAUR_COLLISION_IMG = GAME_SPRITES.get_region(2030, 33, 88, 95)
CACTI_IMGS = (
    GAME_SPRITES.get_region(446, 58, 34, 70),  # Small cacti 1
    GAME_SPRITES.get_region(480, 58, 68, 70),  # Small cacti 2
    GAME_SPRITES.get_region(548, 58, 102, 70), # Small cacti 3
    GAME_SPRITES.get_region(652, 32, 50, 98),  # Large cacti 1
    GAME_SPRITES.get_region(702, 32, 100, 98), # Large cacti 2
    GAME_SPRITES.get_region(802, 30, 150, 98), # Large cacti 3
)
BIRD_ANIMATION = Animation.from_image_sequence(
    ImageGrid(GAME_SPRITES.get_region(260, 48, 184, 80), 1, 2, item_width=92, item_height=80),
    0.3,
    loop=True
)
CLOUD_IMG = GAME_SPRITES.get_region(165, 100, 95, 28)
MOON_PHASES = cycle((
    GAME_SPRITES.get_region(1234, 47, 40, 82),
    GAME_SPRITES.get_region(1194, 47, 40, 82),
    GAME_SPRITES.get_region(1154, 47, 40, 82),
    GAME_SPRITES.get_region(1074, 47, 80, 82),
    GAME_SPRITES.get_region(1034, 47, 40, 82),
    GAME_SPRITES.get_region(994, 47, 40, 82),
    GAME_SPRITES.get_region(954, 47, 40, 82)
))
STAR_IMGS = (
    GAME_SPRITES.get_region(1274, 74, 18, 18),
    GAME_SPRITES.get_region(1274, 92, 18, 18),
    GAME_SPRITES.get_region(1274, 110, 18, 18)
)
RESET_BUTTON_IMG = GAME_SPRITES.get_region(2, 63, 72, 65)
