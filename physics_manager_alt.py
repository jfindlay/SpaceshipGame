from operator import itemgetter
from math import cos
import numpy


__author__ = 'Jacob'


dt = 1/30.
e = .7


objects_effected_by_collision = []
objects_NOT_effected_by_collision = []
gravity_sources = []


class SpaceObject:
    def __init__(self, position, velocity, radius=0., mass=1.,
                 effected_by_collision=True, has_gravitational_pull=False):

        self.position = position
        self.velocity = velocity
        self.sum_of_forces = numpy.array([[0.], [0.], [0.]])
        self.radius = numpy.abs(radius)
        self.mass = mass
        self.effected_by_collision = effected_by_collision
        self.has_gravitational_pull = has_gravitational_pull

        if effected_by_collision:
            objects_effected_by_collision.append(self)
        else:
            objects_NOT_effected_by_collision.append(self)
        if has_gravitational_pull:
            gravity_sources.append(self)

        collision_detector_and_resolver.add_object_to_max_and_min_lists(self)

    def move(self):

        def calculate_gravitational_potential_energy():
            def calculate_gravitational_potential_energy_for_one_gravity_source(gravity_source):
                distance_vector = gravity_source.position - self.position
                mass_times_mass = gravity_source.mass * self.mass
                distance_magnitude = numpy.linalg.norm(distance_vector)

                gravitational_potential_energy = -1 * mass_times_mass/distance_magnitude
                return gravitational_potential_energy

            gravitational_potential_energy = 0.
            for gravity_source in gravity_sources:
                gravitational_potential_energy += calculate_gravitational_potential_energy_for_one_gravity_source(gravity_source)

            return gravitational_potential_energy

        def calculate_gravitational_force():
            def calculate_gravitational_force_for_one_gravity_source(gravity_source):
                distance_vector = gravity_source.position - self.position
                if distance_vector == numpy.array([[0.], [0.], [0.]]):
                    print("self = %r") % self
                    print("gravity = %r") % gravity_source
                mass_times_mass = gravity_source.mass * self.mass
                distance_magnitude = numpy.linalg.norm(distance_vector)
                distance_direction = distance_vector / distance_magnitude
                distance_magnitude_squared = numpy.dot(numpy.transpose(distance_vector), distance_vector)

                gravitational_force = (mass_times_mass / distance_magnitude_squared) * distance_direction
                return gravitational_force

            gravitational_force = 0.
            for gravity_source in gravity_sources:
                gravitational_force += calculate_gravitational_force_for_one_gravity_source(gravity_source)

            return gravitational_force

        def calculate_kinetic_energy():
            speed_squared = numpy.dot(numpy.transpose(self.velocity), self.velocity)
            kinetic_energy = .5 * self.mass * speed_squared
            return kinetic_energy

        def calculate_total_energy():
            kinetic_energy = calculate_kinetic_energy()
            gravitational_potential_energy = calculate_gravitational_potential_energy()
            energy = kinetic_energy - gravitational_potential_energy
            return energy

        acceleration = self.sum_of_forces / self.mass
        self.velocity = acceleration * dt + self.velocity

        starting_energy = calculate_total_energy()

        gravitational_acceleration = calculate_gravitational_force() / self.mass
        gravitational_velocity = gravitational_acceleration * dt
        self.velocity = gravitational_velocity + self.velocity

        self.position = self.velocity * dt + self.position



        self.sum_of_forces = numpy.array([[0.], [0.], [0.]])



def move_all_movable_objects():

    for space_object in (objects_effected_by_collision + objects_NOT_effected_by_collision):
        space_object.move()


