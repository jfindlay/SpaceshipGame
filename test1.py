__author__ = 'Jacob'

import numpy
from visual import *

import physics


def create_sphere_visual(space_object, object_color = color.white, radius = 1):
    created_sphere = sphere(pos = space_object.position)
    created_sphere.color = object_color
    created_sphere.radius = radius
    return created_sphere


objects_and_visual_pairs = []

for i in xrange(45):
    position = numpy.random.uniform(-300, 300, (3,1))
    velocity = numpy.random.uniform(-50, 50, (3,1))
    radius = numpy.random.uniform(1, 5)
    mass = numpy.random.uniform(1, 10)
    new_object = physics.Object(position, velocity, radius, mass)
    new_visualization = create_sphere_visual(new_object, color.white, radius)
    objects_and_visual_pairs.append([new_object, new_visualization])

for i in xrange(5):
    position = numpy.random.uniform(-300, 300, (3,1))
    velocity = numpy.random.uniform(-10, 10, (3,1))
    radius = numpy.random.uniform(1, 5)
    mass = numpy.random.uniform(1, 10)
    new_object = physics.Object(position, velocity, radius, mass, affected_by_gravity=False)
    new_visualization = create_sphere_visual(new_object, color.orange, radius)
    objects_and_visual_pairs.append([new_object, new_visualization])


for i in xrange(3):
    position = numpy.random.uniform(-300, 300, (3,1))
    velocity = numpy.random.uniform(0, 0, (3,1))
    radius = numpy.random.uniform(20, 50)
    mass = radius*50000.
    new_object = physics.Object(position, velocity, radius, mass, gravity_source=True)
    new_visualization = create_sphere_visual(new_object, color.cyan, radius)
    objects_and_visual_pairs.append([new_object, new_visualization])

for i in xrange(30000):
    rate(60)

    for j in xrange(1):
        physics.go_forward_one_time_step()

    for set_of_objects in objects_and_visual_pairs:
        set_of_objects[1].pos = set_of_objects[0].position

