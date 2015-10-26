'''
Physics manager: implements game physics
'''

__author__ = 'Jacob'


from operator import itemgetter
import numpy


# universal physical constants
dt = 1/60.
e = .7


class Object(object):
    '''
    Model objects
    '''
    def __init__(self, position, velocity, radius=0., mass=1.,
                 movable=True, affected_by_gravity=True, gravity_source=False):
        '''
        Set object parameters and register object with physics and collision
        managers
        '''

        self.position = position
        self.velocity = velocity
        self.sum_of_forces = numpy.array([[0.], [0.], [0.]])
        self.radius = numpy.abs(radius)
        self.mass = mass
        self.movable = movable
        self.affected_by_gravity = affected_by_gravity
        self.gravity_source = gravity_source
        self.colliding_with_gravity_source = False
        self.influenced_by_non_gravity_source = False
        self.acceleration = numpy.array([[0.], [0.], [0.]])
        self.constant_forces = numpy.array([[0.], [0.], [0.]])

        manager._register_object(self)

        if self.gravity_source:
            self.movable = False
            self.affected_by_gravity = False

    def move(self):
        '''
        Move the object
        '''
        # Uses Velocity Verlet integration method
        self.position += self.velocity * dt + .5 * self.acceleration * dt * dt

    def calculate_velocity(self):
        '''
        Calculate object velocity
        '''
        previous_speed = numpy.linalg.norm(self.velocity)

        # inductively calculate velocity
        for i in range(2):
            self.velocity += .5 * self.acceleration * dt
        self.sum_of_forces = self.constant_forces

        if self.affected_by_gravity:
            self.sum_of_forces = self.sum_of_forces + gravity_force(self)
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


