import pymunk
from pymunk.vec2d import Vec2d
import random
import math
import time

from CellComponent.Mitochondrion import Mitochondrion
from CellComponent.Nucleus import Nucleus
from CellComponent.ATP import ATP


init_x, init_y = 400, 400
init_rad = 50

init_num_ATP_default = 3
init_num_mitochondria_default = 0

# This should probably be held at one for simplicity, rather
# change how the radius is changed in relation to it
growth_per_atp = 1

growth_cooldown_time = 0.5

split_cooldown_time = 5

shrink_cooldown_time = 0.001

mitochondria_limit = 4


class Cell:
    def __init__(
        self,
        x=init_x,
        y=init_y,
        init_num_ATP=init_num_ATP_default,
        init_num_mitochondria=init_num_mitochondria_default,
    ):
        init_mass = 1
        init_moment = 1666
        body = pymunk.Body(init_mass, init_moment)
        body.position = x, y
        self.shape = pymunk.Circle(body, init_rad)

        self.relative_space = pymunk.Space()
        self.relative_space.damping = 0.7

        self.birth_time = time.time()
        self.last_growth_time = self.birth_time
        self.last_split_time = self.birth_time
        self.last_shrink_time = self.birth_time

        self.growth = 0

        self.growth_penalty_length = 0

        self.relative_boundary_body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        self.relative_boundary_body.position = 0, 0

        self.radius = init_rad
        segments_positions = self.approximate_circle(init_rad)
        segments = [
            pymunk.Segment(
                self.relative_boundary_body,
                segment_positions[0],
                segment_positions[1],
                30,
            )
            for segment_positions in segments_positions
        ]
        self.segments = segments

        objects = [self.relative_boundary_body] + segments
        self.relative_space.add(objects)

        self.mitochondria = []
        for i in range(init_num_mitochondria):
            self.createMitochondrion()

        self.ATP = []
        for i in range(init_num_ATP):
            self.createATP()

        rand_x = random.uniform(-init_rad / 4, init_rad / 4)
        rand_y = random.uniform(-init_rad / 4, init_rad / 4)
        self.nucleus = Nucleus(self, init_position=Vec2d(rand_x, rand_y))
        self.relative_space.add(self.nucleus.shape, self.nucleus.shape.body)

    def createATP(self, init_position=None):
        if init_position == None:
            rand_x = random.uniform(-init_rad / 4, init_rad / 4)
            rand_y = random.uniform(-init_rad / 4, init_rad / 4)
            init_position = Vec2d(rand_x, rand_y)
        new_ATP = ATP(self, init_position)
        self.ATP.append(new_ATP)
        self.relative_space.add(new_ATP.shape.body, new_ATP.shape)

    def approximate_circle(self, radius):
        r = radius
        num_splits = 16  # the resulting number of "pieces of cake
        one_section = math.pi * 2 / num_splits
        segments_positions = []
        for i in range(num_splits):
            current_section = i * one_section
            next_section = (i + 1) * one_section
            ax = math.cos(current_section) * r
            ay = math.sin(current_section) * r
            bx = math.cos(next_section) * r
            by = math.sin(next_section) * r
            segments_positions.append([(ax, ay), (bx, by)])
        return segments_positions

    def shrinkCheck(self):
        if (
            self.growth_penalty_length > 0
            and time.time() - self.last_shrink_time > shrink_cooldown_time
        ):
            self.shrink()
            self.growth_penalty_length -= 1
            self.last_shrink_time = time.time()

    def shrink(self):
        print("shrinking")
        self.growth -= 1
        new_radius = init_rad + (self.growth / 1)
        # Set global space shape
        self.shape.unsafe_set_radius(new_radius)
        self.radius = new_radius

        # Remove the old objects from relative space
        self.relative_space.remove(self.segments)
        # Set relative space shape
        segments_positions = self.approximate_circle(new_radius)
        segments = [
            pymunk.Segment(
                self.relative_boundary_body,
                segment_positions[0],
                segment_positions[1],
                5,
            )
            for segment_positions in segments_positions
        ]
        self.segments = segments
        objects = segments
        self.relative_space.add(objects)

    def growCheck(self):
        if len(self.ATP) > 0 and (
            time.time() - self.last_growth_time >= growth_cooldown_time
        ):
            self.grow()

    def grow(self):
        self.last_growth_time = time.time()
        self.ATP.pop(len(self.ATP) - 1)
        self.growth += 1
        new_radius = init_rad + (self.growth / 1)

        # Set global space shape
        self.shape.unsafe_set_radius(new_radius)
        self.radius = new_radius

        # Remove the old objects from relative space
        self.relative_space.remove(self.segments)
        # Set relative space shape
        segments_positions = self.approximate_circle(new_radius)
        segments = [
            pymunk.Segment(
                self.relative_boundary_body,
                segment_positions[0],
                segment_positions[1],
                5,
            )
            for segment_positions in segments_positions
        ]
        self.segments = segments
        objects = segments
        self.relative_space.add(objects)
        print("Cell growing, growth is now: " + str(self.growth))

    def apply_rand_force(self):
        rand_x = (0.5 - random.random()) * 5
        rand_y = (0.5 - random.random()) * 5
        self.shape.body.apply_impulse_at_local_point((rand_x, rand_y), point=(0, 0))

    def splitCheck(self):
        if (
            self.growth > 40
            and time.time() - self.last_split_time > split_cooldown_time
        ):
            self.last_split_time = time.time()
            return self.split()
        return None

    def split(self):
        print("splitting")
        rand_x = (0.5 - random.random()) / 10
        rand_y = (0.5 - random.random()) / 10

        num_ATP = len(self.ATP) // 2
        remaining_atp = self.ATP[:num_ATP]
        transferred_atp = self.ATP[num_ATP:]

        num_mitochondria = len(self.mitochondria) // 2
        remaining_mitochondria = self.mitochondria[:num_mitochondria]
        transferred_mitochondria = self.mitochondria[num_mitochondria:]

        self.ATP = remaining_atp
        self.mitochondria = remaining_mitochondria

        # self.growth = self.growth // 2
        self.growth_penalty_length = self.growth

        return Cell(
            self.shape.body.position.x + rand_x,
            self.shape.body.position.y + rand_y,
            init_num_ATP=len(transferred_atp),
            init_num_mitochondria=len(transferred_mitochondria),
        )

    def createMitochondrionCheck(self):
        if (
            self.growth / (len(self.mitochondria) + 0.001) > 10
            and random.random() < 0.01
        ):
            self.createMitochondrion()

    def createMitochondrion(self):
        rand_x = random.uniform(-init_rad / 4, init_rad / 4)
        rand_y = random.uniform(-init_rad / 4, init_rad / 4)
        rand_angle = random.uniform(-3.0, 3.0)
        mitochondrion = Mitochondrion(
            self, init_position=Vec2d(rand_x, rand_y), init_angle=rand_angle
        )
        for poly in mitochondrion.snake:
            self.relative_space.add(poly.body, poly)
        self.mitochondria.append(mitochondrion)

    def isWithinCircle(self, position):
        return position.x ** 2 + position.y ** 2 < self.radius ** 2

    def removeLostComponents(self):
        temp_indexes = []
        for i in range(len(self.ATP)):
            if not self.isWithinCircle(self.ATP[i].shape.body.position):
                temp_indexes.append(i)
        for index in sorted(temp_indexes, reverse=True):
            print("removing atp since out of bounds")
            del self.ATP[index]
        temp_indexes = []
        for i in range(len(self.mitochondria)):
            if not self.isWithinCircle(self.mitochondria[i].head.body.position):
                temp_indexes.append(i)
        for index in sorted(temp_indexes, reverse=True):
            print("removing mito since out of bounds")
            del self.mitochondria[index]

    def timeStep(self):
        self.removeLostComponents()
        # Grow
        self.growCheck()
        # Shrink
        self.shrinkCheck()
        # Create new mitochondria
        self.createMitochondrionCheck()
        # Simulate mitochondria
        for mitochondrion in self.mitochondria:
            mitochondrion.timeStep()
        # Simulate ATP
        for ATP in self.ATP:
            ATP.timeStep()
        # Simulate nucleus
        self.nucleus.timeStep()
