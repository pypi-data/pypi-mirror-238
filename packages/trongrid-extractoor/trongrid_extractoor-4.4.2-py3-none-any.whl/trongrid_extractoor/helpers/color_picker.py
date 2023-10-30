"""
Generate a random color of the rainbow that will stay the same across various calls
with the same arguments.
"""
from functools import lru_cache

COLORS = ['red', 'blue', 'bright_green', 'magenta', 'bright_red', 'bright_yellow', 'cyan', 'bright_cyan', 'blue']


class ColorPicker:
    def __init__(self) -> None:
        self.color_idx = 0

    @lru_cache
    def pick_color(self, event_name: str) -> str:
        color = COLORS[self.color_idx]
        self.color_idx += 1

        if self.color_idx == len(COLORS):
            self.color_idx = 0

        return color
