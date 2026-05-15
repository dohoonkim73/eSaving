import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from eSaving.services.plc_service import PlcService

class PlcWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()
    
    data_received_state = pyqtSignal(object)
    data_received_ITinterface = pyqtSignal(object)
    data_received_eventLog = pyqtSignal(object)
    data_received_historyMonth = pyqtSignal(object)
    data_received_historyDay = pyqtSignal(object)
    data_received_historyDate = pyqtSignal(object)
    data_received_historyTime = pyqtSignal(object)
    data_received_historyData = pyqtSignal(object)
    
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
                print("실시간 상태정보 읽기")
                self.data_received_state.emit(eqpState)
                
                # History 정보 읽어오기
                read_history_month = self.plc_service.plc.batchread_wordunits(headdevice="D8000", readsize=30)
                read_history_day = self.plc_service.plc.batchread_wordunits(headdevice="D8100", readsize=30)
                read_history_qty = self.plc_service.plc.batchread_wordunits(headdevice="D8200", readsize=30)
                read_history_runTime = self.plc_service.plc.batchread_wordunits(headdevice="D8300", readsize=30)
                read_history_downTime = self.plc_service.plc.batchread_wordunits(headdevice="D8400", readsize=30)
                read_history_saveTime = self.plc_service.plc.batchread_wordunits(headdevice="D8500", readsize=30)
                read_history_shutDownTime = self.plc_service.plc.batchread_wordunits(headdevice="D8600", readsize=30) 
                read_history_totalTime = self.plc_service.plc.batchread_wordunits(headdevice="D8700", readsize=30)
                #self.data_received_historyMonth.emit(read_history_month)
                #print(read_history_month)
                #self.data_received_historyDay.emit(read_history_day)
                #data_historyDate = [[read_history_month] + [read_history_day]]
                data_history = [
                    read_history_month, read_history_day,
                    read_history_qty,
                    read_history_runTime, read_history_downTime, read_history_saveTime, read_history_shutDownTime, read_history_totalTime
                ]
                self.data_received_historyData.emit(data_history)
                data_historyDate = [read_history_month, read_history_day]
                self.data_received_historyDate.emit(data_historyDate)
                data_historyTime = [read_history_runTime, read_history_downTime, read_history_saveTime, read_history_shutDownTime, read_history_totalTime]
                self.data_received_historyTime.emit(data_historyTime)
                
                # IT 인터페이스 관련 데이터 읽어오기
                read_B300E = self.plc_service.plc.batchread_bitunits(headdevice="B300E", readsize=1)
                read_W300E = self.plc_service.plc.batchread_wordunits(headdevice="W300E", readsize=1)
                read_B400E = self.plc_service.plc.batchread_bitunits(headdevice="B400E", readsize=1)
                read_W400E = self.plc_service.plc.batchread_wordunits(headdevice="W400E", readsize=1)
                
                read_ITinterface = read_B300E + read_W300E + read_B400E + read_B400E
                self.data_received_ITinterface.emit(read_ITinterface)
                
                if read_B400E[0] == True:
                    self.data_received_eventLog.emit(f"PLC로부터 B400E: {read_B400E[0]}이 입력됨")
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
        self.data_received_eventLog.emit(f"PLC로부투 B400E를 입력 받은후 B300E: {cmdFlag}으로 리셋함")
        
        time.sleep(0.5)
        
        self.plc_service.write_wordAddress("W300E", 0)
        self.data_received_eventLog.emit(f"PLC로부터 B400E를 입력 받은후 W400E: {cmdCode}으로 리셋함")
        
    

