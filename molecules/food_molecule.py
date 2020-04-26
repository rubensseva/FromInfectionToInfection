import pymunk
from pymunk.vec2d import Vec2d

import random
import time

from shapes.blob import Blob


class FoodMolecule(Blob):
    def __init__(self, parent_cell=None, init_position=Vec2d(0.0, 0.0)):
        super().__init__(
            init_position=init_position,
            init_mass=1,
            init_moment=100,
            init_radius=5,
            move_force=0.1,
            growth_factor=1,
        )
        self.parent_cell = parent_cell
        print("Food molecule created")

    def time_step(self):
        self.move()
        if random.random() < 0.1:
            self.change_dir_ask()
