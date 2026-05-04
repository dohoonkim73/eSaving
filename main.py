import sys

from PyQt6.QtWidgets import QApplication

from eSaving.views.main_view import MainView
from eSaving.services.plc_service import PlcService
from eSaving.presenters.main_presenter import MainPresenter

class AppManager:
    
    def __init__(self):
        
        # 1. 인스턴스 생성
        self.main_view = MainView()
        self.plc_service = PlcService()
        
        self.main_presenter = MainPresenter(self.main_view, self.plc_service)
        
        
        self.main_view.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = AppManager()
    sys.exit(app.exec())
    