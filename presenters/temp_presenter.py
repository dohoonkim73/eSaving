import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QRadioButton, QStackedWidget
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from eSaving.views.temp_view import TemperatureView
from eSaving.workers.temp_worker import TemperatureWorker

class TemperaturePresenter(QObject):
    
    switch_to_main = pyqtSignal()
    
    target_value = pyqtSignal(object)
    
    def __init__(self, temp_view: TemperatureView, temp_worker: TemperatureWorker):
        super().__init__()
        self.temp_view = temp_view
        self.temp_worker = temp_worker
        
        self.connect_signals()
        
    def connect_signals(self):
        
        # 온도컨트롤 화면에서 메인화면 이동
        self.temp_view.ui.btn_to_main.clicked.connect(self.switch_to_main.emit)
        
        # 온도컨트롤 화면에서 온도 데이터 시그널
        #self.worker.signal_temp.connect(self.update_ui)
        
        # 온도컨트롤 화면에서 시뮬레이션 시작/정지 버튼
        self.temp_view.ui.btn_start_temp.clicked.connect(self.start_tempControl_clicked)
        self.temp_view.ui.btn_stop_temp.clicked.connect(self.stop_tempControl_clicked)
        self.temp_view.ui.btn_value.clicked.connect(self.set_targetValue)
     
    """ 온도 컨트롤 시뮬레이션 스레드 실행 """   
     
    def start_tempControl_clicked(self):
        self.thread: QThread = QThread()
        self.worker = TemperatureWorker()
        
        self.worker.signal_temp.connect(self.update_ui)
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_tempControl)
        
        self.thread.start()
        
    def stop_tempControl_clicked(self):
        self.worker.stop_tempControl()
        self.thread.quit()
        self.thread.wait()
    
    """ 온도 컨트롤 데이터 입력 및 표시"""
    
    def set_targetValue(self):
        
        target_str = self.temp_view.ui.ledit_temp_target.text()
        target_float = float(target_str)
        
        self.target_value.emit(self.worker.set_target(target_float))
        
        
        print(type(target_float))
        print("온도설정값", target_float)
    
    @pyqtSlot(float)
    def update_ui(self, currValue):
        self.temp_view.ui.lbl_tempCurrValue.setText(f"{currValue: .1f} ℃")
        