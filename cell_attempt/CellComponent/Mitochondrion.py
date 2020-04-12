import pymunk
from pymunk.vec2d import Vec2d

import random
import time

from Snake import Snake
from CellComponent.ATP import ATP


class Mitochondrion(Snake):
    def __init__(self, parentCell, init_position=Vec2d(0.0, 0.0), init_angle=0.0):
        super().__init__(
            init_position=init_position,
            init_angle=init_angle,
            init_mass=10000,
            init_moment=1000000,
            head_init_mass=10000,
            head_init_moment=1000000,
            init_width=5,
            init_height=10,
            head_init_width=5,
            head_init_height=10,
            pivot_joint_pos=5,
        )
        self.parentCell = parentCell

    def timeStep(self):
        # Grow
        if (len(self.snake) < 2 and random.random() < 0.01) or random.random() < 0.0001:
            constraint = self.grow()
            new_snake_part = self.getLastBlock()
            self.parentCell.relative_space.add(new_snake_part.body, new_snake_part)
            self.parentCell.relative_space.add(constraint)

        # Create ATP
        if random.random() < 0.1:
            print("creating ATP")
            new_ATP = ATP(self.parentCell, init_position=self.head.body.position)
            self.parentCell.ATP.append(new_ATP)
            self.parentCell.relative_space.add(new_ATP.shape.body, new_ATP.shape)

        # Move
        self.move()
        if random.random() < 0.1:
            self.change_dir_ask()
