import pymunk  # Import pymunk..
import pygame
import pygame.gfxdraw

pygame.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((1000, 1000))

space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, 1  # Set its gravi

body = pymunk.Body(1, 1666)  # Create a Body with mass and moment
body.position = 400, 10  # Set the position of the body

poly = pymunk.Poly.create_box(body)  # Create a box shape and attach to body
space.add(body, poly)  # Add both body and shape to the simulation

boxes = [poly]
circles = []

floor = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
floor.position = 400, 500
floorPoly = pymunk.Poly.create_box(floor, (200, 10))
space.add(floor, floorPoly)

done = False


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


def drawPymunkCircle(pymunk_circle):
    lineThickness = 1
    radius = 10
    pygame.gfxdraw.circle(
        screen,
        int(pymunk_circle.body.position.x),
        int(pymunk_circle.body.position.y),
        radius,
        (255, 255, 255),
    )


count = 0
while not done:  # Infinite loop simulation
    space.step(0.02)  # Step the simulation one step forward
    screen.fill((0, 0, 0))
    if count % 10 == 0:
        new_body = pymunk.Body(1, 1666)  # Create a Body with mass and moment
        new_body.position = 400, 10  # Set the position of the body
        new_poly = pymunk.Circle(new_body, 10)  # Create a box shape and attach to body
        space.add(new_body, new_poly)  # Add both body and shape to the simulation
        circles.append(new_poly)
        count = 0
        print("number of boxes: " + str(len(boxes)))
    count += 1
    drawPymunkPoly(floorPoly)

    boxes = list(
        filter(lambda x: x.body.position.x < 800 and x.body.position.y < 800, boxes)
    )
    circles = list(
        filter(lambda x: x.body.position.x < 800 and x.body.position.y < 800, circles)
    )
    for obj in boxes:
        drawPymunkPoly(obj)
    for obj in circles:
        drawPymunkCircle(obj)
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_body = pymunk.Body(1, 1666)  # Create a Body with mass and moment
                new_body.position = 400, 10  # Set the position of the body
                new_poly = pymunk.Poly.create_box(
                    new_body
                )  # Create a box shape and attach to body
                space.add(
                    new_body, new_poly
                )  # Add both body and shape to the simulation
                boxes.append(new_poly)

    pygame.display.flip()
