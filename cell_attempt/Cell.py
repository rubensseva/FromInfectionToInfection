import pymunk
from pymunk.vec2d import Vec2d
import random

from Snake import Snake


init_x, init_y = 400, 400
init_age = 10
init_rad = 400

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

        self.snakes = []

    def apply_rand_force(self):
        rand_x = (0.5 - random.random()) * 1
        rand_y = (0.5 - random.random()) * 1
        self.shape.body.apply_impulse_at_local_point(
            (rand_x, rand_y), point=(0, 0)
        )

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
        rand_x = random.uniform(-init_rad / 2,init_rad / 2)
        rand_y = random.uniform(-init_rad / 2,init_rad / 2)
        rand_angle = random.uniform(-3.0, 3.0)
        snake = Snake(init_position=Vec2d(rand_x, rand_y), init_angle=rand_angle)
        for poly in snake.snake:
            self.relative_space.add(poly.body, poly)
        self.snakes.append(snake)
    
    def timeStep(self):
        # Create new snakes
        if (random.random() < 0.01):
            self.addSnake()

        # Grow snakes
        for snake in self.snakes:
            if ((len(snake.snake) < 7 and random.random() < 0.05) or random.random() < 0.0001):
                constraint = snake.grow()
                new_snake_part = snake.getLastBlock()
                self.relative_space.add(new_snake_part.body, new_snake_part)
                self.relative_space.add(constraint)

        # Move snakes
        for snake in self.snakes:
            if (random.random() > 0.6): 
                snake.moveForward()
            elif (random.random() > 0.3): 
                snake.moveLeft()
            else:
                snake.moveRight()

