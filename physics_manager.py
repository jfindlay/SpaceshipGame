from operator import itemgetter
import numpy


__author__ = 'Jacob'


dt = 1/60.
e = .7


all_objects = []
movable_objects = []
objects_effected_by_gravity = []
gravity_sources = []


class SpaceObject:
    def __init__(self, position, velocity, radius=0., mass=1.,
                 movable=True, effected_by_gravity=True, gravity_source=False):

        self.position = position
        self.velocity = velocity
        self.sum_of_forces = numpy.array([[0.], [0.], [0.]])
        self.radius = numpy.abs(radius)
        self.mass = mass
        self.movable = movable
        self.effected_by_gravity = effected_by_gravity
        self.gravity_source = gravity_source
        self.colliding_with_gravity_source = False
        self.influenced_by_non_gravity_source = False
        self.acceleration = numpy.array([[0.], [0.], [0.]])
        self.constant_forces = numpy.array([[0.], [0.], [0.]])

        all_objects.append(self)

        if self.gravity_source:
            self.movable = False
            self.effected_by_gravity = False
            gravity_sources.append(self)

        if self.movable:
            movable_objects.append(self)
        
        if self.effected_by_gravity:
            objects_effected_by_gravity.append(self)

        collision_detector_and_resolver.add_object_to_max_and_min_lists(self)

    def move(self):
        # Uses Velocity Verlet integration method
        self.position = self.position + self.velocity * dt + .5 * self.acceleration * dt * dt

    def calculate_velocity(self):
        previous_speed = numpy.linalg.norm(self.velocity)

        self.velocity = self.velocity + .5 * self.acceleration * dt
        self.sum_of_forces = self.constant_forces
        self.velocity = self.velocity + .5 * self.acceleration * dt
        self.sum_of_forces = self.constant_forces
        if self.effected_by_gravity:
            self.sum_of_forces = self.sum_of_forces + calculate_all_gravitational_forces(self)
        self.acceleration = self.sum_of_forces / self.mass

        self.velocity = self.velocity + .5 * self.acceleration * dt

        if self.colliding_with_gravity_source and not self.influenced_by_non_gravity_source:
            speed = numpy.linalg.norm(self.velocity)
            effective_speed = speed * (e + .1)
            if previous_speed < effective_speed:
                self.acceleration = numpy.array([[0.], [0.], [0.]])
                self.velocity = numpy.array([[0.], [0.], [0.]])

        self.colliding_with_gravity_source = False
        self.influenced_by_non_gravity_source = False


def calculate_all_gravitational_forces(space_object):
    def calculate_gravitational_force(space_object1, space_object2):
        distance_vector = space_object1.position - space_object2.position
        distance_direction = distance_vector / numpy.linalg.norm(distance_vector)
        distance_magnitude_squared = numpy.dot(numpy.transpose(distance_vector), distance_vector)
        mass_times_mass = space_object1.mass * space_object2.mass
        individual_force = (mass_times_mass / distance_magnitude_squared) * distance_direction
        return individual_force

    force = numpy.array([[0.], [0.], [0.]])
    for gravity_source in gravity_sources:
        force = calculate_gravitational_force(gravity_source, space_object)

    return force


def move_all_movable_objects():
    for space_object in movable_objects:
        space_object.move()


def calculate_all_velocities():
    for space_object in movable_objects:
        space_object.calculate_velocity()


