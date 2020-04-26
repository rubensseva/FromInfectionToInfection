import pymunk
from pymunk.vec2d import Vec2d

import random
import time

from shapes.snake import Snake
from cell.cell_component.atp import ATP

grow_cooldown_time = 1
create_ATP_cooldown_time = 2


class Mitochondrion(Snake):
    def __init__(self, parent_cell, init_position=Vec2d(0.0, 0.0), init_angle=0.0):
        super().__init__(
            init_position=init_position,
            init_angle=init_angle,
            init_mass=100,
            init_moment=10000,
            head_init_mass=100,
            head_init_moment=10000,
            init_width=5,
            init_height=10,
            head_init_width=5,
            head_init_height=10,
            pivot_joint_pos=6,
            snake_move_force=15,
            snake_rotation_force=1,
        )
        self.parent_cell = parent_cell
        self.birth_time = time.time()
        self.last_grow_time = self.birth_time
        self.last_create_ATP_time = self.birth_time

    def time_step(self):
        # Grow
        current_time = time.time()
        if (
            current_time - self.last_grow_time > grow_cooldown_time
            and len(self.snake) < 2
            and random.random() < 0.01
        ) or random.random() < 0.0001:
            constraint = self.grow()
            new_snake_part = self.get_last_block()
            self.parent_cell.relative_space.add(new_snake_part.body, new_snake_part)
            self.parent_cell.relative_space.add(constraint)
            self.last_grow_time = time.time()

        # Create ATP
        current_time = time.time()
        if (
            current_time - self.last_create_ATP_time > create_ATP_cooldown_time
            and random.random() < 0.05
        ):
            self.parent_cell.create_ATP(init_position=self.head.body.position)
            self.last_create_ATP_time = time.time()

        # Move
        self.move()
        if random.random() < 0.1:
            self.change_dir_ask()
