import pymunk


init_mass = 1
init_moment = 100

head_init_mass = 100
head_init_moment = 10000

init_width = 10
init_height = 50

head_init_width = 12
head_init_height = 60


class Snake:
    def __init__(self):
        head_body = pymunk.Body(
            head_init_mass, head_init_moment, body_type=pymunk.Body.DYNAMIC
        )
        head_body.position = 400, 400
        head_poly = pymunk.Poly.create_box(
            head_body, (head_init_width, head_init_height)
        )
        self.head = head_poly
        self.snake = [self.head]

    def grow(self):
        new_body = pymunk.Body(init_mass, init_moment, body_type=pymunk.Body.DYNAMIC)
        new_body.position = 400, (400 - 60 * len(self.snake))
        new_poly = pymunk.Poly.create_box(new_body, (init_width, init_height))
        last_body = self.snake[len(self.snake) - 1].body
        self.snake.append(new_poly)
        c = pymunk.PivotJoint(new_body, last_body, (0, 30), (0, -30))
        return c
