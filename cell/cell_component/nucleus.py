import pymunk
from pymunk.vec2d import Vec2d

import random
import time

from shapes.blob import Blob


class Nucleus(Blob):
    def __init__(self, parent_cell, init_position=Vec2d(0.0, 0.0)):
        super().__init__(
            init_position=init_position,
            init_mass=10000,
            init_moment=1000000,
            init_radius=20,
            move_force=500,
            growth_factor=1,
        )
        self.parent_cell = parent_cell

    def time_step(self):
        self.move()
        if random.random() < 0.1:
            self.change_dir_ask()
