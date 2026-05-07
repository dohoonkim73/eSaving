import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QRadioButton, QStackedWidget
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from eSaving.views.energy_view import EnergyView
from eSaving.workers.energy_worker import EnergyWorker
from eSaving.models.energy_model import EnergyModel
#from eSaving.services.plc_service import PLCService
#from eSaving.presenters.main_presenter import MainPresenter

class EnergyPresenter(QObject):
    
    switch_to_main = pyqtSignal()
    
    def __init__(self, energy_view: EnergyView, energy_worker: EnergyWorker, energy_model: EnergyModel):
        super().__init__()
        self.energy_view = energy_view
        self.energy_worker = energy_worker
        self.energy_model = energy_model
         
        self.connect_signals()
        
    def connect_signals(self):
        
        # Power Meter 화면에서 화면이동 시그널
        self.energy_view.ui.btn_to_main.clicked.connect(self.switch_to_main.emit)
        
        # Power Meter 화면에서 데이터 시그널
        #self.worker.power_data_update.connect(self.update_ui)
        
        # Power Meter 화면에서 시뮬레이션 Start/Stop 버튼
        self.energy_view.ui.btn_start_power.clicked.connect(self.start_power_clicked)
        self.energy_view.ui.btn_stop_power.clicked.connect(self.stop_power_clicked)
        
    """ Power Meter 화면 버튼 이벤트로 실행되는 메서드 """
    
    
    def start_power_clicked(self):
        self.thread: QThread = QThread()
        self.model = EnergyModel()
        self.worker = EnergyWorker(self.model)
        
        # 여기에 시그널을 넣은 이유: self.worker가 새로운 객체로 덮어쓰기 때문 (위의 worker와 이메서드 안의 worker가 다르다)
        self.worker.power_data_update.connect(self.update_ui)
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_power)
        
        self.thread.start()
        
    def stop_power_clicked(self):
        self.worker.stop_power()
        self.thread.quit()
        self.thread.wait()
        
    """ UI 화면에 표시하는 부분 """
    @pyqtSlot(float, float)
    def update_ui(self, power, energy):
        print("전력량 UI표시")
        self.energy_view.ui.lbl_power.setText(f"{power: .2f} W")
        self.energy_view.ui.lbl_energy.setText(f"{energy: .5f} kwh")
        
        plc_power = power * 100
        plc_energy = energy * 100000
        plc_power = int (plc_power)
        plc_energy = int (plc_energy)
        
        power_data = [plc_power, plc_energy]
        print(power_data)