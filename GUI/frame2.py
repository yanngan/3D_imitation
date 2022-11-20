from ctypes import py_object

import pygame
import numpy as np
from math import *


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SCALE = 100
WIDTH, HEIGHT = 800, 600
DISTANCE_FROM_SCREEN = 1600


# functions

def connect_points(i, j, points, screen):
    pygame.draw.line(
        screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


def avg(num1, num2):
    return (num1+num2)/2




def get_tait_bryan_angle(e0,e1):
    """
    this function get 2 eyes locations (x,y,z)
    :rtype: 3 angle
    """
    # fake the third eye to find the plan to get the perspective
    e2 = (avg(e0[0], e1[0]), avg(e0[1], e1[1]), e0[0], e1[2]),
    to_return_x , to_return_y, to_return_z = 0

    return to_return_x , to_return_y, to_return_z


# code
def draw_frame():
    circle_pos = [WIDTH/2, HEIGHT/2]  # x, y

    pygame.display.set_caption("3D projection in pygame!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    angle_x = 0
    angle_y = 0
    angle_z = 0
    points = [np.matrix([-1, -1, 1]), np.matrix([1, -1, 1]), np.matrix([1, 1, 1]), np.matrix([-1, 1, 1]),
              np.matrix([-1, -1, -1]), np.matrix([1, -1, -1]), np.matrix([1, 1, -1]), np.matrix([-1, 1, -1])]

    # all the cube vertices

    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])

    projected_points = [
        [n, n] for n in range(len(points))
    ]


    # all the cube vertices

    clock = pygame.time.Clock()
    while True:

        clock.tick(60)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        screen.fill(WHITE)

        rotation_z = np.matrix([
            [cos(angle_z), -sin(angle_z), 0],
            [sin(angle_z), cos(angle_z), 0],
            [0, 0, 1],
        ])

        rotation_y = np.matrix([
            [cos(angle_y), 0, sin(angle_y)],
            [0, 1, 0],
            [-sin(angle_y), 0, cos(angle_y)],
        ])

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(angle_x), -sin(angle_x)],
            [0, sin(angle_x), cos(angle_x)],
        ])
        i = 0
        for point in points:
            rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
            rotated2d = np.dot(rotation_y, rotated2d)
            rotated2d = np.dot(rotation_x, rotated2d)
            projected2d = np.dot(projection_matrix, rotated2d)

            x = int(projected2d[0][0] * SCALE) + circle_pos[0]
            y = int(projected2d[1][0] * SCALE) + circle_pos[1]
            pygame.draw.circle(screen, RED, (x, y), 5)
            projected_points[i] = [x, y]

            i += 1

        for p in range(4):
            connect_points(p, (p + 1) % 4, projected_points, screen)
            connect_points(p + 4, ((p + 1) % 4) + 4, projected_points, screen)
            connect_points(p, (p + 4), projected_points, screen)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                x_mouse, y_mouse = pygame.mouse.get_pos()

                x_dist = abs(circle_pos[0] - x_mouse)
                y_dist = abs(circle_pos[1] - y_mouse)
                angle_x = np.arctan(x_dist/0.40)
                angle_y = np.arctan(y_dist/0.40)

                print("angle_x=", angle_x)
                print("angle_y=", angle_y)





