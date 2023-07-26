from PyQt5.QtCore import QRect, Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import *
from GL.source_gl import gl_draw
from GL.react_gl import eva_draw


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

    test_wid = QOpenGLWidget

    def initializeGL(self):
        self.var_init()
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

    def ui_init(self, ui):
        self.height = 0.4
        self.Watch_Mode = 0
        self.ui = ui

    def var_init(self):
        self.gl_draw = gl_draw()
        self.eva_draw = eva_draw()

        self.gl_draw.Watch_floor = self.ui.WatchFloor_comboBox.currentIndex()
        self.eva_draw.Watch_floor = self.gl_draw.Watch_floor
        self.eva_draw.Start_floor = self.ui.StartFloor_comboBox.currentIndex()
        self.eva_draw.Start_room = self.ui.StartRoom_comboBox.currentIndex()

        if self.ui.WatchMode0.isChecked():
            self.gl_draw.Watch_Mode = 0
        elif self.ui.WatchMode1.isChecked():
            self.gl_draw.Watch_Mode = 1
        elif self.ui.WatchMode2.isChecked():
            self.gl_draw.Watch_Mode = 2

        self.Fire = False

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

        if self.eva_draw.Fire:
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
