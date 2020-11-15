'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a subclass of the window class in pyglet.
'''

# Imported modules
import pyglet
import neat
import os
from pyglet.window import key, mouse, FPSDisplay
from pyglet.image import ImageGrid, Animation
from gameObject import GameSprite
from dinosaur import Dinosaur
from itertools import cycle
from random import random, randint, choice


# Chrome dinosaur window class
class ChromeDinosaurGame(pyglet.window.Window):
    def __init__(self, enable_neat=False, *args, **kwargs):
        # Inherit the pyglet window
        super().__init__(*args, **kwargs)

        # Save the configuration that determines if the NEAT algorithm is used
        self.enable_neat = enable_neat

        # Generate the font style
        pyglet.font.add_file('data/fonts/press_start_2p.ttf')
        pyglet.font.load("Press Start 2P")

        # Save and draw the FPS
        self.frame_rate = 1/60
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.x = self.width - 10
        self.fps_display.label.y = 10
        self.fps_display.label.anchor_x = "right"
        self.fps_display.label.font_name = "Press Start 2P"
        self.fps_display.label.font_size = 20
        self.fps_display.label.color = (192, 192, 192, 192)

        # Set the FPS
        pyglet.clock.schedule_interval(self.update, self.frame_rate)

        # Control the horizontal velocity of the obstacles
        self.obstacle_velx = -600

        # Create batches
        self.bg_batch = pyglet.graphics.Batch()
        self.main_batch = pyglet.graphics.Batch()
        if self.enable_neat:
            self.neat_batch = pyglet.graphics.Batch()
        else:
            self.game_over_batch = pyglet.graphics.Batch()

        # Preload the images into memory and save them
        game_sprites = self.preload_image("sprites.png")
        self.terrain_img = game_sprites.get_region(2, 0, 2402, 27)
        self.dinosaur_run_animation = Animation.from_image_sequence(
            ImageGrid(
                game_sprites.get_region(1854, 33, 176, 95),
                1,
                2,
                item_width=88,
                item_height=96
            ),
            0.3,
            loop=True
        )
        self.dinosaur_duck_animation = Animation.from_image_sequence(
            ImageGrid(
                game_sprites.get_region(2203, 33, 240, 61),
                1,
                2,
                item_width=118,
                item_height=62
            ),
            0.3,
            loop=True
        )
        self.dinosaur_jump_img = game_sprites.get_region(1678, 33, 88, 95)
        self.dinosaur_collision_img = game_sprites.get_region(2030, 33, 88, 95)
        self.cacti_imgs = (
            game_sprites.get_region(446, 58, 34, 70),  # Small cacti 1
            game_sprites.get_region(480, 58, 68, 70),  # Small cacti 2
            game_sprites.get_region(548, 58, 102, 70), # Small cacti 3
            game_sprites.get_region(652, 32, 50, 98),  # Large cacti 1
            game_sprites.get_region(702, 32, 100, 98), # Large cacti 2
            game_sprites.get_region(802, 30, 150, 98), # Large cacti 3

        )
        self.bird_animation = Animation.from_image_sequence(
            ImageGrid(
                game_sprites.get_region(260, 48, 184, 80),
                1, 2, item_width=92, item_height=80
            ),
            0.3,
            loop=True
        )
        self.cloud_img = game_sprites.get_region(165, 100, 95, 28)
        self.moon_phases = cycle((
            game_sprites.get_region(1234, 47, 40, 82),
            game_sprites.get_region(1194, 47, 40, 82),
            game_sprites.get_region(1154, 47, 40, 82),
            game_sprites.get_region(1074, 47, 80, 82),
            game_sprites.get_region(1034, 47, 40, 82),
            game_sprites.get_region(994, 47, 40, 82),
            game_sprites.get_region(954, 47, 40, 82)
        ))
        self.reset_button_img = game_sprites.get_region(2, 63, 72, 65)

        # Score and label
        self.score = 0
        self.score_label = pyglet.text.Label(
            f"{self.score:05}",
            font_name="Press Start 2P",
            font_size=20,
            x=self.width - 10,
            y=self.height - 10,
            anchor_x="right",
            anchor_y="top",
            batch=self.bg_batch
        )

        # Game over label (only if the user plays the game manually)
        if not self.enable_neat:
            self.game_over_label = pyglet.text.Label(
                "G A M E  O V E R",
                font_name="Press Start 2P",
                font_size=30,
                x=self.width / 2,
                y=self.height / 2 + 100,
                anchor_x="center",
                anchor_y="center",
                batch=self.game_over_batch
            )
        
        # Initialize the sprites
        self.terrain_1 = GameSprite(
            self.terrain_img,
            0,
            50,
            velx=self.obstacle_velx,
            batch=self.bg_batch
        )
        self.terrain_2 = GameSprite(
            self.terrain_img,
            2400,
            50,
            velx=self.obstacle_velx,
            batch=self.bg_batch
        )
        self.moon = GameSprite(next(self.moon_phases), 2920, 275, velx=-20, batch=self.bg_batch)
        self.clouds = [] # Elements will be randomly generated as the game progresses
        self.obstacles = [] # Elements will be randomly generated as the game progresses
        
        # Reset button is only available when the user plays manually
        if not self.enable_neat:
            self.reset_button = GameSprite(
                self.reset_button_img,
                564,
                150,
                batch=self.game_over_batch
            )
        
        # Generate the user's dinosaur if the user plays manually
        if not self.enable_neat:
            self.dinosaur = Dinosaur(self.dinosaur_run_animation, 65, 45, batch=self.main_batch)

            # Set variables to track user inputs
            self.trigger_duck = False
            self.trigger_jump = False

            # Keep track of any user collisions
            self.user_collision = False

        # Add a delays to control when events happen
        self.next_score_increment = 0.1
        self.next_cloud_spawn = 3 * random() + 1
        self.next_obstacle_spawn = 2 * random() + 1
        self.next_velocity_increase = 1

        # Set up the NEAT algorithm if true. Otherwise, let the user play manually
        if self.enable_neat:
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
                x=10,
                y=self.height - 10,
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
                x=10,
                y=self.height - 40,
                anchor_x="left",
                anchor_y="top",
                batch=self.neat_batch
            )
            # Run the NEAT algorithm and find the best "player"
            winner = population.run(self.eval_genomes, 25)
        else:
            # Run the main loop and play the game manually
            pyglet.app.run()


    # Load and save the image into memory
    def preload_image(self, image):
        return pyglet.image.load(f"data/images/{image}")
    

    # Handle the events when a key is pressed
    def on_key_press(self, symbol, modifiers):
        # Terminate the game if the ESC is pressed
        if symbol == key.ESCAPE:
            self.has_exit = True
            pyglet.app.exit()
        
        # Disable if the NEAT algorithm is being used
        if not self.enable_neat:
            # Check if the user triggers a duck or jump (duck is a priority over jump)
            if symbol in (key.DOWN, key.S):
                self.trigger_duck = True
            elif symbol in (key.SPACE, key.UP, key.W):
                self.trigger_jump = True

            # Accept the ENTER key only if the game is over
            if self.user_collision and symbol == key.ENTER:
                self.reset()

    
    # Handle the events when a key is pressed
    def on_key_release(self, symbol, modifiers):
        # Disable if the NEAT algorithm is being used
        if not self.enable_neat:
            # Check if the user released a key that triggers a duck
            if symbol in (key.DOWN, key.S):
                self.trigger_duck = False
            
            # Check if the user released a key that triggers a jump
            if symbol in (key.SPACE, key.UP, key.W):
                self.trigger_jump = False

    
    # Handle the events when the mouse is pressed
    def on_mouse_press(self, x, y, button, modifiers):
        # Disable if the NEAT algorithm is being used
        if not self.enable_neat:
            if (self.user_collision 
            and button == mouse.LEFT
            and self.reset_button.x <= x <= self.reset_button.x + self.reset_button.width 
            and self.reset_button.y <= y <= self.reset_button.y + self.reset_button.height):
                self.reset()


    # Draw the contents on the screen
    def on_draw(self):
        self.clear()
        self.bg_batch.draw() # Draw the background first
        self.main_batch.draw() # Draw the dinosaur and the obstacles next
        self.fps_display.draw()

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
                dinosaur.change_image(self.dinosaur_run_animation)
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
                    dinosaur.change_image(self.dinosaur_duck_animation)
                    dinosaur.duck()
                if output[0] <= 0.5 and not dinosaur.jumping and dinosaur.ducking:
                    # End duck animation
                    dinosaur.change_image(self.dinosaur_run_animation)
                    dinosaur.rise()
                elif output[1] > 0.5 and not dinosaur.jumping and not dinosaur.ducking:
                    # Start jumping animation
                    dinosaur.change_image(self.dinosaur_jump_img)
                    dinosaur.jump()
        else:
            # Make the dinosaur duck or jump, depending on the key pressed
            if self.trigger_duck and not dinosaur.jumping and not dinosaur.ducking:
                # Start duck animation
                dinosaur.change_image(self.dinosaur_duck_animation)
                dinosaur.duck()
            elif not self.trigger_duck and not dinosaur.jumping and dinosaur.ducking:
                # End duck animation
                dinosaur.change_image(self.dinosaur_run_animation)
                dinosaur.rise()
            elif self.trigger_jump and not self.trigger_duck:
                # Start jump animation
                dinosaur.change_image(self.dinosaur_jump_img)
                dinosaur.jump()

        # Update the dinosaur's position
        dinosaur.update(dt)
    

    # Update the objects
    def update(self, dt):
        # Handle the collisions
        for obstacle in self.obstacles:
            if self.enable_neat:
                # Check each dinosaur for collisions
                for dinosaur, neural_net, genome in zip(self.dinosaurs, self.neural_nets, self.genomes):
                    if self.collide(dinosaur, obstacle):
                        # Remove any animations so that the sprite is properly removed
                        dinosaur.change_image(self.dinosaur_jump_img)

                        # Penalize the genome for the collision
                        genome.fitness -= 100
                        
                        # Eliminate the dinosaur genome
                        self.dinosaurs.remove(dinosaur)
                        self.neural_nets.remove(neural_net)
                        self.genomes.remove(genome)
                        
                        # Decrement the number of dinosaurs left and check if any remain
                        self.number_of_dinosaurs -= 1
                        if not self.dinosaurs:
                            self.reset()
                            pyglet.app.exit()
            else:
                # Check if the user collided with any obstacles
                if self.collide(self.dinosaur, obstacle):
                    self.user_collision = True
                    self.dinosaur.change_image(self.dinosaur_collision_img)
                    
                    # Prevent any further updates if a collision has been detected
                    return
        
        # Update the terrain sprites and check if any of them need to be moved
        if self.terrain_1.x + self.terrain_1.width < 0: # Off the screen
            self.terrain_1.x = self.terrain_2.x + self.terrain_2.width
        elif self.terrain_2.x + self.terrain_2.width < 0: # Off the screen
            self.terrain_2.x = self.terrain_1.x + self.terrain_1.width
        self.terrain_1.update(dt)
        self.terrain_2.update(dt)

        # Update the clouds and delete those that run off the left side of the screen
        for cloud in self.clouds:
            if cloud.x + cloud.width < 0:
                self.clouds.remove(cloud)
            else:
                cloud.update(dt)

        # Update the moon and move the moon if needed
        if self.moon.x + 80 < 0:
            self.moon.x += 3000
            self.moon.change_image(next(self.moon_phases))
        self.moon.update(dt)

        # Update the dinosaur(s)
        if self.enable_neat:
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
            self.update_dinosaur(self.dinosaur, dt)

        # Update the obstacles and delete those that run off the left side of the screen
        for obstacle in self.obstacles:
            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)
            else:
                obstacle.update(dt)

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
                GameSprite(self.cloud_img, 1200, randint(225, 325), velx=-150, batch=self.bg_batch)
            )
            self.next_cloud_spawn += 3 * random() + 2 # Reset delay
        
        # Update the obstacle spawn delay
        self.next_obstacle_spawn -= dt
        if self.next_obstacle_spawn <= 0:
            object_type = randint(1, 6)
            if object_type == 6: # Spawn bird
                self.obstacles.append(
                    GameSprite(
                        self.bird_animation,
                        1200,
                        choice((50, 125, 200)),
                        velx=self.obstacle_velx - 100,
                        batch=self.main_batch
                    )
                )
            else: # Spawn cacti
                self.obstacles.append(
                    GameSprite(
                        choice(self.cacti_imgs),
                        1200,
                        45,
                        velx=self.obstacle_velx,
                        batch=self.main_batch
                    )
                )
            self.next_obstacle_spawn = 1.5 * random() + 1 # Reset delay

        # Update the velocity increase delay
        self.next_velocity_increase -= dt
        if self.next_velocity_increase <= 0:
            # Increment to change the velocity by
            increment = -5

            # Increase the velocity of the terrain and the obstacles
            self.terrain_1.velx += increment
            self.terrain_2.velx += increment

            for obstacle in self.obstacles:
                obstacle.velx += increment
            
            self.obstacle_velx += increment # Change the obstacle velocity
            self.next_velocity_increase += 1 # Reset delay

        # Update the generation and number of dinosaurs labels if the NEAT algorithm is used
        if self.enable_neat:
            self.generation_label.text = f"GENERATION: {self.generation:02}"
            self.number_of_dinosaurs_label.text = f"DINOSAURS: {self.number_of_dinosaurs:03}"
    

    # Reset the game
    def reset(self):
        # To remove the bird animations, all sprites are changed to static images
        for obstacle in self.obstacles:
            obstacle.change_image(self.cacti_imgs[0])
        
        # Clear the list of obstacles
        self.obstacles.clear()

        # Reset the dinosaur(s)
        if self.enable_neat:
            for dinosaur in self.dinosaurs:
                dinosaur.change_image(self.dinosaur_run_animation)
        else:
            self.dinosaur.change_image(self.dinosaur_run_animation)
            self.dinosaur.y = 45
            self.jumping = False
            self.ducking = False

        # Reset the score
        self.score = 0

        # Reset the velocities (obstacles are deleted, so we don't need to worry about them)
        self.obstacle_velx = -600
        self.terrain_1.velx = self.obstacle_velx
        self.terrain_2.velx = self.obstacle_velx

        # Reset the collision boolean so the game can start
        self.user_collision = False

    
    # Run the game with the NEAT algorithm
    def eval_genomes(self, genomes, config):
        # Terminate if the user closed the window
        if self.has_exit:
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
            self.dinosaurs.append(Dinosaur(self.dinosaur_run_animation, 65, 45, batch=self.main_batch))
            self.genomes.append(genome)
        
        # Run the game
        pyglet.app.run()