class DetectAndResolveAllCollisions:
    def __init__(self):
        # Used for the grid collision detection method. Keeps track of how far along each dimension each object stretches.
        self.maxes_and_mins_along_dimensions = ([], [], [])
        self.colliding_pairs = []

    def add_object_to_max_and_min_lists(self, object_to_be_added):
        for dimension_index in xrange(len(self.maxes_and_mins_along_dimensions)):
            dimension = self.maxes_and_mins_along_dimensions[dimension_index]
            # The additional .01 is so the collision detector will pick up objects that are just barely touching.
            object_max = object_to_be_added.position[dimension_index] + object_to_be_added.radius + .005
            object_min = object_to_be_added.position[dimension_index] - object_to_be_added.radius - .005
            dimension.append([object_to_be_added, object_max])
            dimension.append([object_to_be_added, object_min])
            dimension.sort(key=itemgetter(1))

    def detect_all_collisions(self):

        def update_all_maxes_and_mins(objects_to_be_updated=all_objects):

            def update_object_in_dimension(current_dimension_index, space_object):
                dimension = self.maxes_and_mins_along_dimensions[current_dimension_index]

                updating_max = True

                for object_number_pair in dimension:
                    object_to_compare_against = object_number_pair[0]

                    if space_object == object_to_compare_against:
                        if updating_max:
                            # The additional .01 is so the collision detector will pick up objects that are just barely touching.
                            object_number_pair[1] = space_object.position[current_dimension_index] + space_object.radius + .005
                            updating_max = False
                        else:
                            object_number_pair[1] = space_object.position[current_dimension_index] - space_object.radius - .005
                            break

            for dimension_index in xrange(len(self.maxes_and_mins_along_dimensions)):
                for space_object in objects_to_be_updated:
                    update_object_in_dimension(dimension_index, space_object)

                # Sorts the dimension based on the max and min values.
                self.maxes_and_mins_along_dimensions[dimension_index].sort(key=itemgetter(1))

        def collision_detection_grid_method():

            def checking_single_dimension(dimension):
                potentially_colliding_pairs_in_one_dimension = []
                current_set_of_potentially_colliding_objects = set()

                for object_number_pair in dimension:
                    space_object = object_number_pair[0]

                    if space_object in current_set_of_potentially_colliding_objects:
                        current_set_of_potentially_colliding_objects.remove(space_object)
                        for potentially_colliding_object in current_set_of_potentially_colliding_objects:
                            # To make sure the objects in the pairs are in the same order every time they are listed
                            # as potentially colliding:
                            if space_object > potentially_colliding_object:
                                potentially_colliding_pairs_in_one_dimension.append((space_object, potentially_colliding_object))
                            else:
                                potentially_colliding_pairs_in_one_dimension.append((potentially_colliding_object, space_object))
                    else:
                        current_set_of_potentially_colliding_objects.add(space_object)

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
            distance_intersecting = -1
            if space_object0.radius != 0 or space_object1.radius != 0:
                vector_between_centers = space_object0.position - space_object1.position
                distance_between_centers = numpy.linalg.norm(vector_between_centers)
                if distance_between_centers <= space_object0.radius + space_object1.radius:
                    distance_intersecting = (space_object0.radius + space_object1.radius) - distance_between_centers
            return distance_intersecting

        def move_colliding_pair_back(space_object0, space_object1):
            # Uses the quadratic formula to find the amount of time needed to move the objects back
            # so they are just barely touching, aka
            # radius + radius = magnitude(difference in positions + difference in velocity * time)
            # and we are solving for time.

            space_object0_velocity = space_object0.velocity
            space_object1_velocity = space_object1.velocity

            vector_between_centers = space_object0.position - space_object1.position

            if space_object0.movable and not space_object1.movable:
                space_object1_velocity = numpy.array([[0.], [0.], [0.]])
                if numpy.array_equal(space_object0_velocity, numpy.array([[0.], [0.], [0.]])):
                    space_object0_velocity = -1. * vector_between_centers
            elif space_object1.movable and not space_object0.movable:
                space_object0_velocity = numpy.array([[0.], [0.], [0.]])
                if numpy.array_equal(space_object1_velocity, numpy.array([[0.], [0.], [0.]])):
                    space_object1_velocity = vector_between_centers

            vector_velocity_difference = space_object0_velocity - space_object1_velocity

            if not numpy.array_equal(vector_velocity_difference, numpy.array([[0.], [0.], [0.]])):
                a = numpy.dot(numpy.transpose(vector_velocity_difference), vector_velocity_difference)
                b = 2. * numpy.dot(numpy.transpose(vector_between_centers), vector_velocity_difference)
                # Mathematically, it could be "+ (space_object1.radius + space_object2.radius)" instead of "-",
                # but the "+" will lead to the time being a complex number.
                c = numpy.dot(numpy.transpose(vector_between_centers), vector_between_centers) - (space_object0.radius + space_object1.radius)**2

                # The quadratic formula has a "+ or -" in it, but we always want a negative time, so we use the "-".
                time = (-1.*b - (b**2. - 4.*a*c)**(1./2.))/(2.*a)

                space_object0.position = space_object0.position + (time * space_object0_velocity)
                space_object1.position = space_object1.position + (time * space_object1_velocity)
                update_all_maxes_and_mins([space_object0, space_object1])

        current_max_distance_intersecting = 1

        while current_max_distance_intersecting >= .01:

            current_max_distance_intersecting = -1

            update_all_maxes_and_mins()
            potentially_colliding_pairs = collision_detection_grid_method()

            if not potentially_colliding_pairs:
                break

            for pair in potentially_colliding_pairs:
                space_object0, space_object1 = pair

                distance_intersecting = distance_pair_intersecting(space_object0, space_object1)

                if distance_intersecting >= current_max_distance_intersecting:
                    current_max_distance_intersecting = distance_intersecting

                if distance_intersecting >= .01:
                    move_colliding_pair_back(space_object0, space_object1)
                elif distance_intersecting >= -.001:
                    if space_object0.gravity_source:
                        space_object1.colliding_with_gravity_source = True
                    else:
                        space_object1.influenced_by_non_gravity_source = True
                    if space_object1.gravity_source:
                        space_object0.colliding_with_gravity_source = True
                    else:
                        space_object0.influenced_by_non_gravity_source = True

                    self.colliding_pairs.append((space_object0, space_object1))

    def resolve_all_collisions(self):
        colliding_objects = {}
        for pair in self.colliding_pairs:
            space_object0, space_object1 = pair
            colliding_objects.add(space_object0)
            colliding_objects.add(space_object1)

collision_detector_and_resolver = DetectAndResolveAllCollisions()


def go_forward_one_time_step():
    move_all_movable_objects()
    collision_detector_and_resolver.detect_all_collisions()
    calculate_all_velocities()
    collision_detector_and_resolver.resolve_all_collisions()
