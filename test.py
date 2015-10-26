#!/usr/bin/env python

__author__ = 'Jacob'


from argparse import ArgumentParser,ArgumentTypeError,ArgumentDefaultsHelpFormatter
import numpy
from visual import *

import physics


def create_sphere_visual(space_object, object_color = color.white, radius = 1):
    created_sphere = sphere(pos = space_object.position)
    created_sphere.color = object_color
    created_sphere.radius = radius
    return created_sphere


def test_1():
    '''
    run the first test
    '''
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


def test_2():
    '''
    run the second test
    '''
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


def test_3():
    '''
    run the third test
    '''
    objects_and_visual_pairs = []

    for i in xrange(1):
        position = numpy.array([[30.], [0.], [0.]])
        velocity = numpy.array([[0.], [18.], [0.]])
        radius = 1.
        mass = 10.
        new_object = physics.Object(position, velocity, radius, mass)
        new_visualization = create_sphere_visual(new_object, color.white, radius)
        objects_and_visual_pairs.append([new_object, new_visualization])

    for i in xrange(0):
        position = numpy.random.uniform(-25, 25, (3,1))
        velocity = numpy.random.uniform(-10, 10, (3,1))
        radius = numpy.random.uniform(1, 5)
        mass = numpy.random.uniform(1, 10)
        new_object = physics.Object(position, velocity, radius, mass, affected_by_gravity=False)
        new_visualization = create_sphere_visual(new_object, color.orange, radius)
        objects_and_visual_pairs.append([new_object, new_visualization])


    for i in xrange(1):
        position = numpy.array([[0.], [0.], [0.]])
        velocity = numpy.array([[0.], [0.], [0.]])
        radius = 5.
        mass = radius*2500.
        new_object = physics.Object(position, velocity, radius, mass, gravity_source=True)
        new_visualization = create_sphere_visual(new_object, color.cyan, radius)
        objects_and_visual_pairs.append([new_object, new_visualization])

    for i in xrange(30000):
        rate(60)

        for j in xrange(1):
            physics.go_forward_one_time_step()

        for set_of_objects in objects_and_visual_pairs:
            set_of_objects[1].pos = set_of_objects[0].position


def test_4():
    '''
    run the fourth test
    '''
    objects_and_visual_pairs = []

    for i in xrange(10):
        position = numpy.random.uniform(-50, 50, (3,1))
        velocity = numpy.random.uniform(0, 0, (3,1))
        radius = 1
        mass = 10
        new_object = physics.Object(position, velocity, radius, mass)
        new_visualization = create_sphere_visual(new_object, color.white, radius)
        objects_and_visual_pairs.append([new_object, new_visualization])

    for i in xrange(0):
        position = numpy.random.uniform(-25, 25, (3,1))
        velocity = numpy.random.uniform(-10, 10, (3,1))
        radius = numpy.random.uniform(1, 5)
        mass = numpy.random.uniform(1, 10)
        new_object = physics.Object(position, velocity, radius, mass, affected_by_gravity=False)
        new_visualization = create_sphere_visual(new_object, color.orange, radius)
        objects_and_visual_pairs.append([new_object, new_visualization])


    for i in xrange(1):
        position = numpy.array([[0.], [0.], [0.]])
        velocity = numpy.array([[0.], [0.], [0.]])
        radius = 10
        mass = radius*2500.
        new_object = physics.Object(position, velocity, radius, mass, gravity_source=True)
        new_visualization = create_sphere_visual(new_object, color.cyan, radius)
        objects_and_visual_pairs.append([new_object, new_visualization])

    for i in xrange(30000):
        rate(60)

        for j in xrange(1):
            physics.go_forward_one_time_step()

        for set_of_objects in objects_and_visual_pairs:
            set_of_objects[1].pos = set_of_objects[0].position


def get_opts():
    '''
    setup test options
    '''
    def parse_args():
        '''
        collect options from command line
        '''
        description='test physics manager'
        arg_parser = ArgumentParser(description=description,formatter_class=ArgumentDefaultsHelpFormatter)
        arg_parser.add_argument('-t','--test',type=int,default=1,help='test number to run')
        return vars(arg_parser.parse_args())

    return parse_args()


def main():
    '''
    run physics manager tests
    '''
    opts = get_opts()
    if opts['test'] == 1:
        test_1()
    if opts['test'] == 2:
        test_2()
    if opts['test'] == 3:
        test_3()
    if opts['test'] == 4:
        test_4()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
