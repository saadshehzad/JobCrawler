from abc import ABC, abstractmethod


class Human(ABC):
    def __init__(self):
        pass

    def random_sleep(self):
        """Introduce random delays."""

    def random_mouse_move(self):
        """Simulate random mouse movements."""

    def random_scroll(self):
        """Simulate random scrolling behavior."""

    def pause_to_mimic_reading(self):
        """Pause to mimic reading content."""