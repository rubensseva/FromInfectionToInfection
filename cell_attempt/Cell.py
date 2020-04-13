import pymunk
from pymunk.vec2d import Vec2d
import random
import math
import time

from CellComponent.Mitochondrion import Mitochondrion
from CellComponent.Nucleus import Nucleus
from CellComponent.ATP import ATP

from infection_utils import approximate_circle, is_within_circle, convert_points_to_pymunk_segments


init_x, init_y = 400, 400
init_rad = 50

init_num_ATP_default = 7
init_num_mitochondria_default = 0

# This should probably be held at one for simplicity, rather
# change how the radius is changed in relation to it
growth_per_atp = 1

growth_cooldown_time = 0.5

split_growth_target_max = 200
split_growth_target_min = 30
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
        self.ATP_reservoir_states = {
                "EMPTY": 0,
                "STARVING": 5,
                "LOW": 15,
                "MEDIUM": 30,
                "HIGH": 60,
                "ABUNDANT": 200
        }

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
        self.old_growth = self.growth

        self.growth_penalty_length = 0

        self.relative_boundary_body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        self.relative_boundary_body.position = 0, 0

        self.radius = init_rad
        self.old_radius = self.radius
        segments_positions = approximate_circle(init_rad, 16)
        self.segments = convert_points_to_pymunk_segments(self.relative_boundary_body, segments_positions)

        objects = [self.relative_boundary_body] + self.segments
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

        self.update_split_growth_target()
        

    def update_split_growth_target(self):
        self.split_growth_target = random.randint(split_growth_target_min, split_growth_target_max)

    def apply_rand_force(self):
        rand_x = (0.5 - random.random()) * 5
        rand_y = (0.5 - random.random()) * 5
        self.shape.body.apply_impulse_at_local_point((rand_x, rand_y), point=(0, 0))

    def query_ATP_reservoir(self, query_string):
        ATP_limit = self.ATP_reservoir_states[query_string]
        print(ATP_limit)
        num_ATP = len(self.ATP)
        return num_ATP >= ATP_limit

    def createATP(self, init_position=None):
        if init_position == None:
            rand_x = random.uniform(-init_rad / 4, init_rad / 4)
            rand_y = random.uniform(-init_rad / 4, init_rad / 4)
            init_position = Vec2d(rand_x, rand_y)
        new_ATP = ATP(self, init_position)
        self.ATP.append(new_ATP)
        self.relative_space.add(new_ATP.shape.body, new_ATP.shape)

    def shrinkCheck(self):
        if (
            self.growth_penalty_length > 0
            and time.time() - self.last_shrink_time > shrink_cooldown_time
        ):
            self.shrink()
            self.growth_penalty_length -= 1
            self.last_shrink_time = time.time()

    def shrink(self):
        self.growth -= 1

    def growCheck(self):
        if self.query_ATP_reservoir("MEDIUM") and (
            time.time() - self.last_growth_time >= growth_cooldown_time
        ):
            self.grow()

    def grow(self):
        self.last_growth_time = time.time()
        self.ATP.pop(len(self.ATP) - 1)
        self.growth += 1

    def splitCheck(self):
        if (
            self.growth > self.split_growth_target
            and time.time() - self.last_split_time > split_cooldown_time
        ):
            self.last_split_time = time.time()
            self.update_split_growth_target()
            return self.split()
        return None

    def split(self):
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

        self.growth_penalty_length = self.growth

        return Cell(
            self.shape.body.position.x + rand_x,
            self.shape.body.position.y + rand_y,
            init_num_ATP=len(transferred_atp),
            init_num_mitochondria=len(transferred_mitochondria),
        )

    def createMitochondrionCheck(self):
        ATP_cost = 5 * (len(self.mitochondria) ** 4)
        if (
            self.query_ATP_reservoir("STARVING") 
            and len(self.ATP) > ATP_cost
        ):
            self.createMitochondrion()
            split_index = len(self.ATP) - 1 - ATP_cost
            remaining_ATP = self.ATP[:split_index]
            spent_ATP = self.ATP[split_index:]
            for ATP in spent_ATP: 
                self.relative_space.remove(ATP.shape)
                self.relative_space.remove(ATP.shape.body)
            self.ATP = remaining_ATP

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


    def removeLostComponents(self):
        temp_indexes = []
        for i in range(len(self.ATP)):
            if not is_within_circle(self.radius, self.ATP[i].shape.body.position):
                temp_indexes.append(i)
        for index in sorted(temp_indexes, reverse=True):
            print("removing atp since out of bounds")
            del self.ATP[index]
        temp_indexes = []
        for i in range(len(self.mitochondria)):
            if not is_within_circle(self.radius, self.mitochondria[i].head.body.position):
                temp_indexes.append(i)
        for index in sorted(temp_indexes, reverse=True):
            print("removing mito since out of bounds")
            del self.mitochondria[index]

    def updateSimulationComponentsCheck(self):
        if (self.old_growth != self.growth):
            self.updateSimulationComponents()
            self.old_growth = self.growth

    def updateSimulationComponents(self):
        new_radius = init_rad + (self.growth / 1)
        # Set global space shape
        self.shape.unsafe_set_radius(new_radius)
        self.radius = new_radius
        # Remove the old objects from relative space
        self.relative_space.remove(self.segments)
        # Set relative space shape
        segments_positions = approximate_circle(new_radius, 16)
        self.segments = convert_points_to_pymunk_segments(self.relative_boundary_body, segments_positions)
        self.relative_space.add(self.segments)

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
        # Update cell radius for all relevant components
        self.updateSimulationComponentsCheck()
