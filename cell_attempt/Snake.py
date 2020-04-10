import pymunk
from pymunk.vec2d  import Vec2d


init_mass = 10
init_moment = 100

head_init_mass = 10000
head_init_moment = 1000000

# When changing height, should also change pivot joint pos
# Heights should be similar
init_width = 10
init_height = 20
head_init_width = 12
head_init_height = 20
pivot_joint_pos = 11

snake_rotation_force = 80
snake_rotation_y_point = 20
snake_move_force = 10000

class Snake:
    def __init__(self, init_position=Vec2d(0.0, 0.0), init_angle = 0.0):
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

    def getLastBlock(self):
        return self.snake[len(self.snake) - 1]

    def grow(self):
        last_body = self.snake[len(self.snake) - 1].body
        last_body_end_position = Vec2d(0.0, -((init_height) + 1))
        last_body_end_position.rotate(last_body.angle)
        new_body = pymunk.Body(init_mass, init_moment, body_type=pymunk.Body.DYNAMIC)
        new_body.angle = last_body.angle
        new_body.position = last_body.position + last_body_end_position
        new_poly = pymunk.Poly.create_box(new_body, (init_width, init_height))
        self.snake.append(new_poly)
        c = pymunk.PivotJoint(new_body, last_body, (0, pivot_joint_pos), (0, -pivot_joint_pos))
        return c

    def moveForward(self):
        head_body = self.head.body
        head_body.apply_impulse_at_local_point((0, snake_move_force), (0, 0))
    def moveRight(self):
        head_body = self.head.body
        head_body.apply_impulse_at_local_point(
            (snake_rotation_force, 0), (0, snake_rotation_y_point)
        )
        head_body.apply_impulse_at_local_point(
            (-snake_rotation_force, 0), (0, -snake_rotation_y_point)
        )
    def moveLeft(self):
        head_body = self.head.body
        head_body.apply_impulse_at_local_point(
            (-snake_rotation_force, 0), (0, snake_rotation_y_point)
        )
        head_body.apply_impulse_at_local_point(
            (snake_rotation_force, 0), (0, -snake_rotation_y_point)
        )
