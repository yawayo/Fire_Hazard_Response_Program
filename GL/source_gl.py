import math
from OpenGL.GL import *
import numpy as np

class gl_draw:
    def __init__(self):
        super().__init__()
        self.height = 0.4

        self.Watch_floor = 0
        self.color()

    def draw_Building(self):

        glPushMatrix()

        self.draw_Base(4.4, 2.2)

        size = 0.01
        self.draw_Pillar(-2.16 - (size * 5), -1.31 - (size * 5), size, self.height)
        self.draw_Pillar(-1.44 - (size * 5), -0.99 - (size * 5), size, self.height)
        self.draw_Pillar(-0.71 - (size * 5), -0.66 - (size * 5), size, self.height)
        self.draw_Pillar(0.0 - (size * 5), -0.33 - (size * 5), size, self.height)
        self.draw_Pillar(0.71 - (size * 5), 0.0 - (size * 5), size, self.height)
        self.draw_Pillar(1.42 - (size * 5), 0.33 - (size * 5), size, self.height)
        self.draw_Pillar(2.13 - (size * 5), 0.66 - (size * 5), size, self.height)
        self.draw_Pillar(2.84 - (size * 5), 0.99 - (size * 5), size, self.height)
        self.draw_Pillar(-0.61 - (size * 5), 0.25 - (size * 5), size, self.height)
        self.draw_Pillar(0.1 - (size * 5), 0.57 - (size * 5), size, self.height)
        self.draw_1F_Bottom()

        self.draw_EV_3D(0.0, self.height * 5)
        self.draw_Floor_Bottom(self.height * 1, 1)
        self.draw_Floor_Bottom(self.height * 2, 2)
        self.draw_Floor_Bottom(self.height * 3, 3)
        self.draw_Floor_Bottom(self.height * 4, 4)
        glPopMatrix()
        glPushMatrix()
        self.draw_Stairs(self.height * 0, self.height, 10)
        self.draw_Stairs(self.height * 1, self.height, 10)
        self.draw_Stairs(self.height * 2, self.height, 10)
        self.draw_Stairs(self.height * 3, self.height, 10)
        self.draw_Stairs(self.height * 4, self.height, 10)

        self.draw_1F_Back_Wall(self.height)
        self.draw_Back_Wall(self.height * 1, self.height)
        self.draw_Back_Wall(self.height * 2, self.height)
        self.draw_Back_Wall(self.height * 3, self.height)
        self.draw_Back_Wall(self.height * 4, self.height)
        self.draw_1F_Front_Wall(self.height)
        self.draw_Front_Wall(self.height * 1, self.height)
        self.draw_Front_Wall(self.height * 2, self.height)
        self.draw_Front_Wall(self.height * 3, self.height)
        self.draw_Front_Wall(self.height * 4, self.height)
        # self.draw_Roof(self.height * 5)

        glPopMatrix()

    def draw_Floor_3D(self):

        glPushMatrix()

        self.draw_Base(4.4, 2.2)

        self.draw_EV_3D(self.height * self.Watch_floor, self.height)
        if self.Watch_floor == 0:
            self.draw_Stairs(self.height * 0, self.height, 10)
            self.draw_1F_Bottom()
            self.draw_1F_Back_Wall(self.height)
            self.draw_1F_Front_Wall(self.height)
            #self.draw_1F_Room_Wall(self.height)
        else:
            self.draw_Stairs(self.height * (self.Watch_floor - 1), self.height, 10)
            self.draw_Stairs(self.height * self.Watch_floor, self.height, 10)
            self.draw_Floor_Bottom(self.height * self.Watch_floor, self.Watch_floor)
            self.draw_Back_Wall(self.height * self.Watch_floor, self.height)
            # self.draw_Room_Wall(self.height * self.Watch_floor)
            self.draw_Front_Wall(self.height * self.Watch_floor, self.height)

        glPopMatrix()

    def draw_Floor_2D(self):
        glPushMatrix()

        if self.Watch_floor == 0:
            self.draw_1F_Bottom()
        else:
            self.draw_Floor_Bottom(0.0, self.Watch_floor)

        self.draw_Stairs(0.0, 0.0, 10)
        self.draw_EV_2D()

        glPopMatrix()

    def color(self):
        self.base_color = [0.1, 0.1, 0.1, 1.0]
        self.pillar_color = [0.7, 0.7, 0.7, 1.0]
        self.ev_color = [0.4, 0.4, 0.4, 1.0]
        self.bottom_color = [[[0.0, 1.0, 0.0, 1.0]]]
        for _ in range(4):
            floor_color_set = []
            for _ in range(7):
                floor_color_set.append([0.0, 1.0, 0.0, 1.0])
            self.bottom_color.append(floor_color_set)

        self.hallway_color = [0.5, 0.5, 0.5, 1.0]
        self.back_wall_color = [0.3, 0.3, 0.3, 1.0]
        self.front_wall_color = [0.6, 0.6, 0.6, 0.4]
        self.room_wall_color = [0.6, 0.6, 0.6, 0.8]
        self.stairs_color = [0.5, 0.5, 0.5, 1.0]

    def draw_Base(self, x, y):
        bottom = [[x, y, 0.0],
                  [x, -y, 0.0],
                  [-x, -y, 0.0],
                  [-x, y, 0.0]]
        glColor(self.base_color[0], self.base_color[1], self.base_color[2], self.base_color[3])
        glBegin(GL_QUADS)
        for point in bottom:
            glVertex3fv(point)
        glEnd()

    def draw_Pillar(self, x, y, size, height):
        glColor(self.pillar_color[0], self.pillar_color[1], self.pillar_color[2], self.pillar_color[3])
        glBegin(GL_QUAD_STRIP)
        NUM_SEGMENTS = 150
        for segment in range(NUM_SEGMENTS + 2):
            theta = (2.0 * math.pi * float(segment)) / float(NUM_SEGMENTS)
            x = x + size * (math.cos(theta) / 5.0)
            y = y + size * (math.sin(theta) / 5.0)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, height)
        glEnd()

    def draw_EV_3D(self, z, height):
        bottom_point = [[-0.809, 0.799],
                        [-0.809, 0.50],
                        [-0.51, 0.50],
                        [-0.51, 0.799]]
        glColor(self.ev_color[0], self.ev_color[1], self.ev_color[2], self.ev_color[3])
        glBegin(GL_QUAD_STRIP)
        for i in range(5):
            glVertex3fv(bottom_point[i % 4] + [z])
            glVertex3fv(bottom_point[i % 4] + [z + height])
        glEnd()
        glBegin(GL_QUADS)
        for point in bottom_point:
            glVertex3fv(point + [z + height])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        for point in bottom_point:
            glVertex3fv(point + [z + height - 0.001])
        glEnd()

    def draw_EV_2D(self):
        bottom_point = [[-0.809, 0.799],
                        [-0.809, 0.50],
                        [-0.51, 0.50],
                        [-0.51, 0.799]]
        glColor(self.ev_color[0], self.ev_color[1], self.ev_color[2], self.ev_color[3])
        glBegin(GL_QUADS)
        for i in range(4):
            glVertex3fv(bottom_point[i] + [0.001])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        for point in bottom_point:
            glVertex3fv(point + [0.001])
        glEnd()

    def draw_1F_Bottom(self):
        dif_base = 0.001
        all_room_point = []
        room_01 = [[-0.11, 0.46, dif_base],
                   [-0.11, -0.07, dif_base],
                   [-0.06, -0.18, dif_base],
                   [0.53, 0.11, dif_base],
                   [0.53, 0.46, dif_base]]
        room_02 = [[-0.87, -0.25, dif_base],
                   [-0.87, -0.58, dif_base],
                   [-0.35, -0.32, dif_base],
                   [-0.478, -0.045, dif_base]]
        room_03 = [[-0.87, 0.02, dif_base],
                   [-0.87, -0.25, dif_base],
                   [-0.635, -0.127, dif_base],
                   [-0.745, 0.095, dif_base]]
        room_04 = [[-0.87, 0.35, dif_base],
                   [-0.87, 0.02, dif_base],
                   [-0.745, 0.095, dif_base]]
        room_05 = [[-0.35, -0.32, dif_base],
                   [-0.273, -0.485, dif_base],
                   [0.017, -0.345, dif_base],
                   [-0.06, -0.18, dif_base]]
        all_room_point.append(room_01)
        all_room_point.append(room_02)
        all_room_point.append(room_03)
        all_room_point.append(room_04)
        all_room_point.append(room_05)

        all_another_point = []

        hallway_01 = [[-0.478, -0.045, dif_base],
                      [-0.35, -0.32, dif_base],
                      [-0.06, -0.18, dif_base],
                      [-0.11, -0.07, dif_base]]
        hallway_02 = [[-0.87, 0.35, dif_base],
                      [-0.635, -0.127, dif_base],
                      [-0.478, -0.045, dif_base],
                      [-0.478, 0.36, dif_base],
                      [-0.81, 0.37, dif_base]]
        hallway_03 = [[-0.478, 0.36, dif_base],
                      [-0.478, -0.045, dif_base],
                      [-0.11, -0.07, dif_base],
                      [-0.11, 0.36, dif_base]]
        hallway_04 = [[-0.81, 0.50, dif_base],
                      [-0.81, 0.36, dif_base],
                      [-0.11, 0.36, dif_base],
                      [-0.11, 0.50, dif_base]]
        hallway_05 = [[-0.81, 0.80, dif_base],
                      [-0.81, 0.46, dif_base],
                      [-0.17, 0.46, dif_base],
                      [-0.17, 0.80, dif_base]]
        stairs = [[-0.17, 0.90, dif_base],
                  [-0.17, 0.46, dif_base],
                  [0.17, 0.46, dif_base],
                  [0.17, 0.90, dif_base]]

        all_another_point.append(hallway_01)
        all_another_point.append(hallway_02)
        all_another_point.append(hallway_03)
        all_another_point.append(hallway_04)
        all_another_point.append(hallway_05)
        all_another_point.append(stairs)

        another_area = [[-0.87, 0.35, dif_base],
                        [-0.635, -0.127, dif_base],
                        [-0.478, -0.045, dif_base],
                        [-0.35, -0.32, dif_base],
                        [-0.06, -0.18, dif_base],
                        [-0.11, -0.07, dif_base],
                        [-0.11, 0.46, dif_base],
                        [0.17, 0.46, dif_base],
                        [0.17, 0.90, dif_base],
                        [-0.17, 0.90, dif_base],
                        [-0.17, 0.80, dif_base],
                        [-0.51, 0.80, dif_base],
                        [-0.51, 0.50, dif_base],
                        [-0.81, 0.50, dif_base],
                        [-0.81, 0.37, dif_base]]

        glColor(self.bottom_color[0][0][0], self.bottom_color[0][0][1], self.bottom_color[0][0][2], self.bottom_color[0][0][3])
        for room in all_room_point:
            glBegin(GL_POLYGON)
            for point in room:
                glVertex3fv(point)
            glEnd()
        glColor(self.hallway_color[0], self.hallway_color[1], self.hallway_color[2], self.hallway_color[3])
        for room in all_another_point:
            glBegin(GL_POLYGON)
            for point in room:
                glVertex3fv(point)
            glEnd()
        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for room in all_room_point:
            glBegin(GL_LINE_LOOP)
            for point in room:
                point[2] += 0.001
                glVertex3fv(point)
            glEnd()
        glBegin(GL_LINE_LOOP)
        for point in another_area:
            point[2] += 0.001
            glVertex3fv(point)
        glEnd()

    def draw_1F_Back_Wall(self, height):

        all_back_wall_point = [[0.53, 0.11],
                               [0.53, 0.46],
                               [0.17, 0.46],
                               [0.17, 1.57],
                               [-0.17, 1.31],
                               [-0.17, 0.80],
                               [-0.81, 0.80],
                               [-0.81, 0.37],
                               [-0.87, 0.35],
                               [-0.87, -0.58]]

        glColor(self.back_wall_color[0], self.back_wall_color[1], self.back_wall_color[2], self.back_wall_color[3])
        glBegin(GL_QUAD_STRIP)
        for point in all_back_wall_point:
            glVertex3fv(point + [0.0])
            glVertex3fv(point + [height])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for point in all_back_wall_point:
            glBegin(GL_LINES)
            glVertex3fv(point + [0.0])
            glVertex3fv(point + [height])
            glEnd()

    def draw_1F_Front_Wall(self, height):

        all_front_wall_point = [[-0.87, -0.58],
                                [-0.35, -0.32],
                                [-0.273, -0.485],
                                [0.017, -0.345],
                                [-0.06, -0.18],
                                [0.53, 0.11]]
        glColor(self.front_wall_color[0], self.front_wall_color[1], self.front_wall_color[2], self.front_wall_color[3])
        glBegin(GL_QUAD_STRIP)
        for point in all_front_wall_point:
            glVertex3fv(point + [0.0])
            glVertex3fv(point + [height])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for point in all_front_wall_point:
            glBegin(GL_LINES)
            glVertex3fv(point + [0.0])
            glVertex3fv(point + [height])
            glEnd()

    def draw_1F_Room_Wall(self, height):
        all_room_wall_point = []
        room_1_2 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58]]
        room_2_0 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58]]
        room_0_3 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58]]
        room_3_4 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58]]
        room_4_5 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58]]
        room_5_6 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58]]
        room_6_7 = [[0.53, 0.11, height],
                    [0.53, 0.46, height],
                    [0.17, 0.46, height],
                    [-0.87, -0.58, height]]

        all_room_wall_point.append(room_1_2)
        all_room_wall_point.append(room_2_0)
        all_room_wall_point.append(room_0_3)
        all_room_wall_point.append(room_3_4)
        all_room_wall_point.append(room_4_5)
        all_room_wall_point.append(room_5_6)
        all_room_wall_point.append(room_6_7)

        glColor(self.room_wall_color[0], self.room_wall_color[1], self.room_wall_color[2], self.room_wall_color[3])
        for wall in all_room_wall_point:
            glBegin(GL_QUADS)
            for point in wall:
                glVertex3f(point)
            glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for wall in all_room_wall_point:
            glBegin(GL_LINE_LOOP)
            for point in wall:
                glVertex3f(point)
            glEnd()

    def draw_Floor_Bottom(self, height, floor):
        all_room_point = []
        room_01 = [[-2.87, -0.16, height],
                    [-2.87, -1.47, height],
                    [-2.16, -1.47, height],
                    [-2.16, -0.16, height]]
        room_02 = [[-2.16, -0.33, height],
                    [-2.16, -1.15, height],
                    [-1.44, -1.15, height],
                    [-1.44, -0.33, height]]
        room_03 = [[-0.71, 0.26, height],
                    [-0.71, -0.49, height],
                    [0.0, -0.49, height],
                    [0.0, 0.59, height]]
        room_04 = [[0.0, 0.59, height],
                    [0.0, -0.16, height],
                    [0.71, -0.16, height],
                    [0.71, 0.92, height]]
        room_05 = [[0.71, 0.92, height],
                    [0.71, 0.16, height],
                    [1.42, 0.16, height],
                    [1.42, 1.25, height]]
        room_06 = [[1.42, 1.25, height],
                    [1.42, 0.49, height],
                    [2.13, 0.49, height],
                    [2.13, 1.57, height]]
        room_07 = [[2.13, 1.97, height],
                    [2.13, 0.82, height],
                    [2.84, 0.82, height],
                    [2.84, 1.97, height]]
        all_room_point.append(room_01)
        all_room_point.append(room_02)
        all_room_point.append(room_03)
        all_room_point.append(room_04)
        all_room_point.append(room_05)
        all_room_point.append(room_06)
        all_room_point.append(room_07)

        all_another_point = []
        empty = [[-1.44, -0.33, height],
                 [-1.44, -0.82, height],
                 [-0.71, -0.82, height],
                 [-0.71, -0.33, height]]
        hallway_01 = [[-2.16, -0.16, height],
                      [-2.16, -0.33, height],
                      [-0.71, -0.33, height],
                      [-0.71, -0.16, height]]
        hallway_02 = [[-0.87, 0.33, height],
                      [-0.87, -0.33, height],
                      [-0.71, -0.33, height],
                      [-0.71, 0.33, height]]
        hallway_03 = [[-0.87, 0.35, height],
                      [-0.87, 0.18, height],
                      [2.13, 1.57, height],
                      [2.13, 1.74, height]]
        hallway_04 = [[-0.81, 0.50, height],
                      [-0.81, 0.36, height],
                      [-0.51, 0.39, height],
                      [-0.51, 0.50, height]]
        hallway_05 = [[-0.51, 0.80, height],
                      [-0.51, 0.48, height],
                      [-0.17, 0.51, height],
                      [-0.17, 0.80, height]]
        stairs = [[-0.17, 0.90, height],
                  [-0.17, 0.64, height],
                  [0.17, 0.67, height],
                  [0.17, 0.90, height]]
        ev = [[-0.81, 0.80, height],
              [-0.81, 0.50, height],
              [-0.51, 0.50, height],
              [-0.51, 0.80, height]]

        all_another_point.append(empty)
        all_another_point.append(hallway_01)
        all_another_point.append(hallway_02)
        all_another_point.append(hallway_03)
        all_another_point.append(hallway_04)
        all_another_point.append(hallway_05)
        all_another_point.append(stairs)
        all_another_point.append(ev)

        another_area = [[-2.16, -0.16, height],
                        [-2.16, -0.33, height],
                        [-1.44, -0.33, height],
                        [-1.44, -0.82, height],
                        [-0.71, -0.82, height],
                        [-0.71, 0.26, height],
                        [2.13, 1.57, height],
                        [2.13, 1.74, height],
                        [0.17, 0.83, height],
                        [0.17, 1.57, height],
                        [-0.17, 1.31, height],
                        [-0.17, 0.80, height],
                        [-0.51, 0.80, height],
                        [-0.51, 0.50, height],
                        [-0.81, 0.50, height],
                        [-0.81, 0.37, height],
                        [-0.87, 0.35, height],
                        [-0.87, -0.16, height]]

        glBegin(GL_QUADS)
        for idx, room in enumerate(all_room_point):
            glColor(self.bottom_color[floor][idx][0], self.bottom_color[floor][idx][1], self.bottom_color[floor][idx][2], self.bottom_color[floor][idx][3])
            for point in room:
                glVertex3fv(point)
        glColor(self.hallway_color[0], self.hallway_color[1], self.hallway_color[2], self.hallway_color[3])
        for room in all_another_point:
            for point in room:
                glVertex3fv(point)
        glEnd()
        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for room in all_room_point:
            glBegin(GL_LINE_LOOP)
            for point in room:
                point[2] += 0.001
                glVertex3fv(point)
            glEnd()
        glBegin(GL_LINE_LOOP)
        for point in another_area:
            point[2] += 0.001
            glVertex3fv(point)
        glEnd()

    def draw_Back_Wall(self, z, height):
        all_back_wall_point = [[-2.87, -1.47],
                               [-2.87, -0.16],
                               [-0.87, -0.16],
                               [-0.87, 0.35],
                               [-0.81, 0.37],
                               [-0.81, 0.80],
                               [-0.17, 0.80],
                               [-0.17, 1.31],
                               [0.17, 1.57],
                               [0.17, 0.83],
                               [-0.04, 0.73],
                               [0.17, 0.83],
                               [2.13, 1.74],
                               [2.13, 1.97],
                               [2.84, 1.97],
                               [2.84, 0.82]]

        glColor(self.back_wall_color[0], self.back_wall_color[1], self.back_wall_color[2], self.back_wall_color[3])
        glBegin(GL_QUAD_STRIP)
        for point in all_back_wall_point:
            glVertex3fv(point + [z])
            glVertex3fv(point + [z + height])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for point in all_back_wall_point:
            glBegin(GL_LINES)
            glVertex3fv(point + [z])
            glVertex3fv(point + [z + height])
            glEnd()

    def draw_Front_Wall(self, z, height):
        all_front_wall_point = [[-2.87, -1.47],
                                [-2.16, -1.47],
                                [-2.16, -1.15],
                                [-1.44, -1.15],
                                [-1.44, -0.82],
                                [-0.71, -0.82],
                                [-0.71, -0.49],
                                [0.0, -0.49],
                                [0.0, -0.16],
                                [0.71, -0.16],
                                [0.71, 0.16],
                                [1.42, 0.16],
                                [1.42, 0.49],
                                [2.13, 0.49],
                                [2.13, 0.82],
                                [2.84, 0.82]]

        glColor(self.front_wall_color[0], self.front_wall_color[1], self.front_wall_color[2], self.front_wall_color[3])
        glBegin(GL_QUAD_STRIP)
        for point in all_front_wall_point:
            glVertex3fv(point + [z])
            glVertex3fv(point + [z + height])
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for point in all_front_wall_point:
            glBegin(GL_LINES)
            glVertex3fv(point + [z])
            glVertex3fv(point + [z + height])
            glEnd()

    def draw_Room_Wall(self, height):
        all_room_wall_point = []
        room_01 = [[-2.87, -0.16],
                   [-2.87, -1.47],
                   [-2.16, -1.47],
                   [-2.16, -0.16]]
        room_02 = [[-2.16, -0.33],
                   [-2.16, -1.15],
                   [-1.44, -1.15],
                   [-1.44, -0.33]]
        room_03 = [[-0.71, 0.26],
                   [-0.71, -0.49],
                   [0.0, -0.49],
                   [0.0, 0.59]]
        room_04 = [[0.0, 0.59],
                   [0.0, -0.16],
                   [0.71, -0.16],
                   [0.71, 0.92]]
        room_05 = [[0.71, 0.92],
                   [0.71, 0.16],
                   [1.42, 0.16],
                   [1.42, 1.25]]
        room_06 = [[1.42, 1.25],
                   [1.42, 0.49],
                   [2.13, 0.49],
                   [2.13, 1.57]]
        room_07 = [[2.13, 1.97],
                   [2.13, 0.82],
                   [2.84, 0.82],
                   [2.84, 1.97]]

        all_room_wall_point.append(room_01)
        all_room_wall_point.append(room_02)
        all_room_wall_point.append(room_03)
        all_room_wall_point.append(room_04)
        all_room_wall_point.append(room_05)
        all_room_wall_point.append(room_06)
        all_room_wall_point.append(room_07)

        glColor(self.room_wall_color[0], self.room_wall_color[1], self.room_wall_color[2], self.room_wall_color[3])
        for wall in all_room_wall_point:
            glBegin(GL_QUAD_STRIP)
            for idx in range(len(wall) + 1):
                glVertex3fv(wall[idx % 4] + [height])
                glVertex3fv(wall[idx % 4] + [height * 2])
            glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        for wall in all_room_wall_point:
            glBegin(GL_LINE_LOOP)
            for point in wall:
                glVertex3fv(point + [height])
                glVertex3fv(point + [height * 2])
            glEnd()

    def draw_Stairs(self, z, height, num):

        glColor(self.stairs_color[0], self.stairs_color[1], self.stairs_color[2], self.stairs_color[3])
        start = 1.18
        end = 0.90
        space = [[-0.168, 1.31, z + (height / 2.0)],
                 [-0.168, start, z + (height / 2.0)],
                 [0.168, start, z + (height / 2.0)],
                 [0.168, 1.57, z + (height / 2.0)]]
        glBegin(GL_QUADS)
        for point in space:
            glVertex3fv(point)
        glEnd()

        glBegin(GL_QUAD_STRIP)
        for gap in range(num + 1):
            glVertex3f(0, start - gap * ((start - end) / num), z + (height / 2) + (((height / 2) / num) * gap))
            glVertex3f(0.168, start - gap * ((start - end) / num), z + (height / 2) + (((height / 2) / num) * gap))
            glVertex3f(0, start - (gap + 1) * ((start - end) / num), z + (height / 2) + (((height / 2) / num) * gap))
            glVertex3f(0.168, start - (gap + 1) * ((start - end) / num), z + (height / 2) + (((height / 2) / num) * gap))
        glEnd()
        glBegin(GL_QUAD_STRIP)
        for gap in range(num + 1):
            glVertex3f(0, end + gap * ((start - end) / num), z + (((height / 2) / num) * gap))
            glVertex3f(-0.168, end + gap * ((start - end) / num), z + (((height / 2) / num) * gap))
            glVertex3f(0, end + (gap + 1) * ((start - end) / num), z + (((height / 2) / num) * gap))
            glVertex3f(-0.168, end + (gap + 1) * ((start - end) / num), z + (((height / 2) / num) * gap))
        glEnd()

        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        glBegin(GL_LINE_LOOP)
        for point in space:
            point[2] += 0.001
            glVertex3fv(point)
        glEnd()

        glLineWidth(1.0)
        for gap in range(num):
            glBegin(GL_LINE_LOOP)
            glVertex3f(0, start - gap * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(0, start - (gap + 1) * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(0.168, start - (gap + 1) * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(0.168, start - gap * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * gap) + 0.001)
            glEnd()
        for gap in range(num):
            glBegin(GL_LINE_LOOP)
            glVertex3f(0, start - (gap + 1) * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * (gap + 1)) + 0.001)
            glVertex3f(0, start - (gap + 1) * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(0.168, start - (gap + 1) * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(0.168, start - (gap + 1) * ((start - end) / num) + 0.001, z + (height / 2) + (((height / 2) / num) * (gap + 1)) + 0.001)
            glEnd()
        for gap in range(num):
            glBegin(GL_LINE_LOOP)
            glVertex3f(0, end + gap * ((start - end) / num) - 0.001, z + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(0, end + (gap + 1) * ((start - end) / num) - 0.001, z + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(-0.168, end + (gap + 1) * ((start - end) / num) - 0.001, z + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(-0.168, end + gap * ((start - end) / num) - 0.001, z + (((height / 2) / num) * gap) + 0.001)
            glEnd()
        for gap in range(num):
            glBegin(GL_LINE_LOOP)
            glVertex3f(0, end + (gap + 1) * ((start - end) / num) - 0.001, z + (((height / 2) / num) * (gap + 1)) + 0.001)
            glVertex3f(0, end + (gap + 1) * ((start - end) / num) - 0.001, z + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(-0.168, end + (gap + 1) * ((start - end) / num) - 0.001, z + (((height / 2) / num) * gap) + 0.001)
            glVertex3f(-0.168, end + (gap + 1) * ((start - end) / num) - 0.001, z + (((height / 2) / num) * (gap + 1)) + 0.001)
            glEnd()

    def draw_Roof(self, z):
        all_room_point = []
        room_01 = [[-2.87, -0.16, z],
                    [-2.87, -1.47, z],
                    [-2.16, -1.47, z],
                    [-2.16, -0.16, z]]
        room_02 = [[-2.16, -0.33, z],
                    [-2.16, -1.15, z],
                    [-1.44, -1.15, z],
                    [-1.44, -0.33, z]]
        room_03 = [[-0.71, 0.26, z],
                    [-0.71, -0.49, z],
                    [0.0, -0.49, z],
                    [0.0, 0.59, z]]
        room_04 = [[0.0, 0.59, z],
                    [0.0, -0.16, z],
                    [0.71, -0.16, z],
                    [0.71, 0.92, z]]
        room_05 = [[0.71, 0.92, z],
                    [0.71, 0.16, z],
                    [1.42, 0.16, z],
                    [1.42, 1.25, z]]
        room_06 = [[1.42, 1.25, z],
                    [1.42, 0.49, z],
                    [2.13, 0.49, z],
                    [2.13, 1.57, z]]
        room_07 = [[2.13, 1.97, z],
                    [2.13, 0.82, z],
                    [2.84, 0.82, z],
                    [2.84, 1.97, z]]
        all_room_point.append(room_01)
        all_room_point.append(room_02)
        all_room_point.append(room_03)
        all_room_point.append(room_04)
        all_room_point.append(room_05)
        all_room_point.append(room_06)
        all_room_point.append(room_07)

        all_another_point = []
        empty = [[-1.44, -0.33, z],
                 [-1.44, -0.82, z],
                 [-0.71, -0.82, z],
                 [-0.71, -0.33, z]]
        hallway_01 = [[-2.16, -0.16, z],
                      [-2.16, -0.33, z],
                      [-0.71, -0.33, z],
                      [-0.71, -0.16, z]]
        hallway_02 = [[-0.87, 0.33, z],
                      [-0.87, -0.33, z],
                      [-0.71, -0.33, z],
                      [-0.71, 0.33, z]]
        hallway_03 = [[-0.87, 0.35, z],
                      [-0.87, 0.18, z],
                      [2.13, 1.57, z],
                      [2.13, 1.74, z]]
        hallway_04 = [[-0.81, 0.50, z],
                      [-0.81, 0.36, z],
                      [-0.51, 0.39, z],
                      [-0.51, 0.50, z]]
        hallway_05 = [[-0.51, 0.80, z],
                      [-0.51, 0.48, z],
                      [-0.17, 0.51, z],
                      [-0.17, 0.80, z]]
        stairs = [[-0.17, 1.31, z],
                  [-0.17, 0.64, z],
                  [0.17, 0.64, z],
                  [0.17, 1.57, z]]
        ev = [[-0.81, 0.80, z],
              [-0.81, 0.50, z],
              [-0.51, 0.50, z],
              [-0.51, 0.80, z]]

        all_another_point.append(empty)
        all_another_point.append(hallway_01)
        all_another_point.append(hallway_02)
        all_another_point.append(hallway_03)
        all_another_point.append(hallway_04)
        all_another_point.append(hallway_05)
        all_another_point.append(stairs)
        all_another_point.append(ev)

        edge_point = [[-2.87, -0.16, z],
                      [-2.87, -1.47, z],
                      [-2.16, -1.47, z],
                      [-2.16, -1.15, z],
                      [-1.44, -1.15, z],
                      [-1.44, -0.82, z],
                      [-0.71, -0.82, z],
                      [-0.71, -0.49, z],
                      [0.0, -0.49, z],
                      [0.0, -0.16, z],
                      [0.71, -0.16, z],
                      [0.71, 0.16, z],
                      [1.42, 0.16, z],
                      [1.42, 0.49, z],
                      [2.13, 0.49, z],
                      [2.13, 0.82, z],
                      [2.84, 0.82, z],
                      [2.84, 1.97, z],
                      [2.13, 1.97, z],
                      [2.13, 1.74, z],
                      [0.17, 0.83, z],
                      [0.17, 1.57, z],
                      [-0.17, 1.31, z],
                      [-0.17, 0.80, z],
                      [-0.81, 0.80, z],
                      [-0.81, 0.37, z],
                      [-0.87, 0.35, z],
                      [-0.87, -0.16, z]]

        glBegin(GL_QUADS)
        glColor(self.hallway_color[0], self.hallway_color[1], self.hallway_color[2], self.hallway_color[3])
        for room in all_room_point:
            for point in room:
                glVertex3fv(point)
        for room in all_another_point:
            for point in room:
                glVertex3fv(point)
        glEnd()
        glColor(0, 0, 0, 1)
        glLineWidth(3.0)
        glBegin(GL_LINE_LOOP)
        for point in edge_point:
            point[2] += 0.001
            glVertex3fv(point)
        glEnd()