class DetectAndResolveAllCollisions:
    def __init__(self):
        # Used for the grid collision detection method. Keeps track of how far along each dimension each object stretches.
        self.maxes_and_mins_along_dimensions = ([], [], [])

    def add_object_to_max_and_min_lists(self, object_to_be_added):
        for dimension_index in range(len(self.maxes_and_mins_along_dimensions)):
            dimension = self.maxes_and_mins_along_dimensions[dimension_index]
            # The additional .01 is so the collision detector will pick up objects that are just barely touching.
            object_max = object_to_be_added.position[dimension_index] + object_to_be_added.radius + .005
            object_min = object_to_be_added.position[dimension_index] - object_to_be_added.radius - .005
            dimension.append([object_to_be_added, object_max])
            dimension.append([object_to_be_added, object_min])
            dimension.sort(key=itemgetter(1))

    def detect_and_resolve_all_collisions(self):

        def update_all_maxes_and_mins(objects_to_be_updated=objects_effected_by_collision+objects_NOT_effected_by_collision):

            def update_object_in_dimension(dimension_index, space_object):
                dimension = self.maxes_and_mins_along_dimensions[dimension_index]

                updating_max = True

                for object_number_pair in dimension:
                    object_to_compare_against = object_number_pair[0]

                    if space_object == object_to_compare_against:
                        if updating_max:
                            # The additional .01 is so the collision detector will pick up objects that are just barely touching.
                            object_number_pair[1] = space_object.position[dimension_index] + space_object.radius + .005
                            updating_max = False
                        else:
                            object_number_pair[1] = space_object.position[dimension_index] - space_object.radius - .005
                            break

            for dimension_index in range(len(self.maxes_and_mins_along_dimensions)):
                for space_object in objects_to_be_updated:
                    update_object_in_dimension(dimension_index, space_object)

                # Sorts the dimension based on the max and min values.
                self.maxes_and_mins_along_dimensions[dimension_index].sort(key=itemgetter(1))

        def collision_detection_grid_method():

            def checking_single_dimension(dimension):
                potentially_colliding_pairs_in_one_dimension = []
                current_list_of_potentially_colliding_objects = []

                for object_number_pair in dimension:
                    space_object = object_number_pair[0]

                    if space_object in current_list_of_potentially_colliding_objects:
                        current_list_of_potentially_colliding_objects.remove(space_object)
                        for potentially_colliding_object in current_list_of_potentially_colliding_objects:
                            # To make sure the objects in the pairs are in the same order every time they are listed
                            # as potentially colliding:
                            if space_object > potentially_colliding_object:
                                potentially_colliding_pairs_in_one_dimension.append((space_object, potentially_colliding_object))
                            else:
                                potentially_colliding_pairs_in_one_dimension.append((potentially_colliding_object, space_object))
                    else:
                        current_list_of_potentially_colliding_objects.append(space_object)

                return potentially_colliding_pairs_in_one_dimension

            potentially_colliding_pairs_in_0_dimension = checking_single_dimension(self.maxes_and_mins_along_dimensions[0])
            potentially_colliding_pairs_in_1_dimension = checking_single_dimension(self.maxes_and_mins_along_dimensions[1])
            potentially_colliding_pairs_in_2_dimension = checking_single_dimension(self.maxes_and_mins_along_dimensions[2])

            potentially_colliding_pairs = []

            for potentially_colliding_pair in potentially_colliding_pairs_in_0_dimension:
                if (potentially_colliding_pair in potentially_colliding_pairs_in_1_dimension and
                        potentially_colliding_pair in potentially_colliding_pairs_in_2_dimension):

                    potentially_colliding_pairs.append(potentially_colliding_pair)

            return potentially_colliding_pairs

        def distance_pair_intersecting(space_object0, space_object1):
            distance_intersecting = 0
            if space_object0.radius != 0 or space_object1.radius != 0:
                vector_between_centers = space_object0.position - space_object1.position
                distance_between_centers = numpy.linalg.norm(vector_between_centers)
                if distance_between_centers <= space_object0.radius + space_object1.radius:
                    distance_intersecting = (space_object0.radius + space_object1.radius) - distance_between_centers
            else:
                distance_intersecting = -1

            return distance_intersecting

        def move_colliding_pair_back(space_object0, space_object1):
            # Uses the quadratic formula to find the amount of time needed to move the objects back
            # so they are just barely touching, aka
            # radius + radius = magnitude(difference in positions + difference in velocity * time)
            # and we are solving for time.

            vector_between_centers = space_object0.position - space_object1.position
            vector_velocity_difference = space_object0.velocity - space_object1.velocity

            a = numpy.dot(numpy.transpose(vector_velocity_difference), vector_velocity_difference)
            b = 2. * numpy.dot(numpy.transpose(vector_between_centers), vector_velocity_difference)
            # Mathematically, it could be "+ (space_object1.radius + space_object2.radius)" instead of "-",
            # but the "+" will lead to the time being a complex number.
            c = numpy.dot(numpy.transpose(vector_between_centers), vector_between_centers) - (space_object0.radius + space_object1.radius)**2

            # The quadratic formula has a "+ or -" in it, but we always want a negative time, so we use the "-".
            time = (-1.*b - (b**2. - 4.*a*c)**(1./2.))/(2.*a)

            space_object0.position = space_object0.position + (time * space_object0.velocity)
            space_object1.position = space_object1.position + (time * space_object1.velocity)
            update_all_maxes_and_mins(pair)

        def apply_impulse(space_object0, space_object1):

            contact_normal_not_unit = space_object0.position - space_object1.position
            contact_normal = contact_normal_not_unit / numpy.linalg.norm(contact_normal_not_unit)
            object0_relative_velocity = numpy.dot(numpy.transpose(space_object0.velocity), contact_normal) * contact_normal
            object1_relative_velocity = numpy.dot(numpy.transpose(space_object1.velocity), contact_normal) * contact_normal

            vector_velocity_difference = object0_relative_velocity - object1_relative_velocity

            if numpy.dot(numpy.transpose(vector_velocity_difference), contact_normal) >= 0:
                pass

            elif space_object0.effected_by_collision and space_object1.effected_by_collision:

                impulse = (1 + e) * vector_velocity_difference * ((space_object0.mass * space_object1.mass) / (space_object0.mass + space_object1.mass))

                space_object0.velocity -= impulse/space_object0.mass
                space_object1.velocity += impulse/space_object1.mass

            elif space_object0.effected_by_collision:
                computed_velocity_before_e = -2*object0_relative_velocity + space_object0.velocity
                space_object0.velocity = e * computed_velocity_before_e

            elif space_object1.effected_by_collision:
                computed_velocity_before_e = 2*object1_relative_velocity + space_object0.velocity
                space_object1.velocity = e * computed_velocity_before_e

        current_max_distance_intersecting = 1

        while current_max_distance_intersecting >= .01:

            current_max_distance_intersecting = -1

            update_all_maxes_and_mins()
            potentially_colliding_pairs = collision_detection_grid_method()
            colliding_pairs = []

            if not potentially_colliding_pairs:
                break

            for pair in potentially_colliding_pairs:
                space_object0, space_object1  = pair

                distance_intersecting = distance_pair_intersecting(space_object0, space_object1)

                if distance_intersecting >= current_max_distance_intersecting:
                    current_max_distance_intersecting = distance_intersecting

                if distance_intersecting >= .01:
                    move_colliding_pair_back(space_object0, space_object1)
                elif distance_intersecting >= -.01:
                    colliding_pairs.append((space_object0, space_object1))

            ##### How to handle applying impulses when multiple objects are involved?
            for pair in colliding_pairs:
                space_object0, space_object1 = pair
                apply_impulse(space_object0, space_object1)


collision_detector_and_resolver = DetectAndResolveAllCollisions()


def go_forward_one_time_step():
    move_all_movable_objects()
    collision_detector_and_resolver.detect_and_resolve_all_collisions()
