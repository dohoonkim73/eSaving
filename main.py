""" gitHub """
""" 1. git status로 상태 확인 """
""" 2. git add . 파일 추가 """
""" 3. git commit -m " 내용 기입 " """
""" 4. git push -u  origin main """
""" 5. gitHub repository에 제대로 저장되었는지 확인 """

import sys

from PyQt6.QtWidgets import QApplication

from eSaving.views.main_view import MainView
from eSaving.services.plc_service import PlcService
from eSaving.workers.plc_worker import PlcWorker
from eSaving.presenters.main_presenter import MainPresenter

class AppManager:
    
    def __init__(self):
        
        # 1. 인스턴스 생성
        self.main_view = MainView()
        self.plc_service = PlcService()
        self.plc_worker = PlcWorker(self.plc_service)
        
        self.main_presenter = MainPresenter(self.main_view, self.plc_service, self.plc_worker)
        
        
        self.main_view.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = AppManager()
    sys.exit(app.exec())
    