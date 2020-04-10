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

cell = Cell()

cells = [cell]

space.add(cell.shape.body, cell.shape)


count = 0
lastTime = time.time()
done = False
while not done:
    screen.fill((0, 0, 0))
    currentTime = time.time()
    elapsedTime = currentTime - lastTime
    lastTime = time.time()
    space.step(elapsedTime)
    
    cell.relative_space.step(elapsedTime)


    cell.apply_rand_force()

    drawPymunkCircle(cell.shape, screen)

    for cell in cells:
        for snake in cell.snakes:
            for snake_part in snake.snake:
                drawPymunkPoly(snake_part, screen, relativeTo=cell.shape.body.position)

    for cell in cells:
        if (random.random() < 0.1):
            cell.timeStep()

    # drawPymunkPoly(inner_block_poly, screen, relativeTo=outer_block.position)
    # drawPolyRelativeToBody(inner_block_poly, outer_block, screen)
    print(cell.snakes)

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
                cell.addSnake()
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
