'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a Python-based implementation of the dinosaur game featured on 
Google Chrome. The user can choose to play the game manually or the user 
can allow the NEAT algorithm to play the game. If the NEAT algorithm is 
used, the AI will try to survive as long as possible. This project was 
inspired by Code Bullet, who conceived the idea and made an implementation 
in JavaScript.

To play the game manually, type in the following command:
    python main.py

To run the game using NEAT, type in the following command:
    python main.py neat

NOTE: All other arguments will default to the player playing the game manually!
'''

# Imported modules
from sys import argv
from gameWindow import ChromeDinosaurGame

# Execute the program if ran directly
if __name__ == "__main__":
    # Check if the user has enabled or disabled the NEAT implementation
    use_neat = (argv[1] == "neat") if len(argv) >= 2 else False

    # Run the game
    ChromeDinosaurGame(
        width=1200,
        height=400,
        caption="Google Chrome Dinosaur Game",
        enable_neat=use_neat
    )
