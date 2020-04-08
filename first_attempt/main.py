import pymunk               # Import pymunk..
import pygame
import pygame.gfxdraw

import random
import time

from Cell import Cell

pygame.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((1000, 1000))

space = pymunk.Space()
# space.gravity = 0,1


floor = pymunk.Body(100, 1000000, body_type=pymunk.Body.DYNAMIC)
floor.position = 400, 610
floor_poly = pymunk.Poly.create_box(floor, (400, 10))
space.add(floor, floor_poly)

right_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
right_wall.position = 600, 400
right_wall_poly = pymunk.Poly.create_box(right_wall, (10, 400))
space.add(right_wall, right_wall_poly)

roof = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
roof.position = 400, 200
roof_poly = pymunk.Poly.create_box(roof, (400, 10))
space.add(roof, roof_poly)

left_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
left_wall.position = 200, 400
left_wall_poly = pymunk.Poly.create_box(left_wall, (10, 400))
space.add(left_wall, left_wall_poly)



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
    pygame.gfxdraw.circle(screen, int(pymunk_circle.shape.body.position.x), int(pymunk_circle.shape.body.position.y), int(pymunk_circle.shape.radius), (255, 255, 255))

def drawPymunkPoly(pymunk_poly):
    lineThickness = 2
    points = []
    for v in pymunk_poly.get_vertices():
        x,y = v.rotated(pymunk_poly.body.angle) + pymunk_poly.body.position
        points.append((int(x), int(y)))
    last_v = pymunk_poly.get_vertices()[0]
    x,y = last_v.rotated(pymunk_poly.body.angle) + pymunk_poly.body.position
    points.append((int(x), int(y)))
    pygame.draw.lines(screen, (255, 255, 255), False, points, lineThickness)


count = 0
lastTime = time.time()
while not done:         
    currentTime = time.time()
    elapsedTime = currentTime - lastTime
    lastTime = currentTime
    print(elapsedTime)
    space.step(elapsedTime)        
    screen.fill((0, 0, 0))
    if count % 10 == 0:
        print("tick");
        for cell in cells:
            cell.apply_rand_force()
            if (cell.age > 100 and random.random() < 0.01):
                new_cell = cell.split()
                space.add(new_cell.shape.body, new_cell.shape)
                cells.append(new_cell)

    count += 1
    for cell in cells: 
        cell.increment_age()
        drawPymunkCircle(cell)

    drawPymunkPoly(floor_poly)
    drawPymunkPoly(right_wall_poly)
    drawPymunkPoly(roof_poly)
    drawPymunkPoly(left_wall_poly)

    cells = list(filter(lambda cell: cell.shape.body.position.x < 800 and cell.shape.body.position.y < 800, cells))

    for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space pressed")
                    createCell()

    pygame.display.flip();