class Collisions(object):
    '''
    Collision detection and resolution
    '''
    def __init__(self):
        '''
        Setup collision parameter lists
        '''
        # Used for the grid collision detection method. Keeps track of how far
        # along each dimension each object extends.
        self.extrema = ([], [], [])
        self.colliding_pairs = []
        self.tolerance = 0.005
        self.gross_intersect = 0.01
        self.fine_intersect = 0.001

    def register_object(self, o):
        '''
        Add object to max and min lists
        '''
        for index, dimension in enumerate(self.extrema):
            # The additional .01 is so the collision detector will pick up
            # objects that are just barely touching.
            object_max = o.position[index] + o.radius + self.tolerance
            object_min = o.position[index] - o.radius - self.tolerance
            dimension.append([o, object_max])
            dimension.append([o, object_min])
            dimension.sort(key=itemgetter(1))

    def detect(self, objects):
        '''
        Detect collisions
        '''
        def update_extrema(objects=objects):
            '''
            Recalculate object extents
            '''
            def update_object_in_dimension(index, o):
                '''
                Recalculate object extent
                '''
                dimension = self.extrema[index]
                updating_max = True

                for object_pair in dimension:
                    if o == object_pair[0]:
                        if updating_max:
                            # The additional tolerance is so the collision
                            # detector will pick up objects that are just
                            # barely touching.
                            object_pair[1] = o.position[index] + o.radius + self.tolerance
                            updating_max = False
                        else:
                            object_pair[1] = o.position[index] - o.radius - self.tolerance
                            break

            for index, dimension in enumerate(self.extrema):
                for o in objects:
                    update_object_in_dimension(index, o)

                # Sorts the dimension based on the max and min values.
                self.extrema[index].sort(key=itemgetter(1))

        def grid_method():
            '''
            Detect collisions on the grid
            '''
            def check_dimension(dimension):
                '''
                Detect collisions in a dimension
                '''
                potential_1d_collisions = []
                potential_collisions = set()

                for object_number_pair in dimension:
                    o = object_number_pair[0]

                    if o in potential_collisions:
                        potential_collisions.remove(o)
                        for potentially_colliding_object in potential_collisions:
                            # To make sure the objects in the pairs are in the
                            # same order every time they are listed as
                            # potentially colliding:
                            if o > potentially_colliding_object:
                                potential_1d_collisions.append((o, potentially_colliding_object))
                            else:
                                potential_1d_collisions.append((potentially_colliding_object, o))
                    else:
                        potential_collisions.add(o)

                return potential_1d_collisions

            potential_x_collisions = check_dimension(self.extrema[0])
            potential_y_collisions = check_dimension(self.extrema[1])
            potential_z_collisions = check_dimension(self.extrema[2])

            potential_collisions = []

            for potential_x_collision in potential_x_collisions:
                if (potential_x_collision in potential_y_collisions and
                        potential_x_collision in potential_z_collisions):

                    potential_collisions.append(potentially_colliding_pair)

            return potential_collisions

        def intersecting(o_1, o_2):
            '''
            Calculate magnitude of collision (intersection)
            '''
            intersection = -1
            if o_1.radius != 0 or o_2.radius != 0:
                distance_between_centers = numpy.linalg.norm(o_1.position - o_2.position)
                if distance_between_centers <= o_1.radius + o_2.radius:
                    intersection = (o_1.radius + o_2.radius) - distance_between_centers
            return intersection

        def recoil(o_1, o_2):
            '''
            Reconcile collision
            '''
            # Uses the quadratic formula to find the amount of time needed to
            # move the objects back so they are just barely touching, aka
            # 2*(radius) = magnitude(difference in positions + difference in velocity * time)
            # and we are solving for time.

            o_1_velocity = o_1.velocity
            o_2_velocity = o_2.velocity

            vector_between_centers = o_1.position - o_2.position

            if o_1.movable and not o_2.movable:
                o_2_velocity = numpy.array([[0.], [0.], [0.]])
                if numpy.array_equal(o_1_velocity, numpy.array([[0.], [0.], [0.]])):
                    o_1_velocity = -1. * vector_between_centers
            elif o_2.movable and not o_1.movable:
                o_1_velocity = numpy.array([[0.], [0.], [0.]])
                if numpy.array_equal(o_2_velocity, numpy.array([[0.], [0.], [0.]])):
                    o_2_velocity = vector_between_centers

            velocity_difference = o_1_velocity - o_2_velocity

            if not numpy.array_equal(velocity_difference, numpy.array([[0.], [0.], [0.]])):
                a = numpy.dot(numpy.transpose(velocity_difference), velocity_difference)
                b = 2. * numpy.dot(numpy.transpose(vector_between_centers), velocity_difference)
                # Mathematically, it could be "+ (o_2.radius + o_2.radius)"
                # instead of "-", but the "+" will lead to the time being a
                # complex number.
                c = numpy.dot(numpy.transpose(vector_between_centers), vector_between_centers) - (o_1.radius + o_2.radius)**2

                # The quadratic formula has a "+ or -" in it, but we always
                # want a negative time, so we use the "-".
                time = (-1.*b - (b**2. - 4.*a*c)**(1./2.))/(2.*a)

                o_1.position = o_1.position + (time * o_1_velocity)
                o_2.position = o_2.position + (time * o_2_velocity)
                update_extrema([o_1, o_2])

        max_intersect = 1

        while max_intersect >= self.gross_intersect:

            max_intersect = -1

            update_extrema()
            potential_collisions = grid_method()

            if not potential_collisions:
                break

            for pair in potential_collisions:
                o_1, o_2 = pair

                intersection = intersecting(o_1, o_2)

                if intersection >= max_intersect:
                    max_intersect = intersection

                if intersection >= self.gross_intersect:
                    recoil(o_1, o_2)
                elif intersection >= -self.fine_intersect:
                    if o_1.gravity_source:
                        o_2.colliding_with_gravity_source = True
                    else:
                        o_2.influenced_by_non_gravity_source = True
                    if o_2.gravity_source:
                        o_1.colliding_with_gravity_source = True
                    else:
                        o_1.influenced_by_non_gravity_source = True

                    self.colliding_pairs.append((o_1, o_2))

    def resolve(self):
        '''
        Resolve all collisions
        '''
        def apply_impulse(o_1, o_2):
            '''
            Apply impulse to colling objects
            '''
            contact_normal_not_unit = o_1.position - o_2.position
            contact_normal = contact_normal_not_unit / numpy.linalg.norm(contact_normal_not_unit)
            o_0_relative_velocity = numpy.dot(numpy.transpose(o_1.velocity), contact_normal) * contact_normal
            o_1_relative_velocity = numpy.dot(numpy.transpose(o_2.velocity), contact_normal) * contact_normal

            velocity_difference = o_0_relative_velocity - o_1_relative_velocity

            if numpy.dot(numpy.transpose(velocity_difference), contact_normal) >= 0:
                pass

            elif o_1.movable and o_2.movable:

                impulse = (1 + e) * velocity_difference * ((o_1.mass * o_2.mass) / (o_1.mass + o_2.mass))

                o_1.velocity -= impulse/o_1.mass
                o_2.velocity += impulse/o_2.mass

            elif o_1.movable:
                computed_velocity_before_e = -2*o_0_relative_velocity + o_1.velocity
                o_1.velocity = e * computed_velocity_before_e

            elif o_2.movable:
                computed_velocity_before_e = -2*o_1_relative_velocity + o_2.velocity
                o_2.velocity = e * computed_velocity_before_e

        while self.colliding_pairs:
            pair = colliding_pairs.pop()
            o_1, o_2 = pair
            apply_impulse(o_1, o_2)


class Manager(object):
    '''
    Manage game physics
    '''
    def __init__(self):
        '''
        Setup list of all physical objects
        '''
        self.collisions = Collisions()
        self.objects = []

    def _register_object(self, o):
        '''
        Register an object with the physics manager.  This is done internally
        by the object itself
        '''
        self.objects.append(o)
        self.collisions.register(o)

    def time_step(self):
        '''
        Iterate the clock
        '''
        self.move_objects()
        self.collisions.detect(self.objects)
        self.calculate_velocities()
        self.collisions.resolve()

    def gravity_force(self, o):
        '''
        Calculate all gravitational forces on o
        '''
        def calculate_force(o_1, o_2):
            '''
            Calculate gravitational force between two objects
            '''
            distance_vector = o_1.position - o_2.position
            distance_direction = distance_vector / numpy.linalg.norm(distance_vector)
            distance_magnitude_squared = numpy.dot(numpy.transpose(distance_vector), distance_vector)
            mass_times_mass = o_1.mass * o_2.mass
            individual_force = (mass_times_mass / distance_magnitude_squared) * distance_direction
            return individual_force

        force = numpy.array([[0.], [0.], [0.]])
        for gravity_object in self.objects:
            if gravity_object.gravity_source:
                force += calculate_gravitational_force(gravity_object, o)

        return force

    def move_objects(self):
        '''
        Move the objects
        '''
        for o in self.objects:
            if o.movable:
                o.move()

    def calculate_velocities(self):
        '''
        calculate all velocities
        '''
        for o in self.objects:
            if o.movable:
                o.calculate_velocity()

manager = Manager()
