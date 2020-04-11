import pymunk
from pymunk.vec2d import Vec2d
import random
import math

from Snake import Snake


init_x, init_y = 400, 400
init_age = 10
init_rad = 100


class Cell:
    def __init__(self, x=init_x, y=init_y):
        init_mass = 1
        init_moment = 1666
        body = pymunk.Body(init_mass, init_moment)
        body.position = x, y
        self.shape = pymunk.Circle(body, init_rad)
        self.age = init_age

        self.relative_space = pymunk.Space()
        self.relative_space.damping = 0.7

        relative_boundary_body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        relative_boundary_body.position = 0, 0

        r = init_rad

        # sin(a) = opposite / hyp
        # opposite = sin(a) * hyp
        # opposite = y
        # cos(a) = adj / hyp
        # adj = cos(a) * hyp
        # adj = x
        num_splits = 16  # the resulting number of "pieces of cake
        one_section = (
            math.pi * 2 / num_splits
        )  # math.pi * 2 is 360 deg in radians. Split this in equal parts
        segments_positions = []
        for i in range(num_splits):
            current_section = i * one_section
            next_section = (i + 1) * one_section
            ax = math.cos(current_section) * r
            ay = math.sin(current_section) * r
            bx = math.cos(next_section) * r
            by = math.sin(next_section) * r
            segments_positions.append([(ax, ay), (bx, by)])

        segments = [
            pymunk.Segment(
                relative_boundary_body, segment_positions[0], segment_positions[1], 5
            )
            for segment_positions in segments_positions
        ]

        objects = [relative_boundary_body] + segments
        self.relative_space.add(objects)

        self.snakes = []

    def apply_rand_force(self):
        rand_x = (0.5 - random.random()) * 5
        rand_y = (0.5 - random.random()) * 5
        self.shape.body.apply_impulse_at_local_point((rand_x, rand_y), point=(0, 0))

    def split(self):
        self.age = init_age
        rand_x = (0.5 - random.random()) / 10
        rand_y = (0.5 - random.random()) / 10
        return Cell(
            self.shape.body.position.x + rand_x, self.shape.body.position.y + rand_y
        )

    def increment_age(self):
        self.age += 1

    def addSnake(self):
        rand_x = random.uniform(-init_rad / 4, init_rad / 4)
        rand_y = random.uniform(-init_rad / 4, init_rad / 4)
        rand_angle = random.uniform(-3.0, 3.0)
        snake = Snake(init_position=Vec2d(rand_x, rand_y), init_angle=rand_angle)
        for poly in snake.snake:
            self.relative_space.add(poly.body, poly)
        self.snakes.append(snake)

    def timeStep(self):
        # Create new snakes
        if random.random() < 0.01:
            self.addSnake()

        # Grow snakes
        for snake in self.snakes:
            if (
                len(snake.snake) < 5 and random.random() < 0.01
            ) or random.random() < 0.0001:
                constraint = snake.grow()
                new_snake_part = snake.getLastBlock()
                self.relative_space.add(new_snake_part.body, new_snake_part)
                self.relative_space.add(constraint)

        # Move snakes
        for snake in self.snakes:
            snake.move()
            if random.random() < 0.1:
                snake.change_dir_ask()
