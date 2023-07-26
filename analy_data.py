from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem
import numpy as np
import matplotlib.pyplot as plt
import os, io
import time
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

class classification_thread(QThread):
    output_sig = pyqtSignal(object)

    def __init__(self):
        super().__init__( )

        self.rp = RecurrencePlot()

        self.working = False

        self.id = id
        self.temp_datas = None
        self.gas_datas = None
        self.output = []

    def run(self):
        danger_idx = []

        total_data = []
        for datas in self.temp_datas:
            datas = datas[1:]

            frame_data = []
            for data in datas:
                frame_data += data
            total_data.append(frame_data)
        total_datas_reshaped = [total_data[idx] for idx in range(len(total_data))]
        total_datas_reshaped = list(zip(*total_datas_reshaped))
        for idx, input_datas_str in enumerate(total_datas_reshaped):
            input_datas_float = [float(value) for value in input_datas_str]
            input_data = (torch.tensor(self.rp.fit_transform(np.array([input_datas_float]))).unsqueeze(dim=0)).to(device, dtype=torch.float)
            output = model(input_data)
            pred = output.argmax(dim=1, keepdim=True)
            if pred == 1:
                danger_idx.append(idx)

        self.output_sig.emit(danger_idx)

class analy_data:
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.classification_worker = None
        self.warning_count = 0
        self.fire_count = 0
        self.Fire_status = False
        self.Fire_idx = []
        self.init_value()

    def init_value(self):
        self.warning_count = 0
        self.fire_count = 0
        self.Fire_status = False
        self.Fire_idx = []
        self.classification_worker = classification_thread()
        self.classification_worker.output_sig.connect(self.data_analy)

    def data_analy(self, output):
        self.Fire_idx = output
        if len(self.Fire_idx) == 0:
            self.analysis_log("End DL : None")
        else:
            self.analysis_log("End DL : " + str(self.Fire_idx))

    def check_danger(self, temp_datas, gas_datas):

        self.classification_worker.temp_datas = temp_datas
        self.classification_worker.gas_datas = gas_datas

        if self.classification_worker.isRunning():
            self.classification_worker.working = False
        else:
            self.classification_worker.working = True
            self.classification_worker.start()
            self.analysis_log("Start DL")

        danger = False

        if len(self.Fire_idx) != 0:
            self.Fire_status = True
            danger = True

        for data in temp_datas:
            for floor_data in data[1:]:
                for value in floor_data:
                    if float(value) >= 25.0:
                        self.Fire_status = True
                        danger = True
        for data in gas_datas:
            for floor_data in data[1:]:
                for value in floor_data:
                    if float(value) >= 0.02:
                        self.Fire_status = True
                        danger = True

        self.Fire_status = danger
        return self.Fire_status

    def analysis_log(self, log):

        time_str = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]

        self.ui.analysis_log_table.setRowCount(self.ui.analysis_log_table.rowCount() + 1)
        self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, 0, QTableWidgetItem(time_str))
        self.ui.analysis_log_table.setItem(self.ui.analysis_log_table.rowCount() - 1, 1, QTableWidgetItem(log))
        if self.ui.analysis_log_table.rowCount() > 20:
            self.ui.analysis_log_table.removeRow(0)
        self.ui.analysis_log_table.scrollToBottom()
