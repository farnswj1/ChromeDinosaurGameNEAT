# Google Chrome Dinosaur Game (with NEAT)
This is a Python-based implementation of the dinosaur game featured on Google Chrome. The user can choose to play the game manually or the user can allow the NEAT algorithm to play the game. If the NEAT algorithm is used, the AI will try to survive as long as possible. This project was inspired by Code Bullet, who conceived the idea and made an implementation in Processing.

## Installation
To install the game, ensure you have Python 3 installed. The newest version is recommended.

A virtual environment is recommended. To create one, enter `python3 -m venv venv`. Then enter the environment (`source venv/bin/activate` for Linux or `./venv/Scripts/active` for Windows). Then install the necessary dependencies via `pip install -r requirements.txt`.

## Run
To play the game manually, enter the command `python main.py`

To run the game using NEAT, add the argument `neat`. For example: `python main.py neat`

To enable night mode, add the argument `night`. For example: `python main.py night`

To enable both NEAT and night mode, add both arguments to the command. The order of these arguments do not matter.
