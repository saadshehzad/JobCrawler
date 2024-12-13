import random
import time
from abc import ABC, abstractmethod

import pyautogui


class Human(ABC):

    def __init__(self):
        pass

    def random_sleep_between_applying(self, min_sleep=3, max_sleep=10):
        """Introduce random delays."""
        time.sleep(random.uniform(min_sleep, max_sleep))

    def random_sleep_after_apply(self, min_sleep=12, max_sleep=20):
        """Introduce random delays."""
        time.sleep(random.uniform(min_sleep, max_sleep))

    def random_sleep_after_applying_10_jobs(self, min_sleep=20, max_sleep=30):
        """Introduce random delays."""
        time.sleep(random.uniform(min_sleep, max_sleep))

    def random_mouse_move(self, x_range=(0, 1920), y_range=(0, 1080)):
        """Simulate random mouse movements."""
        x = random.randint(*x_range)
        y = random.randint(*y_range)
        duration = random.uniform(0.5, 3)
        pyautogui.move(x, y, duration=duration)

    def random_scroll(self):
        """Simulate random scrolling behavior."""

    def pause_to_mimic_reading(self):
        """Pause to mimic reading content."""
