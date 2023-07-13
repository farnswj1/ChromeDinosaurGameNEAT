from pyglet.window import key, mouse
from ..sprites import Dinosaur
from ..gui.hud import GameOverDisplay, ResetButton
from .base import BaseEventHandler
import pyglet


class PlayerEventHandler(BaseEventHandler):
    def __init__(self, night_mode=False):
        """Create an event handler that allows the user to play the game manually."""
        super().__init__(night_mode=night_mode)

        # Create a game over group
        self.game_over_group = pyglet.graphics.OrderedGroup(3)
        self.game_over_group.visible = False

        # Generate the user's dinosaur
        self.dinosaur = Dinosaur(65, 45, batch=self.batch, group=self.foreground)

        # Set variables to track user inputs
        self.trigger_duck = False
        self.trigger_jump = False

        # Keep track of any user collisions
        self.user_collision = False

        # Player HUD
        self.game_over_label = GameOverDisplay(self.batch, self.game_over_group, night_mode)
        self.reset_button = ResetButton(564, 150, batch=self.batch, group=self.game_over_group)

    @staticmethod
    def run():
        """Run the game."""
        pyglet.app.run()

    def on_key_press(self, symbol, modifiers):
        """Handle the events when a key is pressed."""
        if symbol in (key.DOWN, key.S):
            self.trigger_duck = True
        elif symbol in (key.SPACE, key.UP, key.W):
            self.trigger_jump = True

        # Accept the ENTER key only if the game is over
        if symbol == key.ENTER and self.user_collision:
            self.reset()

    def on_key_release(self, symbol, modifiers):
        """Handle the events when a key is released."""
        if symbol in (key.DOWN, key.S):
            self.trigger_duck = False

        if symbol in (key.SPACE, key.UP, key.W):
            self.trigger_jump = False

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle the events when the mouse is pressed."""
        # Handle the left click
        if button == mouse.LEFT and self.user_collision and self.reset_button.clicked(x, y):
            self.reset()

    def update_dinosaurs(self, dt):
        """Update the dinosaurs."""
        for obstacle in self.obstacles:
            # Check if the dinosaur collided with any obstacles
            if self.dinosaur.has_collided(obstacle):
                self.user_collision = True
                self.game_over_group.visible = True
                self.dinosaur.collided()
                return

        controller = [int(self.trigger_duck), int(self.trigger_jump)]
        self.dinosaur.update(dt, controller)

    def update(self, dt):
        """Update the objects."""
        if self.user_collision:
            return

        self.update_dinosaurs(dt)
        super().update(dt)

    def reset(self):
        """Reset the game."""
        super().reset()
        self.dinosaur.reset(45)
        self.user_collision = False
        self.game_over_group.visible = False

    def on_close(self):
        """Close the game."""
        super().on_close()
        self.dinosaur.delete()
        self.reset_button.delete()
