import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from eSaving.services.plc_service import PlcService

class PlcWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()
    
    def __init__(self, plc_service):
        super().__init__()
        self.plc_service = plc_service
        self._running = False
        
    @pyqtSlot()
    def run(self):
        self._running = True
        
        while self._running:
            try:
                print(" Polling 진행중 ")
                
            except Exception as e:
                print("Polling Error", e)
                
            time.sleep(1)
            
        self.finished.emit()
        
    def stop(self):
        self._running = False
        
    

