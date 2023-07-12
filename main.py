'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a Python-based implementation of the dinosaur game featured on
Google Chrome. The user can choose to play the game manually or the user
can allow the NEAT algorithm to play the game. If the NEAT algorithm is
used, the AI will try to survive as long as possible. This project was
inspired by Code Bullet, who conceived the idea and made an implementation
in Processing.

To play the game manually, type in the following command:
    python main.py

To run the game using NEAT, add the argument 'neat' to the command. For example:
    python main.py neat

To enable night mode, add the argument 'night' to the command. For example:
    python main.py night

To enable both NEAT and night mode, add both arguments to the command.
The order of these arguments do not matter.
'''

# Imported modules
import chrome_dinosaur_game_neat
from sys import argv


if __name__ == "__main__":
    # Check if the user has enabled or disabled the NEAT implementation
    enable_neat = ("neat" in argv)

    # Check if the user has enabled night mode
    night_mode = ("night" in argv)

    # Run the game
    chrome_dinosaur_game_neat.run(enable_neat=enable_neat, night_mode=night_mode)
