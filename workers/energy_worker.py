import time 
import random
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

from eSaving.models.energy_model import EnergyModel


class EnergyWorker(QObject):
    
    finished = pyqtSignal()
    progress = pyqtSignal()
    
    power_data_update = pyqtSignal(float, float)   # 전력값, 누적 전력값
    
    def __init__(self, model: EnergyModel):
        super().__init__()
        self.model = model
        
        self._running = False
        self.energy_total = 0
    
    @pyqtSlot()
    def run_power(self):
        self._running = True
        prev_time = time.time()
        
        while self._running:
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            
            # 전력 시뮬레이션 (랜덤)
            power = random.uniform(10, 12)
            
            # 모델 업데이트.
            self.model.update(power, dt)
            print(f"파워값{power}")
            print(f"시간변화량{dt}")
            
            # UI로 전달
            self.power_data_update.emit(power, self.model.energy_kwh)
            
            print(f"에너지값{self.model.energy_kwh}")
            print("전력량계 Polling 진행중")
                
            time.sleep(3)
            
        self.finished.emit()
        
    def stop_power(self):
        self._running = False