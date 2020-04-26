import pymunk
import pygame
from pymunk.vec2d import Vec2d


def pymunk_to_pygame_coords(vector, displayHeight):
    vector.y = displayHeight - vector.y
    return vector


def zoom(position, scale, screen):
    total_pix = screen.get_height() + screen.get_width()
    height_frac = total_pix / screen.get_height()
    width_frac = total_pix / screen.get_width()
    return Vec2d(position.x * (1 + scale), position.y * (1 + scale))


def draw_pymunk_circle(
    pymunk_circle,
    screen,
    relativeTo=Vec2d(0.0, 0.0),
    scale=0,
    cameraPosition=Vec2d(0, 0),
):
    height = screen.get_height()
    position = pymunk_circle.body.position + cameraPosition + relativeTo
    zoomed_pos = zoom(position, scale, screen)
    x, y = pymunk_to_pygame_coords(zoomed_pos, height)
    pygame.gfxdraw.circle(
        screen, int(x), int(y), int(pymunk_circle.radius * (1 + scale)), (255, 255, 255)
    )


def draw_pymunk_poly(
    pymunk_poly, screen, relativeTo=Vec2d(0.0, 0.0), scale=0, cameraPosition=Vec2d(0, 0)
):
    height = screen.get_height()
    lineThickness = 2
    points = []
    body_position = pymunk_poly.body.position
    for v in pymunk_poly.get_vertices():
        relative_position = v.rotated(pymunk_poly.body.angle)
        this_position = body_position + relative_position + relativeTo + cameraPosition
        zoomed_pos = zoom(this_position, scale, screen)
        x, y = pymunk_to_pygame_coords(zoomed_pos, height)
        points.append((int(x), int(y)))
    last_v = pymunk_poly.get_vertices()[0]
    relative_position = last_v.rotated(pymunk_poly.body.angle)
    this_position = body_position + relative_position + relativeTo + cameraPosition
    zoomed_pos = zoom(this_position, scale, screen)
    x, y = pymunk_to_pygame_coords(zoomed_pos, height)
    points.append((int(x), int(y)))
    pygame.draw.lines(screen, (255, 255, 255), False, points, lineThickness)


def draw_pymunk_segments(body, screen, scale=0, cameraPosition=Vec2d(0, 0)):
    height = screen.get_height()
    shapes = body.shapes
    lineThickness = 2
    points = []
    for shape in shapes:
        a_pos = shape.a.rotated(body.angle) + body.position + cameraPosition
        zoomed_pos = zoom(a_pos, scale, screen)
        ax, ay = pymunk_to_pygame_coords(zoomed_pos, height)
        b_pos = shape.b.rotated(body.angle) + body.position + cameraPosition
        zoomed_pos = zoom(b_pos, scale, screen)
        bx, by = pymunk_to_pygame_coords(zoomed_pos, height)
        points.append((int(ax), int(ay)))
        points.append((int(bx), int(by)))
    pygame.draw.lines(screen, (255, 255, 255), False, points, lineThickness)
