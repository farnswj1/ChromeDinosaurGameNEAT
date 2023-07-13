from ..sprites import DinosaurAI
from ..gui.hud import DinosaurCountDisplay, GenerationDisplay
from .base import BaseEventHandler
from ..libs.neat import Population
from ..constants import GENERATIONS, POPULATION_SIZE
import pyglet
import os
import pickle


class NEATEventHandler(BaseEventHandler):
    # Constructor
    def __init__(self, night_mode=False):
        """Create an event handler that uses the NEAT algorithm to play the game."""
        super().__init__(night_mode=night_mode)

        # Generation label
        self.generation_display = GenerationDisplay(self.batch, self.hud, night_mode)

        # Number of dinosaurs label
        self.dinosaur_count_display = DinosaurCountDisplay(self.batch, self.hud, night_mode)

    def run(self):
        """Set up and run the game with the NEAT algorithm."""
        # Generate the population
        population = Population()

        # Run the NEAT algorithm and find the best "player"
        winner = population.run(self.eval_genomes, GENERATIONS)

        # If the program is terminated at the last generation, don't show the results
        if not self.user_exit:
            print(f"\nBest genome:\n{winner}")
            pkl_file = os.path.abspath("chrome_dinosaur_game_neat/winner.pkl")

            # Save the best genome
            if os.path.exists(pkl_file):
                saved_genome = self.load_genome(pkl_file)

                if winner.fitness > saved_genome.fitness:
                    print(
                        "This genome performed better than the saved genome!\n"
                        "Overwriting the saved genome with this session's best genome..."
                    )
                    self.save_genome(winner, pkl_file)
            else:
                print("Saving the best genome...")
                self.save_genome(winner, pkl_file)

    @staticmethod
    def load_genome(path):
        """Load the genome saved at the specified path."""
        with open(path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def save_genome(genome, path):
        """Save the genome at the specified path."""
        with open(path, "wb") as f:
            pickle.dump(genome, f)

    def update_dinosaurs(self, dt):
        """Update the dinosaurs."""
        # Handle the collisions and keep track of which dinosaurs collided with an obstacle
        dinosaurs_to_remove = []

        for obstacle in self.obstacles:
            # Check each dinosaur for collisions
            for dinosaur in self.dinosaurs:
                if dinosaur.has_collided(obstacle):
                    # Add the dinosaur genome to the list of objects to remove
                    dinosaurs_to_remove.append(dinosaur)

        # Delete the dinosaurs that collided with an obstacle
        for dinosaur in dinosaurs_to_remove:
            dinosaur.delete()
            self.dinosaurs.remove(dinosaur)

            # Decrement the number of dinosaurs left and check if any remain
            self.dinosaur_count_display.increment(-1)

        if not self.dinosaurs:
            self.reset()
            pyglet.app.exit()

        next_obstacle = self.obstacles[0] if self.obstacles else None

        # Update the dinosaur genomes
        for dinosaur in self.dinosaurs:
            dinosaur.reward(dt)
            controller = dinosaur.think(next_obstacle)
            dinosaur.update(dt, controller)

    def update(self, dt):
        """Update the objects."""
        self.update_dinosaurs(dt)
        super().update(dt)

    def eval_genomes(self, genomes, config):
        """Run the game with the NEAT algorithm."""
        # Terminate if the user closed the window
        if self.user_exit:
            exit()

        self.generation_display.increment(1)
        self.dinosaurs = [
            DinosaurAI(
                65,
                45,
                genome=genome,
                config=config,
                batch=self.batch,
                group=self.foreground
            )
            for _, genome in genomes
        ]

        pyglet.app.run()

    def reset(self):
        """Reset the game."""
        super().reset()
        self.dinosaur_count_display.set(POPULATION_SIZE)

    def on_close(self):
        """Close the game."""
        super().on_close()

        for dinosaur in self.dinosaurs:
            dinosaur.delete()
