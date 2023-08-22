from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from plot_data          import plot_data
from analy_data import analy_data, FireDetection_thread
from node_weight        import weight_checker
from GL.build_gl        import build_gl
import time
from datetime import datetime
import pymysql

class db_thread(QThread):

    data_sig = pyqtSignal(object)
    end_sig = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.head = [[], [], [], [], [], []]
        self.floor_idx_list = [[], [], [], [], [], []]
        self.temp_index = [[], [], [], [], [], []]
        self.gas_index = [[], [], [], [], [], []]

        self.IP = None
        self.Port = None
        self.ID = None
        self.PW = None
        self.DB_Name = None

        self.working = False
        self.connection = False
        self.db_connection = None
        self.speed = 1
        self.sensor_stack = 30
        self.floor_num = 4

        self.cur = None

        self.var_init()

    def var_init(self):
        idx_1F = [i for i in range(1, 12)]
        idx_2F = [i for i in range(12, 61)]
        idx_3F = [i for i in range(61, 110)]
        idx_4F = [i for i in range(110, 159)]
        idx_5F = [i for i in range(159, 208)]
        idx_6F = [i for i in range(208, 210)]
        self.floor_idx_list = [idx_1F, idx_2F, idx_3F, idx_4F, idx_5F, idx_6F]

    def init_DB(self):

        try:
            sql = 'CREATE DATABASE IF NOT EXISTS ' + self.DB_Name
            self.cur.execute(sql)
        except Exception as e:
            print(e)

        time.sleep(1)

        create_danger_level = "CREATE TABLE IF NOT EXISTS danger_level(time SMALLINT(3) NOT NULL, `101` FLOAT default 0.0, `102` FLOAT default 0.0, `1-1` FLOAT default 0.0, `1-2` FLOAT default 0.0, " \
                              "`201` FLOAT default 0.0, `202` FLOAT default 0.0, `203` FLOAT default 0.0, `204` FLOAT default 0.0, `205` FLOAT default 0.0, `206` FLOAT default 0.0, `207` FLOAT default 0.0, " \
                              "`2-1` FLOAT default 0.0, `2-2` FLOAT default 0.0, `2-3` FLOAT default 0.0, `2-4` FLOAT default 0.0, " \
                              "`301` FLOAT default 0.0, `302` FLOAT default 0.0, `303` FLOAT default 0.0, `304` FLOAT default 0.0, `305` FLOAT default 0.0, `306` FLOAT default 0.0, `307` FLOAT default 0.0, " \
                              "`3-1` FLOAT default 0.0, `3-2` FLOAT default 0.0, `3-3` FLOAT default 0.0, `3-4` FLOAT default 0.0, " \
                              "`401` FLOAT default 0.0, `402` FLOAT default 0.0, `403` FLOAT default 0.0, `404` FLOAT default 0.0, `405` FLOAT default 0.0, `406` FLOAT default 0.0, `407` FLOAT default 0.0, " \
                              "`4-1` FLOAT default 0.0, `4-2` FLOAT default 0.0, `4-3` FLOAT default 0.0, `4-4` FLOAT default 0.0, " \
                              "`501` FLOAT default 0.0, `502` FLOAT default 0.0, `503` FLOAT default 0.0, `504` FLOAT default 0.0, `505` FLOAT default 0.0, `506` FLOAT default 0.0, `507` FLOAT default 0.0, " \
                              "`5-1` FLOAT default 0.0, `5-2` FLOAT default 0.0, `5-3` FLOAT default 0.0, `5-4` FLOAT default 0.0, " \
                              "PRIMARY KEY(time));"
        create_exit_route = "CREATE TABLE IF NOT EXISTS exit_route(time SMALLINT(3) NOT NULL, `101` TINYINT default 0, `102` TINYINT default 0, " \
                              "`201` TINYINT default 0, `202` TINYINT default 0, `203` TINYINT default 0, `204` TINYINT default 0, `205` TINYINT default 0, `206` TINYINT default 0, `207` TINYINT default 0, " \
                              "`301` TINYINT default 0, `302` TINYINT default 0, `303` TINYINT default 0, `304` TINYINT default 0, `305` TINYINT default 0, `306` TINYINT default 0, `307` TINYINT default 0, " \
                              "`401` TINYINT default 0, `402` TINYINT default 0, `403` TINYINT default 0, `404` TINYINT default 0, `405` TINYINT default 0, `406` TINYINT default 0, `407` TINYINT default 0, " \
                              "`501` TINYINT default 0, `502` TINYINT default 0, `503` TINYINT default 0, `504` TINYINT default 0, `505` TINYINT default 0, `506` TINYINT default 0, `507` TINYINT default 0, " \
                              "PRIMARY KEY(time));"

        try:
            self.cur.execute(create_danger_level)
        except Exception as e:
            print("err create_danger_level: ", e)
        try:
            self.cur.execute(create_exit_route)
        except Exception as e:
            print("err create_exit_route: ", e)

        danger_level_value = ""
        for _ in range(48):
            danger_level_value += "0.0, "
        danger_level_value = danger_level_value[:-2]

        insert_danger_level_1 = "INSERT INTO danger_level VALUES"
        insert_danger_level_2 = ""
        for i in range(61):
            insert_danger_level_2 += "(" + str(i) + ", " + danger_level_value + "), "

        exit_route_value = ""
        for _ in range(30):
            exit_route_value += "0, "
        exit_route_value = exit_route_value[:-2]

        insert_exit_route_1 = "INSERT INTO exit_route VALUES"
        insert_exit_route_2 = ""
        for i in range(61):
            insert_exit_route_2 += "(" + str(i) + ", " + exit_route_value + "), "

        try:
            self.cur.execute(insert_danger_level_1 + insert_danger_level_2[:-2] + ";")
        except Exception as e:
            print("err insert_danger_level: ", e)
        try:
            self.cur.execute(insert_exit_route_1 + insert_exit_route_2[:-2] + ";")
        except Exception as e:
            print("err insert_exit_route: ", e)

    def connect_DB(self):
        if not self.connection:
            try:
                self.db_connection = pymysql.connect(host=self.IP,
                                                     port=int(self.Port),
                                                     user=self.ID,
                                                     password=self.PW,
                                                     db=self.DB_Name,
                                                     charset='utf8',
                                                     autocommit=True,
                                                     read_timeout=5,
                                                     write_timeout=5,
                                                     connect_timeout=5)
                self.cur = self.db_connection.cursor()
                self.init_DB()
                self.connection = True
            except Exception as err:
                print(err)
        else:
            try:
                self.db_connection.close()
                self.connection = False
            except Exception as err:
                print(err)

    def disconnect_DB(self):
        if self.connection:
            try:
                self.db_connection.close()
                self.connection = False

            except Exception as err:
                print(err)

    def list_split_per_floor(self, data, all_index):
        output = []
        for _ in range(len(all_index)):
            output.append([])
        for floor, idx_list in enumerate(all_index):
            for idx in idx_list:
                output[floor].append(data[idx])

        return output

    def run(self):
        self.connect_DB()
        if self.connection:

            sql = "SELECT * FROM sensor_data;"

            self.cur.execute(sql)
            result = self.cur.fetchall()
            self.disconnect_DB()

            head = list(result[0]).copy()
            for idx, type in enumerate(head):
                this_floor = 0
                for floor, floor_nodes in enumerate(self.floor_idx_list):
                    if idx in floor_nodes:
                        this_floor = floor
                if type == 'temp':
                    self.temp_index[this_floor].append(idx)
                if type == 'gas':
                    self.gas_index[this_floor].append(idx)
            self.head = [head[1:12], head[12:61], head[61:110], head[110:159], head[159:208], head[208:210]]

            total_datas = []

            for _ in range(self.sensor_stack):
                frame_datas = [result[1][1:12], result[1][12:61], result[1][61:110], result[1][110:159], result[1][159:208], result[1][208:210]]
                total_datas.append([time.time()] + frame_datas)

            for data in result[1:]:
                data = list(data)
                print(data[0])
                if self.working:
                    frame_datas = [data[1:12], data[12:61], data[61:110], data[110:159], data[159:208], data[208:210]]
                    total_datas.pop(0)
                    total_datas.append([time.time()] + frame_datas)
                    self.data_sig.emit(total_datas)
                    time.sleep(self.speed / 1)
                else:
                    break

            self.working = False
            self.end_sig.emit(True)
            self.quit()
            self.wait(1000)

