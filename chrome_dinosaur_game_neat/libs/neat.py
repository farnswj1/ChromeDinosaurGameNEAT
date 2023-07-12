from neat import (
    Config,
    DefaultGenome,
    DefaultReproduction,
    DefaultSpeciesSet,
    DefaultStagnation,
    Population as BasePopulation,
    StatisticsReporter,
    StdOutReporter
)
import os


class Population(BasePopulation):
    def __init__(self):
        """Create a NEAT population object."""
        config_file = os.path.abspath("chrome_dinosaur_game_neat/neat_config.txt")
        config = Config(
            DefaultGenome,
            DefaultReproduction,
            DefaultSpeciesSet,
            DefaultStagnation,
            config_file
        )
        super().__init__(config)

        # Add reporters to show progress in the terminal
        self.add_reporter(StdOutReporter(True))
        self.add_reporter(StatisticsReporter())
