from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from plot_data          import plot_data
from analy_data         import analy_data
from node_weight        import weight_checker
from GL.build_gl        import build_gl
import time
from datetime import datetime
import pyautogui
import pymysql

class db_thread(QThread):

    data_sig = pyqtSignal(object, object)
    end_sig = pyqtSignal(object)

    def __init__(self):
        super().__init__()

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
        a = 0

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
                # self.make_database()
                # self.make_tabels()
                # self.set_tables_values()
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

    def list_chunk(self, lst, n):
        return [lst[i:i + int(len(lst) / 4)] for i in range(0, len(lst), int(len(lst) / 4))]

    def run(self):
        self.connect_DB()
        if self.connection:
            sql = "SELECT * FROM data_full;"

            self.cur.execute(sql)
            result = self.cur.fetchall()
            temp_index = []
            gas_index = []
            for idx, type in enumerate(result[0]):
                if type == 'Sensor Temperature':
                    temp_index.append(idx)
                if type == 'Sensor Obscuration':
                    gas_index.append(idx)

            all_temp_datas = []
            all_gas_datas = []

            for _ in range(self.sensor_stack):
                all_temp_datas.append([time.time()] + self.list_chunk([result[1][i] for i in temp_index], 4))
                all_gas_datas.append([time.time()] + self.list_chunk([result[1][i] for i in gas_index], 4))
                # all_temp_datas.append([datetime.now().strftime('%Y/%m/%d %H:%M:%S')] + self.list_chunk([result[1][i] for i in temp_index], 4))
                # all_gas_datas.append([datetime.now().strftime('%Y/%m/%d %H:%M:%S')] + self.list_chunk([result[1][i] for i in gas_index], 4))

            for data in result[1:]:
                if self.working:
                    all_temp_datas.pop(0)
                    all_gas_datas.pop(0)
                    all_temp_datas.append([time.time()] + self.list_chunk([data[i] for i in temp_index], 4))
                    all_gas_datas.append([time.time()] + self.list_chunk([data[i] for i in gas_index], 4))
                    # all_temp_datas.append([datetime.now().strftime('%Y/%m/%d %H:%M:%S')] + self.list_chunk([data[i] for i in temp_index], 4))
                    # all_gas_datas.append([datetime.now().strftime('%Y/%m/%d %H:%M:%S')] + self.list_chunk([data[i] for i in gas_index], 4))
                    self.data_sig.emit(all_temp_datas, all_gas_datas)
                    time.sleep(self.speed / 1)
                else:
                    break

            self.disconnect_DB()
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
        self.ui.system_log_table.setGeometry(QRect((self.ui.log_tabWidget.geometry().width() / 3.0) * 0.0, 0, self.ui.log_tabWidget.geometry().width() / 3.0, self.ui.log_tabWidget.geometry().height()))
        self.ui.analysis_log_table.setGeometry(QRect((self.ui.log_tabWidget.geometry().width() / 3.0) * 1.0, 0, self.ui.log_tabWidget.geometry().width() / 3.0, self.ui.log_tabWidget.geometry().height()))
        self.ui.react_log_table.setGeometry(QRect((self.ui.log_tabWidget.geometry().width() / 3.0) * 2.0, 0, self.ui.log_tabWidget.geometry().width() / 3.0, self.ui.log_tabWidget.geometry().height()))
        self.ui.temp_data_log_table.setGeometry(QRect(0, 0, self.ui.log_tabWidget.geometry().width(), self.ui.log_tabWidget.geometry().height()))
        self.ui.gas_data_log_table.setGeometry(QRect(0, 0, self.ui.log_tabWidget.geometry().width(), self.ui.log_tabWidget.geometry().height()))

    def event_init(self):
        self.db_worker.data_sig.connect(self.data_analy)
        self.db_worker.end_sig.connect(self.thread_end)

    def set_Parameters(self):
        self.db_worker.IP = str(self.ui.IP_Edit.text())
        self.db_worker.Port = self.ui.PORT_Edit.text()
        self.db_worker.ID = self.ui.ID_Edit.text()
        self.db_worker.PW = self.ui.PW_Edit.text()
        self.db_worker.DB_Name = self.ui.DBName_Edit.text()

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

    def data_analy(self, temp_datas, gas_datas):
        self.pd.data_plot(temp_datas, gas_datas)
        self.bg.eva_draw.Fire = self.ad.check_danger(temp_datas, gas_datas)
        # self.bg.data = self.wc.danger_check(temp_datas, gas_datas)

        if self.bg.eva_draw.Fire:
            start_node = 'room10'
            if self.bg.eva_draw.Start_floor != 0:
                start_node = 'room' + str(self.bg.eva_draw.Start_floor) + str(self.bg.eva_draw.Start_room)

            self.bg.eva_draw.path_route = self.bg.eva_draw.rs.search(self.wc.node, start_node)

            path_output = 'path : '
            for point in self.bg.eva_draw.path_route:
                path_output += point + ' -> '
            self.react_log(path_output[:-3])

        else:
            self.bg.Fire = False
            self.bg.gl_draw.show_route = False
            self.bg.eva_draw.path_route = None

        self.data_log(temp_datas[-1], gas_datas[-1])

    def change_Watch_Mode(self):
        if self.ui.WatchMode0.isChecked():
            self.bg.Watch_Mode = 0
        elif self.ui.WatchMode1.isChecked():
            self.bg.Watch_Mode = 1
        elif self.ui.WatchMode2.isChecked():
            self.bg.Watch_Mode = 2

    def change_Start_Point(self):
        self.bg.eva_draw.Start_floor = self.ui.StartFloor_comboBox.currentIndex()
        self.bg.eva_draw.Start_room = self.ui.StartRoom_comboBox.currentIndex()

    def change_Watch_Floor(self):
        self.bg.gl_draw.Watch_floor = self.ui.WatchFloor_comboBox.currentIndex()
        self.bg.eva_draw.Watch_floor = self.bg.gl_draw.Watch_floor

    def thread_end(self, object):
        self.thread_event_set_ui()

    def system_log(self, log):

        time_str = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]

        self.ui.system_log_table.setRowCount(self.ui.system_log_table.rowCount() + 1)
        self.ui.system_log_table.setItem(self.ui.system_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.system_log_table.setItem(self.ui.system_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        self.ui.system_log_table.scrollToBottom()

    def data_log(self, temp_log, gas_log):

        time_str = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
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

        time_str = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]

        self.ui.react_log_table.setRowCount(self.ui.react_log_table.rowCount() + 1)
        self.ui.react_log_table.setItem(self.ui.react_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.react_log_table.setItem(self.ui.react_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        if self.ui.react_log_table.rowCount() > 20:
            self.ui.react_log_table.removeRow(0)
        self.ui.react_log_table.scrollToBottom()