class get_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.pd = None
        self.bg = None
        self.ad = None
        self.db_worker = None
        self.wc = None

        self.IP = None
        self.Port = None
        self.ID = None
        self.PW = None
        self.DB_Name = None

        self.last_exit_rout = {}

        self.func_init()
        self.var_init()
        self.event_init()


    def func_init(self):
        self.pd = plot_data(self.ui)
        self.bg = build_gl(self.ui.openGLWidget)
        self.bg.ui_init(self.ui)
        self.ad = analy_data(self.ui)
        self.wc = weight_checker()

    def var_init(self):
        self.db_worker = db_thread()
        self.set_Parameters()

    def resizeWidget(self):
        self.bg.resizeWidget(self.ui.openGLWidget.geometry())
        width = self.ui.log_tabWidget.geometry().width() - 6
        height = self.ui.log_tabWidget.geometry().height() - 25
        self.ui.system_log_table.setGeometry(QRect((width / 3.0) * 0.0, 0, width / 3.0 - 1, height))
        self.ui.analysis_log_table.setGeometry(QRect((width / 3.0) * 1.0, 0, width / 3.0 - 1, height))
        self.ui.react_log_table.setGeometry(QRect((width / 3.0) * 2.0, 0, width / 3.0 - 1, height))
        self.ui.temp_data_log_table.setGeometry(QRect(0, 0, width, height))
        self.ui.gas_data_log_table.setGeometry(QRect(0, 0, width, height))

    def event_init(self):
        self.db_worker.data_sig.connect(self.data_analy)
        self.db_worker.end_sig.connect(self.thread_end)

    def set_Parameters(self):
        self.IP = self.ui.IP_Edit.text()
        self.Port = self.ui.PORT_Edit.text()
        self.ID = self.ui.ID_Edit.text()
        self.PW = self.ui.PW_Edit.text()
        self.DB_Name = self.ui.DBName_Edit.text()
        self.db_worker.IP = self.IP
        self.db_worker.Port = self.Port
        self.db_worker.ID = self.ID
        self.db_worker.PW = self.PW
        self.db_worker.DB_Name = self.DB_Name

        for floor in range(5):
            if floor == 0:
                for room in range(2):
                    self.last_exit_rout[str(floor + 1) + '0' + str(room + 1)] = 0
            else:
                for room in range(7):
                    self.last_exit_rout[str(floor + 1) + '0' + str(room + 1)] = 0

    def worker_start(self):
        if self.db_worker.isRunning():
            self.db_worker.working = False
            # self.db_worker.stop()
        else:
            self.set_Parameters()
            self.db_worker.working = True
            self.db_worker.start()
            self.thread_event_set_ui()

    def thread_event_set_ui(self):
        if self.db_worker.working == True:
            self.ui.Start_Service_btn.setText("STOP")
            self.system_log("TCP start")
        if self.db_worker.working == False:
            self.ui.Start_Service_btn.setText("START")
            self.system_log("TCP End")

    def split_datas_sensor_type(self, head, datas):
        total_temp_datas = []
        total_gas_datas = []
        for data in datas:
            temp_datas = [[], [], [], [], [], []]
            gas_datas = [[], [], [], [], [], []]
            for floor, (types, values) in enumerate(zip(head, data[1:])):
                for type, value in zip(types, values):
                    if type == 'temp':
                        temp_datas[floor].append(value)
                    elif type == 'gas':
                        gas_datas[floor].append(value)
            total_temp_datas.append([data[0]] + temp_datas)
            total_gas_datas.append([data[0]] + gas_datas)
        return total_temp_datas, total_gas_datas

    def update_danger_level_DB(self):
        a = 0

    def update_exit_rout_DB(self, time, exit_routes):
        exit_rout_sql = 'UPDATE exit_route SET '
        for room in exit_routes.keys():
            exit_rout_sql += ('`' + room + '` = ' + str(exit_routes[room]) + ', ')
        exit_rout_sql = exit_rout_sql[:-2] + ' WHERE time = ' + str(time) + ';'

        try:
            with pymysql.connect(host=self.IP, port=int(self.Port), user=self.ID, password=self.PW, db=self.DB_Name,
                                 charset='utf8', autocommit=True, read_timeout=5, write_timeout=5, connect_timeout=5) as conn:
                with conn.cursor() as cur:
                    cur.execute(exit_rout_sql)
        except Exception as e:
            print(e)

    def data_analy(self, total_datas):

        temp_datas, gas_datas = self.split_datas_sensor_type(self.db_worker.head, total_datas)

        Fire_status, temp_idx, gas_idx = self.ad.check_danger(temp_datas, gas_datas)

        for floor, last, new in zip(range(5), self.bg.eva_draw.Fire, Fire_status):
            if (not last) and (new):
                if (floor >= 1) and (floor <= 4):
                    self.bg.scenario_data[floor - 1]['time'] = time.time()
        self.bg.eva_draw.Fire = Fire_status

        self.wc.set_node_weight(temp_idx, gas_idx, self.db_worker.temp_index,
                                self.db_worker.gas_index)

        exit_routs = {}
        for floor in range(5):
            if floor == 0:
                for room in range(2):
                    start_node = 'room' + str(floor) + str(room)
                    path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)
                    if path_route[-1] == 'escape00':
                        exit_routs[str(floor + 1) + '0' + str(room + 1)] = 0
                    elif path_route[-1] == 'escape01':
                        exit_routs[str(floor + 1) + '0' + str(room + 1)] = 1
            else:
                for room in range(7):
                    start_node = 'room' + str(floor) + str(room)
                    path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)
                    if path_route[-1] == 'escape00':
                        exit_routs[str(floor + 1) + '0' + str(room + 1)] = 0
                    elif path_route[-1] == 'escape01':
                        exit_routs[str(floor + 1) + '0' + str(room + 1)] = 1

        exit_rout_change = False
        for key in exit_routs.keys():
            if self.last_exit_rout[key] != exit_routs[key]:
                exit_rout_change = True
                break
        if exit_rout_change:
            self.update_exit_rout_DB(0, exit_routs)

        danger_level = []
        for floor in range(6):
            danger_level.append(self.bg.set_danger_level(floor, self.db_worker.head[floor], total_datas[-1][floor + 1]))


        if True in self.bg.eva_draw.Fire:
            if self.bg.Watch_Mode == 0:
                for floor in range(6):
                    if floor == self.bg.eva_draw.Start_floor:
                        self.bg.gl_draw.Transparency[floor] = 1.0
                    elif floor <= self.bg.eva_draw.Start_floor:
                        self.bg.gl_draw.Transparency[floor] = 0.1
                    else:
                        self.bg.gl_draw.Transparency[floor] = 0.0

            scenario_idx = self.ad.check_scenario(self.bg.eva_draw.Fire, temp_datas, gas_datas)

            change_scenario = False
            for floor, danger in enumerate(self.bg.eva_draw.Fire):
                if danger and (floor != 0):
                    floor -= 1
                    if self.bg.scenario_data[floor]['index'] != scenario_idx[floor]:
                        change_scenario = True
                        self.bg.scenario_data[floor]['index'] = scenario_idx[floor]
                        self.bg.load_scenario(floor)

            if change_scenario:
                a = 0

        else:
            for floor in range(6):
                self.bg.gl_draw.Transparency[floor] = 1.0




        if True in self.bg.eva_draw.Fire:
            # for i in range(len(scenario_idx)):
            #     if self.bg.scenario_idx[i] != scenario_idx[i]:
            #         self.bg.scenario_idx[i] = scenario_idx[i]
            #         self.bg.load_scenario(i)

            if self.bg.Watch_Present:
                for floor in range(6):
                    self.bg.set_danger_level(floor, self.db_worker.head[floor], total_datas[-1][floor + 1])

                self.wc.set_node_weight(self.ad.temp_Fire_idx, self.ad.gas_Fire_idx, self.db_worker.temp_index, self.db_worker.gas_index)
                start_node = 'room' + str(self.bg.eva_draw.Start_floor) + str(self.bg.eva_draw.Start_room)

                self.bg.eva_draw.path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)

                path_output = 'path : '
                for point in self.bg.eva_draw.path_route:
                    path_output += point + ' -> '
                self.react_log(path_output[:-3])

        else:
            self.bg.eva_draw.Fire = [False for _ in range(5)]
            self.bg.gl_draw.show_route = False
            self.bg.eva_draw.path_route = None

        self.pd.data_plot(temp_datas, gas_datas)
        self.data_log(temp_datas[-1], gas_datas[-1])

    def change_Watch_Mode(self):
        if self.ui.WatchMode0.isChecked():
            self.bg.Watch_Mode = 0
            self.ui.WatchFloor_comboBox.setEnabled(False)
            if self.ui.WatchMode_Highlight.isChecked():
                for floor in range(6):
                    if floor == self.bg.eva_draw.Start_floor:
                        self.bg.gl_draw.Transparency[floor] = 1.0
                    elif floor <= self.bg.eva_draw.Start_floor:
                        self.bg.gl_draw.Transparency[floor] = 0.1
                    else:
                        self.bg.gl_draw.Transparency[floor] = 0.0
            else:
                for floor in range(6):
                    self.bg.gl_draw.Transparency[floor] = 1.0
        elif self.ui.WatchMode1.isChecked():
            self.bg.Watch_Mode = 1
            self.ui.WatchFloor_comboBox.setEnabled(True)
            for floor in range(6):
                self.bg.gl_draw.Transparency[floor] = 1.0
        elif self.ui.WatchMode2.isChecked():
            self.bg.Watch_Mode = 2
            self.ui.WatchFloor_comboBox.setEnabled(True)
            for floor in range(6):
                self.bg.gl_draw.Transparency[floor] = 1.0

        self.bg.trans_pos_x, self.bg.trans_pos_y, self.bg.trans_pos_z = (0, 0, 0)
        self.bg.x_angle, self.bg.z_angle = 1, 1

        # camera
        self.bg.last_pos_x, self.bg.last_pos_y, self.bg.last_pos_z = 0.0, 5.0, -5.0

        # object move
        self.bg.move_last_pos_x, self.bg.move_last_pos_y, self.bg.move_last_pos_z = 0.0, 0.0, 0.0
        self.bg.trans_pos_x, self.bg.trans_pos_y, self.bg.trans_pos_z = 0, 0, 0

    def change_Start_Floor(self):
        self.bg.eva_draw.Start_floor = self.ui.StartFloor_comboBox.currentIndex()
        if self.bg.eva_draw.Start_floor == 0:
            self.ui.StartRoom_comboBox.clear()
            for i in range(2):
                self.ui.StartRoom_comboBox.addItem(str(i + 1))
        else:
            self.ui.StartRoom_comboBox.clear()
            for i in range(7):
                self.ui.StartRoom_comboBox.addItem(str(i + 1))
        self.bg.eva_draw.Start_room = 0

        if not self.bg.Watch_Present:
            if self.ui.N_min_later_combobox.currentIndex() <= 60:
                self.bg.time_gap = self.ui.N_min_later_combobox.currentIndex() * 60
                time = self.bg.set_time + 1 + self.bg.time_gap
                if time >= 3600:
                    time = 3600

                temp_idx = [[], [], [], [], [], []]
                gas_idx = [[], [], [], [], [], []]

                for floor, danger in enumerate(self.bg.eva_draw.Fire):
                    if danger and (floor != 0):
                        self.bg.set_danger_level(floor - 1, self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:])
                        temp_count = 0
                        gas_count = 0
                        for type, value in zip(self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:]):
                            if type == 'temp':
                                if float(value) >= 70.0:
                                    temp_idx[floor].append(temp_count)
                                temp_count += 1
                            elif type == 'gas':
                                if float(value) >= 0.15:
                                    gas_idx[floor].append(gas_count)
                                gas_count += 1

            self.wc.set_node_weight(temp_idx, gas_idx, self.db_worker.temp_index, self.db_worker.gas_index)
            start_node = 'room' + str(self.bg.eva_draw.Start_floor) + str(self.bg.eva_draw.Start_room)
            self.bg.eva_draw.path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)

            path_output = 'path : '
            for point in self.bg.eva_draw.path_route:
                path_output += point + ' -> '
            self.react_log(path_output[:-3])

    def change_Start_Room(self):
        if self.ui.StartRoom_comboBox.currentIndex() >= 0:
            self.bg.eva_draw.Start_room = self.ui.StartRoom_comboBox.currentIndex()

        if not self.bg.Watch_Present:
            if self.ui.N_min_later_combobox.currentIndex() <= 60:
                self.bg.time_gap = self.ui.N_min_later_combobox.currentIndex() * 60
                time = self.bg.set_time + 1 + self.bg.time_gap
                if time >= 3600:
                    time = 3600

                temp_idx = [[], [], [], [], [], []]
                gas_idx = [[], [], [], [], [], []]

                for floor, danger in enumerate(self.bg.eva_draw.Fire):
                    if danger and (floor != 0):
                        self.bg.set_danger_level(floor - 1, self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:])
                        temp_count = 0
                        gas_count = 0
                        for type, value in zip(self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:]):
                            if type == 'temp':
                                if float(value) >= 70.0:
                                    temp_idx[floor].append(temp_count)
                                temp_count += 1
                            elif type == 'gas':
                                if float(value) >= 0.15:
                                    gas_idx[floor].append(gas_count)
                                gas_count += 1

            self.wc.set_node_weight(temp_idx, gas_idx, self.db_worker.temp_index, self.db_worker.gas_index)
            start_node = 'room' + str(self.bg.eva_draw.Start_floor) + str(self.bg.eva_draw.Start_room)
            self.bg.eva_draw.path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)

            path_output = 'path : '
            for point in self.bg.eva_draw.path_route:
                path_output += point + ' -> '
            self.react_log(path_output[:-3])

    def change_Watch_Floor(self):
        self.bg.gl_draw.Watch_floor = self.ui.WatchFloor_comboBox.currentIndex()
        self.bg.eva_draw.Watch_floor = self.bg.gl_draw.Watch_floor

        self.bg.gl_draw.Transparency[self.bg.gl_draw.Watch_floor] = 1.0


    def change_N_Mode(self):
        if self.ui.watch_present.isChecked():
            self.bg.Watch_Present = True
            self.ui.N_min_later_combobox.setEnabled(False)
        else:
            self.ui.N_min_later_combobox.setEnabled(True)
            self.bg.Watch_Present = False
            self.ui.N_min_later_combobox.setCurrentIndex(0)
            self.bg.time_gap = self.ui.N_min_later_combobox.currentIndex() * 60
            for floor, danger in enumerate(self.bg.eva_draw.Fire):
                if danger and (floor != 0):
                    time = self.bg.set_time + 1 + self.bg.time_gap
                    if time >= len(self.bg.future_data[floor - 1][1:]):
                        time = len(self.bg.future_data[floor - 1][1:]) - 1
                    if len(self.bg.future_data[floor - 1]) != 0:
                        self.bg.set_danger_level(floor - 1, self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:])

    def change_N_min(self):
        if not self.bg.Watch_Present:
            if self.ui.N_min_later_combobox.currentIndex() <= 60:
                self.bg.time_gap = self.ui.N_min_later_combobox.currentIndex() * 60
                time = self.bg.set_time + 1 + self.bg.time_gap
                if time >= 3600:
                    time = 3600

                temp_idx = [[], [], [], [], [], []]
                gas_idx = [[], [], [], [], [], []]

                for floor, danger in enumerate(self.bg.eva_draw.Fire):
                    if danger and (floor != 0):
                        self.bg.set_danger_level(floor - 1, self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:])
                        temp_count = 0
                        gas_count = 0
                        for type, value in zip(self.db_worker.head[floor][:-1], self.bg.future_data[floor - 1][time][1:]):
                            if type == 'temp':
                                if float(value) >= 70.0:
                                    temp_idx[floor].append(temp_count)
                                temp_count += 1
                            elif type == 'gas':
                                if float(value) >= 0.15:
                                    gas_idx[floor].append(gas_count)
                                gas_count += 1

            self.wc.set_node_weight(temp_idx, gas_idx, self.db_worker.temp_index, self.db_worker.gas_index)
            start_node = 'room' + str(self.bg.eva_draw.Start_floor) + str(self.bg.eva_draw.Start_room)
            self.bg.eva_draw.path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)

            path_output = 'path : '
            for point in self.bg.eva_draw.path_route:
                path_output += point + ' -> '
            self.react_log(path_output[:-3])

    def thread_end(self, object):
        self.thread_event_set_ui()

    def system_log(self, log):

        time_str = datetime.today().strftime('%H:%M:%S.%f')[:-3]

        self.ui.system_log_table.setRowCount(self.ui.system_log_table.rowCount() + 1)
        self.ui.system_log_table.setItem(self.ui.system_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.system_log_table.setItem(self.ui.system_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        self.ui.system_log_table.scrollToBottom()

    def data_log(self, temp_log, gas_log):

        time_str = datetime.today().strftime('%H:%M:%S.%f')[:-3]
        temp_item = ', '.join([str(data) for data in temp_log][1:])
        gas_item = ', '.join([str(data) for data in gas_log][1:])

        self.ui.temp_data_log_table.setRowCount(self.ui.temp_data_log_table.rowCount() + 1)
        self.ui.gas_data_log_table.setRowCount(self.ui.gas_data_log_table.rowCount() + 1)
        self.ui.temp_data_log_table.setItem(self.ui.temp_data_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.gas_data_log_table.setItem(self.ui.gas_data_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.temp_data_log_table.setItem(self.ui.temp_data_log_table.rowCount() - 1, 1, QTableWidgetItem(temp_item))
        self.ui.gas_data_log_table.setItem(self.ui.gas_data_log_table.rowCount() - 1, 1, QTableWidgetItem(gas_item))
        if self.ui.temp_data_log_table.rowCount() > 20:
            self.ui.temp_data_log_table.removeRow(0)
        if self.ui.gas_data_log_table.rowCount() > 20:
            self.ui.gas_data_log_table.removeRow(0)
        self.ui.temp_data_log_table.scrollToBottom()
        self.ui.gas_data_log_table.scrollToBottom()

    def react_log(self, log):

        time_str = datetime.today().strftime('%H:%M:%S.%f')[:-3]

        self.ui.react_log_table.setRowCount(self.ui.react_log_table.rowCount() + 1)
        self.ui.react_log_table.setItem(self.ui.react_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.react_log_table.setItem(self.ui.react_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        if self.ui.react_log_table.rowCount() > 20:
            self.ui.react_log_table.removeRow(0)
        self.ui.react_log_table.scrollToBottom()
