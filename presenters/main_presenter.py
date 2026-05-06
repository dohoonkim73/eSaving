import sys
from datetime import datetime

from PyQt6.QtCore import QThread, QObject, pyqtSignal

from eSaving.views.main_view import MainView
from eSaving.services.plc_service import PlcService
from eSaving.workers.plc_worker import PlcWorker

class MainPresenter(QObject):
    
    switch_to_power = pyqtSignal()
    switch_to_tmep = pyqtSignal()
    
    def __init__(self, main_view: MainView, plc_service: PlcService):    # IDE 자동완성을 위해 타입힌트 사용
        super().__init__()
        
        # 객체 생성
        self.main_view = main_view
        self.plc_service = plc_service
        
        self.connect_signals()
        
    def connect_signals(self):
        
        # PLC 연결 버튼
        self.main_view.ui.btn_connect.clicked.connect(self.connect_plc)
        
        # Polling Start/Stop 버튼
        self.main_view.ui.btn_start_polling.clicked.connect(self.start_polling)
        self.main_view.ui.btn_stop_polling.clicked.connect(self.stop_polling)
        
        # Energy Save Mode 실행
        self.main_view.ui.btn_eSaving.clicked.connect(lambda: self.eSaveMode_execute(91))
        self.main_view.ui.btn_shutDown.clicked.connect(lambda: self.eSaveMode_execute(92))
        
        # Energy Save Mode 해제
        self.main_view.ui.btn_release.clicked.connect(lambda: self.eSaveMode_release(90))
        
        # 이벤트 로그 클리어 버튼
        self.main_view.ui.btn_eventLog_clear.clicked.connect(self.eventLog_clear)
        
        # 장비 상태 설정 라디오 버튼
        self.main_view.ui.rBtn_state_run.toggled.connect(self.set_eqpState)
        
        
        
    def connect_plc(self):
        success, message = self.plc_service.connection()   # PlcService 클래스 내 connectio함수를 실행해라
        
        lampColor = "qradialgradient(cx: 0.5, cy: 0.5, radius: 0.8,fx: 0.4, fy:0.4,stop: 0 #aaffaa,stop: 0.5 #22dd22,stop: 1.0 #118811)"
        lampBorder = "1px solid #333333;"
        color = f"{lampColor}" if success else "gray"
        self.main_view.ui.lbl_connect.setStyleSheet(
            f"background-color: {color};"
            "border-radius: 10px;"
            f"border: {lampBorder}"
            ) 
        
    def start_polling(self):
        # 1. 스레드 생성
        self.thread: QThread = QThread()
        self.worker = PlcWorker(self.plc_service)
        
        # 2. 스레드 이동 및 연결
        self.worker.moveToThread(self.thread)  # PlcWorker클래스를 스레드로 이동
        self.thread.started.connect(self.worker.run)
        
        # 3. 스레드 시작
        self.thread.start()
        
    def stop_polling(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        
    def eSaveMode_execute(self, cmd):
        success, cmdCode = self.plc_service.write_wordAddress("W300E", cmd)
        
        if success:
            self.plc_service.write_bitAddress("B300E", 1)
            
    def eSaveMode_release(self, cmd):
        success, cmdCode = self.plc_service.write_wordAddress("W300E", cmd)
        
        if success:
            self.plc_service.write_bitAddress("B300E", 1)
     
     # 장비 상태 라디오 버튼으로 설정       
    def set_eqpState(self):
        if self.main_view.ui.rBtn_state_run.isChecked():
            value = 1
        elif self.main_view.ui.rBtn_state_wait.isChecked():
            value = 2
        elif self.main_view.ui.rBtn_state_userStop.isChecked():
            value = 4
        elif self.main_view.ui.rBtn_state_trouble.isChecked():
            value = 8
        else:
            return
        
        success, message = self.plc_service.write_wordAddress("W4010", value)
        
        if success:
            self.main_view.ui.lbl_EqpState.setText(f"W4010 상태값: {value}")
        else:
            self.main_view.ui.lbl_EqpState.setText(f"쓰기 실패: {message}")
    
    # 장비간 인터페이스 라디오 버튼으로 설정        
    def set_LD_interface(self):
        if self.main_view.ui.rBtn_IF_LD_deployReq.isChecked():
            self.plc_service.write_bitAddress("B101", False)
            self.plc_service.write_bitAddress("B100", True)
        elif self.main_view.ui.rBtn_IF_LD_wait.isChecked():
            self.plc_service.write_bitAddress("B100", False)
            self.plc_service.write_bitAddress("B101", True)
        else:
            return
            
    def update_eSaveState(self, eSaveState):
        radioButton = [
            self.main_view.ui.rBtn_eSave_None,
            self.main_view.ui.rBtn_eSave_wait,
            self.main_view.ui.rBtn_eSave_saveMode,
            self.main_view.ui.rBtn_eSave_shutDown
        ]
        
        for btn in radioButton:
            btn.blockSignals(True)
            
            if eSaveState[1] == 0:
                self.main_view.ui.rBtn_eSave_None.setChecked(True)
                self.main_view.ui.lbl_eSaveState.setText(f"W401D 상태값: {eSaveState[1]}(Disable)")
                
            elif eSaveState[1] == 1:
                self.main_view.ui.rBtn_eSave_wait.setChecked(True)
                self.main_view.ui.lbl_eSaveState.setText(f"W401D 상태값: {eSaveState[1]}(Enable)")
                
            elif eSaveState[1] == 2:
                self.main_view.ui.rBtn_eSave_saveMode.setChecked(True)
                self.main_view.ui.lbl_eSaveState.setText(f"W401D 상태값: {eSaveState[1]}(Save Mode)")
                
            elif eSaveState[1] == 4:
                self.main_view.ui.rBtn_eSave_shutDown.setChecked(True)
                self.main_view.ui.lbl_eSaveState.setText(f"W401D 상태값: {eSaveState[1]}(Shut Down Mode)")
                
            for btn in radioButton:
                btn.blockSignals(False)
                       
    
    
    """ 이벤트 로그 """
    def event_log(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{now}] {message}"
        
        self.main_view.ui.text_event_log.append(log_message)
            
    def eventLog_clear(self):
        self.main_view.ui.text_event_log.clear()
            
    
        