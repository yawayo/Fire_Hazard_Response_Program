from PyQt5.QtCore import QRect, Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import *
from GL.source_gl import gl_draw
from GL.react_gl import eva_draw
import os
import csv


class build_gl(QOpenGLWidget):

    left_mouse_press = False
    right_mouse_press = False
    trans_pos_x, trans_pos_y, trans_pos_z = (0, 0, 0)
    x_angle, z_angle = 1, 1

    # camera
    last_pos_x, last_pos_y, last_pos_z = 0.0, 5.0, -5.0

    # object move
    move_last_pos_x, move_last_pos_y, move_last_pos_z = 0.0, 0.0, 0.0
    trans_pos_x, trans_pos_y, trans_pos_z = 0, 0, 0



    def initializeGL(self):
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glShadeModel(GL_SMOOTH)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        self.var_init()

    def ui_init(self, ui):
        self.height = 0.4
        self.Watch_Mode = 0
        self.set_time = 0
        self.time_gap = 0
        self.scenario_idx = [-1, -1, -1, -1]
        self.future_data = [[], [], [], []]

        self.ui = ui

        self.var_init()

    def var_init(self):
        self.gl_draw = gl_draw()
        self.eva_draw = eva_draw()

        self.gl_draw.Watch_floor = self.ui.WatchFloor_comboBox.currentIndex()
        self.eva_draw.Watch_floor = self.gl_draw.Watch_floor
        self.eva_draw.Start_floor = self.ui.StartFloor_comboBox.currentIndex()
        self.eva_draw.Start_room = self.ui.StartRoom_comboBox.currentIndex()

        if self.ui.WatchMode0.isChecked():
            self.Watch_Mode = 0
        elif self.ui.WatchMode1.isChecked():
            self.Watch_Mode = 1
        elif self.ui.WatchMode2.isChecked():
            self.Watch_Mode = 2

    def load_scenario(self, floor):
        Dir_path = 'C:/Users/iyaso/PycharmProjects/test.csv'#'D:/.2. 4차년도 국토부/data/'
        #File_path = os.path.join(Dir_path, 'M' + format(self.scenario[floor], '05') + '.csv')

        scenario_data = []
        temp_sensor_idx = []
        gas_sensor_idx = []
        with open(Dir_path, 'r', encoding='utf-8-sig') as f:
            time_value = csv.reader(f)
            found = False
            for time, frame_datas in enumerate(time_value):
                if time == 0:
                    for i, sensor_name in enumerate(frame_datas):
                        if sensor_name == 'Sensor Temperature':
                            temp_sensor_idx.append(i)
                        elif sensor_name == 'Sensor Obscuration':
                            gas_sensor_idx.append(i)
                else:
                    if not found:
                        for i, value in enumerate(frame_datas):
                            if i in temp_sensor_idx:
                                if float(value) >= 70.0:
                                    self.set_time = time
                                    found = True
                                    break
                            elif i in gas_sensor_idx:
                                if float(value) >= 0.15:
                                    self.set_time = time
                                    found = True
                                    break
                scenario_data.append(frame_datas)
        self.future_data[floor] = scenario_data.copy()
        self.set_danger_level()

    def set_danger_level(self):
        for floor, floor_future_data in enumerate(self.future_data):
            if len(floor_future_data) != 0:
                time = self.set_time + 1 + self.time_gap
                if time >= len(floor_future_data[1:]):
                    time = len(floor_future_data[1:]) - 1

                head = floor_future_data[0][1:].copy()
                data = floor_future_data[time][1:].copy()
                room1 = [head[0:7], data[0:7]]
                room2 = [head[7:13], data[7:13]]
                room3 = [head[13:19], data[13:19]]
                room4 = [head[19:25], data[19:25]]
                room5 = [head[25:31], data[25:31]]
                room6 = [head[31:37], data[31:37]]
                room7 = [head[37:44], data[37:44]]
                floor_data = [room1, room2, room3, room4, room5, room6, room7]

                for room, room_data in enumerate(floor_data):
                    room_danger_level = [[0, 'temp', 20.0], [0, 'gas', 0.0]]
                    for i in range(len(room_data[0])):
                        sensor_danger_level = [0, '', 0.0]
                        if room_data[0][i] == 'Sensor Temperature':
                            if float(room_data[1][i]) >= 70.0:
                                sensor_danger_level = [2, 'temp', float(room_data[1][i])]
                            elif float(room_data[1][i]) >= 30.0:
                                sensor_danger_level = [1, 'temp', float(room_data[1][i])]
                            else:
                                sensor_danger_level = [0, 'temp', float(room_data[1][i])]
                        elif room_data[0][i] == 'Sensor Obscuration':
                            if float(room_data[1][i]) >= 0.15:
                                sensor_danger_level = [2, 'gas', float(room_data[1][i])]
                                gas = float(room_data[1][i])
                            elif float(room_data[1][i]) >= 0.01:
                                sensor_danger_level = [1, 'gas', float(room_data[1][i])]
                            else:
                                sensor_danger_level = [0, 'gas', float(room_data[1][i])]
                        sensor_type = 0 if sensor_danger_level[1] == 'temp' else 1
                        if room_danger_level[sensor_type][0] <= sensor_danger_level[0]:
                            room_danger_level[sensor_type] = sensor_danger_level

                    temp_red = (room_danger_level[0][2] / 100.0) if (room_danger_level[0][2] <= 100) else 1.0
                    gas_red = room_danger_level[1][2]
                    red_value = max(temp_red, gas_red) * 2.0
                    if red_value <= 1.0:
                        self.gl_draw.bottom_color[floor + 1][room] = [red_value, 1.0, 0.0, 1.0]
                    else:
                        self.gl_draw.bottom_color[floor + 1][room] = [1.0, 1.0 - (red_value - 1.0), 0.0, 1.0]

    def resizeGL(self, w, h):
        glGetError()

        aspect = w if (h == 0) else w / h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(45, aspect, 0.1, 1000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def resizeWidget(self, geometry):
        self.setGeometry(QRect(0, 0, geometry.width(), geometry.height()))

    def mouseMoveEvent(self, event):
        speed = 1.0
        if self.left_mouse_press == True:
            if abs(event.x() - self.move_last_pos_x) > abs(event.y() - self.move_last_pos_y):
                if event.x() < self.move_last_pos_x:
                    self.trans_pos_x -= 0.1
                else:
                    self.trans_pos_x += 0.1
            else:
                if event.y() < self.move_last_pos_y:
                    self.trans_pos_y += 0.1
                else:
                    self.trans_pos_y -= 0.1
        elif self.right_mouse_press == True:
            if abs(abs(event.x()) - abs(self.move_last_pos_x)) > abs(abs(event.y()) - abs(self.move_last_pos_y)):
                if event.x() < self.move_last_pos_x:
                    self.z_angle -= 2
                else:
                    self.z_angle += 2
            elif abs(abs(event.x()) - abs(self.move_last_pos_x)) == abs(abs(event.y()) - abs(self.move_last_pos_y)):
                pass
            else:
                if event.y() < self.move_last_pos_y:
                    self.x_angle -= 2
                else:
                    self.x_angle += 2
        self.move_last_pos_x = event.x()
        self.move_last_pos_y = event.y()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            if self.trans_pos_z >= -9.0:
                self.trans_pos_z -= 0.5
        else:
            if self.trans_pos_z <= 6.5:
                self.trans_pos_z += 0.5

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_mouse_press = True
            self.move_last_pos_x = event.x()
            self.move_last_pos_y = event.y()
        if event.button() == Qt.LeftButton:
            self.left_mouse_press = True
            self.move_last_pos_x = event.x()
            self.move_last_pos_y = event.y()

    def mouseReleaseEvent(self, event):
        self.left_mouse_press = False
        self.right_mouse_press = False

    def paintGL(self):
        Fire = False
        for status in self.eva_draw.Fire:
            if status:
                Fire = True
        if Fire:
            if self.height <= 0.6:
                self.height += 0.01
        self.eva_draw.height = self.height
        self.gl_draw.height = self.height


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if self.Watch_Mode == 0:
            gluLookAt(-0.5, -9.0, 3,
                      -0.5, 1.0, 0.9,
                      0.0, 0.0, 1.0)

            glTranslatef(self.trans_pos_x, self.trans_pos_z, self.trans_pos_y)
            glRotatef(self.x_angle, 1, 0, 0)
            glRotatef(self.z_angle, 0, 0, 1)

            self.eva_draw.draw_Danger_Building()
            self.gl_draw.draw_Building()

        elif self.Watch_Mode == 1:
            gluLookAt(-0.5, -9.0, 3,
                      -0.5, 1.0, 0.9,
                      0.0, 0.0, 1.0)

            glTranslatef(self.trans_pos_x, self.trans_pos_z, self.trans_pos_y)
            glRotatef(self.x_angle, 1, 0, 0)
            glRotatef(self.z_angle, 0, 0, 1)

            self.eva_draw.draw_Danger_Floor_3D()
            self.gl_draw.draw_Floor_3D()

        elif self.Watch_Mode == 2:
            gluLookAt(0.0, -9.0, 0.0,
                      0.0, 0.0, 0.0,
                      0.0, 0.0, 1.0)

            glTranslatef(self.trans_pos_x, self.trans_pos_z, self.trans_pos_y)
            glRotatef(90, 1, 0, 0)

            self.eva_draw.draw_Danger_Floor_2D()
            self.gl_draw.draw_Floor_2D()

        glFinish()

        self.update()
