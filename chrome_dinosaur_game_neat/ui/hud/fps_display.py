from pyglet.window import FPSDisplay as BaseFPSDisplay
from ...constants import WINDOW_WIDTH, FONT_NAME


class FPSDisplay(BaseFPSDisplay):
    def __init__(self, window):
        """Create a HUD item that shows the FPS."""
        super().__init__(window)
        self.label.x = WINDOW_WIDTH - 10
        self.label.y = 10
        self.label.anchor_x = "right"
        self.label.font_name = FONT_NAME
        self.label.font_size = 20
        self.label.color = (192, 192, 192, 192)
