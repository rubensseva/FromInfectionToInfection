import pymunk  # Import pymunk..
import pymunk.pygame_util
import pygame
import pygame.gfxdraw
import pygame.transform

import random
import time

from PygamePymunkTranslation import drawPymunkSegments, drawPymunkPoly

pygame.init()

width = 1000
height = 1000

screen = pygame.display.set_mode((width, height))
options = pymunk.pygame_util.DrawOptions(screen)

outer_space = pymunk.Space()
outer_space.damping = 0.7
inner_space = pymunk.Space()
inner_space.damping = 0.7

outer_block = pymunk.Body(1, 1666, body_type=pymunk.Body.DYNAMIC)
outer_block.position = 400, 400
segments_positions = [
    [(-50, 50), (50, 50)],
    [(50, 50), (50, -50)],
    [(50, -50), (-50, -50)],
    [(-50, -50), (-50, 50)],
]
segments = [
    pymunk.Segment(outer_block, segment_positions[0], segment_positions[1], 1)
    for segment_positions in segments_positions
]
objects = [outer_block] + segments
outer_space.add(objects)


inner_border = pymunk.Body(1, 1666, body_type=pymunk.Body.KINEMATIC)
inner_border.position = 0, 0
segments_positions = [
    [(-50, 50), (50, 50)],
    [(50, 50), (50, -50)],
    [(50, -50), (-50, -50)],
    [(-50, -50), (-50, 50)],
]
segments = [
    pymunk.Segment(inner_border, segment_positions[0], segment_positions[1], 1)
    for segment_positions in segments_positions
]
objects = [inner_border] + segments
inner_space.add(objects)

inner_block = pymunk.Body(1, 1666, body_type=pymunk.Body.DYNAMIC)
inner_block.position = 0, 0
inner_block_poly = pymunk.Poly.create_box(inner_block, (30, 30))
inner_space.add(inner_block, inner_block_poly)

lastTime = time.time()
done = False
while not done:
    currentTime = time.time()
    elapsedTime = currentTime - lastTime
    lastTime = time.time()
    outer_space.step(elapsedTime)
    inner_space.step(elapsedTime)

    screen.fill((0, 0, 0))
    drawPymunkSegments(outer_block, screen)
    drawPymunkPoly(inner_block_poly, screen, relativeTo=outer_block.position)
    # drawPolyRelativeToBody(inner_block_poly, outer_block, screen)

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
        outer_block.apply_force_at_local_point((-20, 0), (0, 0))
    if keystate[pygame.K_RIGHT]:
        outer_block.apply_force_at_local_point((20, 0), (0, 0))
    if keystate[pygame.K_UP]:
        outer_block.apply_force_at_local_point((0, 20), (0, 0))
    if keystate[pygame.K_DOWN]:
        outer_block.apply_force_at_local_point((0, -20), (0, 0))

    if keystate[pygame.K_a]:
        inner_block.apply_force_at_local_point((-20, 0), (0, 0))
    if keystate[pygame.K_d]:
        inner_block.apply_force_at_local_point((20, 0), (0, 0))
    if keystate[pygame.K_w]:
        inner_block.apply_force_at_local_point((0, 20), (0, 0))
    if keystate[pygame.K_s]:
        inner_block.apply_force_at_local_point((0, -20), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space pressed")

    pygame.display.flip()