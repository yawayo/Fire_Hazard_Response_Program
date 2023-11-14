import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem
import numpy as np
from datetime import datetime
import torch
import torch.nn as nn
from pyts.image import GramianAngularField, MarkovTransitionField, RecurrencePlot
from model import resnet18

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(777)
if device == 'cuda':
    torch.cuda.manual_seed_all(777)
fire_Detect_model_temp = resnet18()
fire_Detect_model_temp = nn.DataParallel(fire_Detect_model_temp).to(device)
fire_Detect_model_temp.load_state_dict(torch.load("model/fire_Detect_model_temp.pt", map_location=torch.device('cpu')))
fire_Detect_model_temp.eval()
fire_Detect_model_gas = resnet18()
fire_Detect_model_gas = nn.DataParallel(fire_Detect_model_gas).to(device)
fire_Detect_model_gas.load_state_dict(torch.load("model/fire_Detect_model_gas.pt", map_location=torch.device('cpu')))
fire_Detect_model_gas.eval()

scenario_serach_model = resnet18()


RP = RecurrencePlot()

class FireDetection_thread(QThread):
    output_sig = pyqtSignal(object, object)

    def __init__(self):
        super().__init__( )

        self.rp = RecurrencePlot()

        self.working = False

        self.temp_datas = None
        self.gas_datas = None
        self.output = []

    def run(self):
        input_temp_datas = self.temp_datas.copy()
        input_gas_datas = self.gas_datas.copy()

        total_temp_datas = [[], [], [], [], [], []]
        total_gas_datas = [[], [], [], [], [], []]
        for frame_temp_datas in input_temp_datas:
            for floor, floor_temp_datas in enumerate(frame_temp_datas[1:]):
                total_temp_datas[floor].append(floor_temp_datas)
        for frame_gas_datas in input_gas_datas:
            for floor, floor_gas_datas in enumerate(frame_gas_datas[1:]):
                total_gas_datas[floor].append(floor_gas_datas)

        danger_temp_idx = [[], [], [], [], [], []]
        danger_gas_idx = [[], [], [], [], [], []]

        for floor, floor_temp_datas in enumerate(total_temp_datas):
            for idx, value in enumerate(floor_temp_datas[-1]):
                if float(value) >= 70.0:
                    if not(idx in danger_temp_idx[floor]):
                        danger_temp_idx[floor].append(idx)
            total_temp_datas_reshaped = floor_temp_datas
            total_temp_datas_reshaped = list(zip(*total_temp_datas_reshaped))
            for idx, input_datas_str in enumerate(total_temp_datas_reshaped):
                input_datas_float = [float(value) for value in input_datas_str]
                input_data = (torch.tensor(self.rp.fit_transform(np.array([input_datas_float]))).unsqueeze(dim=0)).to(device, dtype=torch.float)
                with torch.no_grad():
                    output = fire_Detect_model_temp(input_data).data[0]
                pred = output.argmax(dim=0, keepdim=True)
                if pred == 1:
                    print(input_datas_float)
                    if not(idx in danger_temp_idx[floor]):
                        danger_temp_idx[floor].append(idx)

        for floor, floor_gas_datas in enumerate(total_gas_datas):
            for idx, value in enumerate(floor_gas_datas[-1]):
                if float(value) >= 0.15:
                    if not(idx in danger_gas_idx[floor]):
                        danger_gas_idx[floor].append(idx)
            total_gas_datas_reshaped = floor_gas_datas
            total_gas_datas_reshaped = list(zip(*total_gas_datas_reshaped))
            for idx, input_datas_str in enumerate(total_gas_datas_reshaped):
                input_datas_float = [float(value) for value in input_datas_str]
                input_data = (torch.tensor(self.rp.fit_transform(np.array([input_datas_float]))).unsqueeze(dim=0)).to(device, dtype=torch.float)
                with torch.no_grad():
                    output = fire_Detect_model_gas(input_data).data[0]
                pred = output.argmax(dim=0, keepdim=True)
                if pred == 1:
                    print(input_datas_float)
                    if not(idx in danger_gas_idx[floor]):
                        danger_gas_idx[floor].append(idx)

        self.output_sig.emit(danger_temp_idx, danger_gas_idx)

