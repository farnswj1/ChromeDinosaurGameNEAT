import pyglet
from ..sprites import (
    Bird,
    Cactus,
    Cloud,
    Moon,
    Star,
    Terrain
)
from ..gui.hud import ScoreDisplay
from random import uniform, randint, choice


class BaseEventHandler:
    def __init__(self, night_mode=False):
        """Create an event handler that allows the user to play the game manually."""
        # Keep track of when the program is terminated
        self.user_exit = False

        # Control the horizontal velocity of the obstacles
        self.obstacle_velx = -600

        # Create batches and groups
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)
        self.hud = pyglet.graphics.OrderedGroup(2)

        # Score and label
        self.score_display = ScoreDisplay(self.batch, self.hud, night_mode)

        # Initialize the sprites
        self.terrain = [
            Terrain(0, 50, velx=self.obstacle_velx, batch=self.batch, group=self.background),
            Terrain(2400, 50, velx=self.obstacle_velx, batch=self.batch, group=self.background)
        ]
        self.moon = Moon(2920, 275, velx=-20, batch=self.batch, group=self.background)

        # These elements will be randomly generated as the game progresses
        self.clouds = []
        self.obstacles = []
        self.stars = []

        # Add delays to control when events happen
        self.next_score_increment = 0.1
        self.next_cloud_spawn = uniform(1, 4)
        self.next_obstacle_spawn = uniform(1, 3)
        self.next_star_spawn = 0  # Spawn a star immediately
        self.next_velocity_increase = 1

        # Control the star opacity by increasing it when the moon comes out
        self.star_opacity = 0

    def run(self):
        """Run the game."""
        raise NotImplementedError()

    def on_key_press(self, symbol, modifiers):
        """Handle the events when a key is pressed."""
        pass

    def on_key_release(self, symbol, modifiers):
        """Handle the events when a key is released."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle the events when the mouse is pressed."""
        pass

    def draw(self):
        """Draw the contents of the game onto the window."""
        self.batch.draw()

    def update_dinosaurs(self, dt):
        """Update the dinosaur."""
        raise NotImplementedError()

    def update_obstacles(self, dt):
        """Update the obstacles."""
        obstacles_to_remove = []

        for obstacle in self.obstacles:
            # Delete any obstacles that ran off the screen
            if obstacle.x + obstacle.width < 0:
                obstacles_to_remove.append(obstacle)
            else:
                obstacle.update(dt)

        for obstacle in obstacles_to_remove:
            obstacle.delete()
            self.obstacles.remove(obstacle)

    def update_terrain(self, dt):
        """Update the terrain."""
        for terrain in self.terrain:
            terrain.update(dt)

    def update_clouds(self, dt):
        """Update the clouds."""
        clouds_to_remove = []

        for cloud in self.clouds:
            # Delete the clouds that ran off the screen
            if cloud.x + cloud.width < 0:
                clouds_to_remove.append(cloud)
            else:
                cloud.update(dt)

        for cloud in clouds_to_remove:
            cloud.delete()
            self.clouds.remove(cloud)

    def update_moon(self, dt):
        """Update the moon."""
        self.moon.update(dt)

    def update_opacity(self, dt):
        """Update the star opacity."""
        if self.moon.x < 1280:
            self.star_opacity = round(min(self.star_opacity + (64 * dt), 255))
        else:
            self.star_opacity = round(max(self.star_opacity - (64 * dt), 0))

    def update_stars(self, dt):
        """Update the stars."""
        stars_to_remove = []

        for star in self.stars:
            # Delete the stars that ran off the screen
            if star.x + star.width < 0:
                stars_to_remove.append(star)
            else:
                star.update(dt, self.star_opacity)

        for star in stars_to_remove:
            star.delete()
            self.stars.remove(star)

    def update_score(self, dt):
        """Update the score and reset the schedule if needed."""
        self.next_score_increment -= dt

        if self.next_score_increment <= 0:
            self.score_display.increment(1)
            self.next_score_increment += 0.1

    def update_cloud_spawn(self, dt):
        """Update the cloud spawn delay and create a cloud if needed."""
        self.next_cloud_spawn -= dt

        if self.next_cloud_spawn <= 0:
            cloud = Cloud(
                1200,
                randint(225, 325),
                velx=-150,
                batch=self.batch,
                group=self.background
            )
            self.clouds.append(cloud)
            self.next_cloud_spawn += uniform(2, 5)

    def update_obstacle_spawn(self, dt):
        """Update the obstacle spawn delay and create an obstacle if needed."""
        self.next_obstacle_spawn -= dt

        if self.next_obstacle_spawn <= 0:
            object_type = randint(1, 6)

            if object_type == 6:
                bird = Bird(
                    1200,
                    choice((50, 125, 200)),
                    velx=self.obstacle_velx - 100,
                    batch=self.batch,
                    group=self.foreground
                )
                self.obstacles.append(bird)
            else:
                cactus = Cactus(
                    1200,
                    45,
                    velx=self.obstacle_velx,
                    batch=self.batch,
                    group=self.foreground
                )
                self.obstacles.append(cactus)

            self.next_obstacle_spawn = uniform(1, 2.5)

    def update_star_spawn(self, dt):
        """Update the star spawn delay and create a star if needed."""
        self.next_star_spawn -= dt

        if self.next_star_spawn <= 0:
            star = Star(
                1200,
                randint(200, 350),
                velx=-10,
                batch=self.batch,
                group=self.background
            )
            self.stars.append(star)
            self.next_star_spawn += uniform(30, 50)

    def update_velocity(self, dt):
        """Update the velocity and increase it if needed."""
        self.next_velocity_increase -= dt

        if self.next_velocity_increase <= 0:
            increment = -5  # Increment to change the velocity by

            for terrain in self.terrain:
                terrain.velx += increment

            for obstacle in self.obstacles:
                obstacle.velx += increment

            self.obstacle_velx += increment
            self.next_velocity_increase += 1

    def update(self, dt):
        """Update the objects."""
        self.update_obstacles(dt)
        self.update_terrain(dt)
        self.update_clouds(dt)
        self.update_moon(dt)
        self.update_opacity(dt)
        self.update_stars(dt)
        self.update_score(dt)
        self.update_cloud_spawn(dt)
        self.update_obstacle_spawn(dt)
        self.update_star_spawn(dt)
        self.update_velocity(dt)

    def reset(self):
        """Reset the game."""
        # Forcibly delete the sprites from video memory
        for obstacle in self.obstacles:
            obstacle.delete()

        self.obstacles.clear()
        self.score_display.set(0)

        # Reset the velocities (obstacles are deleted, so we don't need to worry about them)
        self.obstacle_velx = -600

        for terrain in self.terrain:
            terrain.velx = self.obstacle_velx

    def on_close(self):
        """Close the game."""
        self.user_exit = True

        for terrain in self.terrain:
            terrain.delete()

        for cloud in self.clouds:
            cloud.delete()

        for obstacle in self.obstacles:
            obstacle.delete()

        for star in self.stars:
            star.delete()

        self.moon.delete()
