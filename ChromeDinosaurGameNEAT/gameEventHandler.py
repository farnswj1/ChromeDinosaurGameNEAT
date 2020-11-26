'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 21, 2020

This is the game script, which handles the game objects and logic.
'''

# Imported modules
import pyglet
import neat
import os
import pickle
from .gameSprite import GameSprite
from .dinosaur import Dinosaur
from .constants import *
from random import uniform, randint, choice


# Game class handles the game events
class GameEventHandler:
    # Constructor
    def __init__(self, enable_neat=False, night_mode=False):
        # Save the configuration that determines if the NEAT algorithm is used
        self.enable_neat = enable_neat

        # Save the configuration that determines if night mode is enabled
        self.night_mode = night_mode

        # Change the background color to white unless the user selects night mode
        if not self.night_mode:
            pyglet.gl.glClearColor(1, 1, 1, 1)

        # Keep track of when the program is terminated
        self.user_exit = False

        # Control the horizontal velocity of the obstacles
        self.obstacle_velx = -600

        # Create batches
        self.bg_batch = pyglet.graphics.Batch()
        self.main_batch = pyglet.graphics.Batch()
        if self.enable_neat:
            self.neat_batch = pyglet.graphics.Batch()
        else:
            self.game_over_batch = pyglet.graphics.Batch()
        
        # Score and label
        self.score = 0
        self.score_label = pyglet.text.Label(
            f"{self.score:05}",
            font_name="Press Start 2P",
            font_size=20,
            color=(255, 255, 255, 255) if self.night_mode else (0, 0, 0, 255),
            x=WINDOW_WIDTH - 10,
            y=WINDOW_HEIGHT - 10,
            anchor_x="right",
            anchor_y="top",
            batch=self.bg_batch
        )
        
        # Initialize the sprites
        self.terrain_1 = GameSprite(
            TERRAIN_IMG,
            0,
            50,
            velx=self.obstacle_velx,
            batch=self.bg_batch
        )
        self.terrain_2 = GameSprite(
            TERRAIN_IMG,
            2400,
            50,
            velx=self.obstacle_velx,
            batch=self.bg_batch
        )
        self.moon = GameSprite(next(MOON_PHASES), 2920, 275, velx=-20, batch=self.bg_batch)
        self.clouds = [] # Elements will be randomly generated as the game progresses
        self.obstacles = [] # Elements will be randomly generated as the game progresses
        self.stars = [] # Elements will be randomly generated as the game progresses

        # Add a delays to control when events happen
        self.next_score_increment = 0.1
        self.next_cloud_spawn = uniform(1, 4)
        self.next_obstacle_spawn = uniform(1, 3)
        self.next_star_spawn = 0 # Spawn a star immediately
        self.next_velocity_increase = 1

        # Control the star opacity by increasing it at night 
        self.star_opacity = 0

        # Initalize the player's dinosaur if NEAT is disabled
        if not self.enable_neat:
            # Generate the user's dinosaur if the user plays manually
            self.dinosaur = Dinosaur(DINOSAUR_RUN_ANIMATION, 65, 45, batch=self.main_batch)

            # Set variables to track user inputs
            self.trigger_duck = False
            self.trigger_jump = False

            # Keep track of any user collisions
            self.user_collision = False

            # Game over label
            self.game_over_label = pyglet.text.Label(
                "G A M E  O V E R",
                font_name="Press Start 2P",
                font_size=30,
                color=(255, 255, 255, 255) if self.night_mode else (0, 0, 0, 255),
                x=WINDOW_WIDTH / 2,
                y=WINDOW_HEIGHT / 2 + 100,
                anchor_x="center",
                anchor_y="center",
                batch=self.game_over_batch
            )

            # Reset button
            self.reset_button = GameSprite(
                RESET_BUTTON_IMG,
                564,
                150,
                batch=self.game_over_batch
            )
    

    # Setup and run the game with the NEAT algorithm
    def run_neat(self):
        # Locate the NEAT configuration file
        config_file = os.path.join(os.path.dirname(__file__), "neat_config.txt")

        # Configure the NEAT algorithm
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file
        )

        # Generate the population
        population = neat.Population(config)

        # Add a reporter to show progress in the terminal
        population.add_reporter(neat.StdOutReporter(True))
        population.add_reporter(neat.StatisticsReporter())

        # Generation label
        self.generation = -1
        self.generation_label = pyglet.text.Label(
            f"GENERATION: {self.generation:02}",
            font_name="Press Start 2P",
            font_size=20,
            color=(255, 255, 255, 255) if self.night_mode else (0, 0, 0, 255),
            x=10,
            y=WINDOW_HEIGHT - 10,
            anchor_x="left",
            anchor_y="top",
            batch=self.neat_batch
        )

        # Number of dinosaurs label
        self.number_of_dinosaurs = 0
        self.number_of_dinosaurs_label = pyglet.text.Label(
            f"DINOSAURS: {self.number_of_dinosaurs:03}",
            font_name="Press Start 2P",
            font_size=20,
            color=(255, 255, 255, 255) if self.night_mode else (0, 0, 0, 255),
            x=10,
            y=WINDOW_HEIGHT - 40,
            anchor_x="left",
            anchor_y="top",
            batch=self.neat_batch
        )

        # Run the NEAT algorithm and find the best "player"
        winner = population.run(self.eval_genomes, GENERATIONS)

        # If the program is terminated at the last generation, don't show the results
        if not self.user_exit:
            # Print the genome that performed the best
            print(f"\nBest genome:\n{winner}")

            # If winner.pkl exists, save the best genome
            pkl_file = os.path.join(os.path.dirname(__file__), "winner.pkl")
            if os.path.exists(pkl_file):
                # Get the current genome saved in the .pkl file
                with open(pkl_file, "rb") as f:
                    saved_genome = pickle.load(f)
                
                # Save the winner genome if it has a higher fitness than the saved genome
                if winner.fitness > saved_genome.fitness:
                    print(
                        "This genome performed better than the saved genome!\n"
                        "Overwriting the saved genome with this session's best genome..."
                    )
                    with open(pkl_file, "wb") as f:
                        pickle.dump(winner, f)
            else:
                # Create the .pkl file and save the winner genome
                print("Saving the best genome...")
                with open(pkl_file, "wb") as f:
                    pickle.dump(winner, f)
    

    # Handle the events when the mouse is pressed
    def on_mouse_press(self, x, y):
        # Disable if the NEAT algorithm is being used
        if not self.enable_neat:
            if (self.user_collision 
            and self.reset_button.x <= x <= self.reset_button.x + self.reset_button.width 
            and self.reset_button.y <= y <= self.reset_button.y + self.reset_button.height):
                self.reset()
    

    # Draw the contents of the game onto the window
    def draw(self):
        self.bg_batch.draw() # Draw the background first
        self.main_batch.draw() # Draw the dinosaur and the obstacles next

        # Draw the NEAT batch if used. Otherwise, draw the game over batch if a collision occurs
        if self.enable_neat:
            self.neat_batch.draw()
        else:
            # Draw the game over label if a collision has been detected 
            if self.user_collision:
                self.game_over_batch.draw()
    

    # Check if the sprites collide
    def collide(self, sprite_1, sprite_2): 
        # If one sprite is on left side of other, then no collision is possible
        if sprite_1.x + sprite_1.width <= sprite_2.x or sprite_2.x + sprite_2.width <= sprite_1.x: 
            return False
        
        # If one sprite is above other, then no collision is possible 
        if sprite_1.y + sprite_1.height <= sprite_2.y or sprite_2.y + sprite_2.height <= sprite_1.y: 
            return False
        
        # The only other outcome is that they overlap
        return True
    

    # Update the dinosaur
    def update_dinosaur(self, dinosaur, dt, output=None):
        # Check if the dinosaur is jumping first
        if dinosaur.jumping:
            # Dinosaur is in the air. Check if it has landed
            if dinosaur.y <= 45 and dinosaur.vely <= 0:
                # Dinosaur hits the ground after jumping
                dinosaur.land()
            else:
                # Decrement the dinosaur's vertical velocity
                dinosaur.vely -= 75
        
        # If NEAT is used, let it make the next move. Otherwise, let the user do so
        if self.enable_neat:
            # If an output is provided, let it make the next move
            if output:
                # Determine if the dinosaur should duck or jump
                if output[0] > 0.5 and not dinosaur.jumping and not dinosaur.ducking:
                    # Start ducking animation
                    dinosaur.duck()
                elif output[0] <= 0.5 and not dinosaur.jumping and dinosaur.ducking:
                    # End duck animation
                    dinosaur.rise()
                elif output[1] > 0.5 and not dinosaur.jumping and not dinosaur.ducking:
                    # Start jumping animation
                    dinosaur.jump()
        else:
            # Make the dinosaur duck or jump, depending on the key pressed
            if self.trigger_duck and not dinosaur.jumping and not dinosaur.ducking:
                # Start duck animation
                dinosaur.duck()
            elif not self.trigger_duck and not dinosaur.jumping and dinosaur.ducking:
                # End duck animation
                dinosaur.rise()
            elif self.trigger_jump and not dinosaur.jumping and not dinosaur.ducking:
                # Start jump animation
                dinosaur.jump()

        # Update the dinosaur's position
        dinosaur.update(dt)
    

    # Update the objects
    def update(self, dt):
        # Handle the collisions and keep track of which dinosaurs collided with an obstacle
        dinosaurs_to_remove = []
        neural_nets_to_remove = []
        genomes_to_remove = []
        for obstacle in self.obstacles:
            if self.enable_neat:
                # Check each dinosaur for collisions
                for dinosaur, neural_net, genome in zip(self.dinosaurs, self.neural_nets, self.genomes):
                    if self.collide(dinosaur, obstacle):
                        # Add the dinosaur genome to the list of objects to remove
                        dinosaurs_to_remove.append(dinosaur)
                        neural_nets_to_remove.append(neural_net)
                        genomes_to_remove.append(genome)
            else:
                # Check if the user collided with any obstacles
                if self.collide(self.dinosaur, obstacle):
                    self.user_collision = True
                    self.dinosaur.collided()
                    
                    # Prevent any further updates if a collision has been detected
                    return
        
        # Update the dinosaur(s) and, if NEAT is enabled, delete those that collided with an obstacle
        if self.enable_neat:
            # Delete the dinosaurs that collided with an obstacle
            for dinosaur, neural_net, genome in zip(dinosaurs_to_remove, neural_nets_to_remove, genomes_to_remove):
                # Delete the image from video memory
                dinosaur.delete()

                # Penalize the genome for the collision
                genome.fitness -= 100

                # Add the dinosaur genome to the list of objects to remove
                self.dinosaurs.remove(dinosaur)
                self.neural_nets.remove(neural_net)
                self.genomes.remove(genome)

                # Decrement the number of dinosaurs left and check if any remain
                self.number_of_dinosaurs -= 1
                if not self.dinosaurs:
                    self.reset()
                    pyglet.app.exit()
            
            # Update the dinosaur genomes
            for dinosaur, neural_net, genome in zip(self.dinosaurs, self.neural_nets, self.genomes):
                # Reward the genome with points for surviving
                genome.fitness += dt

                # Get the first obstacle if it exists and let the network make a decision
                output = neural_net.activate((
                    dinosaur.y, # Dinosaur's y-coordinate
                    self.obstacles[0].y, # Obstacle's y-coordinate
                    self.obstacles[0].width, # Width of the obstacle
                    self.obstacles[0].height, # Height of the obstacle
                    abs(dinosaur.x + dinosaur.width - self.obstacles[0].x), # Distance
                    self.obstacle_velx # Game speed
                )) if self.obstacles else None
                
                # Update the dinosaur and have the neural network determine its next move
                self.update_dinosaur(dinosaur, dt, output=output)
        else:
            # Update the player's dinosaur
            self.update_dinosaur(self.dinosaur, dt)
        
        # Update the obstacles and keep track of those that run off the left side of the screen
        obstacles_to_remove = []
        for obstacle in self.obstacles:
            if obstacle.x + obstacle.width < 0:
                obstacles_to_remove.append(obstacle)
            else:
                obstacle.update(dt)
        
        # Delete the obstacles that ran off the screen
        for obstacle in obstacles_to_remove:
            obstacle.delete() # Delete the image from video memory
            self.obstacles.remove(obstacle)
        
        # Update the terrain sprites and check if any of them need to be moved
        if self.terrain_1.x + self.terrain_1.width < 0: # Off the screen
            self.terrain_1.x = self.terrain_2.x + self.terrain_2.width
        elif self.terrain_2.x + self.terrain_2.width < 0: # Off the screen
            self.terrain_2.x = self.terrain_1.x + self.terrain_1.width
        self.terrain_1.update(dt)
        self.terrain_2.update(dt)

        # Update the clouds and keep track of those that run off the left side of the screen
        clouds_to_remove = []
        for cloud in self.clouds:
            if cloud.x + cloud.width < 0:
                clouds_to_remove.append(cloud)
            else:
                cloud.update(dt)

        # Delete the clouds that ran off the screen
        for cloud in clouds_to_remove:
            cloud.delete() # Delete the image from video memory
            self.clouds.remove(cloud)

        # Update the moon and move the moon if needed
        if self.moon.x + 80 < 0:
            self.moon.x += 3000
            self.moon.image = next(MOON_PHASES)
        self.moon.update(dt)

        # Update the star opacity variable before updating the stars
        if self.moon.x < 1280:
            self.star_opacity = min(self.star_opacity + (64 * dt), 255)
        else:
            self.star_opacity = max(self.star_opacity - (64 * dt), 0)

        # Update the stars and keep track of those that run off the left side of the screen
        stars_to_remove = []
        for star in self.stars:
            if star.x + star.width < 0:
                stars_to_remove.append(star)
            else:
                star.update(dt)
                star.opacity = round(self.star_opacity) # Opacity value must be an integer
        
        # Delete the stars that ran off the screen
        for star in stars_to_remove:
            star.delete() # Delete the image from video memory
            self.stars.remove(star)
                
        # Increment the score if scheduled to do so
        self.next_score_increment -= dt
        if self.next_score_increment <= 0:
            self.score += 1
            self.score_label.text = f"{self.score:05}"
            self.next_score_increment += 0.1 # Reset delay
        
        # Update the cloud spawn delay
        self.next_cloud_spawn -= dt
        if self.next_cloud_spawn <= 0:
            self.clouds.append(
                GameSprite(CLOUD_IMG, 1200, randint(225, 325), velx=-150, batch=self.bg_batch)
            )
            self.next_cloud_spawn += uniform(2, 5) # Reset delay
        
        # Update the obstacle spawn delay
        self.next_obstacle_spawn -= dt
        if self.next_obstacle_spawn <= 0:
            object_type = randint(1, 6)
            if object_type == 6: # Spawn bird
                self.obstacles.append(
                    GameSprite(
                        BIRD_ANIMATION,
                        1200,
                        choice((50, 125, 200)),
                        velx=self.obstacle_velx - 100,
                        batch=self.main_batch
                    )
                )
            else: # Spawn cacti
                self.obstacles.append(
                    GameSprite(
                        choice(CACTI_IMGS),
                        1200,
                        45,
                        velx=self.obstacle_velx,
                        batch=self.main_batch
                    )
                )
            self.next_obstacle_spawn = uniform(1, 2.5) # Reset delay
        
        # Update the star spawn delay
        self.next_star_spawn -= dt
        if self.next_star_spawn <= 0:
            self.stars.append(
                GameSprite(choice(STAR_IMGS),
                1200,
                randint(200, 350),
                velx=-10,
                batch=self.bg_batch)
            )
            self.next_star_spawn += uniform(30, 50) # Reset delay

        # Update the velocity increase delay
        self.next_velocity_increase -= dt
        if self.next_velocity_increase <= 0:
            # Increment to change the velocity by
            increment = -5

            # Increase the velocity of the terrain
            self.terrain_1.velx += increment
            self.terrain_2.velx += increment

            # Increase the velocity of the obstacles
            for obstacle in self.obstacles:
                obstacle.velx += increment
            
            self.obstacle_velx += increment # Change the obstacle velocity
            self.next_velocity_increase += 1 # Reset delay

        # Update the generation and number of dinosaurs labels if the NEAT algorithm is used
        if self.enable_neat:
            self.generation_label.text = f"GENERATION: {self.generation:02}"
            self.number_of_dinosaurs_label.text = f"DINOSAURS: {self.number_of_dinosaurs:03}"
    

    # Run the game with the NEAT algorithm
    def eval_genomes(self, genomes, config):
        # Terminate if the user closed the window
        if self.user_exit:
            exit()

        # Increment the generation number
        self.generation += 1
        self.number_of_dinosaurs = len(genomes)

        # Set up the list of genomes
        self.neural_nets = []
        self.dinosaurs = []
        self.genomes = []

        # Set up the genomes
        for _, genome in genomes:
            genome.fitness = 0  # Start with fitness level of 0
            self.neural_nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
            self.dinosaurs.append(Dinosaur(DINOSAUR_RUN_ANIMATION, 65, 45, batch=self.main_batch))
            self.genomes.append(genome)
        
        # Run the game
        pyglet.app.run()
    
    
    # Reset the game
    def reset(self):
        # Delete the image from video memory
        for obstacle in self.obstacles:
            obstacle.delete()
        
        # Clear the list of obstacles
        self.obstacles.clear()

        # Reset the dinosaur(s)
        if not self.enable_neat:
            self.dinosaur.reset(45)

            # Reset the collision boolean so the game can start for the player
            self.user_collision = False

        # Reset the score
        self.score = 0

        # Reset the velocities (obstacles are deleted, so we don't need to worry about them)
        self.obstacle_velx = -600
        self.terrain_1.velx = self.obstacle_velx
        self.terrain_2.velx = self.obstacle_velx