class scenarioMatching_thread(QThread):
    output_sig = pyqtSignal(object)

    def __init__(self):
        super().__init__( )

        self.working = False

        self.scenario = [-1, -1, -1, -1]
        self.Fire = None
        self.temp_datas = None
        self.gas_datas = None

    def run(self):
        Fire = self.Fire
        input_temp_datas = self.temp_datas.copy()
        input_gas_datas = self.gas_datas.copy()

        for floor, danger in enumerate(Fire):
            if floor != 0:
                if danger:
                    floor_temp_data = [frame_data[floor + 1] for frame_data in input_temp_datas]
                    floor_gas_data = [frame_data[floor + 1] for frame_data in input_gas_datas]
                    """
                    remove stair sensor code here
                    """

                    DL_output  = 3
                    self.scenario[floor - 1] = DL_output

        self.output_sig.emit(self.scenario)

class analy_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.FireDetection_worker = None
        self.scenarioMatching_worker = None
        self.warning_count = 0
        self.fire_count = 0
        self.Fire_status = False
        self.temp_Fire_idx = []
        self.gas_Fire_idx = []
        self.scenario_idx = [-1, -1, -1, -1]
        self.init_value()

    def init_value(self):
        self.warning_count = 0
        self.fire_count = 0
        self.Fire_status = False
        self.temp_Fire_idx = []
        self.gas_Fire_idx = []
        self.scenario_idx = [-1, -1, -1, -1]
        self.FireDetection_worker = FireDetection_thread()
        self.FireDetection_worker.output_sig.connect(self.FireDetection_data_analy)
        self.scenarioMatching_worker = scenarioMatching_thread()
        self.scenarioMatching_worker.output_sig.connect(self.scenarioMatching_data_analy)

    def FireDetection_data_analy(self, temp_output, gas_output):
        self.temp_Fire_idx = temp_output
        self.gas_Fire_idx = gas_output
        check_temp = False
        check_gas = False
        for temp, gas in zip(self.temp_Fire_idx, self.gas_Fire_idx):
            if len(temp) != 0:
                check_temp = True
            if len(gas) != 0:
                check_gas = True

        if (not check_temp) and (not check_gas):
            self.analysis_log("End Fire Detection : None")
        else:
            if check_temp:
                self.analysis_log("End Fire Detection(temp) : " + str(self.temp_Fire_idx))
            if check_gas:
                self.analysis_log("End Fire Detection(gas) : " + str(self.gas_Fire_idx))

    def scenarioMatching_data_analy(self, scenario_output):
        self.scenario_idx = scenario_output
        self.analysis_log("End scenario : " + str(scenario_output))

    def check_danger(self, temp_datas, gas_datas):

        self.FireDetection_worker.temp_datas = temp_datas
        self.FireDetection_worker.gas_datas = gas_datas

        if self.FireDetection_worker.isRunning():
            self.FireDetection_worker.working = False
        else:
            self.FireDetection_worker.working = True
            self.FireDetection_worker.start()
            self.analysis_log("Start Fire Detection")

        danger = [False for i in range(5)]
        for floor, floor_idx in enumerate(self.temp_Fire_idx):
            if len(floor_idx) != 0:
                danger[floor] = True
        for floor, floor_idx in enumerate(self.gas_Fire_idx):
            if len(floor_idx) != 0:
                danger[floor] = True
        self.Fire_status = danger

        return self.Fire_status, self.temp_Fire_idx, self.gas_Fire_idx

    def check_scenario(self, Fire, temp_datas, gas_datas):

        self.scenarioMatching_worker.Fire = Fire
        self.scenarioMatching_worker.temp_datas = temp_datas
        self.scenarioMatching_worker.gas_datas = gas_datas

        if self.scenarioMatching_worker.isRunning():
            self.scenarioMatching_worker.working = False
        else:
            self.scenarioMatching_worker.working = True
            #self.scenarioMatching_worker.start()
            self.analysis_log("Start scenario search")

        return self.scenario_idx

    def analysis_log(self, log):

        time_str = datetime.today().strftime('%H:%M:%S.%f')[:-3]

        self.ui.analysis_log_table.setRowCount(self.ui.analysis_log_table.rowCount() + 1)
        self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        if self.ui.analysis_log_table.rowCount() > 20:
            self.ui.analysis_log_table.removeRow(0)
        self.ui.analysis_log_table.scrollToBottom()
