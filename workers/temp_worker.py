import time 
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread




class TemperatureWorker(QObject):
    
    finished = pyqtSignal()
    progress = pyqtSignal()
    
    signal_temp = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        
        
        
        self._running = False
        self.current_temp = 25.0
        self.target_temp = 50.0
        
        # 시스템 파라미터
        self.tau = 10.0
        self.k = 0.5
        
        #self.presenter.target_value.connect(self.set_target)
        
    def set_target(self, temp: float):
        self.target_temp = temp
        print("온도설정값 확인", self.target_temp)
    
    @pyqtSlot()
    def run_tempControl(self):
        self._running = True
        
        while self._running:
            # 단순 비례제어(P 제어)
            error = self.target_temp - self.current_temp
            heater = self.k * error
            
            # 1차 시스템
            dT = (heater - 0.1 *(self.current_temp - 25)) / self.tau
            self.current_temp += dT
            
            self.signal_temp.emit(self.current_temp)
            print(" 온도 컨트롤 Polling 진행중")
            
            time.sleep(3) 
            
        self.finished.emit()
            
    def stop_tempControl(self):
        self._running = False
        