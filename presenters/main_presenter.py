import sys
from datetime import datetime

from PyQt6.QtCore import QThread, QObject, pyqtSignal

from eSaving.views.main_view import MainView
from eSaving.services.plc_service import PlcService

class MainPresenter(QObject):
    
    switch_to_power = pyqtSignal()
    switch_to_tmep = pyqtSignal()
    
    def __init__(self, main_view: MainView, plc_service: PlcService):
        super().__init__()
        
        # 객체 생성
        self.main_view = main_view
        self.plc_service = plc_service
        
        self.connect_signals()
        
    def connect_signals(self):
        
        # PLC 연결 버튼
        self.main_view.ui.btn_connect.clicked.connect(self.connect_plc)
        
        
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
        