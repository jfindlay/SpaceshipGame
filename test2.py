__author__ = 'Jacob'

import numpy

from visual import *

import physics


__author__ = 'Jacob'


objects_and_visual_pairs = []


def create_sphere_visual(space_object, object_color = color.white):
    created_sphere = sphere(pos = space_object.position)
    created_sphere.color = object_color
    if space_object.radius == 0:
        created_sphere.radius = 1
    else:
        created_sphere.radius = space_object.radius

    objects_and_visual_pairs.append([space_object, created_sphere])


object1 = physics.Object(position = numpy.array([[0.], [0.], [0.]]), velocity = numpy.array([[0.], [0.], [0.]]),
                         radius = 5., mass = 10., gravity_source=True)
object2 = physics.Object(position = numpy.array([[10.], [0.], [0.]]), velocity = numpy.array([[-50.], [0.], [0.]]),
                         radius = 1., mass = 1.)
object3 = physics.Object(position = numpy.array([[-200.], [0.], [4.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                         radius = 5., mass = 5.)
object4 = physics.Object(position = numpy.array([[-160.], [1.], [0.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                         radius = 5., mass = 5.)
object5 = physics.Object(position = numpy.array([[-140.], [2.], [-4.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                         radius = 5., mass = 5.)
object6 = physics.Object(position = numpy.array([[-120.], [3.], [2.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                                 radius = 5., mass = 5.)
object7 = physics.Object(position = numpy.array([[-100.], [4.], [0.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                         radius = 5., mass = 5.)
object8 = physics.Object(position = numpy.array([[-80.], [5.], [-2.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                         radius = 5., mass = 5.)
object9 = physics.Object(position = numpy.array([[-60.], [6.], [0.]]), velocity = numpy.array([[50.], [0.], [0.]]),
                         radius = 5., mass = 5.)
object10 = physics.Object(position = numpy.array([[100.], [0.], [0.]]), velocity = numpy.array([[-50.], [0.], [0.]]),
                          radius = 5., mass = 5.)


create_sphere_visual(object1, color.white)
create_sphere_visual(object2, color.green)
create_sphere_visual(object3, color.green)
create_sphere_visual(object4, color.green)
create_sphere_visual(object5, color.green)
create_sphere_visual(object6, color.green)
create_sphere_visual(object7, color.green)
create_sphere_visual(object8, color.green)
create_sphere_visual(object9, color.green)
create_sphere_visual(object10, color.orange)



for i in xrange(30000):
    rate(100)

    for j in xrange(1):
        physics.go_forward_one_time_step()

    for set_of_objects in objects_and_visual_pairs:
        set_of_objects[1].pos = set_of_objects[0].position
