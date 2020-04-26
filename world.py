import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util
import pygame
import pygame.gfxdraw
import pygame.transform

import random
import time

from other.pygame_pymunk_translation import (
    draw_pymunk_circle,
    draw_pymunk_segments,
    draw_pymunk_poly,
)

from cell.cell import Cell

from molecules.food_molecule import FoodMolecule


class World:

    def __init__(self):
        self.width = 1000
        self.height = 1000
        self.max_width = 2000
        self.max_height = 2000

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.options = pymunk.pygame_util.DrawOptions(self.screen)

        self.space = pymunk.Space()
        self.space.damping = 0.7

        first_cell = Cell(self)

        self.cells = [first_cell]

        self.space.add(first_cell.shape.body, first_cell.shape)

        self.molecules = []

        self.camera_zoom = 0
        self.camera_position = Vec2d(0, 0)



    def borders(self):
        pass
        # floor = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
        # floor.position = width / 2, 0
        # floor_poly = pymunk.Poly.create_box(floor, (width, 10))
        # space.add(floor, floor_poly)
        # right_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
        # right_wall.position = width, height / 2
        # right_wall_poly = pymunk.Poly.create_box(right_wall, (10, height))
        # space.add(right_wall, right_wall_poly)
        # roof = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
        # roof.position = width / 2, height
        # roof_poly = pymunk.Poly.create_box(roof, (width, 10))
        # space.add(roof, roof_poly)
        # left_wall = pymunk.Body(0, 0, body_type=pymunk.Body.KINEMATIC)
        # left_wall.position = 0, height / 2
        # left_wall_poly = pymunk.Poly.create_box(left_wall, (10, height))
        # space.add(left_wall, left_wall_poly)

    

    def run(self):
        pygame.init()

        count = 0
        last_time = time.time()
        last_molecule_time = time.time()
        done = False
        while not done:
            self.screen.fill((0, 0, 0))
            current_time = time.time()
            elapsed_time = current_time - last_time
            last_time = current_time
            self.space.step(elapsed_time)

            
            curr_molecule_time = time.time()
            elapsed_molecule_time = curr_molecule_time - last_molecule_time
            if elapsed_molecule_time > 2:

                init_molecule_pos = Vec2d(random.uniform(-2000, 2000), random.uniform(-2000, 2000))
                new_molecule = FoodMolecule(init_position=init_molecule_pos)
                self.molecules.append(new_molecule)
                self.space.add(new_molecule.shape.body, new_molecule.shape)
                last_molecule_time = time.time()

            for molecule in self.molecules:
                draw_pymunk_circle(
                    molecule.shape,
                    self.screen,
                    scale=self.camera_zoom,
                    camera_position=self.camera_position,
                )
             

            for cell in self.cells:
                cell.move()

            for cell in self.cells:
                draw_pymunk_circle(
                    cell.shape, self.screen, scale=self.camera_zoom, camera_position=self.camera_position
                )

            for cell in self.cells:
                for mitochondrion in cell.mitochondria:
                    for snake_part in mitochondrion.snake:
                        draw_pymunk_poly(
                            snake_part,
                            self.screen,
                            relative_to=cell.shape.body.position,
                            scale=self.camera_zoom,
                            camera_position=self.camera_position,
                        )
                for ATP in cell.ATP:
                    draw_pymunk_circle(
                        ATP.shape,
                        self.screen,
                        relative_to=cell.shape.body.position,
                        scale=self.camera_zoom,
                        camera_position=self.camera_position,
                    )
                for food_molecule in cell.molecules:
                    draw_pymunk_circle(
                        food_molecule.shape,
                        self.screen,
                        relative_to=cell.shape.body.position,
                        scale=self.camera_zoom,
                        camera_position=self.camera_position,
                    )

                draw_pymunk_circle(
                    cell.nucleus.shape,
                    self.screen,
                    relative_to=cell.shape.body.position,
                    scale=self.camera_zoom,
                    camera_position=self.camera_position,
                )

            for cell in self.cells:
                cell.time_step()
            for cell in self.cells:
                new_cell = cell.split_check()
                if new_cell != None:
                    self.cells.append(new_cell)
                    self.space.add(new_cell.shape.body, new_cell.shape)

            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.camera_position.x += 1 * (self.camera_zoom ** 10 + 1)
            if keystate[pygame.K_RIGHT]:
                self.camera_position.x -= 1 * (self.camera_zoom ** 10 + 1)
            if keystate[pygame.K_UP]:
                self.camera_position.y -= 1 * (self.camera_zoom ** 10 + 1)
            if keystate[pygame.K_DOWN]:
                self.camera_position.y += 1 * (self.camera_zoom ** 10 + 1)

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
                self.camera_zoom += 0.01
            if keystate[pygame.K_x]:
                print("x key pressed")
                self.camera_zoom -= 0.01

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        cell = Cell(self)
                        self.space.add(cell.shape.body, cell.shape)
                        self.cells.append(cell)
                        print("Space pressed")

            pygame.display.flip()
