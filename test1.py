__author__ = 'Jacob'

import numpy
from visual import *

import physics_manager


__author__ = 'Jacob'


def create_sphere_visual(space_object, object_color = color.white, radius = 1):
    created_sphere = sphere(pos = space_object.position)
    created_sphere.color = object_color
    created_sphere.radius = radius
    return created_sphere


objects_and_visual_pairs = []


for i in range(50):
    position = numpy.random.uniform(-150, 150, (3,1))
    velocity = numpy.random.uniform(-10, 10, (3,1))
    radius = numpy.random.uniform(1, 5)
    mass = numpy.random.uniform(1, 10)
    new_object = physics_manager.SpaceObject(position, velocity, radius, mass)
    new_visualization = create_sphere_visual(new_object, color.white, radius)
    objects_and_visual_pairs.append([new_object, new_visualization])


for i in range(4):
    position = numpy.random.uniform(-150, 150, (3,1))
    velocity = numpy.random.uniform(0, 0, (3,1))
    radius = numpy.random.uniform(5, 10)
    mass = radius*50000.
    new_object = physics_manager.SpaceObject(position, velocity, radius, mass, gravity_source=True)
    new_visualization = create_sphere_visual(new_object, color.cyan, radius)
    objects_and_visual_pairs.append([new_object, new_visualization])

for i in range(30000):
    rate(100)

    for j in range(1):
        physics_manager.go_forward_one_time_step()

    for set_of_objects in objects_and_visual_pairs:
        set_of_objects[1].pos = set_of_objects[0].position

