import pymunk
from pymunk.vec2d import Vec2d

import random
import time

from Blob import Blob


class ATP(Blob):
    def __init__(self, parentCell, init_position=Vec2d(0.0, 0.0)):
        super().__init__(
            init_position=init_position,
            init_mass=1,
            init_moment=100,
            init_radius=1,
            move_force=1,
            growth_factor=1,
        )
        self.parentCell = parentCell

    def timeStep(self):
        self.move()
        if random.random() < 0.1:
            self.change_dir_ask()
