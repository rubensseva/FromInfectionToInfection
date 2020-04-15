import pymunk
from pymunk.vec2d import Vec2d

import random
import time


init_position_default = Vec2d(0.0, 0.0)
init_angle_default = 0.0

init_mass_default = 10
init_moment_default = 100

head_init_mass_default = 10
head_init_moment_default = 1000

init_width_default = 5
init_height_default = 10
head_init_width_default = 7
head_init_height_default = 10
pivot_joint_pos_default = 7

snake_rotation_force_default = 70
snake_rotation_y_point_default = 20
snake_move_force_default = 5


class Snake:
    def __init__(
        self,
        init_position=init_position_default,
        init_angle=init_angle_default,
        init_mass=init_mass_default,
        init_moment=init_moment_default,
        head_init_mass=head_init_mass_default,
        head_init_moment=head_init_moment_default,
        init_width=init_width_default,
        init_height=init_height_default,
        head_init_width=head_init_width_default,
        head_init_height=head_init_height_default,
        pivot_joint_pos=pivot_joint_pos_default,
        snake_rotation_force=snake_rotation_force_default,
        snake_rotation_y_point=snake_rotation_y_point_default,
        snake_move_force=snake_move_force_default,
    ):
        self.init_height = init_height
        self.init_width = init_width
        self.init_mass = init_mass
        self.init_moment = init_moment
        self.pivot_joint_pos = pivot_joint_pos
        self.snake_move_force = snake_move_force
        self.snake_rotation_force = snake_rotation_force
        self.snake_rotation_y_point = snake_rotation_y_point

        head_body = pymunk.Body(
            head_init_mass, head_init_moment, body_type=pymunk.Body.DYNAMIC
        )
        head_body.position = init_position
        head_body.angle = init_angle
        head_poly = pymunk.Poly.create_box(
            head_body, (head_init_width, head_init_height)
        )
        self.head = head_poly
        self.snake = [self.head]

        self.time_of_last_turn = time.time() - 10000
        self.move_state = "FORWARD"
        self.move_dict = {
            "FORWARD": self.moveForward,
            "LEFT": self.moveLeft,
            "RIGHT": self.moveRight,
        }
        self.change_dir_ask()

    def getLastBlock(self):
        return self.snake[len(self.snake) - 1]

    def grow(self):
        last_body = self.snake[len(self.snake) - 1].body
        last_body_end_position = Vec2d(0.0, -((self.init_height) + 1))
        last_body_end_position.rotate(last_body.angle)
        new_body = pymunk.Body(
            self.init_mass, self.init_moment, body_type=pymunk.Body.DYNAMIC
        )
        new_body.angle = last_body.angle
        new_body.position = last_body.position + last_body_end_position
        new_poly = pymunk.Poly.create_box(new_body, (self.init_width, self.init_height))
        self.snake.append(new_poly)
        c = pymunk.PivotJoint(
            new_body, last_body, (0, self.pivot_joint_pos), (0, -self.pivot_joint_pos)
        )
        c.max_force = 100000
        return c

    def change_dir_ask(self):
        current_time = time.time()
        if current_time - self.time_of_last_turn < 1:
            return
        rand = random.random()
        if rand < 0.33:
            self.move_state = "FORWARD"
        elif rand < 0.66:
            self.move_state = "LEFT"
        else:
            self.move_state = "RIGHT"
        self.time_of_last_turn = time.time()

    def move(self):
        self.move_dict[self.move_state]()

    def moveForward(self):
        head_body = self.head.body
        head_body.apply_impulse_at_local_point((0, self.snake_move_force), (0, 0))

    def moveRight(self):
        head_body = self.head.body
        head_body.apply_impulse_at_local_point(
            (self.snake_rotation_force, 0), (0, self.snake_rotation_y_point)
        )
        head_body.apply_impulse_at_local_point(
            (-self.snake_rotation_force, 0), (0, -self.snake_rotation_y_point)
        )

    def moveLeft(self):
        head_body = self.head.body
        head_body.apply_impulse_at_local_point(
            (-self.snake_rotation_force, 0), (0, self.snake_rotation_y_point)
        )
        head_body.apply_impulse_at_local_point(
            (self.snake_rotation_force, 0), (0, -self.snake_rotation_y_point)
        )
