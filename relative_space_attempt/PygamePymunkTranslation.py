import pymunk
import pygame
from pymunk.vec2d import Vec2d


def pymunkToPygameCoords(vector, displayHeight):
    vector.y = displayHeight - vector.y
    return vector


def drawPymunkCircle(pymunk_circle, screen):
    height = screen.get_height()
    lineThickness = 1
    radius = 10
    x, y = pymunkToPygameCoords(pymunk_circle.shape.body.position, height)
    pygame.gfxdraw.circle(
        screen, int(x), int(y), int(pymunk_circle.shape.radius), (255, 255, 255)
    )


def drawPymunkPoly(pymunk_poly, screen, relativeTo=Vec2d(0.0, 0.0)):
    height = screen.get_height()
    lineThickness = 2
    points = []
    for v in pymunk_poly.get_vertices():
        body_position = pymunk_poly.body.position
        relative_position = v.rotated(pymunk_poly.body.angle)
        x, y = pymunkToPygameCoords(
            relative_position + body_position + relativeTo, height
        )
        points.append((int(x), int(y)))
    last_v = pymunk_poly.get_vertices()[0]
    body_position = pymunk_poly.body.position
    relative_position = last_v.rotated(pymunk_poly.body.angle)
    x, y = pymunkToPygameCoords(relative_position + body_position + relativeTo, height)
    points.append((int(x), int(y)))
    pygame.draw.lines(screen, (255, 255, 255), False, points, lineThickness)


def drawPymunkSegments(body, screen):
    height = screen.get_height()
    shapes = body.shapes
    lineThickness = 2
    points = []
    for shape in shapes:
        ax, ay = pymunkToPygameCoords(
            shape.a.rotated(body.angle) + body.position, height
        )
        bx, by = pymunkToPygameCoords(
            shape.b.rotated(body.angle) + body.position, height
        )
        points.append((int(ax), int(ay)))
        points.append((int(bx), int(by)))
    pygame.draw.lines(screen, (255, 255, 255), False, points, lineThickness)
