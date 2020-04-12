import pymunk  # Import pymunk..
import pymunk.pygame_util
import pygame
import pygame.gfxdraw
import pygame.transform

import random
import time

from PygamePymunkTranslation import drawPymunkCircle, drawPymunkSegments, drawPymunkPoly
from Cell import Cell

pygame.init()

width = 1000
height = 1000

screen = pygame.display.set_mode((width, height))
options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()
space.damping = 0.7

floor = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
floor.position = width / 2, 0
floor_poly = pymunk.Poly.create_box(floor, (width, 10))
space.add(floor, floor_poly)

right_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
right_wall.position = width, height / 2
right_wall_poly = pymunk.Poly.create_box(right_wall, (10, height))
space.add(right_wall, right_wall_poly)

roof = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
roof.position = width / 2, height
roof_poly = pymunk.Poly.create_box(roof, (width, 10))
space.add(roof, roof_poly)

left_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
left_wall.position = 0, height / 2
left_wall_poly = pymunk.Poly.create_box(left_wall, (10, height))
space.add(left_wall, left_wall_poly)

first_cell = Cell()

cells = [first_cell]

space.add(first_cell.shape.body, first_cell.shape)


count = 0
lastTime = time.time()
done = False
while not done:
    screen.fill((0, 0, 0))
    currentTime = time.time()
    elapsedTime = currentTime - lastTime
    space.step(elapsedTime)

    for cell in cells:
        currentTime = time.time()
        elapsedTime = currentTime - lastTime
        cell.relative_space.step(elapsedTime)
    lastTime = time.time()

    for cell in cells:
        cell.apply_rand_force()

    for cell in cells:
        drawPymunkCircle(cell.shape, screen)

    for cell in cells:
        for mitochondrion in cell.mitochondria:
            for snake_part in mitochondrion.snake:
                drawPymunkPoly(snake_part, screen, relativeTo=cell.shape.body.position)
        for ATP in cell.ATP:
            drawPymunkCircle(ATP.shape, screen, relativeTo=cell.shape.body.position)

    for cell in cells:
        if random.random() < 0.1:
            cell.timeStep()

    # drawPymunkPoly(inner_block_poly, screen, relativeTo=outer_block.position)
    # drawPolyRelativeToBody(inner_block_poly, outer_block, screen)

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        print("key pressed")
    if keystate[pygame.K_RIGHT]:
        print("key pressed")
    if keystate[pygame.K_UP]:
        print("key pressed")
    if keystate[pygame.K_DOWN]:
        print("key pressed")

    if keystate[pygame.K_a]:
        print("key pressed")
    if keystate[pygame.K_d]:
        print("key pressed")
    if keystate[pygame.K_w]:
        print("key pressed")
    if keystate[pygame.K_s]:
        print("key pressed")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cell = Cell()
                space.add(cell.shape.body, cell.shape)
                cells.append(cell)
                print("Space pressed")
            if event.key == pygame.K_a:
                constraint = cell.snakes[0].grow()
                new_snake_part = cell.snakes[0].snake[len(cell.snakes[0].snake) - 1]
                cell.relative_space.add(new_snake_part.body, new_snake_part)
                cell.relative_space.add(constraint)
                print("Space pressed")
            if event.key == pygame.K_f:
                cell.snakes[0].moveForward()
                print("Space pressed")

    pygame.display.flip()
