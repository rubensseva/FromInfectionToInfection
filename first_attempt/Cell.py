import pymunk
import random


init_x, init_y = 400, 400
init_age = 10


class Cell:
    def __init__(self, x=init_x, y=init_y):
        init_mass = 1
        init_moment = 1666
        init_rad = 15
        body = pymunk.Body(init_mass, init_moment)
        body.position = x, y
        self.shape = pymunk.Circle(body, init_rad)
        self.age = init_age

    def apply_rand_force(self):
        rand_x = (0.5 - random.random()) * 10
        rand_y = (0.5 - random.random()) * 10
        self.shape.body.apply_impulse_at_local_point(
            (rand_x, rand_y), point=(-rand_x, -rand_y)
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
