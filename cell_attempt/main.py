import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util
import pygame
import pygame.gfxdraw
import pygame.transform

import random
import time

from pygame_pymunk_translation import (
    draw_pymunk_circle,
    draw_pymunk_segments,
    draw_pymunk_poly,
)
from cell import Cell

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
# space.add(floor, floor_poly)

right_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
right_wall.position = width, height / 2
right_wall_poly = pymunk.Poly.create_box(right_wall, (10, height))
# space.add(right_wall, right_wall_poly)

roof = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
roof.position = width / 2, height
roof_poly = pymunk.Poly.create_box(roof, (width, 10))
# space.add(roof, roof_poly)

left_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
left_wall.position = 0, height / 2
left_wall_poly = pymunk.Poly.create_box(left_wall, (10, height))
# space.add(left_wall, left_wall_poly)

first_cell = Cell()

cells = [first_cell]

space.add(first_cell.shape.body, first_cell.shape)

cameraZoom = 0
cameraPosition = Vec2d(0, 0)

count = 0
lastTime = time.time()
done = False
while not done:
    screen.fill((0, 0, 0))
    currentTime = time.time()
    elapsedTime = currentTime - lastTime
    lastTime = currentTime
    space.step(elapsedTime)

    for cell in cells:
        cell.apply_rand_force()

    for cell in cells:
        draw_pymunk_circle(
            cell.shape, screen, scale=cameraZoom, cameraPosition=cameraPosition
        )

    for cell in cells:
        for mitochondrion in cell.mitochondria:
            for snake_part in mitochondrion.snake:
                draw_pymunk_poly(
                    snake_part,
                    screen,
                    relativeTo=cell.shape.body.position,
                    scale=cameraZoom,
                    cameraPosition=cameraPosition,
                )
        for ATP in cell.ATP:
            draw_pymunk_circle(
                ATP.shape,
                screen,
                relativeTo=cell.shape.body.position,
                scale=cameraZoom,
                cameraPosition=cameraPosition,
            )
        draw_pymunk_circle(
            cell.nucleus.shape,
            screen,
            relativeTo=cell.shape.body.position,
            scale=cameraZoom,
            cameraPosition=cameraPosition,
        )

    for cell in cells:
        cell.time_step()
    for cell in cells:
        new_cell = cell.split_check()
        if new_cell != None:
            cells.append(new_cell)
            space.add(new_cell.shape.body, new_cell.shape)

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        cameraPosition.x += 1 * (cameraZoom ** 10 + 1)
    if keystate[pygame.K_RIGHT]:
        cameraPosition.x -= 1 * (cameraZoom ** 10 + 1)
    if keystate[pygame.K_UP]:
        cameraPosition.y -= 1 * (cameraZoom ** 10 + 1)
    if keystate[pygame.K_DOWN]:
        cameraPosition.y += 1 * (cameraZoom ** 10 + 1)

    if keystate[pygame.K_a]:
        print("key pressed")
    if keystate[pygame.K_d]:
        print("key pressed")
    if keystate[pygame.K_w]:
        print("key pressed")
    if keystate[pygame.K_s]:
        print("key pressed")

    if keystate[pygame.K_z]:
        print("z key pressed")
        cameraZoom += 0.01
    if keystate[pygame.K_x]:
        print("x key pressed")
        cameraZoom -= 0.01

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
