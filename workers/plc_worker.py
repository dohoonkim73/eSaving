import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from eSaving.services.plc_service import PlcService

class PlcWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()
    
    def __init__(self, plc_service:PlcService):
        super().__init__()
        self.plc_service = plc_service
        self._running = False
        
    @pyqtSlot()
    def run(self):
        self._running = True
        
        while self._running:
            try:
                # 상태정보 읽어오기
                eqpState = self.plc_service.plc.batchread_wordunits(headdevice="D100", readsize=2)
                
                # IT 인터페이스 관련 데이터 읽어오기
                read_B300E = self.plc_service.plc.batchread_bitunits(headdevice="B300E", readsize=1)
                read_W300E = self.plc_service.plc.batchread_wordunits(headdevice="W300E", readsize=1)
                read_B400E = self.plc_service.plc.batchread_bitunits(headdevice="B400E", readsize=1)
                read_W400E = self.plc_service.plc.batchread_wordunits(headdevice="W400E", readsize=1)
                
                read_ITinterface = read_B300E + read_B400E
                
                if read_B400E[0] == True:
                    self.handle_command(read_B400E, read_W400E)
                    
                print(" Polling 진행중 ")
                
            except Exception as e:
                print("Polling Error", e)
                
            time.sleep(1)
            
        self.finished.emit()
        
    def stop(self):
        self._running = False
        
    def handle_command(self, cmdFlag, cmdCode):
        self.plc_service.write_bitAddress("B300E", False)
        
        time.sleep(0.5)
        
        self.plc_service.write_wordAddress("W300E", 0)
        
    

