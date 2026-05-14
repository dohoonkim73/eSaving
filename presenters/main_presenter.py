import sys
from datetime import datetime

from PyQt6.QtCore import QThread, QObject, pyqtSignal

from eSaving.views.main_view import MainView
from eSaving.services.plc_service import PlcService
from eSaving.workers.plc_worker import PlcWorker

from eSaving.presenters.energy_presenter import EnergyPresenter

class MainPresenter(QObject):
    
    switch_to_energy = pyqtSignal()
    switch_to_tmep = pyqtSignal()
    switch_to_history = pyqtSignal()
    
    def __init__(self, main_view: MainView, plc_service: PlcService, plc_worker: PlcWorker, energy_presenter: EnergyPresenter):    # IDE 자동완성을 위해 타입힌트 사용
        super().__init__()
        
        # 객체 생성
        self.main_view = main_view
        self.plc_service = plc_service
        self.plc_worker = plc_worker
        
        self.energy_presenter = energy_presenter
        
        self.connect_signals()
        
    def connect_signals(self):
        
        # 메인화면에서 서브화면 호출
        self.main_view.ui.btn_to_Energy.clicked.connect(self.switch_to_energy.emit)
        self.main_view.ui.btn_to_temp.clicked.connect(self.switch_to_tmep.emit)
        self.main_view.ui.btn_to_history.clicked.connect(self.switch_to_history.emit)
        
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
        self.main_view.ui.rBtn_state_wait.toggled.connect(self.set_eqpState)
        self.main_view.ui.rBtn_state_userStop.toggled.connect(self.set_eqpState)
        self.main_view.ui.rBtn_state_trouble.toggled.connect(self.set_eqpState)
        
        # 장비간 인터페이스 라디오 버튼
        self.main_view.ui.rBtn_IF_LD_deployReq.toggled.connect(self.set_LD_interface)
        self.main_view.ui.rBtn_IF_LD_wait.toggled.connect(self.set_LD_interface)
        
        self.energy_presenter.dataSend_energyToMain.connect(self.energyMeter_data)
        
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
        self.plc_worker = PlcWorker(self.plc_service)
        
        # 2. 스레드 이동 및 연결
        self.plc_worker.moveToThread(self.thread)  # PlcWorker클래스를 스레드로 이동
        self.thread.started.connect(self.plc_worker.run)
        
        self.plc_worker.data_received_eventLog.connect(self.event_log)
        self.plc_worker.data_received_state.connect(self.update_eSaveState)
        self.plc_worker.data_received_ITinterface.connect(self.update_ITinterface)
        
        # 3. 스레드 시작
        self.thread.start()
        
    def stop_polling(self):
        self.plc_worker.stop()
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
        print("장비상태 라디오버튼에 표시")
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
                       
    def update_ITinterface(self, ITinterface):
        self.main_view.ui.lcd_W300E.display(ITinterface[1])
        self.main_view.ui.lcd_W400E.display(ITinterface[3])
        
        lampColor = "qradialgradient(cx: 0.5, cy: 0.5, radius: 0.8,fx: 0.4, fy:0.4,stop: 0 #aaffaa,stop: 0.5 #22dd22,stop: 1.0 #118811)"
        lampBorder = "1px solid #333333;"
        color = f"{lampColor}" if ITinterface[0] else "gray"
        self.main_view.ui.lbl_B300E.setStyleSheet(
            f"background-color: {color};"
                "border-radius: 14px;"
            f"border: {lampBorder}"
            )
            
        
        lampColor = "qradialgradient(cx: 0.5, cy: 0.5, radius: 0.8,fx: 0.4, fy:0.4,stop: 0 #aaffaa,stop: 0.5 #22dd22,stop: 1.0 #118811)"
        lampBorder = "1px solid #333333;"
        color = f"{lampColor}" if ITinterface[2] else "gray"
        self.main_view.ui.lbl_B400E.setStyleSheet(
            f"background-color: {color};"
            "border-radius: 14px;"
            f"border: {lampBorder}"
            ) 
    
    """ 이벤트 로그 """
    def event_log(self, message):
        print("이벤트 로그 입력")
        now = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{now}] {message}"
        
        self.main_view.ui.text_event_log.append(log_message)
            
    def eventLog_clear(self):
        self.main_view.ui.text_event_log.clear()
        
    """ 전력량계 """
    def energyMeter_data(self, data):
        
        power_value = int(data[0] * 100)
        energy_value = int(data[1] * 1000000)
        print(f"전력량계 전압: {power_value}")
        print(f"전력량계 전산전력: {energy_value}")
        print(type(power_value))
        print(type(energy_value))
        success, message = self.plc_service.wirte_DwordAddress(["D7000", "D7002"], [power_value, energy_value])
        if success:
            print("전력량계 값 쓰기 성공")
        else:
            print("전력량계 값 쓰기 실패", f"{message}")
        
            
    
        