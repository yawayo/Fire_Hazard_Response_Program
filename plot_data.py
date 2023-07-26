import pyqtgraph as pg
import time
import numpy as np
from datetime import datetime

class plot_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.temp_sensor_num = 28
        self.gas_sensor_num = 20

        self.var_init()

    def var_init(self):
        self.start_label_counter = False
        self.fire_label_counter = False
        self.outlier_label_counter = False
        self.output = ''
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(useOpenGL=True)

        # 화살표 추가
        self.arrow_01 = pg.ArrowItem(angle=-60, tipAngle=30, headLen=30, tailWidth=10, pen={'color': 'w', 'width': 3}, brush='r')

        # Bar Graph 설정
        self.ui.temp_floor_graph.setTitle('Temperature (%s)' % datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        self.ui.gas_floor_graph.setTitle('Gas (%s)' % datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        self.ui.temp_floor_graph.setMouseEnabled(x=False, y=False)
        self.ui.gas_floor_graph.setMouseEnabled(x=False, y=False)
        self.ui.temp_floor_graph.setBackground('w')
        self.ui.gas_floor_graph.setBackground('w')
        self.ui.temp_floor_graph.setLimits(yMin=0)
        self.ui.gas_floor_graph.setLimits(yMin=0)
        self.ui.temp_floor_graph.showGrid(x=False, y=True)
        self.ui.gas_floor_graph.showGrid(x=False, y=True)
        self.ui.temp_floor_graph.setRange(xRange=(0, 29), disableAutoRange=True, padding=0)
        self.ui.gas_floor_graph.setRange(xRange=(0, 21), disableAutoRange=True, padding=0)

        temp_floor_graph_axis = self.ui.temp_floor_graph.getAxis('bottom')
        gas_floor_graph_axis = self.ui.gas_floor_graph.getAxis('bottom')
        temp_floor_graph_axis.setStyle(tickTextOffset=8)
        gas_floor_graph_axis.setStyle(tickTextOffset=8)

        temp_ticks = [list(zip(range(1, 29), [str(i) for i in range(1, 29)]))]
        gas_ticks = [list(zip(range(1, 21), [str(i) for i in range(1, 21)]))]
        temp_floor_graph_axis.setTicks(temp_ticks)
        gas_floor_graph_axis.setTicks(gas_ticks)

        # Line Graph 설정
        self.room_index = ['1', '2', '3', '4', '5', '6', '7']

        self.ui.temp_sensor_graph.setAxisItems(axisItems={'bottom': TimeAxisItem(orientation='bottom')})    # axis x축 시간값으로 출력
        self.ui.gas_sensor_graph.setAxisItems(axisItems={'bottom': TimeAxisItem(orientation='bottom')})    # axis x축 시간값으로 출력
        self.ui.temp_sensor_graph.setMouseEnabled(x=False, y=False)                                         # mouse grab disable
        self.ui.gas_sensor_graph.setMouseEnabled(x=False, y=False)                                         # mouse grab disable
        self.ui.temp_sensor_graph.setBackground('w')                                                        # 배경 색 변경
        self.ui.gas_sensor_graph.setBackground('w')                                                        # 배경 색 변경
        self.ui.temp_sensor_graph.setTitle(self.ui.floor_comboBox.currentText() + ' - ' + self.ui.temp_sensor_combobox.currentText() + ' T_Sensor')
        self.ui.gas_sensor_graph.setTitle(self.ui.floor_comboBox.currentText() + ' - ' + self.ui.gas_sensor_combobox.currentText() + ' G_Sensor')
        self.ui.temp_sensor_graph.getAxis('left').setStyle(autoExpandTextSpace=False, textFillLimits=[(0, 0.7)])
        self.ui.gas_sensor_graph.getAxis('left').setStyle(autoExpandTextSpace=False)
        self.ui.temp_sensor_graph.getAxis('left').setLabel('Temperature', units='°C')
        self.ui.gas_sensor_graph.getAxis('left').setLabel('Gas', units='%')
        self.temp_sensor_graph_plot = self.ui.temp_sensor_graph.plot()                                                    # PlotDataItem 객체 생성
        self.gas_sensor_graph_plot = self.ui.gas_sensor_graph.plot()

    def data_plot(self, temp_datas, gas_datas):
        t = time.time()
        # if "00:00:00" == time.strftime("%H:%M:%S", time.localtime(t)):
        #     self.ui.gr_01.setXRange(int(time.time()), int(time.time()) + 60)
        #     self.ui.gr_02.setXRange(int(time.time()), int(time.time()) + 60)

        self.ui.temp_sensor_graph.setTitle(self.ui.floor_comboBox.currentText() + ' - ' + self.ui.temp_sensor_combobox.currentText() + ' T_Sensor')
        self.ui.gas_sensor_graph.setTitle(self.ui.floor_comboBox.currentText() + ' - ' + self.ui.gas_sensor_combobox.currentText() + ' G_Sensor')

        time_item = [data[0] for data in temp_datas]
        temp_data_item = [float(data[self.ui.floor_comboBox.currentIndex() + 1][self.ui.temp_sensor_combobox.currentIndex()]) for data in temp_datas]
        gas_data_item = [int(float(data[self.ui.floor_comboBox.currentIndex() + 1][self.ui.gas_sensor_combobox.currentIndex()]) * 100) for data in gas_datas]

        self.temp_sensor_graph_plot.setData(time_item, temp_data_item, pen='r', connect='finite')
        self.gas_sensor_graph_plot.setData(time_item, gas_data_item, pen='b', connect='finite')

            # if self.output == 'Start' and self.start_label_counter == False:
            #     self.start_label_counter = True
            #
            #     self.text_01 = pg.TextItem(text='분석 시작', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
            #                                angle=-30, rotateAxis=(1, 0))
            #     self.text_01.setPos(data['x'][-1], data['t'+str(i).zfill(2)][-1] + 0.05)
            #     self.ui.gr_01.addItem(self.text_01)
            #
            #     self.text_02 = pg.TextItem(text='분석 시작', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
            #                                angle=-30, rotateAxis=(1, 0))
            #     self.text_02.setPos(data['x'][-1], data['g'+str(i).zfill(2)][-1] + 0.05)
            #     self.ui.gr_02.addItem(self.text_02)
            #
            # elif self.output == 'Fire' and self.fire_label_counter == False:
            #     self.fire_label_counter = True
            #     self.text_01 = pg.TextItem(text='화재 발생', fill=(255, 0, 0), color=(255, 255, 255), anchor=(1, 1),
            #                                angle=-30, rotateAxis=(1, 0))
            #     self.text_01.setPos(data['x'][-1], data['t'+str(i).zfill(2)][-1] + 0.05)
            #     self.ui.gr_01.addItem(self.text_01)
            #
            #     self.text_02 = pg.TextItem(text='화재 발생', fill=(255, 0, 0), color=(255, 255, 255), anchor=(1, 1),
            #                                angle=-30, rotateAxis=(1, 0))
            #     self.text_02.setPos(data['x'][-1], data['g'+str(i).zfill(2)][-1] + 0.05)
            #     self.ui.gr_02.addItem(self.text_02)
            #
            # elif self.output == 'Outlier' and self.outlier_label_counter == False:
            #     self.outlier_label_counter = False
            #     self.text_01 = pg.TextItem(text='이상치', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
            #                                angle=-30, rotateAxis=(1, 0))
            #     self.text_01.setPos(data['x'][-1], data['t'+str(i).zfill(2)][-1] + 0.05)
            #     self.ui.gr_01.addItem(self.text_01)
            #
            #     self.text_02 = pg.TextItem(text='이상치', fill=(0, 0, 255), color=(255, 255, 255), anchor=(1, 1),
            #                                angle=-30, rotateAxis=(1, 0))
            #     self.text_02.setPos(data['x'][-1], data['g'+str(i).zfill(2)][-1] + 0.05)
            #     self.ui.gr_02.addItem(self.text_02)


        self.ui.temp_floor_graph.setTitle('Temperature (%s)' % datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        self.ui.gas_floor_graph.setTitle('Gas (%s)' % datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        self.ui.temp_floor_graph.clear()
        self.ui.gas_floor_graph.clear()
        t_barChar = pg.BarGraphItem(x=np.arange(1, len(temp_datas[-1][1:][self.ui.floor_comboBox.currentIndex()]) + 1), height=[float(value) for value in temp_datas[-1][1:][self.ui.floor_comboBox.currentIndex()]], width=0.6, brush=(255, 0, 0))
        g_barChar = pg.BarGraphItem(x=np.arange(1, len(gas_datas[-1][1:][self.ui.floor_comboBox.currentIndex()]) + 1), height=[(float(value) * 100) for value in gas_datas[-1][1:][self.ui.floor_comboBox.currentIndex()]], width=0.6, brush=(0, 97, 158))
        self.ui.temp_floor_graph.addItem(t_barChar)
        self.ui.gas_floor_graph.addItem(g_barChar)

class TimeAxisItem(pg.AxisItem): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        """
        override 하여, tick 옆에 써지는 문자를 원하는대로 수정함. values --> x축 값들
        숫자로 이루어진 Itarable data --> ex) List[int]
        """
        # print("--tickStrings valuse ==>", values)
        return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]