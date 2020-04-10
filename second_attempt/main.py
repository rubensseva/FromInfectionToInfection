import pymunk  # Import pymunk..
import pymunk.pygame_util
import pygame
import pygame.gfxdraw

import random
import time

from Snake import Snake
from Cell import Cell

pygame.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((1000, 1000))
options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()
space.damping = 0.7
# space.gravity = 0,1


floor = pymunk.Body(100, 1000000, body_type=pymunk.Body.DYNAMIC)
floor.position = 400, 610
floor_poly = pymunk.Poly.create_box(floor, (400, 10))
# space.add(floor, floor_poly)

right_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
right_wall.position = 600, 400
right_wall_poly = pymunk.Poly.create_box(right_wall, (10, 400))
space.add(right_wall, right_wall_poly)

roof = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
roof.position = 400, 100
roof_poly = pymunk.Poly.create_box(roof, (400, 10))
# space.add(roof, roof_poly)

left_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
left_wall.position = 200, 400
left_wall_poly = pymunk.Poly.create_box(left_wall, (10, 400))
# space.add(left_wall, left_wall_poly)


snake = Snake()

for i in range(30):
    constraint = snake.grow()
    space.add(constraint)

for poly in snake.snake:
    space.add(poly.body, poly)


cells = []


def createCell():
    # body = pymunk.Body(1, 1666)
    # body.position = 400, 400
    # circle = pymunk.Circle(body, 15)
    new_cell = Cell()
    space.add(new_cell.shape.body, new_cell.shape)
    cells.append(new_cell)


done = False


def drawPymunkCircle(pymunk_circle):
    lineThickness = 1
    radius = 10
    pygame.gfxdraw.circle(
        screen,
        int(pymunk_circle.shape.body.position.x),
        int(pymunk_circle.shape.body.position.y),
        int(pymunk_circle.shape.radius),
        (255, 255, 255),
    )


def drawPymunkPoly(pymunk_poly):
    lineThickness = 2
    points = []
    for v in pymunk_poly.get_vertices():
        x, y = v.rotated(pymunk_poly.body.angle) + pymunk_poly.body.position
        points.append((int(x), int(y)))
    last_v = pymunk_poly.get_vertices()[0]
    x, y = last_v.rotated(pymunk_poly.body.angle) + pymunk_poly.body.position
    points.append((int(x), int(y)))
    pygame.draw.lines(screen, (255, 255, 255), False, points, lineThickness)


count = 0
lastTime = time.time()
while not done:
    currentTime = time.time()
    elapsedTime = currentTime - lastTime
    lastTime = time.time()
    space.step(elapsedTime)

    screen.fill((0, 0, 0))
    if count % 100 == 0:
        print("tick")
    count += 1

    space.debug_draw(options)

    cells = list(
        filter(
            lambda cell: cell.shape.body.position.x < 800
            and cell.shape.body.position.y < 800,
            cells,
        )
    )

    for cell in cells:
        cell.apply_rand_force()
        cell.increment_age()
        if cell.age > 1000 and random.random() < 0.0001:
            new_cell = cell.split()
            space.add(new_cell.shape.body, new_cell.shape)
            cells.append(new_cell)

    snake_rotation_force = 800
    snake_rotation_y_point = 20
    snake_move_force = 3000
    keystate = pygame.key.get_pressed()
    print(snake.head.body.angle)
    if keystate[pygame.K_LEFT]:
        print("applying force")
        head_body = snake.head.body
        head_body.apply_force_at_local_point(
            (-snake_rotation_force, 0), (0, snake_rotation_y_point)
        )
        head_body.apply_force_at_local_point(
            (snake_rotation_force, 0), (0, -snake_rotation_y_point)
        )
    if keystate[pygame.K_RIGHT]:
        print("applying force")
        head_body = snake.head.body
        head_body.apply_force_at_local_point(
            (snake_rotation_force, 0), (0, snake_rotation_y_point)
        )
        head_body.apply_force_at_local_point(
            (-snake_rotation_force, 0), (0, -snake_rotation_y_point)
        )
    if keystate[pygame.K_UP]:
        print("applying force")
        head_body = snake.head.body
        head_body.apply_force_at_local_point((0, snake_move_force), (0, 0))
    if keystate[pygame.K_DOWN]:
        print("applying force")
        head_body = snake.head.body
        head_body.apply_force_at_local_point((0, -snake_move_force), (0, 0))

    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space pressed")

    pygame.display.flip()
