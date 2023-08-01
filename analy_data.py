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
model = resnet18()
model = nn.DataParallel(model).to(device)

model.load_state_dict(torch.load("model/weight.pt", map_location=torch.device('cpu')))
model.eval()

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

        total_temp_data = []
        total_gas_data = []

        for datas in input_temp_datas:
            datas = datas[1:]
            frame_data = []
            for data in datas:
                frame_data += data
            total_temp_data.append(frame_data)
        for datas in input_gas_datas:
            datas = datas[1:]
            frame_data = []
            for data in datas:
                frame_data += data
            total_gas_data.append(frame_data)

        temp_danger_idx = []
        gas_danger_idx = []

        for idx, value in enumerate(total_temp_data[-1]):
            if float(value) >= 25.0:
                if not(idx in temp_danger_idx):
                    temp_danger_idx.append(idx)
        for idx, value in enumerate(total_gas_data[-1]):
            if float(value) >= 0.02:
                if not(idx in gas_danger_idx):
                    gas_danger_idx.append(idx)

        total_temp_datas_reshaped = [total_temp_data[idx] for idx in range(len(total_temp_data))]
        total_temp_datas_reshaped = list(zip(*total_temp_datas_reshaped))
        total_gas_datas_reshaped = [total_gas_data[idx] for idx in range(len(total_gas_data))]
        total_gas_datas_reshaped = list(zip(*total_gas_datas_reshaped))

        for idx, input_datas_str in enumerate(total_temp_datas_reshaped):
            input_datas_float = [float(value) for value in input_datas_str]
            input_data = (torch.tensor(self.rp.fit_transform(np.array([input_datas_float]))).unsqueeze(dim=0)).to(device, dtype=torch.float)
            output = model(input_data)
            pred = output.argmax(dim=1, keepdim=True)
            if pred == 1:
                if not(idx in temp_danger_idx):
                    temp_danger_idx.append(idx)

        self.output_sig.emit(temp_danger_idx, gas_danger_idx)

class SinarioMatching_thread(QThread):
    output_sig = pyqtSignal(object, object)

    def __init__(self):
        super().__init__( )

        self.working = False

        self.sinario = 0
        self.temp_datas = None
        self.gas_datas = None
        self.output = []

    def run(self):
        input_temp_datas = self.temp_datas.copy()
        input_gas_datas = self.gas_datas.copy()

        total_temp_data = []
        total_gas_data = []
        for datas in input_temp_datas:
            datas = datas[1:]
            frame_data = []
            for data in datas:
                frame_data += data
            total_temp_data.append(frame_data)
        for datas in input_gas_datas:
            datas = datas[1:]
            frame_data = []
            for data in datas:
                frame_data += data
            total_gas_data.append(frame_data)


        print(np.array(total_temp_data).shape, np.array(total_gas_data).shape)

        # temp_danger_idx = []
        # gas_danger_idx = []
        #
        # for idx, value in enumerate(total_temp_data[-1]):
        #     if float(value) >= 25.0:
        #         if not(idx in temp_danger_idx):
        #             temp_danger_idx.append(idx)
        # for idx, value in enumerate(total_gas_data[-1]):
        #     if float(value) >= 0.02:
        #         if not(idx in gas_danger_idx):
        #             gas_danger_idx.append(idx)
        #
        # total_temp_datas_reshaped = [total_temp_data[idx] for idx in range(len(total_temp_data))]
        # total_temp_datas_reshaped = list(zip(*total_temp_datas_reshaped))
        # total_gas_datas_reshaped = [total_gas_data[idx] for idx in range(len(total_gas_data))]
        # total_gas_datas_reshaped = list(zip(*total_gas_datas_reshaped))
        #
        # for idx, input_datas_str in enumerate(total_temp_datas_reshaped):
        #     input_datas_float = [float(value) for value in input_datas_str]
        #     input_data = (torch.tensor(self.rp.fit_transform(np.array([input_datas_float]))).unsqueeze(dim=0)).to(device, dtype=torch.float)
        #     output = model(input_data)
        #     pred = output.argmax(dim=1, keepdim=True)
        #     if pred == 1:
        #         if not(idx in temp_danger_idx):
        #             temp_danger_idx.append(idx)

        self.output_sig.emit(temp_danger_idx, gas_danger_idx)

class analy_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.FireDetection_worker = None
        self.SinarioMatching_worker = None
        self.warning_count = 0
        self.fire_count = 0
        self.Fire_status = False
        self.temp_Fire_idx = []
        self.gas_Fire_idx = []
        self.last_sinario_idx = 0
        self.sinario_idx = 0
        self.init_value()

    def init_value(self):
        self.warning_count = 0
        self.fire_count = 0
        self.Fire_status = False
        self.temp_Fire_idx = []
        self.gas_Fire_idx = []
        self.last_sinario_idx = 0
        self.sinario_idx = 0
        self.FireDetection_worker = FireDetection_thread()
        self.FireDetection_worker.output_sig.connect(self.FireDetection_data_analy)
        self.SinarioMatching_worker = SinarioMatching_thread()
        self.SinarioMatching_worker.output_sig.connect(self.SinarioMatching_data_analy)

    def FireDetection_data_analy(self, temp_output, gas_output):
        self.temp_Fire_idx = temp_output
        self.gas_Fire_idx = gas_output
        if (len(self.temp_Fire_idx) == 0) and (len(self.gas_Fire_idx) == 0):
            self.analysis_log("End Fire Detection : None")
        else:
            if len(self.temp_Fire_idx) != 0:
                self.analysis_log("End Fire Detection(temp) : " + str(self.temp_Fire_idx))
            if len(self.gas_Fire_idx) != 0:
                self.analysis_log("End Fire Detection(gas) : " + str(self.gas_Fire_idx))

    def SinarioMatching_data_analy(self, sinario_output):
        self.last_sinario_idx = self.sinario_idx
        self.sinario_idx = sinario_output
        self.analysis_log("End Sinario(temp) : " + str(sinario_output))

    def check_danger(self, temp_datas, gas_datas):

        self.FireDetection_worker.temp_datas = temp_datas
        self.FireDetection_worker.gas_datas = gas_datas

        if self.FireDetection_worker.isRunning():
            self.FireDetection_worker.working = False
        else:
            self.FireDetection_worker.working = True
            self.FireDetection_worker.start()
            self.analysis_log("Start Fire Detection")

        danger = False
        if len(self.temp_Fire_idx) != 0:
            danger = True
        if len(self.gas_Fire_idx) != 0:
            danger = True
        self.Fire_status = danger

        return self.Fire_status, self.temp_Fire_idx, self.gas_Fire_idx

    def check_sinario(self, temp_datas, gas_datas):

        self.SinarioMatching_worker.temp_datas = temp_datas
        self.SinarioMatching_worker.gas_datas = gas_datas

        if self.SinarioMatching_worker.isRunning():
            self.SinarioMatching_worker.working = False
        else:
            self.SinarioMatching_worker.working = True
            self.SinarioMatching_worker.start()
            self.analysis_log("Start sinario search")

        return self.sinario_idx

    def analysis_log(self, log):

        time_str = datetime.today().strftime('%H:%M:%S.%f')[:-3]

        self.ui.analysis_log_table.setRowCount(self.ui.analysis_log_table.rowCount() + 1)
        self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        if self.ui.analysis_log_table.rowCount() > 20:
            self.ui.analysis_log_table.removeRow(0)
        self.ui.analysis_log_table.scrollToBottom()
