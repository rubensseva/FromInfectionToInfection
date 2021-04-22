import pymunk
from pymunk.vec2d import Vec2d
import random
import math
import time

from cell.cell_component.mitochondrion import Mitochondrion
from cell.cell_component.nucleus import Nucleus
from cell.cell_component.atp import ATP

from other.infection_utils import (
    approximate_circle,
    is_within_circle,
    convert_points_to_pymunk_segments,
)


init_x, init_y = 400, 400
init_rad = 50

init_num_ATP_default = 7
init_num_mitochondria_default = 0

# This should probably be held at one for simplicity, rather
# change how the radius is changed in relation to it
growth_per_atp = 1

growth_cooldown_time = 0.5

split_growth_target_max = 100
split_growth_target_min = 30
split_cooldown_time = 5

shrink_cooldown_time = 0.001

remove_lost_components_cooldown = 0.5

mitochondria_limit = 4


class Cell:
    def __init__(
        self,
        world,
        x=init_x,
        y=init_y,
        init_num_ATP=init_num_ATP_default,
        init_num_mitochondria=init_num_mitochondria_default,
    ):
        self.world = world
        self.ATP_reservoir_states = {
            "EMPTY": 0,
            "STARVING": 5,
            "LOW": 15,
            "MEDIUM": 30,
            "HIGH": 60,
            "ABUNDANT": 200,
        }
        self.target = None

        self.last_simulation_update = time.time()

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
        self.last_remove_lost_time = self.birth_time

        self.growth = 0
        self.old_growth = self.growth

        self.growth_penalty_length = 0

        self.relative_boundary_body = pymunk.Body(0, 0, pymunk.Body.KINEMATIC)
        self.relative_boundary_body.position = 0, 0

        self.radius = init_rad
        self.old_radius = self.radius
        segments_positions = approximate_circle(init_rad, 16)
        self.segments = convert_points_to_pymunk_segments(
            self.relative_boundary_body, segments_positions
        )

        objects = [self.relative_boundary_body] + self.segments
        self.relative_space.add(objects)

        self.mitochondria = []
        for i in range(init_num_mitochondria):
            self.create_mitochondrion()

        self.ATP = []
        for i in range(init_num_ATP):
            self.create_ATP()

        self.molecules = []

        rand_x = random.uniform(-init_rad / 4, init_rad / 4)
        rand_y = random.uniform(-init_rad / 4, init_rad / 4)
        self.nucleus = Nucleus(self, init_position=Vec2d(rand_x, rand_y))
        self.relative_space.add(self.nucleus.shape, self.nucleus.shape.body)

        self.update_split_growth_target()

    def find_closest_molecule(self):
        closest_dist = 999999999
        closest_molecule = None
        for molecule in self.world.molecules:
            x, y = molecule.shape.body.position
            x, y = (x - self.shape.body.position.x, y - self.shape.body.position.y)
            current_dist = x ** 2 + y ** 2
            if current_dist < closest_dist:
                closest_dist = current_dist
                closest_molecule = molecule
        if closest_molecule:
            return closest_molecule.shape.body.position
        return None

    def update_target(self):
        self.target = self.find_closest_molecule()

    def absorb_close_food_molecules(self):
        molecules_copy = self.world.molecules.copy()
        for molecule in molecules_copy:
            x, y = molecule.shape.body.position - self.shape.body.position
            current_dist = math.sqrt(x ** 2 + y ** 2)
            if current_dist < self.radius * 2:
                self.world.space.remove(molecule.shape, molecule.shape.body)
                self.world.molecules.remove(molecule)
                molecule.shape.body.position = Vec2d(0.0, 0.0)
                self.molecules.append(molecule)
                self.relative_space.add(molecule.shape, molecule.shape.body)

    def remove_ATP(self, num_ATP):
        if num_ATP > len(self.ATP):
            print("WARNING: Trying to remove more ATP than what the cell currently has")
            raise Exception(
                "Trying to remove more ATP than what the cell currently has"
            )
        split_index = len(self.ATP) - num_ATP
        remaining_ATP = self.ATP[:split_index]
        spent_ATP = self.ATP[split_index:]
        for ATP in spent_ATP:
            self.relative_space.remove(ATP.shape)
            self.relative_space.remove(ATP.shape.body)
        self.ATP = remaining_ATP
        return spent_ATP

    def update_split_growth_target(self):
        self.split_growth_target = random.randint(
            split_growth_target_min, split_growth_target_max
        )

    def move(self):
        if self.target:
            target_vec = self.target - self.shape.body.position
            self.shape.body.apply_force_at_local_point(target_vec / 10, point=(0, 0))
        else:
            self.apply_rand_force()

    def apply_rand_force(self):
        rand_x = (0.5 - random.random()) * 5
        rand_y = (0.5 - random.random()) * 5
        self.shape.body.apply_impulse_at_local_point((rand_x, rand_y), point=(0, 0))

    def query_ATP_reservoir(self, query_string):
        ATP_limit = self.ATP_reservoir_states[query_string]
        num_ATP = len(self.ATP)
        return num_ATP >= ATP_limit

    def create_ATP(self, init_position=None):
        if init_position == None:
            rand_x = random.uniform(-init_rad / 4, init_rad / 4)
            rand_y = random.uniform(-init_rad / 4, init_rad / 4)
            init_position = Vec2d(rand_x, rand_y)
        new_ATP = ATP(self, init_position)
        self.ATP.append(new_ATP)
        self.relative_space.add(new_ATP.shape.body, new_ATP.shape)

    def shrink_check(self):
        if (
            self.growth_penalty_length > 0
            and time.time() - self.last_shrink_time > shrink_cooldown_time
        ):
            self.shrink()
            self.growth_penalty_length -= 1
            self.last_shrink_time = time.time()

    def shrink(self):
        self.growth -= 1

    def grow_check(self):
        if self.query_ATP_reservoir("MEDIUM") and (
            time.time() - self.last_growth_time >= growth_cooldown_time
        ):
            self.grow()

    def grow(self):
        self.last_growth_time = time.time()
        self.ATP.pop(len(self.ATP) - 1)
        self.growth += 1

    def split_check(self):
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
        transferred_atp = self.remove_ATP(len(self.ATP[num_ATP:]))
        num_mitochondria = len(self.mitochondria) // 2
        remaining_mitochondria = self.mitochondria[:num_mitochondria]
        transferred_mitochondria = self.mitochondria[num_mitochondria:]
        self.mitochondria = remaining_mitochondria
        self.growth_penalty_length = self.growth
        return Cell(
            self.world,
            self.shape.body.position.x + rand_x,
            self.shape.body.position.y + rand_y,
            init_num_ATP=len(transferred_atp),
            init_num_mitochondria=len(transferred_mitochondria),
        )

    def create_mitochondrion_check(self):
        ATP_cost = 5 * (len(self.mitochondria) ** 3)
        if self.query_ATP_reservoir("STARVING") and len(self.ATP) > ATP_cost:
            self.create_mitochondrion()
            self.remove_ATP(ATP_cost)

    def create_mitochondrion(self):
        rand_x = random.uniform(-init_rad / 4, init_rad / 4)
        rand_y = random.uniform(-init_rad / 4, init_rad / 4)
        rand_angle = random.uniform(-3.0, 3.0)
        mitochondrion = Mitochondrion(
            self, init_position=Vec2d(rand_x, rand_y), init_angle=rand_angle
        )
        for poly in mitochondrion.snake:
            self.relative_space.add(poly.body, poly)
        self.mitochondria.append(mitochondrion)

    def remove_lost_components_check(self):
        current_time = time.time()
        if current_time - self.last_remove_lost_time > remove_lost_components_cooldown:
            self.remove_lost_components()
            self.last_remove_lost_time = current_time

    def remove_lost_components(self):
        temp_indexes = []
        for i in range(len(self.ATP)):
            if not is_within_circle(self.radius, self.ATP[i].shape.body.position):
                temp_indexes.append(i)
        for index in sorted(temp_indexes, reverse=True):
            del self.ATP[index]
        temp_indexes = []
        for i in range(len(self.mitochondria)):
            if not is_within_circle(
                self.radius, self.mitochondria[i].head.body.position
            ):
                temp_indexes.append(i)
        for index in sorted(temp_indexes, reverse=True):
            del self.mitochondria[index]

    def update_simulation_components_check(self):
        # If there is now new growth, there is no need to update simulation related components
        if self.old_growth != self.growth:
            self.update_simulation_components()
            self.old_growth = self.growth

    def update_simulation_components(self):
        new_radius = init_rad + (self.growth / 1)
        # Set global space shape
        self.shape.unsafe_set_radius(new_radius)
        self.radius = new_radius
        # Remove the old objects from relative space
        self.relative_space.remove(self.segments)
        # Set relative space shape
        segments_positions = approximate_circle(new_radius, 16)
        self.segments = convert_points_to_pymunk_segments(
            self.relative_boundary_body, segments_positions
        )
        self.relative_space.add(self.segments)

    def time_step(self):
        self.remove_lost_components_check()
        self.update_target()
        self.absorb_close_food_molecules()
        # Grow
        self.grow_check()
        # Shrink
        self.shrink_check()
        # Create new mitochondria
        self.create_mitochondrion_check()
        # Simulate mitochondria
        for mitochondrion in self.mitochondria:
            mitochondrion.time_step()
        # Simulate ATP
        for ATP in self.ATP:
            ATP.time_step()
        # Simulate nucleus
        self.nucleus.time_step()
        # Update cell radius for all relevant components
        self.update_simulation_components_check()
        # Step throught relative space simulation
        current_time = time.time()
        elapsed_time = current_time - self.last_simulation_update
        self.last_simulation_update = current_time
        self.relative_space.step(elapsed_time)
