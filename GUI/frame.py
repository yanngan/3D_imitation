import numpy
import pygame
import numpy as np
from math import *


WHITE = (255, 255, 255)
RED = (255, 0, 0)
COLORS = [(255, 0, 0), (250, 126, 2), (143, 250, 2),
          (0, 255, 157), (0, 229, 255), (0, 38, 255),
          (0, 38, 250), (230, 0, 255)]
BLACK = (0, 0, 0)
# self.scale = 100
# self.screen_width, self.screen_height = 800, 600
DISTANCE_FROM_SCREEN = 30

PIXEL_TO_CM = 0.0264583333


def avg(num1, num2):
    return (num1+num2)/2


class Frame:

    def __init__(self, screen_width=1200, screen_height=800, scale=100, lines_color=(0, 0, 0), dots_color=(255, 0, 0),
                 background_color=(255, 255, 255)):
        # optional params
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale = scale
        self.lines_color = lines_color
        self.dots_color = dots_color
        self.background_color = background_color

        self.points = None
        self.projected_points = None
        self.projection_matrix = None
        self.init_point()

        self.angle_x, self.angle_y, self.angle_z = None, None, None
        self.init_angle()

        self.circle_pos = None
        self.init_axis()

        self.screen = None
        self.clock = None
        self.init_screen()


    def init_point(self):
        self.points = [np.matrix([-1, -1, 1]), np.matrix([1, -1, 1]), np.matrix([1, 1, 1]), np.matrix([-1, 1, 1]),
                       np.matrix([-1, -1, -1]), np.matrix([1, -1, -1]), np.matrix([1, 1, -1]), np.matrix([-1, 1, -1])]
        self.projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0]
        ])
        self.projected_points = [
            [n, n] for n in range(len(self.points))
        ]

    def init_angle(self):
        self.angle_x = 0  # the angle around the X (this will be fixed)
        self.angle_y = 0  # the angle around the Y
        self.angle_z = 0  # the angle around the Z

    def connect_points(self, i, j, screen):
        pygame.draw.line(
            screen,
            BLACK,
            (self.projected_points[i][0], self.projected_points[i][1]),
            (self.projected_points[j][0], self.projected_points[j][1])
        )

    def reset_tait_bryan_angles(self, x_camera: float, y_camera: float, z_camera: float):
        """
        reset Tait Bryan Angles By Point Of View Location
        :param x_camera:
        :param y_camera:
        :param z_camera:
        """
        y_screen, z_screen = self._to_screen_axis(y_camera, z_camera)
        x_screen = x_camera / PIXEL_TO_CM

        # y_angle = numpy.arctan(abs(z_screen)/abs(y_screen))
        # if y_screen < 0:
        #     y_angle = 180 - y_angle
        # z_angle = numpy.arctan(abs(y_screen)/abs(z_screen))
        # if z_screen < 0:
        #     z_angle = 180 - z_angle

        x_angle = np.arctan(np.square(y_screen**2 + z_screen**2)/x_screen)
        y_angle = np.arctan(np.square(x_screen**2 + z_screen**2)/y_screen)
        z_angle = np.arctan(np.square(x_screen**2 + y_screen**2)/z_screen)

        self.angle_x = radians(x_angle)
        self.angle_y = radians(y_angle)
        self.angle_z = radians(z_angle)

        print(" x_screen = " + str(x_screen) + "y_screen = " + str(y_screen) + " z_screen = " + str(z_screen)
              + " x_angle = " + str(self.angle_x) + " y_angle = "
              + str(self.angle_y) + " z_angle  = "
              + str(self.angle_z))

    def _to_screen_axis(self, y_camera: float, z_camera: float):
        """
        :param y_camera:
        :param z_camera:
        :rtype: the x,y,z representing the screen axis
        """
        z_screen = -(z_camera - (self.screen_height/2))
        y_screen = y_camera-(self.screen_width/2)

        return y_screen, z_screen

    def init_axis(self):
        self.circle_pos = [self.screen_width/2, self.screen_height/2]  # x, y

    def init_screen(self):
        pygame.display.set_caption("3D projection in pygame!")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

    def draw_frame(self, e0, e1):
        while True:
            self.clock.tick(60)
            screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        x_mouse, y_mouse = pygame.mouse.get_pos()
                        self.reset_tait_bryan_angles(DISTANCE_FROM_SCREEN, x_mouse, y_mouse)

            screen.fill(WHITE)

            rotation_z = np.matrix([
                [cos(self.angle_z), -sin(self.angle_z), 0],
                [sin(self.angle_z), cos(self.angle_z), 0],
                [0, 0, 1],
            ])

            rotation_y = np.matrix([
                [cos(self.angle_y), 0, sin(self.angle_y)],
                [0, 1, 0],
                [-sin(self.angle_y), 0, cos(self.angle_y)],
            ])

            rotation_x = np.matrix([
                [1, 0, 0],
                [0, cos(self.angle_x), -sin(self.angle_x)],
                [0, sin(self.angle_x), cos(self.angle_x)],
            ])
            i = 0
            for point in self.points:
                rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
                rotated2d = np.dot(rotation_y, rotated2d)
                rotated2d = np.dot(rotation_x, rotated2d)
                projected2d = np.dot(self.projection_matrix, rotated2d)

                x = int(projected2d[0][0] * self.scale) + self.circle_pos[0]
                y = int(projected2d[1][0] * self.scale) + self.circle_pos[1]
                pygame.draw.circle(screen, COLORS[i], (x, y), 5)
                self.projected_points[i] = [x, y]

                i += 1

            for p in range(4):
                self.connect_points(p, (p + 1) % 4, screen)
                self.connect_points(p + 4, ((p + 1) % 4) + 4, screen)
                self.connect_points(p, (p + 4), screen)

            pygame.display.update()







