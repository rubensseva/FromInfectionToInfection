import pymunk
from pymunk.vec2d import Vec2d

import random
import time


init_position_default = Vec2d(0.0, 0.0)
init_mass_default = 10
init_moment_default = 10000
init_radius_default = 5
move_force_default = 1000
growth_factor_default = 1


class Blob:
    def __init__(
        self,
        init_position=init_position_default,
        init_mass=init_mass_default,
        init_moment=init_moment_default,
        init_radius=init_radius_default,
        move_force=move_force_default,
        growth_factor=growth_factor_default,
    ):
        self.init_mass = init_mass
        self.init_moment = init_moment
        self.init_radius = init_radius
        self.move_force = move_force
        self.growth_factor = growth_factor
        body = pymunk.Body(init_mass, init_moment, body_type=pymunk.Body.DYNAMIC)
        body.position = init_position
        poly = pymunk.Circle(body, init_radius)
        self.shape = poly
        self.time_of_last_turn = time.time() - 10000
        self.move_state = "FORWARD"
        self.move_dict = {
            "FORWARD": self.moveForward,
            "LEFT": self.moveLeft,
            "RIGHT": self.moveRight,
            "BACK": self.moveBack,
        }
        self.change_dir_ask()

    def grow(self):
        self.shape.radius += self.growth_factor

    def change_dir_ask(self):
        current_time = time.time()
        if current_time - self.time_of_last_turn < 1:
            return
        rand = random.random()
        if rand < 0.25:
            self.move_state = "FORWARD"
        elif rand < 0.50:
            self.move_state = "LEFT"
        elif rand < 0.75:
            self.move_state = "RIGHT"
        else:
            self.move_state = "BACK"
        self.time_of_last_turn = time.time()

    def move(self):
        self.move_dict[self.move_state]()

    def moveForward(self):
        body = self.shape.body
        body.apply_impulse_at_local_point((0, self.move_force), (0, 0))

    def moveRight(self):
        body = self.shape.body
        body.apply_impulse_at_local_point((self.move_force, 0), (0, 0))

    def moveLeft(self):
        body = self.shape.body
        body.apply_impulse_at_local_point((-self.move_force, 0), (0, 0))

    def moveBack(self):
        body = self.shape.body
        body.apply_impulse_at_local_point((0, -self.move_force), (0, 0))
