'''
Justin Farnsworth
Google Chrome Dinosaur Game (with NEAT)
November 12, 2020

This is a subclass of the window class in pyglet.
'''

# Imported modules
import pyglet
from pyglet.window import key, mouse, FPSDisplay
from .gameEventHandler import GameEventHandler
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME, GENERATIONS


# Game window class
class GameWindow(pyglet.window.Window):
    # Constructor
    def __init__(self, enable_neat=False, night_mode=False, *args, **kwargs):
        # Inherit the pyglet window
        super().__init__(
            caption="Google Chrome Dinosaur Game (with NEAT)",
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            *args,
            **kwargs
        )

        # Save the configuration that determines if the NEAT algorithm is used
        self.enable_neat = enable_neat
        
        # Generate the font style
        pyglet.font.add_file(FONT_NAME)
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

        # Create the game instance
        self.game = GameEventHandler(enable_neat=enable_neat, night_mode=night_mode)

        # If NEAT is enabled, run the game using NEAT. Otherwise, let the player play manually
        if enable_neat:
            self.game.run_neat()
        else:
            pyglet.app.run()


    # Handle the events when a key is pressed
    def on_key_press(self, symbol, modifiers):
        # Terminate the game if the ESC key is pressed
        if symbol == key.ESCAPE:
            self.on_close()
        
        # Disable if the NEAT algorithm is being used
        if not self.enable_neat:
            # Check if the user triggers a duck or jump (duck is a priority over jump)
            if symbol in (key.DOWN, key.S):
                self.game.trigger_duck = True
            elif symbol in (key.SPACE, key.UP, key.W):
                self.game.trigger_jump = True

            # Accept the ENTER key only if the game is over
            if self.game.user_collision and symbol == key.ENTER:
                self.game.reset()

    
    # Handle the events when a key is released
    def on_key_release(self, symbol, modifiers):
        # Disable if the NEAT algorithm is being used
        if not self.enable_neat:
            # Check if the user released a key that triggers a duck
            if symbol in (key.DOWN, key.S):
                self.game.trigger_duck = False
            
            # Check if the user released a key that triggers a jump
            if symbol in (key.SPACE, key.UP, key.W):
                self.game.trigger_jump = False

    
    # Handle the events when the mouse is pressed
    def on_mouse_press(self, x, y, button, modifiers):
        # Handle the left click
        if button == mouse.LEFT:
            self.game.on_mouse_press(x, y)


    # Draw the contents on the screen
    def on_draw(self):
        self.clear() # Clear the screen
        self.game.draw() # Draw the game
        self.fps_display.draw() # Draw the FPS

    
    # Update the objects
    def update(self, dt):
        self.game.update(dt)
    

    # Terminate the game if the window is closed
    def on_close(self):
        self.game.user_exit = True
        super().on_close()
