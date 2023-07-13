import pyglet
from pyglet.window import key, Window as BaseWindow
from .hud import FPSDisplay
from ..event_handlers import PlayerEventHandler, NEATEventHandler
from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_FILE_NAME, FONT_NAME


class Window(BaseWindow):
    def __init__(self, enable_neat=False, night_mode=False, *args, **kwargs):
        """Create a window."""
        super().__init__(
            caption="Google Chrome Dinosaur Game (with NEAT)",
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            *args,
            **kwargs
        )

        # Change the background color to white unless the user selects night mode
        if not night_mode:
            pyglet.gl.glClearColor(1, 1, 1, 1)

        # Generate the font style
        pyglet.font.add_file(FONT_FILE_NAME)
        pyglet.font.load(FONT_NAME)

        # Create the game event handler
        if enable_neat:
            self.game = NEATEventHandler(night_mode=night_mode)
        else:
            self.game = PlayerEventHandler(night_mode=night_mode)

        # Set and draw the FPS display
        self.fps_display = FPSDisplay(self)
        pyglet.clock.schedule_interval(self.update, 1/60)

    def run(self):
        """Run the window."""
        self.game.run()

    def on_key_press(self, symbol, modifiers):
        """Handle the events when a key is pressed."""
        # Terminate the game if the ESC key is pressed
        if symbol == key.ESCAPE:
            self.on_close()

        self.game.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        """Handle the events when a key is released."""
        self.game.on_key_release(symbol, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle the events when the mouse is pressed."""
        self.game.on_mouse_press(x, y, button, modifiers)

    def on_draw(self):
        """Draw the contents on the screen."""
        self.clear()  # Clear the screen
        self.game.draw()
        self.fps_display.draw()

    def update(self, dt):
        """Update the game."""
        self.game.update(dt)

    def on_close(self):
        """Terminate the game if the window is closed."""
        self.game.on_close()
        super().on_close()
